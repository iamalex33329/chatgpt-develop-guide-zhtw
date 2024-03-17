from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    SystemMessage,
    HumanMessage,
)

import ApiKey


model = ChatOpenAI(
    temperature=0,
    openai_api_key=ApiKey.OPENAI_API_KEY
)

messages = ([HumanMessage(content='回答問題使用繁體中文和台灣詞語解釋, 問題：NBA 的英文全名是？')])
response = model(messages)

print(response.content)
