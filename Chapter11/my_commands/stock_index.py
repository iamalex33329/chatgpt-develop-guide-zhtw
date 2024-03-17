from tabulate import tabulate

import datetime
import requests


def index_info():
    # 現在時間
    date = datetime.datetime.now().strftime("%Y%m%d")

    # 大盤指數資訊 (指數、漲跌點數)
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?date={date}&response=json'
    index_json = requests.get(url).json()

    # 取得本月最新的資料
    data = index_json['data'][-1]
    # header = ["日期", "大盤指數", "Up/Down"]
    header = ["Date", "Market_Index", "Up/Down"]
    filtered_data = [[data[0], data[4], data[5]]]

    # 轉換成 tabulate 的文字表格
    index_data = tabulate(filtered_data, headers=header, tablefmt='ascii')

    return index_data
