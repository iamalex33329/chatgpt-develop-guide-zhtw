from googlesearch import search

import datetime
import requests


def stock_search(stock_index):
    # 取得昨天日期
    current_date = datetime.datetime.now()
    current_date = current_date - datetime.timedelta(days=1)
    date = current_date.strftime("%Y%m%d")

    # 利用證交所資料將股票代號轉換成公司名稱
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={date}&stockNo={stock_index}'
    stock_json = requests.get(url).json()

    company_name = stock_json['title'].split()[2]  # 只取得公司名稱
    print(company_name)
    msg = f'{company_name} 市場新聞'

    news_data = ""

    for res in search(msg, advanced=True, num_results=5):
        news_data += f"標題：{res.title}\n摘要：{res.description}\n\n"

    return news_data
