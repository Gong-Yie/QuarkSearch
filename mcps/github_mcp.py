from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def load_github_tools():
    client= MultiServerMCPClient(
        {
            "github": {
                "transport": "stdio",
                "command": "docker",
                "args": [
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "-e",
                    "GITHUB_READ_ONLY=1",
                    "-e",
                    "GITHUB_TOOLSETS=repos,issues,pull_requests",
                    "ghcr.io/github/github-mcp-server",
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "")
                },
            }
        }
    )
    async with client.session("github") as session:
        tools = await load_mcp_tools(session)
        yield tools

async def github_search(search):
    llm=ChatOpenAI(
        model=os.getenv("GITHUB_MODEL")or os.getenv("TOOL_MODEL"),
        temperature=0.1,
        api_key=os.getenv("GITHUB_API_KEY")or os.getenv("TOOL_API_KEY"),
        base_url=os.getenv("GITHUB_BASE_URL")or os.getenv("TOOL_BASE_URL")
    )                
    async with load_github_tools() as tools:
        agent=create_agent(llm,tools)

        result=await agent.ainvoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":f"""
请使用 GitHub MCP 工具处理下面每一行搜索词。

要求：
1. 对每个搜索词分别执行 GitHub 搜索，不要合并不同搜索词的结果。
2. 优先搜索最相关的 GitHub 仓库；如果仓库结果不充分，再补充相关 issue 或 pull request。
3. 每个搜索词最多保留前 5 条最相关结果。
4. 如果结果是仓库，优先返回：仓库名、仓库链接、描述、主要语言、Star 数、Fork 数、更新时间。
5. 如果结果是 issue 或 pull request，优先返回：标题、链接、所属仓库、状态、创建时间、摘要。
6. 明显无关、过旧、无人维护或名称碰瓷的结果要剔除。
7. 如果一个搜索词对应多个方向，请优先保留最主流、最活跃、最可信的结果。
8. 最后按搜索词分组整理输出，中文说明即可。
9. 不要编造不存在的仓库、issue 或 pull request；拿不到的信息可以省略，但要保证结果真实。

搜索词如下：
{search}
""".strip()
                    }
                ]
            }
        )
    return result           
                                                        

