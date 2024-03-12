import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY


hist = []       # 歷史對話紀錄
backtrace = 5   # 記錄幾組對話


def chat_stream(sys_msg, user_msg):
    hist.append({"role": "user", "content": user_msg})
    reply_full = ""

    for reply in get_reply_stream(
        hist + [{"role": "system", "content": sys_msg}]):
        reply_full += reply
        yield reply

    while len(hist) >= 2 * backtrace:
        hist.pop(0)

    hist.append({"role": "assistant", "content": reply_full})


def get_reply_stream(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        for chunk in response:
            if 'content' in chunk['choices'][0]['delta']:
                yield chunk["choices"][0]["delta"]["content"]
    except openai.OpenAIError as err:
        reply = f'Error Type: {err.error.type}\nError msg: {err.error.message}'


if __name__ == '__main__':
    sys_msg = input("AI Role: ")
    if not sys_msg.strip(): sys_msg = 'Assistant'
    print()

    while True:
        msg = input('=> ')
        if not msg.strip(): break
        for reply in chat_stream(sys_msg, msg):
            print(f'{reply}', end='')

        print('\n')
