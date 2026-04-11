from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools


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