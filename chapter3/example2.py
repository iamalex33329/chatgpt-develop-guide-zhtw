import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY

replies = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'How to define \'Love\'? In 20 words.'}
    ],
    stream=True
)

for reply in replies:
    if 'content' in reply['choices'][0]['delta']:
        print(reply['choices'][0]['delta']['content'], end='')
