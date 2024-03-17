from tabulate import tabulate

import datetime
import requests


# 抓取基本面資料
def stock_value(stock_index, month_num=2, data_num=10):
    current_date = datetime.datetime.now()

    date_list = [(datetime.datetime(current_date.year, current_date.month - i, 1)).strftime('%Y%m%d') for i in
                 range(month_num)]
    date_list.reverse()
    all_value_data = []
    # headers = ["日期", "殖利率", "本益比","股價淨值比"]
    headers = ["Date", "Dividend", "P/E", "PB_ratio"]

    for date in date_list:
        url = f'https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU?date={date}&stockNo={stock_index}'
        try:
            daily_value_json = requests.get(url).json()

            # 提取數據
            daily_value_data = daily_value_json['data']

            # 只保留需要的列, 避免資料過長
            for row in daily_value_data:
                all_value_data.append([row[0], row[1], row[3], row[4]])

        except Exception as e:
            print(f"無法取得{date}的資料, 可能資料量不足.")

    # 取得最近數據
    recent_data = all_value_data[-data_num:]

    # 將資料轉換成tabulate表格
    table = tabulate(recent_data, headers=headers, tablefmt='ascii')

    return table
