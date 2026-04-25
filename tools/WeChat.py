import sys

# 兼容补丁：wechatsogou 依赖旧版 werkzeug.contrib.cache，新版已移除，用 cachelib 替代
try:
    import werkzeug.contrib.cache  # noqa: F401
except ModuleNotFoundError:
    import cachelib
    import werkzeug
    if not hasattr(werkzeug, "contrib"):
        werkzeug.contrib = type(sys)("werkzeug.contrib")
        sys.modules["werkzeug.contrib"] = werkzeug.contrib
    werkzeug.contrib.cache = type(sys)("werkzeug.contrib.cache")
    sys.modules["werkzeug.contrib.cache"] = werkzeug.contrib.cache
    werkzeug.contrib.cache.FileSystemCache = cachelib.FileSystemCache

from dotenv import load_dotenv
from langchain.tools import tool
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

load_dotenv()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://weixin.sogou.com/",
}


def _fetch_sogou_wechat(query: str, page: int = 1):
    """请求搜狗微信搜索文章列表页面，返回 BeautifulSoup 对象。"""
    url = f"https://weixin.sogou.com/weixin?type=2&query={quote(query)}&page={page}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


@tool
def wechat_article_search(query: str) -> str:
    """
    使用搜狗微信搜索引擎搜索微信公众号文章，并返回搜索结果的摘要。
    """
    try:
        soup = _fetch_sogou_wechat(query)
    except Exception as e:
        return f"搜狗微信搜索请求失败：{e}"

    # 搜狗微信搜索结果在 ul[class="news-list"] > li
    news_list = soup.select("ul.news-list > li")
    if not news_list:
        # 可能是反爬验证页或没有结果
        if soup.select_one("p.tips") or "验证码" in soup.get_text():
            return "搜狗微信搜索触发了反爬验证，请稍后重试或更换关键词。"
        return "未找到相关的微信公众号文章。"

    results = []
    for li in news_list[:5]:
        # 标题和链接
        title_tag = li.select_one("h3 a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        href = title_tag.get("href", "")
        # 搜狗微信的链接是跳转链接，需要拼接完整地址
        if href.startswith("/"):
            href = f"https://weixin.sogou.com{href}"

        # 摘要
        abstract_tag = li.select_one("p")
        abstract = abstract_tag.get_text(strip=True) if abstract_tag else ""

        # 公众号名称、时间
        account_tag = li.select_one("a.account")
        account = account_tag.get_text(strip=True) if account_tag else "未知公众号"

        time_tag = li.select_one("span.s2")
        time_str = time_tag.get_text(strip=True) if time_tag else ""

        results.append(
            f"标题：{title}\n公众号：{account}\n时间：{time_str}\n摘要：{abstract}\n链接：{href}"
        )

    if not results:
        return "未解析到有效的微信公众号文章。"

    return "微信公众号文章搜索结果：\n\n" + "\n\n".join(results)


if __name__ == "__main__":
    result = wechat_article_search.invoke({"query": "人工智能"})
    print(result)
