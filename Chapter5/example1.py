from googlesearch import search


for link in search('台灣2024總統'):
    print(link)


for item in search('台灣2024總統', advanced=True, num_results=3):
    print(item.title)
    print(item.description)
    print(item.url)
    print('-' * 10)
