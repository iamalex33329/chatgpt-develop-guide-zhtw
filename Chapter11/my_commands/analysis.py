from Chapter11.my_commands.stock_index import index_info
from Chapter11.my_commands.stock_price import stock_price
from Chapter11.my_commands.stock_value import stock_value
from Chapter11.my_commands.stock_news import stock_search

import openai
import ApiKey


openai.api_key = ApiKey.OPENAI_API_KEY


def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as err:
        reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
    return reply


def stock_analysis(stock_index):
    # 大盤資訊
    index_data = index_info()
    # 個股近期股價資訊
    stock_price_data = stock_price(stock_index, month_num=3, data_num=30)
    # 個股基本面
    stock_value_data = stock_value(stock_index, month_num=3, data_num=30)
    # 新聞資訊
    news_data = stock_search(stock_index)

    msg = [
        {
            "role": "system",
            "content": "你現在是一位專業的證券分析師, 你會統整大盤趨勢、近期的股價、基本面、新聞資訊等方面並進行分析, 然後回覆該股票的趨勢分析報告",
        },
        {
            "role": "user",
            "content": f"你現在是一位專業的證券分析師, 你會依據以下資料來進行分析並給出一份完整的分析報告: \n 大盤趨勢資料主要反映整體的市場情況:\n {index_data} \n 個股近期股價資訊: \n {stock_price_data} \n 近期基本面資訊：\n {stock_value_data} 近期新聞資訊: \n {news_data} \n 請給我此股票近期的趨勢報告,請以詳細、嚴謹及專業的角度撰寫此報告, 不要有模糊不定的回答, reply in 繁體中文",
        },
    ]

    reply_data = get_reply(msg)

    return reply_data
