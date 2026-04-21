from github import Github
from github import Auth
from dotenv import load_dotenv
from langchain.tools import tool
import os

load_dotenv()

access_token=os.getenv("GITHUB_PAT_TOKEN")
auth=Auth.Token(access_token)
g = Github(auth=auth)

@tool
def github_search(query: str) -> str:
    """
    使用 GitHub 搜索引擎进行搜索，并返回搜索结果的摘要。
    """
    
    sort_by="stars"
    order="desc"

    repositories = g.search_repositories(query=query, sort=sort_by, order=order)
    results = []
    for repo in repositories[:5]:  # 只返回前5个结果
        result = {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "url": repo.html_url
        }
        results.append(result)
    
    return f"GitHub 搜索结果：\n" + "\n".join([f"{res['full_name']} - {res['description']} (⭐ {res['stars']})\nURL: {res['url']}" for res in results])

if __name__=="__main__":
    result=github_search.invoke({"query": "机器学习"})
    print(result)