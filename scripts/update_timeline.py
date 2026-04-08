#!/usr/bin/env python3
"""
Fetches RSS feeds from major AI companies and appends new service entries to data.json.
Runs weekly via GitHub Actions. Entries are auto-categorized and marked impact=3 by default.
Manual review recommended before major entries are added.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import xml.etree.ElementTree as ET

DATA_FILE = Path(__file__).parent.parent / "data.json"

# RSS feeds to monitor
FEEDS = [
    {
        "url": "https://openai.com/blog/rss",
        "company": "OpenAI",
        "icon": "⚡",
        "default_category": "LLM",
    },
    {
        "url": "https://www.anthropic.com/rss.xml",
        "company": "Anthropic",
        "icon": "🔮",
        "default_category": "LLM",
    },
    {
        "url": "https://blog.google/technology/ai/rss/",
        "company": "Google",
        "icon": "💎",
        "default_category": "LLM",
    },
    {
        "url": "https://ai.meta.com/blog/rss/",
        "company": "Meta",
        "icon": "🦙",
        "default_category": "LLM",
    },
]

# Keywords that suggest this post is a product/service launch (not a research paper or misc)
LAUNCH_KEYWORDS = [
    "introducing", "launch", "release", "announce", "available",
    "출시", "발표", "공개", "소개", "업데이트",
    "gpt", "claude", "gemini", "llama", "sora", "dall-e", "whisper",
    "copilot", "cursor", "codex", "model", "api",
]

# Skip if these words are in title (blog posts, not products)
SKIP_KEYWORDS = [
    "research", "paper", "study", "report", "policy", "safety",
    "team", "hiring", "job", "responsibility", "approach",
]


def guess_category(title: str, desc: str) -> str:
    text = (title + " " + desc).lower()
    if any(w in text for w in ["image", "dall-e", "midjourney", "stable diffusion", "vision"]):
        return "이미지"
    if any(w in text for w in ["video", "sora", "gen-", "영상"]):
        return "영상"
    if any(w in text for w in ["code", "copilot", "cursor", "codex", "coding", "developer"]):
        return "코딩"
    if any(w in text for w in ["voice", "speech", "audio", "whisper", "tts", "음성"]):
        return "음성"
    if any(w in text for w in ["search", "perplexity", "검색"]):
        return "검색"
    if any(w in text for w in ["agent", "autonomous", "에이전트"]):
        return "에이전트"
    return "LLM"


def is_launch_post(title: str) -> bool:
    t = title.lower()
    if any(w in t for w in SKIP_KEYWORDS):
        return False
    return any(w in t for w in LAUNCH_KEYWORDS)


def parse_date(raw: str) -> tuple[str, int]:
    """Return (YYYY.MM, year) from RSS date string."""
    # Try RFC 2822
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
    ]:
        try:
            dt = datetime.strptime(raw.strip(), fmt)
            return dt.strftime("%Y.%m"), dt.year
        except ValueError:
            pass
    # fallback: extract 4-digit year and 2-digit month
    m = re.search(r"(\d{4})-(\d{2})", raw)
    if m:
        return f"{m.group(1)}.{m.group(2)}", int(m.group(1))
    now = datetime.now()
    return now.strftime("%Y.%m"), now.year


def fetch_feed(feed: dict) -> list[dict]:
    try:
        req = Request(feed["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()
    except URLError as e:
        print(f"[WARN] Failed to fetch {feed['url']}: {e}")
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"[WARN] Failed to parse XML from {feed['url']}: {e}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)

    results = []
    for item in items:
        title_el = item.find("title") or item.find("atom:title", ns)
        date_el = (
            item.find("pubDate")
            or item.find("published")
            or item.find("atom:published", ns)
            or item.find("updated")
            or item.find("atom:updated", ns)
        )
        desc_el = (
            item.find("description")
            or item.find("summary")
            or item.find("atom:summary", ns)
            or item.find("content")
            or item.find("atom:content", ns)
        )

        if title_el is None or date_el is None:
            continue

        title = (title_el.text or "").strip()
        date_raw = (date_el.text or "").strip()
        desc_raw = (desc_el.text or "") if desc_el is not None else ""

        # Strip HTML tags
        desc_clean = re.sub(r"<[^>]+>", " ", desc_raw).strip()
        desc_short = " ".join(desc_clean.split())[:120] + ("..." if len(desc_clean) > 120 else "")

        if not is_launch_post(title):
            continue

        date_fmt, year = parse_date(date_raw)

        results.append({
            "name": title[:60],
            "icon": feed["icon"],
            "company": feed["company"],
            "date": date_fmt,
            "year": year,
            "category": guess_category(title, desc_clean),
            "desc": desc_short or title,
            "impact": 3,
            "_auto": True,
        })

    return results


def main():
    # Load existing data
    existing = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    existing_names = {e["name"].lower() for e in existing}

    new_entries = []
    for feed in FEEDS:
        print(f"Fetching {feed['company']}...")
        entries = fetch_feed(feed)
        for entry in entries:
            key = entry["name"].lower()
            if key not in existing_names:
                existing_names.add(key)
                new_entries.append(entry)
                print(f"  + {entry['name']} ({entry['date']})")

    if not new_entries:
        print("No new entries found.")
        return

    combined = existing + new_entries
    # Sort by year desc, then date desc
    combined.sort(key=lambda x: x["date"], reverse=True)

    DATA_FILE.write_text(
        json.dumps(combined, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nAdded {len(new_entries)} new entries to data.json")


if __name__ == "__main__":
    main()
