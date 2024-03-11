import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY

reply = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'How to define \'Love\'? In 20 words.'}
    ],
    presence_penalty=0,
    frequency_penalty=0,
    temperature=0.2,
    top_p=1,
    stop=[],
    n=3
)

for choice in reply['choices']:
    print(choice['index'], choice['message']['content'])