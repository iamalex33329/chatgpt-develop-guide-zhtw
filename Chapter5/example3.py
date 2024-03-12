import requests
import apikey

r = requests.get(
    'https://www.googleapis.com/customsearch/v1?' \
    'key={}&' \
    'cx={}&' \
    'num={}&' \
    'q={}'.format(
        apikey.CUSTOM_SEARCH_JSON_API,
        apikey.SEARCH_ENGINE_ID,
        5,
        '2024 President in Taiwan'
    )
)

for item in r.json()['items']:
    print(item['title'])
    print(item['snippet'])
    print(item['link'])
    print()
