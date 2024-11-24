import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(SCRIPT_DIR, "metadata.json")
README_FILE = os.path.join(SCRIPT_DIR, "../README.md")

def update_readme():
    metadata = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    if not metadata:
        print("No papers found. README not updated.")
        return

    content = "# Papers Repository\n\n## Papers List\n"
    for paper in metadata:
        content += f"- [{paper['title']}]({paper['file_path']}) ({paper['year']})\n"

    with open(README_FILE, "w") as f:
        f.write(content)
    print("README updated successfully!")
