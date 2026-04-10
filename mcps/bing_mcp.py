from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

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
        