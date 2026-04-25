from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="QuarkSearch")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ---------------------------------------------------------------------------
# Mock 数据构建器（骨架阶段：仅用于演示页面结构与数据流）
# ---------------------------------------------------------------------------

def build_mock_terms(query: str) -> list[str]:
    """根据用户输入生成 Mock 搜索词。"""
    query = query.strip()
    if not query:
        return []
    return [
        query,
        f"{query} 教程",
        f"{query} 实战",
    ]


def build_mock_results(query: str, terms: list[str], platforms: list[str]) -> dict[str, list[dict[str, str]]]:
    """根据搜索词和平台列表生成 Mock 搜索结果。"""
    platform_labels = {
        "github": "GitHub",
        "bilibili": "Bilibili",
        "bing": "必应",
        "google": "Google",
        "cnki": "中国知网",
        "wechat": "微信",
    }
    results: dict[str, list[dict[str, str]]] = {}

    for platform in platforms:
        label = platform_labels.get(platform, platform)
        results[label] = []
        for index, term in enumerate(terms[:3], start=1):
            results[label].append(
                {
                    "title": f"{term} - 示例结果 {index}",
                    "description": f"这是 {label} 的演示数据，原始查询是「{query}」。",
                    "url": f"https://example.com/{platform}/{index}",
                    "relevance_score": 85 - index * 5,  # 相关性评分骨架字段
                }
            )
    return results


def build_mock_agent_logs(query: str, terms: list[str], platforms: list[str]) -> list[dict[str, str]]:
    """生成 Mock 的 Agent 思考与工具调用日志（流程透明化骨架）。"""
    logs = [
        {"step": "理解需求", "detail": f"用户输入：{query}"},
        {"step": "生成搜索词", "detail": f"LLM 提炼出 {len(terms)} 条候选搜索词"},
        {"step": "语言处理", "detail": "已按选定语言模式处理搜索词"},
    ]
    for platform in platforms:
        logs.append({"step": "工具调用", "detail": f"调用 {platform} 搜索工具"})
    logs.append({"step": "结果聚合", "detail": f"聚合 {len(platforms)} 个平台的结果"})
    return logs


# ---------------------------------------------------------------------------
# 页面渲染辅助
# ---------------------------------------------------------------------------

def render_page(
    request: Request,
    query: str = "",
    terms: list[str] | None = None,
    selected_platforms: list[str] | None = None,
    language_mode: str = "mono",
    results: dict[str, list[dict[str, str]]] | None = None,
    agent_logs: list[dict[str, str]] | None = None,
    is_searching: bool = False,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "query": query,
            "terms": terms or [],
            "selected_platforms": selected_platforms or ["github"],
            "language_mode": language_mode,
            "results": results or {},
            "agent_logs": agent_logs or [],
            "is_searching": is_searching,
        },
    )


# ---------------------------------------------------------------------------
# 路由
# ---------------------------------------------------------------------------

@app.get("/")
async def index(request: Request):
    """首页：展示空骨架。"""
    return render_page(request)


@app.post("/generate-terms")
async def generate_terms(request: Request, query: str = Form(...)):
    """根据用户输入生成 Mock 搜索词。"""
    terms = build_mock_terms(query)
    return render_page(request, query=query, terms=terms)


@app.post("/search")
async def search(
    request: Request,
    query: str = Form(...),
    term_text: str = Form(""),
    language_mode: str = Form("mono"),
    platforms: list[str] = Form(default=[]),
):
    """根据搜索词和选中的平台返回 Mock 搜索结果。"""
    terms = [line.strip() for line in term_text.splitlines() if line.strip()]
    if not terms:
        terms = build_mock_terms(query)
    if not platforms:
        platforms = ["github"]

    results = build_mock_results(query, terms, platforms)
    agent_logs = build_mock_agent_logs(query, terms, platforms)

    return render_page(
        request,
        query=query,
        terms=terms,
        selected_platforms=platforms,
        language_mode=language_mode,
        results=results,
        agent_logs=agent_logs,
    )
