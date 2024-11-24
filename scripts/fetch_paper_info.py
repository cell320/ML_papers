import json
import os
import requests
from bs4 import BeautifulSoup
from add_papers import add_paper
from search_papers import view_papers, search_papers
from update_readme import update_readme

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(SCRIPT_DIR, "metadata.json")


def fetch_arxiv_info(arxiv_url):
    import requests
    from bs4 import BeautifulSoup

    arxiv_id = arxiv_url.split("/")[-1]  # 提取 arXiv ID
    arxiv_api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"  # 构建 API 查询 URL
    response = requests.get(arxiv_api_url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from arXiv API.")

    soup = BeautifulSoup(response.text, "lxml-xml")

    # 确保从 <entry> 中提取标题，而不是从 <feed>
    entry = soup.find("entry")
    if not entry:
        raise Exception("No entry found for the given arXiv ID.")

    # 提取论文标题
    title_tag = entry.find("title")
    title = title_tag.text.strip() if title_tag else "Unknown Title"
    title = " ".join(title.split())  # 去除多余空格

    # 提取作者
    authors = [author.find("name").text for author in entry.find_all("author") if author.find("name")]

    # 提取年份
    published_tag = entry.find("published")
    year = int(published_tag.text[:4]) if published_tag else 0

    # 提取 PDF 链接
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    return {
        "title": title,        # 论文标题
        "authors": authors,    # 作者列表
        "year": year,          # 出版年份
        "url": pdf_url,        # PDF 链接
        "tags": ["arXiv"]
    }

# 从 DOI 获取论文信息
def fetch_by_doi(doi):
    from crossref.restful import Works

    works = Works()
    result = works.doi(doi)

    return {
        "title": result["title"][0],
        "authors": [f"{author['given']} {author['family']}" for author in result["author"]],
        "year": result["created"]["date-parts"][0][0],
        "url": result.get("URL", ""),
        "tags": ["DOI"]
    }


# 主程序
def main():
    while True:
        # 打印菜单
        print("\n==== Paper Manager ====")
        print("1. Add a new paper (DOI or arXiv URL)")
        print("2. View all papers")
        print("3. Search for a paper by keyword")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # 添加论文
            doi_or_url = input("Enter DOI or arXiv URL: ").strip()
            if doi_or_url.startswith("10."):
                try:
                    paper_info = fetch_by_doi(doi_or_url)
                except Exception as e:
                    print(f"Failed to fetch paper information by DOI: {e}")
                    continue
            elif "arxiv.org" in doi_or_url:
                try:
                    paper_info = fetch_arxiv_info(doi_or_url)
                except Exception as e:
                    print(f"Failed to fetch paper information from arXiv: {e}")
                    continue
            else:
                print("Invalid input. Please enter a valid DOI or arXiv URL.")
                continue

            try:
                add_paper(paper_info, pdf_url=paper_info.get("url"))
                print(f"Successfully added paper: {paper_info['title']}")

                # 自动更新 README
                update_readme()
                print("README file updated successfully.")
            except Exception as e:
                print(f"Failed to add paper: {e}")

        elif choice == "2":
            # 查看所有论文
            try:
                metadata = view_papers()
                if not metadata:
                    print("No papers available.")
                    continue

                print("\n==== Papers ====")
                for idx, paper in enumerate(metadata, start=1):
                    print(f"{idx}. Title: {paper['title']}")
                    print(f"   Authors: {', '.join(paper['authors'])}")
                    print(f"   Year: {paper['year']}")
                    print(f"   Tags: {', '.join(paper['tags'])}")
                    print(f"   Link: {paper.get('url') or 'No URL available'}")
                    print()
            except Exception as e:
                print(f"Failed to view papers: {e}")

        elif choice == "3":
            # 搜索论文
            keyword = input("Enter a keyword to search: ").strip()
            try:
                results = search_papers(keyword)
                if not results:
                    print("No matching papers found.")
                    continue

                print("\n==== Search Results ====")
                for idx, paper in enumerate(results, start=1):
                    print(f"{idx}. Title: {paper['title']}")
                    print(f"   Authors: {', '.join(paper['authors'])}")
                    print(f"   Year: {paper['year']}")
                    print(f"   Tags: {', '.join(paper['tags'])}")
                    print(f"   Link: {paper.get('url') or 'No URL available'}")
                    print()
            except Exception as e:
                print(f"Failed to search papers: {e}")

        elif choice == "4":
            # 退出
            print("Exiting Paper Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
