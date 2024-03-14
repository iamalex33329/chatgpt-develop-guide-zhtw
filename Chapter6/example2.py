from googlesearch import search

import openai
import apikey
import json

openai.api_key = apikey.OPENAI_API_KEY


prompt = '''
如果我想知道以下這個問題, 請確認是否需要搜尋網路才知道？
---
{}
---
如果需要，請以下列 JSON 格式回答，除了 JSON 格式資料外，不要加上額外資訊，就算你知道答案，也不要回覆：
---
{{
    "search": true,
    "keyword": "你建議的搜尋關鍵字"
}}
---
如果不需要，請用下列 JSON 格式回答：
---
{{
    "search": false,
    "keyword": ""
}}
'''


def get_reply(messages, stream=False):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=stream
        )

        if stream:
            # In streaming mode, use a helper function to obtain complete text
            for res in response:
                if 'content' in res['choices'][0]['delta']:
                    yield res['choices'][0]['delta']['content']
        else:
            # In non-streaming mode, directly yield the complete reply text
            yield response['choices'][0]['message']['content']

    except openai.OpenAIError as err:
        # Handle OpenAI errors
        reply = f'An {err.error.type} error occurred\n{err.error.message}'
        print(reply)
        yield reply


def check_google(hist, msg, verbose=False):
    # 將歷史訊息與使用者訊息組合成一條對話紀錄
    combined_hist = hist + [{
        'role': 'user',
        'content': prompt.format(msg)
    }]

    # 取得回覆
    reply_generator = get_reply(combined_hist)
    for ans in reply_generator:
        # 若 verbose 為 True，則印出回覆
        if verbose:
            print(ans)

    # 回傳回覆
    return ans


def google_res(user_msg, num_results=5, verbose=False):
    content = "The following are the facts that have occurred:\n"

    for res in search(user_msg, advanced=True, num_results=num_results, lang='en'):
        content += f"Title: {res.title}\nSummary: {res.description}\n\n"

    content += "Please answer the following questions based on the above facts:\n"

    if verbose:
        print(f'------------\n{content}')

    return content


hist = []
backtrace = 3


def chat_g(sys_msg, user_msg, stream=False, verbose=False):
    global hist
    messages = [{'role': 'user', 'content': user_msg}]
    ans = json.loads(check_google(hist, user_msg, verbose=verbose))

    if ans['search'] is True:
        print(f'Trying to search online: {ans["keyword"]}...')
        res = google_res(ans['keyword'], verbose=verbose)
        messages = [{'role': 'user', 'content': res + user_msg}]

    reply_full = ''
    replies = get_reply(
        hist + messages + [{"role": "system", "content": sys_msg}],
        stream
    )

    for reply in replies:
        reply_full += reply
        yield reply

    hist += [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": reply_full}
    ]

    while len(hist) >= 2 * backtrace:
        hist.pop(0)


if __name__ == '__main__':
    sys_msg = 'Assistance'

    while True:
        msg = input('=> ')

        if not msg.strip():
            break

        for reply in chat_g(sys_msg, msg, stream=False):
            print(reply, end='')

        print('\n')
