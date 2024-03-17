# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import ApiKey


model = ChatOpenAI(
    temperature=0,
    openai_api_key=ApiKey.OPENAI_API_KEY
)

system_message = '你是一位助手，回答答案時使用 {input_language}'
human_message = '問題：{text}'

system_template = SystemMessagePromptTemplate.from_template(system_message)
human_template = HumanMessagePromptTemplate.from_template(human_message)

chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])

message = chat_prompt.from_messages(
    input_language='繁體中文和台灣詞語',
    text='台灣最高的建築物是？'
)

response = model(message)
print(response.content)
