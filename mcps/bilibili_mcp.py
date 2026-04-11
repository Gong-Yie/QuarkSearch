from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def load_bilibili_tools():
    client=MultiServerMCPClient(
        {
            "bilibili":{
                "transport":"stdio",
                "command":"npx",
                "args":[
                    "-y",
                    "@wangshunnn/bilibili-mcp-server"
                ]
            }
        }
    )
    async with client.session("bilibili") as session:
        tools= await load_mcp_tools(session)
        yield tools

async def bilibili_search(search):
    llm=ChatOpenAI(
        model=os.getenv("BILIBILI_MODEL")or os.getenv("TOOL_MODEL"),
        temperature=0.1,
        api_key=os.getenv("BILIBILI_API_KEY")or os.getenv("TOOL_API_KEY"),
        base_url=os.getenv("BILIBILI_BASE_URL")or os.getenv("TOOL_BASE_URL")
    )
    async with load_bilibili_tools() as tools:
        agent=create_agent(llm,tools)

        result=await agent.ainvoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":f"""
请使用 bilibili MCP 工具处理下面每一行搜索词。

要求：
1. 对每个搜索词分别调用搜索工具。
2. 每个搜索词只保留前 5 条最相关视频。
3. 输出标题、BV号、UP主、播放量、视频链接、简介摘要。
4. 最后按搜索词分组整理输出。
5. 如果结果明显无关，请剔除。

搜索词如下：
{search}
""".strip()
                    }
                ]
            }
        )
    return result