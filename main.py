from Bilingual_terms import generate_bilingual_terms
from Monolingual_terms import generate_search_terms
from mcps.bing_mcp import bing_search
from mcps.bilibili_mcp import bilibili_search
import asyncio

def build_search_text()->str:
    search_CN=generate_search_terms()
    language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
    if language_mode=="1":
        print("\n单语搜索词列表：")
        print(search_CN)
        return search_CN
    elif language_mode=="2":
        search_EN=generate_bilingual_terms(search_CN)
        search=search_CN+"\n"+search_EN
        print("\n双语搜索词列表：")
        print("中文搜索词：")
        print(search_CN)
        print("\n英文搜索词：")
        print(search_EN)
        return search
    else:
        print("无效的选择，请输入1或2。默认选择单语模式")
        return search_CN


async def main():
    search=build_search_text()

    platforms={
        "1":("必应搜索",bing_search),
        "2":("哔哩哔哩",bilibili_search)
    }

    options=[f"{key}-{name}" for key,(name,_) in platforms.items()]
    print("\n请选择要搜索的平台："+", ".join(options))
    select=input("请选择搜索的平台（输入数字，多选请用,分隔。如果是全部平台，请输入 all）：").strip().lower()

    if select=="all":
        selected_keys = list(platforms.keys())
    else:
        selected_keys = [item.strip() for item in select.split(",") if item.strip()]

    invalid = [key for key in selected_keys if key not in platforms]

    if invalid:
        print(f"无效的平台选择：{', '.join(invalid)}")
        return
    
    tasks = []
    selected_names = []
    for key in selected_keys:
        platform_name, platform_func = platforms[key]
        selected_names.append(platform_name)
        tasks.append(platform_func(search))

    results = await asyncio.gather(*tasks)

    for platform_name, result in zip(selected_names, results):
        print(f"\n{platform_name} 搜索结果：")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())



# if __name__ == "__main__":
#     search_CN=generate_search_terms()
#     language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
#     if language_mode=="1":
#         print("\n单语搜索词列表：")
#         print(search_CN)
#     elif language_mode=="2":
#         search_EN=generate_bilingual_terms(search_CN)
#         print("\n双语搜索词列表：")
#         print("中文搜索词：")
#         print(search_CN)
#         print("\n英文搜索词：")
#         print(search_EN)
#     else:
#         print("无效的选择，请输入1或2。")