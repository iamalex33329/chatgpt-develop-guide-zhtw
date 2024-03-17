import openai
import ApiKey

openai.api_key = ApiKey.OPENAI_API_KEY

try:
    reply = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': 'How to define \'Love\'? In 20 words.'}
        ]
    )

    for choice in reply['choices']:
        print(choice['index'], choice['message']['content'])

except openai.OpenAIError as err:
    print('Error Type: ', err.error.type)
    print('Error msg: ', err.error.message)
