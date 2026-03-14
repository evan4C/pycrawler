from dataclasses import dataclass
import re
from pathlib import Path

@dataclass
class RedbookNote:
    title: str
    content: str
    likes: str
    collects: str
    comments: str

def _parse_redbook_html(html: str) -> RedbookNote:
    """Parse the HTML content of a Redbook note and extract the relevant information."""

    patterns = {
        "title": r'<meta name="og:title" content="([^"]*)"',
        "content": r'<meta name="description" content="([^"]*)"',
        "likes": r'<meta name="og:xhs:note_like" content="([^"]*)"',
        "collects": r'<meta name="og:xhs:note_collect" content="([^"]*)"',
        "comments": r'<meta name="og:xhs:note_comment" content="([^"]*)"',
    }

    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, html)
        results[key] = match.group(1) if match else ""

    # clean up title: remove "小红书" suffix
    if results["title"].endswith(" - 小红书"):
        results["title"] = results["title"][:-len(" - 小红书")]

    return RedbookNote(**results)

def extract_redbook(html_path: Path) -> RedbookNote:
    """Extract information from a redbook HTML file"""
    if not html_path.exists():
        print(f"Error: File not found: {html_path}")
        return
    
    html = html_path.read_text(encoding="utf-8")
    note = _parse_redbook_html(html)

    if note:
        print(f"Title: {note.title}")
        print(f"Content: {note.content}")
        print(f"Likes: {note.likes}")
        print(f"Collects: {note.collects}")
        print(f"Comments: {note.comments}")
    
    return note

def extract_folder(html_folder: Path) -> list[RedbookNote]:
    """Extract info from a HTML folder"""
    notes = []
    # glob 递归匹配所有 .html/.htm 文件，rglob = recursive glob
    for file in html_folder.rglob("*.html"):
        note = extract_redbook(file)
        notes.append(note)
    return notes