import json
import os
from add_papers import add_paper
from search_papers import view_papers, search_papers
from update_readme import update_readme

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(SCRIPT_DIR, "metadata.json")

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

            pdf_url = None
            if "arxiv.org" in doi_or_url:
                arxiv_id = doi_or_url.split("/")[-1]
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            try:
                add_paper(paper_info, pdf_url=pdf_url)
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
