#!/usr/bin/env python3
"""
WordPress RSS 동기화 스크립트. GitHub Actions에서 정기 실행됨.

하는 일:
  1. RSS 피드 → data/insights.json
  2. index.html   의 INSIGHTS:HOME    마커 사이에 최신 글 HTML을 정적 주입
  3. insights.html 의 INSIGHTS:ARCHIVE 마커 사이에 전체 아카이브 HTML을 정적 주입
  4. insights.html 의 INSIGHTS:JSONLD  마커 사이에 ItemList 구조화 데이터를 주입
  5. sitemap.xml 의 lastmod 를 최신 발행일 기준으로 갱신

왜 정적 주입인가:
  이전에는 브라우저가 /data/insights.json 을 fetch 해서 렌더했습니다.
  그 방식은 검색엔진과 AI 크롤러가 받아가는 HTML에 글 목록이 전혀 담기지 않아,
  뉴스레터 콘텐츠가 GEO/SEO 측면에서 통째로 보이지 않았습니다.
  이제 빌드 시점에 HTML로 구워 넣어 크롤러가 본문을 그대로 읽습니다.

의존성 없이 표준 라이브러리만 사용.
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
SITE = "https://feelyoworks.com"

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "insights.json"
INDEX_PATH = ROOT / "index.html"
INSIGHTS_PATH = ROOT / "insights.html"
SITEMAP_PATH = ROOT / "sitemap.xml"

MAX_ITEMS = 30
HOME_ITEMS = 5           # 홈에 노출할 개수 (featured 1 + 리스트 4)
USER_AGENT = "Feelyoworks-Insights-Sync/2.0 (+https://feelyoworks.com)"

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

KO_MONTHS = "1월 2월 3월 4월 5월 6월 7월 8월 9월 10월 11월 12월".split()


# ─────────────────────────── 파싱 유틸 ───────────────────────────

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
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            continue
    return ""


def fmt_date_ko(iso: str) -> str:
    """2026-07-13 → 2026년 7월 13일"""
    try:
        d = dt.date.fromisoformat(iso)
    except Exception:
        return iso or ""
    return f"{d.year}년 {KO_MONTHS[d.month - 1]} {d.day}일"


def esc(s: str | None) -> str:
    """HTML 속성/텍스트 양쪽에 안전하게."""
    return html.escape(str(s or ""), quote=True)


# ─────────────────────────── 렌더링 ───────────────────────────

def render_home(items: list[dict]) -> str:
    """홈 섹션: featured 1개 + 리스트 4개. 기존 클라이언트 렌더 마크업과 동일 구조."""
    if not items:
        return '<p class="insights-empty">아직 발행된 글이 없어요. 곧 첫 번째 뉴스레터를 보내드릴게요.</p>'

    featured = items[0]
    rest = items[1:HOME_ITEMS]

    img = ""
    if featured.get("image"):
        img = (
            '<div class="insights-featured-img">'
            f'<img src="{esc(featured["image"])}" alt="" loading="lazy" referrerpolicy="no-referrer">'
            "</div>"
        )

    out = [
        f'<a class="insights-featured" href="{esc(featured["link"])}" target="_blank" rel="noopener">',
        img,
        '<div class="insights-featured-body">',
        '<div class="insights-meta">',
        '<span class="chip">LATEST</span>',
        f'<span class="insights-date">{esc(fmt_date_ko(featured.get("date", "")))}</span>',
        "</div>",
        f'<h3>{esc(featured["title"])}</h3>',
        f'<p>{esc(featured.get("summary", ""))}</p>',
        '<span class="insights-go">읽으러 가기 ↗</span>',
        "</div>",
        "</a>",
    ]

    if rest:
        out.append('<ul class="insights-list" role="list">')
        for it in rest:
            out += [
                "<li>",
                f'<a href="{esc(it["link"])}" target="_blank" rel="noopener">',
                f'<span class="insights-date">{esc(fmt_date_ko(it.get("date", "")))}</span>',
                f'<span class="insights-title">{esc(it["title"])}</span>',
                '<span class="insights-go" aria-hidden="true">↗</span>',
                "</a>",
                "</li>",
            ]
        out.append("</ul>")

    return "\n".join(p for p in out if p)


def render_archive(items: list[dict]) -> str:
    """인사이트 페이지: 카드 그리드 전체."""
    if not items:
        return (
            '<p class="insights-empty" style="grid-column:1/-1;">'
            "아직 발행된 글이 없어요. 곧 첫 번째 뉴스레터를 보내드릴게요.</p>"
        )

    out: list[str] = []
    for it in items:
        img = ""
        if it.get("image"):
            img = (
                '<div class="insights-card-img">'
                f'<img src="{esc(it["image"])}" alt="" loading="lazy" referrerpolicy="no-referrer">'
                "</div>"
            )
        out += [
            f'<a class="insights-card" href="{esc(it["link"])}" target="_blank" rel="noopener">',
            img,
            '<div class="insights-card-body">',
            f'<span class="insights-date">{esc(fmt_date_ko(it.get("date", "")))}</span>',
            f'<h3>{esc(it["title"])}</h3>',
            f'<p>{esc(it.get("summary", ""))}</p>',
            '<span class="insights-go">읽으러 가기 ↗</span>',
            "</div>",
            "</a>",
        ]
    return "\n".join(p for p in out if p)


def render_jsonld(items: list[dict]) -> str:
    """뉴스레터 목록을 ItemList + BlogPosting 으로 구조화."""
    if not items:
        return ""

    elements = []
    for i, it in enumerate(items, start=1):
        posting = {
            "@type": "BlogPosting",
            "headline": it["title"],
            "url": it["link"],
            "inLanguage": "ko-KR",
            "author": {"@id": f"{SITE}/profile#person"},
            "publisher": {"@id": f"{SITE}/#organization"},
            "isPartOf": {"@id": f"{SITE}/insights#webpage"},
        }
        if it.get("date"):
            posting["datePublished"] = it["date"]
        if it.get("summary"):
            posting["description"] = it["summary"]
        if it.get("image"):
            posting["image"] = it["image"]
        if it.get("categories"):
            posting["keywords"] = ", ".join(it["categories"])

        elements.append({"@type": "ListItem", "position": i, "item": posting})

    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "@id": f"{SITE}/insights#archive",
        "name": "오늘AI 뉴스레터 아카이브",
        "description": "미래가치개발원 Feelyoworks의 오늘AI 주간 뉴스레터 글 목록입니다.",
        "numberOfItems": len(elements),
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "itemListElement": elements,
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{body}\n</script>'


# ─────────────────────────── 주입 ───────────────────────────

def inject(path: pathlib.Path, marker: str, content: str) -> bool:
    """<!-- MARKER:START --> ... <!-- MARKER:END --> 사이를 교체. 변경 시 True."""
    text = path.read_text(encoding="utf-8")
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"

    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(f"ERROR: {path.name} 에서 {marker} 마커를 찾지 못했습니다.")

    replacement = f"{start}\n{content}\n{end}"
    new_text = pattern.sub(lambda _: replacement, text, count=1)

    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def update_sitemap(latest_date: str) -> bool:
    """
    홈과 /insights 의 lastmod 를 최신 발행일로 갱신.

    lastmod 는 절대 과거로 되돌리지 않습니다. 페이지 본문을 손으로 고쳐
    lastmod 를 오늘로 올려둔 경우, 마지막 발행글이 그보다 오래되었다고 해서
    날짜를 뒤로 끌어내리면 크롤러에게 "오히려 오래된 페이지"라는 잘못된
    신호를 주기 때문입니다.
    """
    if not latest_date or not SITEMAP_PATH.exists():
        return False

    text = SITEMAP_PATH.read_text(encoding="utf-8")
    original = text

    def bump_lastmod(xml: str, loc: str, date: str) -> str:
        pattern = re.compile(
            r"(<url>\s*<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)([^<]*)(</lastmod>)"
        )

        def repl(m: re.Match[str]) -> str:
            current = m.group(2).strip()
            newest = max(current, date) if current else date
            return m.group(1) + newest + m.group(3)

        return pattern.sub(repl, xml)

    for loc in (f"{SITE}/", f"{SITE}/insights"):
        text = bump_lastmod(text, loc, latest_date)

    if text == original:
        return False
    SITEMAP_PATH.write_text(text, encoding="utf-8")
    return True


# ─────────────────────────── 메인 ───────────────────────────

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
        if len(summary) > 220:
            summary = summary[:220].rstrip() + "…"

        if not title or not link:
            continue

        items.append({
            "title": title,
            "link": link,
            "date": parse_pubdate(pub_raw),
            "categories": categories[:3],
            "summary": summary,
            "image": first_image(content_html),
        })

    # 글 목록이 그대로면 updated 타임스탬프도 그대로 둡니다.
    # 매 실행마다 타임스탬프만 바꾸면 내용이 하나도 안 바뀐 날에도
    # 커밋과 재배포가 발생해, 변경 이력이 노이즈로 가득 차기 때문입니다.
    previous_updated = ""
    previous_items = None
    if OUT_PATH.exists():
        try:
            prev = json.loads(OUT_PATH.read_text(encoding="utf-8"))
            previous_updated = prev.get("updated", "")
            previous_items = prev.get("items")
        except Exception:
            pass

    unchanged = previous_items == items and bool(previous_updated)
    updated = previous_updated if unchanged else dt.datetime.now(
        dt.timezone.utc
    ).isoformat(timespec="seconds")

    payload = {"source": FEED_URL, "updated": updated, "items": items}

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"OK: {len(items)} items → {OUT_PATH.relative_to(ROOT)}"
        + ("  (no feed changes)" if unchanged else "")
    )

    changed = []
    if inject(INDEX_PATH, "INSIGHTS:HOME", render_home(items)):
        changed.append("index.html")
    if inject(INSIGHTS_PATH, "INSIGHTS:ARCHIVE", render_archive(items)):
        changed.append("insights.html (archive)")
    if inject(INSIGHTS_PATH, "INSIGHTS:JSONLD", render_jsonld(items)):
        changed.append("insights.html (json-ld)")

    latest = next((it["date"] for it in items if it.get("date")), "")
    if update_sitemap(latest):
        changed.append(f"sitemap.xml (lastmod={latest})")

    print("Updated: " + (", ".join(changed) if changed else "no HTML changes"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
