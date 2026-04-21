from langchain_core.messages import HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def generate_search_terms():
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0.1,
        api_key=os.getenv("TERM_API_KEY"),
        base_url=os.getenv("TERM_BASE_URL")
    )

    SYSTEM_PROMPT = """
    你是一个搜索引擎的智能助手，你需要根据用户的输入，给出相关搜索词或者相近词，但是不允许进行词义扩展.
    """.strip()

    user_input = input("请输入想搜的东西：").strip()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"用户原始需求：{user_input}\n请给出相关搜索词、近义词和可直接用于搜索的增强表达。")
    ]

    response = llm.invoke(messages)
    result = response.content

    rounds=1

    print(f"\n第{rounds}次增强后的搜索词：")
    print(result)
    feedback = input("\n这些结果是否符合你的增强需求？(yes/no)：").strip().lower()
    if feedback == "no":
        while feedback != "yes":
            print("\n哪些地方还需要修改删除或者限定？请详细说明你的反馈意见。")
            detailed_feedback = input("请输入你的反馈：").strip()
            messages.append(HumanMessage(content=f"用户反馈：{detailed_feedback}\n请根据反馈进一步优化搜索词:{result}。"))
            refined_response = llm.invoke(messages)
            result = refined_response.content
            rounds += 1
            print(f"\n第{rounds}次优化后的搜索词：{result}")
            feedback = input("\n这些结果是否符合你的增强需求？(yes/no)：").strip().lower()
    messages.append(HumanMessage(content=f"现在只保留相关、近义词和可直接用于搜索的增强表达，一行一个，删除其他无关内容。然后保留和刚刚用户最相关的前三条结果。下面是要操作的内容：{result}"))
    result=llm.invoke(messages).content
    print(f"\n最终的搜索词列表：{result}")

    return result