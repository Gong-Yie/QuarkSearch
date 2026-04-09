from Monolingual_terms import generate_search_terms
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def generate_bilingual_terms(search_CN):
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0.1,
        api_key=os.getenv("ENGLISH_API_KEY"),
        base_url=os.getenv("ENGLISH_BASE_URL")
    )

    SYSTEM_PROMPT = """结合语境，把下面的中文搜索词列表翻译成英文，并且保持格式不变，去除重复的，一行一个。
    """.strip()

    result=search_CN
    search_EN=llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=result)
    ]).content
    return search_EN