from langchain_core import tools

def bing_api_search(term: str) -> str:
    # 这里应该实现调用必应搜索API的逻辑，并返回搜索结果
    # 下面是一个示例，假设我们有一个函数叫做call_bing_api来调用必应搜索API
    search_results = call_bing_api(term)
    return search_results


@tools
def bing_search(query: str) -> str:
    """
    使用必应搜索引擎进行搜索，并返回搜索结果的摘要。
    """
    # 这里可以使用任何你喜欢的搜索引擎API来实现搜索功能
    # 下面是一个示例，假设我们有一个函数叫做bing_api_search来调用必应搜索API
    terms = query.splitlines()
    for term in terms:
        print(f"正在使用必应搜索引擎搜索：{term}")
        result=bing_api_search(term)
    
    # 对搜索结果进行处理，提取摘要信息
    summary = summarize_search_results(search_results)
    
    return summary

