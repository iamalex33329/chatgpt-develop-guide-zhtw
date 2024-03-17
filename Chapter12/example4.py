from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
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

ai_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template('以下是使用者與AI之間的對話，AI很健談而且能根據上下文提供具體細節，如果AI不知道問題會如實說不知道。'),
    MessagesPlaceholder(variable_name='history'),
    HumanMessagePromptTemplate.from_template('{input}')
])

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(
    memory=memory,
    prompt=ai_prompt,
    llm=model,
    verbose=True
)

while True:
    question = input('Q: ')
    if not question.strip(): break
    response = conversation.predict(input=question)
    print(response + '\n')
