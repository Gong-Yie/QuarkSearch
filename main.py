from Bilingual_terms import generate_bilingual_terms
from Monolingual_terms import generate_search_terms

if __name__ == "__main__":
    search_CN=generate_search_terms()
    language_mode=input("请选择语言模式（1-单语，2-双语）：").strip()
    if language_mode=="1":
        print("\n单语搜索词列表：")
        print(search_CN)
    elif language_mode=="2":
        search_EN=generate_bilingual_terms(search_CN)
        print("\n双语搜索词列表：")
        print("中文搜索词：")
        print(search_CN)
        print("\n英文搜索词：")
        print(search_EN)
    else:
        print("无效的选择，请输入1或2。")