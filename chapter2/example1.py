import openai
import apikey

openai.api_key = apikey.OPENAI_API_KEY

reply = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': 'Your name is Alex.'},
        {'role': 'user', 'content': 'how are you, what\'s your name?'}
    ]
)

print(reply)
