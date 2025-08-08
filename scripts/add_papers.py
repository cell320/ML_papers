import os
import json
import requests
from update_readme import update_readme

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(SCRIPT_DIR, "metadata.json")
PAPERS_DIR = os.path.join(SCRIPT_DIR, "../papers")
NOTES_DIR = os.path.join(SCRIPT_DIR, "../notes")

def load_metadata():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: metadata.json is corrupted. Resetting to an empty list.")
            return []
    return []

def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

def add_paper(paper_info, pdf_url=None):
    metadata = load_metadata()

    # 检查是否已存在
    for entry in metadata:
        if entry["title"].lower() == paper_info["title"].lower():
            print(f"Error: Paper '{paper_info['title']}' already exists.")
            return

    # 自动生成路径
    tags = paper_info.get("tags", ["Uncategorized"])
    topic_dir = os.path.join(PAPERS_DIR, tags[0])
    os.makedirs(topic_dir, exist_ok=True)
    pdf_path = os.path.join(topic_dir, f"{paper_info['title'].replace(' ', '_')}.pdf")
    note_path = os.path.join(NOTES_DIR, f"{tags[0]}/{paper_info['title'].replace(' ', '_')}.md")

    paper_info["file_path"] = pdf_path
    paper_info["notes_path"] = note_path

    # 下载 PDF
    if pdf_url:
        response = requests.get(pdf_url)
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded PDF: {pdf_path}")

    # 生成笔记模板
    os.makedirs(os.path.dirname(note_path), exist_ok=True)
    with open(note_path, "w") as f:
        f.write(f"# {paper_info['title']}\n\n")
        f.write(f"- **Authors**: {', '.join(paper_info['authors'])}\n")
        f.write(f"- **Year**: {paper_info['year']}\n")
        f.write(f"- **Tags**: {', '.join(tags)}\n\n")
        f.write("## Summary\n\n")

    # 保存元数据
    metadata.append(paper_info)
    save_metadata(metadata)

    print(f"Paper '{paper_info['title']}' added successfully!")

    # 自动更新 README
    update_readme()
    print("README.md updated successfully!")