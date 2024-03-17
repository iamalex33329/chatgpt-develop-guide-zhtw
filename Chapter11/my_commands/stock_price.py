from tabulate import tabulate

import datetime
import requests


# 抓取股價資料
def stock_price(stock_index, month_num=2, data_num=10):
    current_date = datetime.datetime.now()
    date_list = []

    date_list = [(datetime.datetime(current_date.year, current_date.month - i, 1)).strftime('%Y%m%d') for i in
                 range(month_num)]
    date_list.reverse()
    all_daily_price_data = []
    # headers = ["日期", "成交股數", "最高價", "最低價","收盤價", "漲跌"]
    headers = ["Date", "Volume", "High", "Low", "Close", "Up/Down"]

    for date in date_list:
        url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={date}&stockNo={stock_index}'
        try:
            daily_price_json = requests.get(url).json()

            # 提取數據
            daily_price_data = daily_price_json['data']

            # 只保留需要的列, 避免資料過長
            for row in daily_price_data:
                all_daily_price_data.append([row[0], row[1], row[4], row[5], row[6], row[7]])

        except Exception as e:
            print(f"無法取得{date}的資料, 可能資料量不足.")

    # 取得最近數據
    recent_data = all_daily_price_data[-data_num:]

    # 將資料轉換成tabulate表格
    table = tabulate(recent_data, headers=headers, tablefmt='ascii')

    return table
