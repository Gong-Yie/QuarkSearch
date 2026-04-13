from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def load_cnki_tools():
    client=MultiServerMCPClient(
        {
            "cnki":{
                "transport":"stdio",
                "command":"uvx",
                "args":[
                    "--from",
                    "git+https://github.com/h-lu/cnki-mcp",
                    "cnki-mcp"
                ]
            }
        }
    )
    async with client.session("cnki") as session:
        tools= await load_mcp_tools(session)
        yield tools

async def cnki_search(search):
    llm=ChatOpenAI(
        model=os.getenv("CNKI_MODEL")or os.getenv("TOOL_MODEL"),
        temperature=0.1,
        api_key=os.getenv("CNKI_API_KEY")or os.getenv("TOOL_API_KEY"),
        base_url=os.getenv("CNKI_BASE_URL")or os.getenv("TOOL_BASE_URL")
    )

    async with load_cnki_tools() as tools:
        agent=create_agent(llm,tools)

        result=await agent.ainvoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":f"""
请使用 CNKI MCP 工具处理下面每一行搜索词。

要求：
1. 对每个搜索词调用 search_cnki。
2. 每个搜索词只保留前 5 篇最相关论文。
3. 优先返回标题、作者、机构、来源、发表时间、DOI、链接、摘要。
4. 如有需要，可调用 get_paper_detail 补充详情。
5. 最后按搜索词分组整理输出。

搜索词如下：
{search}
""".strip(),
                    }
                ]
            }
        )

    return result