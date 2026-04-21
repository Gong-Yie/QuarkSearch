from bilibili_api import request_settings,search,sync
from dotenv import load_dotenv
from langchain.tools import tool
import os

load_dotenv()


# request_settings.set_proxy(os.getenv("BILIBILI_PROXY"))

@tool
def bilibili_search(query: str) -> str:
    """
    使用 bilibili 搜索引擎进行搜索，并返回搜索结果的摘要。
    """
    search_results = sync(search.search_by_type(
        keyword=query,
        search_type=search.SearchObjectType.VIDEO,
        page=1,         # 页码
        page_size=5     # 每页结果数量
    ))
    results = []
    for item in search_results['result']:
        result = {
            "title": item['title'],
            "author": item['author'],
            "view": item['play'],
            "danmaku": item['video_review'],
            "url": f"https://www.bilibili.com/video/{item['bvid']}"
        }
        results.append(result)
    return f"Bilibili 搜索结果：\n" + "\n".join([f"{res['title']} - {res['author']} (观看: {res['view']}, 弹幕: {res['danmaku']})\nURL: {res['url']}" for res in results])

if __name__=="__main__":
    result=bilibili_search.invoke({"query": "机器学习"})
    print(result)