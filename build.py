#!/usr/bin/env python3
"""Build the Lifetourchina Realty static site.

    python build.py            # write to dist/
    python build.py --serve    # build, then serve dist/ on localhost:8080

Zero third-party dependencies. Python 3.10+.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen import config as C          # noqa: E402
from sitegen import layout as L          # noqa: E402
from sitegen import svg                  # noqa: E402
from sitegen import pages, pages_extra   # noqa: E402

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

# Which layer each guide belongs to. Used for tagging cards and for the
# "guides that support this layer" block on framework chapters.
GUIDE_LAYERS = {
    "can-foreigners-buy-property-in-china": 1,
    "the-one-year-rule": 1,
    "the-full-cost-of-buying-a-home-in-china": 2,
    "mortgages-for-foreign-buyers": 2,
    "property-tax-in-china": 2,
    "seventy-fifty-forty-year-land-use": 4,
    "buying-off-plan-vs-resale": 4,
    "escrow-and-payment-stages": 5,
    "moving-money-into-china-for-property": 5,
    "renting-in-china-as-a-foreigner": 5,
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def human_date(iso: str) -> str:
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        return f"{d} {MONTHS[m - 1]} {y}"
    except (ValueError, IndexError):
        return C.LAST_UPDATED


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a `---` delimited frontmatter block from the body."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.strip()
        if raw[:1] in "[{":
            try:
                meta[key] = json.loads(raw)
                continue
            except json.JSONDecodeError:
                pass
        meta[key] = raw.strip('"').strip("'")
    return meta, parts[2].lstrip("\n")


def load_json(name: str):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def load_guides() -> list[dict]:
    guides = []
    for path in sorted((CONTENT / "guides").glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = meta.get("slug") or path.stem
        guide = {
            "slug": slug,
            "title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "category": meta.get("category", "Living"),
            "answer": meta.get("answer", ""),
            "answer_md": "",           # the :::answer block lives in the body
            "updated": meta.get("updated", "2026-01-01"),
            "updated_human": human_date(meta.get("updated", "2026-01-01")),
            "read": meta.get("read", "8"),
            "author": meta.get("author", C.AUTHOR_NAME),
            "reviewer": meta.get("reviewer", C.REVIEWER_NAME),
            "body": body,
            "layer": GUIDE_LAYERS.get(slug),
            "related": [x.strip() for x in (meta.get("related") or "").split(",") if x.strip()],
        }
        guides.append(guide)
    order = ["Legal & eligibility", "Money & tax", "Transaction", "Living"]
    guides.sort(key=lambda g: (order.index(g["category"]) if g["category"] in order else 9, g["title"]))
    return guides


def load_framework(guides: list[dict]) -> list[dict]:
    chapters = []
    for layer in C.LAYERS:
        path = CONTENT / "framework" / f"{layer['slug']}.md"
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        chapters.append({
            **layer,
            "description": meta.get("description", layer["summary"]),
            "updated": meta.get("updated", "2026-01-01"),
            "updated_human": human_date(meta.get("updated", "2026-01-01")),
            "read": meta.get("read", "8"),
            "author": meta.get("author", C.AUTHOR_NAME),
            "reviewer": meta.get("reviewer", C.REVIEWER_NAME),
            "body": body,
        })
    return chapters


def load_pages() -> list[dict]:
    out = []
    for path in sorted((CONTENT / "pages").glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        out.append({
            "slug": path.stem,
            "title": meta.get("title", path.stem),
            "description": meta.get("description", ""),
            "kicker": meta.get("kicker", ""),
            "path": meta.get("path", f"/{path.stem}/"),
            "crumbs": meta.get("crumbs", [["Home", "/"], [meta.get("title", path.stem), None]]),
            "body": body,
            "updated": meta.get("updated", "2026-01-01"),
        })
    return out


def write(rel: str, html: str) -> None:
    target = DIST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def url_to_file(path: str) -> str:
    if path.endswith(".html"):
        return path.lstrip("/")
    if path.endswith("/"):
        return path.lstrip("/") + "index.html"
    return path.lstrip("/") + "/index.html"


# ------------------------------------------------------------------ og image

def make_og_image() -> bool:
    """Draw a 1200x630 social card if Pillow and a system font are available."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False

    fonts = [
        Path(r"C:\Windows\Fonts\georgia.ttf"),
        Path(r"C:\Windows\Fonts\georgiab.ttf"),
        Path(r"C:\Windows\Fonts\times.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
        Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
    ]
    serif = next((f for f in fonts if f.exists()), None)
    sans_candidates = [
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    sans = next((f for f in sans_candidates if f.exists()), None)
    if not serif or not sans:
        return False

    W, H = 1200, 630
    ink = (18, 25, 43)
    amber = (217, 138, 58)
    paper = (250, 248, 244)

    img = Image.new("RGB", (W, H), ink)
    d = ImageDraw.Draw(img)

    # amber glow, approximated with concentric ellipses
    for i in range(28, 0, -1):
        a = 4 + i
        r = 90 * i
        d.ellipse([180 - r, 60 - r, 180 + r, 60 + r], fill=(18 + a, 25 + a // 2, 43 - a // 4))

    skyline = [
        (0, 540, 60, 90), (62, 505, 40, 125), (104, 555, 54, 75), (160, 470, 34, 160),
        (196, 520, 48, 110), (246, 545, 30, 85), (278, 480, 58, 150), (338, 530, 36, 100),
        (376, 500, 46, 130), (424, 560, 62, 70), (488, 490, 40, 140), (530, 545, 52, 85),
        (584, 470, 36, 160), (622, 515, 60, 115), (684, 550, 28, 80), (714, 495, 44, 135),
        (760, 545, 58, 85), (820, 505, 34, 125), (856, 555, 50, 75), (908, 475, 40, 155),
        (950, 540, 30, 90), (982, 515, 52, 115), (1036, 550, 38, 80), (1076, 490, 46, 140),
        (1124, 545, 40, 85), (1166, 520, 34, 110),
    ]
    for x, y, w, h in skyline:
        d.rectangle([x + 12, y + 58, x + 12 + w, H], fill=(26, 34, 58))

    # brand mark
    cx = 92
    d.rounded_rectangle([cx - 8, 96, cx + 8, 102], radius=3, fill=paper)
    d.rounded_rectangle([cx - 26, 112, cx + 26, 122], radius=5, fill=paper)
    d.rounded_rectangle([cx - 20, 126, cx + 20, 214], radius=18, fill=amber)
    d.rounded_rectangle([cx - 4, 138, cx + 4, 200], radius=4, fill=(255, 250, 244))
    d.rounded_rectangle([cx - 24, 216, cx + 24, 226], radius=5, fill=paper)

    f_title = ImageFont.truetype(str(serif), 78)
    f_sub = ImageFont.truetype(str(sans), 30)
    f_small = ImageFont.truetype(str(sans), 24)

    def tracked(xy, text, font, fill, tracking):
        """Draw letter-spaced text; Pillow has no tracking option."""
        x, y = xy
        for ch in text:
            d.text((x, y), ch, font=font, fill=fill)
            x += d.textlength(ch, font=font) + tracking

    tracked((160, 100), "LIFETOURCHINA", ImageFont.truetype(str(sans), 23),
            (250, 248, 244), 5.2)
    tracked((160, 130), "REALTY", ImageFont.truetype(str(sans), 23),
            (217, 138, 58), 5.2)

    d.text((160, 176), "Before you look at", font=f_title, fill=(250, 248, 244))
    d.text((160, 258), "a single apartment", font=f_title, fill=(250, 248, 244))
    d.text((160, 340), "in China.", font=f_title, fill=amber)

    d.text((160, 462), "Five decisions before the price — and how to check each one.",
           font=f_sub, fill=(196, 198, 206))
    d.text((160, 508), "Free · independent · no advertising · no data collected",
           font=f_small, fill=(150, 152, 162))

    (STATIC / "img").mkdir(parents=True, exist_ok=True)
    img.save(STATIC / "img" / "og.png", "PNG", optimize=True)
    return True


# ------------------------------------------------------------------- builder

def asset_version() -> str:
    """Short hash of the CSS/JS bundle, used to bust the immutable cache."""
    import hashlib

    digest = hashlib.sha1()
    for path in sorted(list((STATIC / "css").glob("*")) + list((STATIC / "js").glob("*"))):
        digest.update(path.read_bytes())
    return digest.hexdigest()[:8]


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)

    C.ASSET_V = asset_version()

    cities = load_json("cities.json")
    faq = load_json("faq.json")
    guides = load_guides()
    chapters = load_framework(guides)
    content_pages = load_pages()

    written: list[tuple[str, str]] = []   # (path, lastmod)

    # home
    write("index.html", pages.home(cities, guides))
    written.append(("/", "2026-03-06"))

    # framework
    write(url_to_file("/framework/"), pages_extra.framework_index())
    written.append(("/framework/", "2026-03-06"))
    for i, ch in enumerate(chapters):
        prev = chapters[i - 1] if i > 0 else None
        nxt = chapters[i + 1] if i + 1 < len(chapters) else None
        layer_guides = [g for g in guides if g.get("layer") == ch["n"]] or guides[:3]
        write(url_to_file(f"/framework/{ch['slug']}/"),
              pages_extra.framework_chapter(ch, prev, nxt, layer_guides))
        written.append((f"/framework/{ch['slug']}/", ch["updated"]))

    # cities
    write(url_to_file("/cities/"), pages.cities_index(cities))
    written.append(("/cities/", "2026-03-06"))
    core = [g for g in guides if g["slug"] in (
        "can-foreigners-buy-property-in-china", "the-one-year-rule",
        "the-full-cost-of-buying-a-home-in-china", "escrow-and-payment-stages")]
    for city in cities:
        write(url_to_file(f"/cities/{city['slug']}/"),
              pages.city_page(city, cities, core))
        written.append((f"/cities/{city['slug']}/", "2026-03-06"))

    # guides
    write(url_to_file("/guides/"), pages.guides_index(guides))
    written.append(("/guides/", "2026-03-06"))
    by_slug = {g["slug"]: g for g in guides}
    for g in guides:
        rel = [by_slug[s] for s in g["related"] if s in by_slug][:3]
        if len(rel) < 3:
            for cand in guides:
                if cand["slug"] != g["slug"] and cand not in rel:
                    rel.append(cand)
                if len(rel) == 3:
                    break
        write(url_to_file(f"/guides/{g['slug']}/"), pages.guide_page(g, rel))
        written.append((f"/guides/{g['slug']}/", g["updated"]))

    # tools
    write(url_to_file("/tools/"), pages_extra.tools_index())
    written.append(("/tools/", "2026-03-06"))
    write(url_to_file("/tools/eligibility/"), pages_extra.eligibility_tool(cities))
    written.append(("/tools/eligibility/", "2026-03-06"))
    write(url_to_file("/tools/purchase-cost/"), pages_extra.cost_tool(cities))
    written.append(("/tools/purchase-cost/", "2026-03-06"))
    write(url_to_file("/tools/rent-vs-buy/"), pages_extra.rentbuy_tool())
    written.append(("/tools/rent-vs-buy/", "2026-03-06"))

    # content pages (verify, about, legal)
    for post in content_pages:
        write(url_to_file(post["path"]), pages_extra.content_page(post, nav_active="About"))
        written.append((post["path"], post["updated"]))

    # faq + 404
    write(url_to_file("/faq/"), pages_extra.faq_page(faq))
    written.append(("/faq/", "2026-03-06"))
    write("404.html", pages_extra.not_found())

    # static assets
    for sub in ("css", "js"):
        src = STATIC / sub
        dst = DIST / sub
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*"):
            shutil.copy2(f, dst / f.name)

    (DIST / "img").mkdir(parents=True, exist_ok=True)
    (DIST / "img" / "favicon.svg").write_text(svg.FAVICON, encoding="utf-8")
    if (STATIC / "img" / "og.png").exists():
        shutil.copy2(STATIC / "img" / "og.png", DIST / "img" / "og.png")

    # sitemap
    today = date.today().isoformat()
    entries = "".join(
        f"  <url><loc>{C.SITE_URL}{path}</loc><lastmod>{lastmod}</lastmod>"
        f"<changefreq>{'weekly' if path == '/' else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if path == '/' else '0.7'}</priority></url>\n"
        for path, lastmod in written
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + entries + f"<!-- generated {today} -->\n</urlset>\n",
        encoding="utf-8",
    )

    (DIST / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {C.SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )

    (DIST / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  X-Frame-Options: DENY\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; script-src 'self'; "
        "form-action 'none'; base-uri 'self'\n\n"
        "/css/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
        "/js/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
        "/img/*\n  Cache-Control: public, max-age=31536000, immutable\n",
        encoding="utf-8",
    )

    (DIST / "_redirects").write_text(
        "# Legacy paths from the pre-launch structure\n"
        "/services/*  /framework/  301\n"
        "/listings/*  /cities/     301\n"
        "/contact/    /about/      301\n",
        encoding="utf-8",
    )

    pages_count = len(written)
    print(f"built {pages_count} pages -> {DIST}")
    print(f"  cities:    {len(cities)}")
    print(f"  guides:    {len(guides)}")
    print(f"  framework: {len(chapters)}")
    print(f"  pages:     {len(content_pages)}")


if __name__ == "__main__":
    if "--og" in sys.argv:
        print("og image:", "written" if make_og_image() else "skipped (no Pillow/font)")
    build()
    if "--serve" in sys.argv:
        import http.server
        import socketserver
        import functools
        import os
        os.chdir(DIST)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        with socketserver.TCPServer(("127.0.0.1", 8080), handler) as httpd:
            print("serving http://127.0.0.1:8080")
            httpd.serve_forever()
