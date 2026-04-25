from Bilingual_terms import generate_bilingual_terms
from Monolingual_terms import generate_search_terms
from tools.Bilibili import bilibili_search
from tools.Github import github_search
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

def build_search_text()->str:
    search_CN=generate_search_terms()
    language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
    if language_mode=="1":
        print("\n单语搜索词列表：")
        print(search_CN)
        return search_CN
    elif language_mode=="2":
        search_EN=generate_bilingual_terms(search_CN)
        search=search_CN+"\n"+search_EN
        print("\n双语搜索词列表：")
        print("中文搜索词：")
        print(search_CN)
        print("\n英文搜索词：")
        print(search_EN)
        return search
    else:
        print("无效的选择，请输入1或2。默认选择单语模式")
        return search_CN

def core():
    search=build_search_text()
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0.1,
        api_key=os.getenv("CORE_API_KEY"),
        base_url=os.getenv("CORE_BASE_URL")  
    )

    tools=[bilibili_search,github_search]

    agent=create_agent(
        model=llm,
        tools=tools
    )

    result=agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":f"""
请使用以下工具处理下面每一行搜索词：
1. bilibili_search：用于在哔哩哔哩平台上搜索相关视频内容。
2. github_search：用于在GitHub平台上搜索相关代码仓库和
要求：
1. 对每个搜索词调用工具进行搜索。
2. 每个搜索词只保留前 5 条最相关的结果。
搜索词如下：
{search}
""".strip(),
                }
            ]
        }
    )

    return result.choices[0].message.content

if __name__=="__main__":
    print(core())
