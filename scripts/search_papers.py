import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(SCRIPT_DIR, "metadata.json")

def load_metadata():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: metadata.json is corrupted or empty. Resetting to an empty list.")
            return []
    return []

def view_papers():
    metadata = load_metadata()
    if not metadata:
        print("No papers found.")
        return metadata

    for paper in metadata:
        print(f"Title: {paper['title']}\nYear: {paper['year']}\nTags: {', '.join(paper['tags'])}\n")
    return metadata

def search_papers(keyword):
    metadata = load_metadata()
    return [paper for paper in metadata if keyword.lower() in paper["title"].lower()]
