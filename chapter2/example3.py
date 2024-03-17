import requests
import ApiKey

openai_api_url = 'https://api.openai.com/v1/chat/completions'

response = requests.post(
    openai_api_url,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ApiKey.OPENAI_API_KEY}'
    },
    json={
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': 'how are you'}
        ]
    }
)

reply = response.json()

print(reply['choices'][0]['message']['content'])
