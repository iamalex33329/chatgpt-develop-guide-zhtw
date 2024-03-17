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


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role": "user", "content": "2023 Golden Melody Awards winner?"
    }],
    functions=[{                                        # 可用的函式清單
        "name": "google_res",                           # 函式名稱
        "description": "Get Google search results",     # 函式說明
        "parameters": {
            "type": "object",
            "properties": {
                "user_msg": {
                    "type": "string",
                    "description": "Keyword to search"  # 要搜尋的關鍵字
                }
            },
            "required": ["user_msg"],                   # 必要參數
        },
    }],
    function_call="auto",                               # 讓 AI 判斷是否需要叫用函式
)

# print(response)

func_call = response['choices'][0]['message']['function_call']
func_name = func_call["name"]
args = json.loads(func_call["arguments"])
arg_val = args.popitem()[1]

print(f'{func_name}("{arg_val}")')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": "2023 Golden Melody Awards winner?"},
        # 返回 AI 傳給我們的 function calling 結果
        response["choices"][0]["message"],
        {   # 以 function 角色加上 name 屬性指定函式名稱傳回執行結果
            "role": "function",
            "name": func_name,
            "content": eval(f'{func_name}("{arg_val}")')
        }
    ]
)

print(response['choices'][0]['message']['content'])