from langchain_openai import ChatOpenAI
from langchain import GoogleSearchAPIWrapper
from langchain import LLMMathChain
from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType

import ApiKey
import os


os.environ['GOOGLE_CSE_ID'] = ApiKey.SEARCH_ENGINE_ID
os.environ['GOOGLE_API_KEY'] = ApiKey.CUSTOM_SEARCH_JSON_API

model = ChatOpenAI(
    temperature=0,
    openai_api_key=ApiKey.OPENAI_API_KEY
)

search = GoogleSearchAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm=model, verbose=True)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description='如果不曉得答案，用此工具搜尋資料'
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description='如果需要數學計算，用此工具計算'
    ),
]

agent = initialize_agent(
    llm=model,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run('台灣最高的建築物相當於世界上最高的建築物的幾倍？請注意計算單位需一致！')
print(response)
