import openai
import json
from googlesearch import search

__all__ = ['func_table', 'get_reply', 'chat',
           'set_backtrace', 'empty_history', 'set_verify_depth']

import apikey

openai.api_key = apikey.OPENAI_API_KEY


def _google_res(user_msg, num_results=5, verbose=False):
    content = "以下為已發生的事實：\n"                # 強調資料可信度
    for res in search(user_msg, advanced=True,    # 一一串接搜尋結果
                      num_results=num_results):
        content += f"標題：{res.title}\n" \
                    f"摘要：{res.description}\n\n"
    content += "請依照上述事實回答以下問題：\n"        # 下達明確指令
    if verbose:
        print('------------')
        print(content)
        print('------------')
    return content


func_table = [
    {                       # 每個元素代表一個函式
        "chain": True,      # 函式執行結果是否要再傳回給 API
        "func": _google_res, # 函式
        "spec": {           # function calling 需要的函式規格
            "name": "google_res",
            "description": "取得 Google 搜尋結果",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_msg": {
                        "type": "string",
                        "description": "要搜尋的關鍵字",
                    }
                },
                "required": ["user_msg"],
            },
        }
    }
]


# 從 API 傳回的 function_calling 物件中
# 取出函式名稱與參數內容自動呼叫函式並傳回結果
def _call_func(func_call):
    func_name = func_call['name']
    args = json.loads(func_call['arguments'])
    for f in func_table: # 找出包含此函式的項目
        if func_name == f['spec']['name']:
            print(f"嘗試叫用：{func_name}(**{args})")
            val = f['func'](**args)
            return val, f['chain']
    return '', False


# 從 API 傳回內容找出 function_calling 內容
def _get_func_call(messages, stream=False, func_table=None,
                  **kwargs):
    model = kwargs.get('model', 'gpt-3.5-turbo')
    debug = kwargs.get('debug', False)

    if debug:
        print('\n--------------')
        print(f'model:{model}')
        if func_table:
            print('function table:')
            for func in func_table:
                print(f"\t{func['spec']['name']}")
        print('messages:')
        for msg in messages:
            print(f"\t{msg}")
        print('--------------')

    funcs = {}
    if func_table:
        funcs = {'functions':[f['spec'] for f in func_table]}
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        stream = stream,
        **funcs
    )
    if stream:
        chunk = next(response)
        delta = chunk["choices"][0]["delta"]
        if 'function_call' in delta:
            func_call = delta['function_call']
            args = ''
            for chunk in response:
                delta = chunk["choices"][0]["delta"]
                if 'function_call' in delta:
                    args += delta['function_call']['arguments']
            func_call['arguments'] = args
            return func_call, None
    else:
        msg = response["choices"][0]["message"]
        if 'function_call' in msg:
            return msg['function_call'], None
    return None, response


def get_reply(messages, stream=False, func_table=None,
                **kwargs):
    try:
        func_call, response = _get_func_call(messages,
                                            stream, func_table,
                                            **kwargs)
        if func_call:
            res, chain = _call_func(func_call)
            if chain:  # 如果需要將函式執行結果送回給 AI 再回覆
                messages += [
                    {  # 必須傳回原本 function_calling 的內容
                        "role": "assistant",
                        "content": None,
                        "function_call": func_call
                    },
                    {  # 以及以 function 角色的函式執行結果
                        "role": "function",        # function 角色
                        "name": func_call['name'], # 傳回函式名名稱
                        "content": res             # 傳回執行結果
                    }]
                yield from get_reply(messages, stream, func_table,
                                     **kwargs)
            else:
                yield res
        elif stream:
            for chunk in response:
                if 'content' in chunk['choices'][0]['delta']:
                    yield chunk['choices'][0]['delta']['content']
        else:
            yield response['choices'][0]['message']['content']
    except openai.OpenAIError as err:
        reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
        print(reply)
        yield reply


_hist = []       # 歷史對話紀錄
_backtrace = 2   # 記錄幾組對話
_verify_depth = 3 # 最多驗證 3 次
_verify_msg = {
    "role": "user",
    "content": "如果之前是問句, 且剛剛的回答內容確實已經回答了問題, "
               "請回覆 'Y', 否則回覆 'N', 只要單一字母,"
               " 不要加任何其他說明"
}


def chat(sys_msg, user_msg, stream=False, func_table=func_table,
         **kwargs):
    global _hist
    verify = kwargs.get('verify', False)
    depth = 0
    while True:
        replies = get_reply(    # 使用函式功能版的函式
            _hist                          # 先提供歷史紀錄
            + [{"role": "user", "content": user_msg}]
            + [{"role": "system", "content": sys_msg}],
            stream, func_table, **kwargs)
        reply_full = ''
        for reply in replies:
            reply_full += reply
            yield reply

        _hist += [
            {"role":"user", "content":user_msg},
            {"role":"assistant", "content":reply_full}
        ]
        if not verify or depth == _verify_depth: break
        for reply in get_reply(_hist + [_verify_msg]):pass
        print(f"(已完成：{reply})")
        if reply=='Y': break
        user_msg = '繼續'
        depth += 1
    while len(_hist) >= 2 * _backtrace: # 超過記錄限制
        _hist.pop(0)  # 移除最舊的紀錄


def empty_history():
    _hist.clear()


def set_backtrace(backtrace=0):
    global _backtrace
    if backtrace > 0:
        _backtrace = backtrace
    return _backtrace


def set_verify_depth(verify_depyh=0):
    global _verify_depth
    if verify_depyh > 0:
        _verify_depth = verify_depyh
    return _verify_depth
