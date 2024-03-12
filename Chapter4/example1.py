import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY

hist = []       # 歷史對話紀錄
backtrace = 3   # 記錄幾組對話


def chat(sys_msg, user_msg):
    hist.append({"role": "user", "content": user_msg})
    reply = get_reply(hist + [{"role": "system", "content": sys_msg}])

    while len(hist) >= 2 * backtrace:
        hist.pop(0)

    hist.append({"role": "assistant", "content": reply})
    return reply


def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=1.5,

        )
        reply = response['choices'][0]['message']['content']

    except openai.OpenAIError as err:
        reply = f'Error Type: {err.error.type}\nError msg: {err.error.message}'

    return reply


if __name__ == '__main__':
    sys_msg = input("AI Role: ")
    if not sys_msg.strip(): sys_msg = 'Assistant'
    print()

    while True:
        msg = input('=> ')
        if not msg.strip(): break
        ai_reply = chat(sys_msg, msg)
        print(f'=> {ai_reply}\n')

    hist = []
