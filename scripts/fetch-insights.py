#!/usr/bin/env python3
"""
WordPress RSS → /data/insights.json 동기화 스크립트.
GitHub Actions에서 정기 실행됨. 의존성 없이 표준 라이브러리만 사용.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://feelyoworks.wordpress.com/feed/"
OUT_PATH = pathlib.Path("data/insights.json")
MAX_ITEMS = 30
USER_AGENT = "Feelyoworks-Insights-Sync/1.0 (+https://feelyoworks.com)"

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def strip_html(s: str | None) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def first_image(html_str: str | None) -> str | None:
    if not html_str:
        return None
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_str)
    return m.group(1) if m else None


def parse_pubdate(s: str) -> str:
    """RFC 822 → ISO 8601(YYYY-MM-DD)."""
    try:
        return dt.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z").date().isoformat()
    except Exception:
        try:
            return dt.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").date().isoformat()
        except Exception:
            return ""


def main() -> int:
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()

    root = ET.fromstring(raw)
    channel = root.find("channel")
    if channel is None:
        print("ERROR: <channel> not found in feed", file=sys.stderr)
        return 1

    items: list[dict] = []
    for item in channel.findall("item")[:MAX_ITEMS]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_raw = (item.findtext("pubDate") or "").strip()
        desc = item.findtext("description") or ""
        content_html = item.findtext("content:encoded", default="", namespaces=NS) or ""
        categories = [c.text.strip() for c in item.findall("category") if c.text]

        summary = strip_html(content_html) or strip_html(desc)
        # 220자 정도로 트리밍
        if len(summary) > 220:
            summary = summary[:220].rstrip() + "…"

        items.append({
            "title": title,
            "link": link,
            "date": parse_pubdate(pub_raw),
            "categories": categories[:3],
            "summary": summary,
            "image": first_image(content_html),
        })

    payload = {
        "source": FEED_URL,
        "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "items": items,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(items)} items → {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
