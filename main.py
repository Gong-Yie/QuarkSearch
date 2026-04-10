from Bilingual_terms import generate_bilingual_terms
from Monolingual_terms import generate_search_terms
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from mcps.bing_mcp import load_playwright_tools
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    search=""
    search_CN=generate_search_terms()
    language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
    if language_mode=="1":
        search=search_CN
        print("\n单语搜索词列表：")
        print(search_CN)
    elif language_mode=="2":
        search_EN=generate_bilingual_terms(search_CN)
        search=search_CN+"\n"+search_EN
        print("\n双语搜索词列表：")
        print("中文搜索词：")
        print(search_CN)
        print("\n英文搜索词：")
        print(search_EN)
    else:
        print("无效的选择，请输入1或2。")


    llm=ChatOpenAI(
        model=os.getenv("BING_MODEL"),
        temperature=0.1,
        api_key=os.getenv("BING_API_KEY"),
        base_url=os.getenv("BING_BASE_URL")
    )    

    async with load_playwright_tools(persistent=True) as (tools,run_dir):
        agent=create_agent(llm,tools)

        result=await agent.ainvoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":f"""
你必须直接通过 URL 打开 Bing 搜索结果页，不要访问 Bing 首页，也不要点击页面输入框。

对下面每一行搜索词分别执行：
1. 将搜索词进行 URL 编码。
2. 直接访问 https://www.bing.com/search?q=<编码后的搜索词>。
3. 页面打开后先重新获取页面快照。
4. 如果当前页面不是正常搜索结果页，而是出现“请验证您是真人”、“Verify you are human”、“captcha”、“unusual traffic”之类验证提示：
   - 先重新获取一次页面快照；
   - 尝试点击页面中最明显、最直接的验证入口，例如“请验证您是真人”按钮、复选框或继续按钮；
   - 点击后再次获取页面快照；
   - 如果仍然是验证页，不要反复盲点，直接说明当前页面需要人工验证。
5. 如果已经进入正常搜索结果页，只提取前 3 条自然搜索结果，输出标题、链接和摘要。
6. 不要依赖旧的页面引用；每次点击或跳转后都先重新获取页面快照，再继续操作。

搜索词如下：
{search}
""".strip()
                    }
                ]
            }
        )
    print(f"\n搜索结果：\n{result}")

if __name__ == "__main__":
    asyncio.run(main())



# if __name__ == "__main__":
#     search_CN=generate_search_terms()
#     language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
#     if language_mode=="1":
#         print("\n单语搜索词列表：")
#         print(search_CN)
#     elif language_mode=="2":
#         search_EN=generate_bilingual_terms(search_CN)
#         print("\n双语搜索词列表：")
#         print("中文搜索词：")
#         print(search_CN)
#         print("\n英文搜索词：")
#         print(search_EN)
#     else:
#         print("无效的选择，请输入1或2。")