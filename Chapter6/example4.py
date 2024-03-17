from googlesearch import search

import openai
import ApiKey
import json

openai.api_key = ApiKey.OPENAI_API_KEY


def google_res(user_msg, num_results=5, verbose=False):
    content = "The following are the facts that have occurred:\n"

    for res in search(user_msg, advanced=True, num_results=num_results, lang='en'):
        content += f"Title: {res.title}\nSummary: {res.description}\n\n"

    content += "Please answer the following questions based on the above facts:\n"

    if verbose:
        print(f'------------\n{content}')

    return content


func_table = [
    {                                                         # 每個元素代表一個函式
        "chain": True,                                        # 函式執行結果是否要再傳回給 API
        "func": google_res,                                   # 函式本身
        "spec": {                                             # 函式的規格
            "name": "google_res",                             # 函式名稱
            "description": "Get Google search results",       # 函式說明
            "parameters": {                                   # 函式參數
                "type": "object",
                "properties": {
                    "user_msg": {                             # 參數名稱
                        "type": "string",                     # 參數類型
                        "description": "Keyword to search",   # 參數說明
                    }
                },
                "required": ["user_msg"],                     # 必要參數
            },
        }
    }
]


def call_func(func_call):
    func_name = func_call['name']               # 取得要呼叫的函式名稱
    args = json.loads(func_call['arguments'])   # 取得函式的參數內容
    for f in func_table:                        # 在函式表格中尋找符合函式名稱的項目
        if func_name == f['spec']['name']:
            print(f"Attempting to call: {func_name}(**{args})")  # 印出正在嘗試呼叫的函式
            val = f['func'](**args)             # 使用函式表格中的對應函式呼叫函式並傳入參數
            return val, f['chain']              # 回傳呼叫函式的結果以及是否需要再次呼叫的標誌
    return '', False                            # 如果找不到對應的函式，則回傳空字串和 False


def get_func_call(messages, stream=False, func_table=None, **kwargs):
    model = 'gpt-3.5-turbo'         # 預設使用的模型版本
    if 'model' in kwargs:           # 如果使用者指定了模型版本，則使用指定的模型版本
        model = kwargs['model']

    funcs = {}                      # 初始化函式字典
    if func_table:                  # 如果提供了函式表格，則將函式表格中的函式規格加入到 funcs 中
        funcs = {'functions': [f['spec'] for f in func_table]}

    # 呼叫 ChatCompletion API 以獲取回應
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream,
        **funcs
    )

    if stream:                                  # 如果使用串流模式
        chunk = next(response)                  # 獲取串流中的下一個回應
        delta = chunk["choices"][0]["delta"]    # 獲取回應中的變化部分
        if 'function_call' in delta:            # 如果變化部分中包含 function_calling
            func_call = delta['function_call']  # 獲取 function_calling 的內容
            args = ''                           # 初始化參數字串
            for chunk in response:              # 從串流中獲取下一個回應
                delta = chunk["choices"][0]["delta"]                # 獲取回應中的變化部分
                if 'function_call' in delta:                        # 如果變化部分中包含 function_calling
                    args += delta['function_call']['arguments']     # 將參數內容加入到參數字串中
            func_call['arguments'] = args                           # 將參數字串加入到 function_calling 中
            return func_call, None                                  # 返回 function_calling 和空值
    else:  # 如果不是串流模式
        msg = response["choices"][0]["message"]     # 獲取回應中的訊息部分
        if 'function_call' in msg:                  # 如果訊息部分中包含 function_calling
            return msg['function_call'], None       # 返回 function_calling 和空值

    return None, response                           # 如果沒有找到 function_calling，則返回空值和回應


