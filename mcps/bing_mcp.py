from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MCP_ROOT = PROJECT_ROOT / ".mcp-data"/"playwright"/"bing"

def _make_run_dir(run_id: str|None=None)->Path:
    run_id = run_id or uuid4().hex
    run_dir=MCP_ROOT/run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def _build_args(run_dir: Path,persistent:bool=True)->list[str]:
    args=[
        "-y",
        "@playwright/mcp@latest",
        "--browser","chromium",
        "--viewport-size","1366x768",
        "--timeout-navigation","30000",
        "--timeout-action","5000",
    ]
    if persistent:
        profile_dir=MCP_ROOT / "persistent-profile"
        profile_dir.mkdir(parents=True, exist_ok=True)
        args.extend(["--user-data-dir",str(profile_dir)])
    else:
        args.append("--isolated")
    return args

@asynccontextmanager
async def load_playwright_tools(persistent:bool=True):
    run_dir=_make_run_dir()

    client=MultiServerMCPClient(
        {
            "playwright": {
                "transport": "stdio",
                "command":"npx",
                "args": _build_args(run_dir,persistent=persistent),
            }
        }
    )

    async with client.session("playwright") as session:
        tools=await load_mcp_tools(session)
        yield tools,run_dir

async def bing_search(search):
    llm=ChatOpenAI(
        model=os.getenv("BING_MODEL","TOOL_MODEL"),
        temperature=0.1,
        api_key=os.getenv("BING_API_KEY","TOOL_API_KEY"),
        base_url=os.getenv("BING_BASE_URL","TOOL_BASE_URL")
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