def get_reply_f(messages, stream=False, func_table=None, **kwargs):
    try:
        # 從 API 回傳的訊息中獲取 function_calling 的內容以及回應本身
        func_call, response = get_func_call(messages, stream, func_table, **kwargs)

        if func_call:  # 如果有 function_calling 的內容
            # 呼叫函式並獲取函式執行結果以及是否需要將結果傳回給 API 再回覆
            res, chain = call_func(func_call)

            if chain:  # 如果需要將函式執行結果送回給 API 再回覆
                # 準備訊息列表，將原本的 function_calling 的內容和函式執行結果加入其中
                messages += [
                    {
                        "role": "assistant",  # 助手角色
                        "content": None,  # 內容為空
                        "function_call": func_call  # 傳回原本的 function_calling 的內容
                    },
                    {
                        "role": "function",  # 函式角色
                        "name": func_call['name'],  # 傳回函式名稱
                        "content": res  # 傳回函式執行結果
                    }
                ]

                # 遞迴呼叫自身，處理新的訊息並繼續尋找 function_calling
                yield from get_reply_f(messages, stream, func_table, **kwargs)
            else:
                yield res  # 直接回覆函式執行結果
        elif stream:  # 如果是串流模式
            for chunk in response:
                if 'content' in chunk['choices'][0]['delta']:  # 獲取回應中的內容部分
                    yield chunk['choices'][0]['delta']['content']  # 回覆內容
        else:  # 如果不是串流模式
            yield response['choices'][0]['message']['content']  # 回覆整個訊息的內容
    except openai.OpenAIError as err:  # 處理 OpenAI 錯誤
        reply = f"An {err.error.type} error occurred.\n{err.error.message}"
        print(reply)
        yield reply  # 回覆錯誤訊息


'''
# 測試非串流方式呼叫 function_calling
for chunk in get_reply_f([{'role': 'user', 'content': '2023 金曲歌后是誰？'}], func_table=func_table):
    print(chunk)

# 測試串流方式呼叫 function_calling
for chunk in get_reply_f([{"role":"user", "content":"2023 金曲歌后是誰？"}], stream=True, func_table=func_table):
    print(chunk, end='')
'''

hist = []  # 歷史對話紀錄
backtrace = 2  # 記錄幾組對話


def chat_f(sys_msg, user_msg, stream=False, **kwargs):
    global hist

    # 使用函式功能版的函式來處理對話
    replies = get_reply_f(
        hist + [{"role": "user", "content": user_msg}] + [{"role": "system", "content": sys_msg}],
        stream, func_table, **kwargs)

    reply_full = ''  # 初始化回覆結果的字串
    for reply in replies:
        reply_full += reply  # 將每個回覆串連成一個完整的回覆內容
        yield reply  # 回傳每個回覆內容

    # 將對話紀錄加入到 hist 中，包括用戶訊息、助手回覆和完整對話回覆
    hist += [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": reply_full}
    ]

    # 當 hist 的對話紀錄超過設定的回溯次數時，移除最舊的對話紀錄
    while len(hist) >= 2 * backtrace:
        hist.pop(0)  # 移除最舊的紀錄


verify_msg = {
    'role': 'user',
    'content': '如果之前是問句，且剛剛的回答內容確實已經回答了問題，請回覆 ${Y} 否則回覆 ${N}，只要單一字母，不要加任何其他說明。'
}


def chat_v(sys_msg, user_msg, stream=False, **kwargs):
    global hist
    verify = kwargs.get('verify', False)  # 檢查是否有提供驗證訊息
    while True:
        replies = get_reply_f(
            hist + [{'role': 'user', 'content': user_msg}] + [{'role': 'system', 'content': sys_msg}],
            stream, func_table, **kwargs)

        reply_full = ''
        for reply in replies:
            reply_full += reply
            yield reply

        hist += [
            {'role': 'user', 'content': user_msg},
            {'role': 'assistant', 'content': reply_full}
        ]

        if not verify: break
        for reply in get_reply_f(hist + [verify_msg]): pass
        print(f'(已完成：{reply})')

        if reply == 'Y': break
        user_msg = '繼續'

    while len(hist) >= backtrace * 2:
        hist.pop(0)


if __name__ == '__main__':
    sys_msg = 'Assistance'
    print()

    while True:
        msg = input("=> ")
        if not msg.strip():
            break

        for reply in chat_v(sys_msg, msg, stream=False, verify=True):
            print(reply, end="")

        print('\n')