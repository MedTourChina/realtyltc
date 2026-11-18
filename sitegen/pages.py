"""Page builders: home, city index, city detail, guide index, guide detail."""

from __future__ import annotations

from . import config as C
from . import layout as L
from . import md, svg

esc = L.esc

ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": C.SITE_NAME,
    "url": C.SITE_URL,
    "description": C.SITE_DESCRIPTION,
}

WEBSITE_LD = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": C.SITE_NAME,
    "url": C.SITE_URL,
    "description": C.SITE_DESCRIPTION,
    "inLanguage": "en",
}


def breadcrumb_ld(items: list[tuple[str, str | None]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": (C.SITE_URL + href) if href else C.SITE_URL + "/",
            }
            for i, (name, href) in enumerate(items)
        ],
    }


def article_ld(post: dict, path: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "dateModified": post["updated"],
        "datePublished": post["updated"],
        "inLanguage": "en",
        "author": {"@type": "Person", "name": post.get("author", C.AUTHOR_NAME)},
        "reviewedBy": {"@type": "Person", "name": post.get("reviewer", C.REVIEWER_NAME)},
        "publisher": {"@type": "Organization", "name": C.SITE_NAME, "url": C.SITE_URL},
        "mainEntityOfPage": C.SITE_URL + path,
    }


# --------------------------------------------------------------------- home

def home(cities: list[dict], guides: list[dict]) -> str:
    layer_rows = "".join(
        f"""<li>
          <span class="hero-layer-num">{l['n']:02d}</span>
          <span class="hero-layer-q">{esc(l['question'])}</span>
          <span class="hero-layer-name">{esc(l['name'])}</span>
        </li>"""
        for l in C.LAYERS
    )

    hero = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="hero-kicker"><span class="dot"></span> Free · independent · no advertising</p>
      <h1 class="hero-title">Before you look at a<br>single apartment in <em>China</em>.</h1>
      <p class="hero-sub">There are five decisions before the price, and most foreign buyers get to the fifth one without having made the first. This is the order, the rules, and how to check each of them yourself.</p>
      <div class="hero-actions">
        {L.btn('Start with layer 1', '/framework/eligibility/', 'light', size='lg', icon_name='arrow')}
        {L.btn('See the whole framework', '/framework/', 'outline-light', size='lg', icon_name=None)}
      </div>
      <div class="hero-stats">
        {L.stat('5', 'layers, in order', 'each one can veto')}
        {L.stat('12', 'cities compared', 'same seven dimensions')}
        {L.stat('0', 'things we sell', 'and no data collected')}
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-panel">
        <p class="hero-panel-kicker">The five decisions</p>
        <ol class="hero-layers">{layer_rows}</ol>
        <p class="hero-panel-note">Read left to right. A "no" at any layer ends the purchase — that is the point of doing them in order.</p>
      </div>
    </div>
  </div>
</section>"""

    why = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Why this exists</p>
      <h2 class="section-title">The information is not missing. The order is.</h2>
      <p class="section-sub">English-language material about Chinese property is abundant and almost entirely unstructured. Every source answers one question; nobody tells you which question comes first, or when to walk away.</p>
    </div>
    <div class="grid grid-3">
      <div class="pillar">
        <p class="pillar-num">01 — Sequence</p>
        <h3 class="pillar-title">Order changes the answer</h3>
        <p>Eligibility, motive, city, asset, closing. Ask them out of order and you will fall in love with an apartment in a city where you cannot legally buy it — the most expensive mistake in this market, and the most common.</p>
      </div>
      <div class="pillar">
        <p class="pillar-num">02 — Veto</p>
        <h3 class="pillar-title">Someone has to say no</h3>
        <p>Your agent is paid when you buy. Your lawyer is paid either way. Nobody in the chain is paid to tell you to wait, so this site is written to help you conclude "not yet" as quickly as possible.</p>
      </div>
      <div class="pillar">
        <p class="pillar-num">03 — Verification</p>
        <h3 class="pillar-title">Paths, not conclusions</h3>
        <p>We do not tell you a city is fine. We tell you which counter to stand at, which three questions to ask, and what a written answer looks like — because the rules are applied locally.</p>
      </div>
    </div>
  </div>
</section>"""

    flow_block = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The sequence</p>
      <h2 class="section-title">Five decisions, in this order</h2>
      <p class="section-sub">Each layer has a stop condition. If you hit one, stop — you have saved yourself the cost of finding out later.</p>
    </div>
    {L.flow([(l['name'], l['question']) for l in C.LAYERS])}
    <p class="mt-2">{L.btn('Open the framework', '/framework/', 'primary')}</p>
  </div>
</section>"""

    layers = "".join(L.layer_card(l) for l in C.LAYERS)
    layer_block = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Read in order</p>
      <h2 class="section-title">The five layers</h2>
    </div>
    <div class="grid grid-3 layer-grid">{layers}</div>
  </div>
</section>"""

    city_cards = "".join(L.city_card(c, i) for i, c in enumerate(cities))
    cities_block = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Layer 3, applied</p>
      <h2 class="section-title">Twelve cities, one set of questions</h2>
      <p class="section-sub">Same seven dimensions everywhere — eligibility practice, price band, yield, buyer pool, service depth, schools and commute, and the risks specific to that market.</p>
    </div>
    <div class="grid grid-4">{city_cards}</div>
    <p class="mt-2">{L.btn('Compare all cities', '/cities/', 'ghost')}</p>
  </div>
</section>"""

    tools = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Work it out yourself</p>
      <h2 class="section-title">Three calculators that run in your browser</h2>
      <p class="section-sub">No accounts, no uploads, nothing leaves the page. They exist to help you reach a decision, not to collect a lead.</p>
    </div>
    <div class="grid grid-3">
      <a class="tool-card" href="/tools/eligibility/">
        <span class="tool-icon">{svg.icon('shield', 22)}</span>
        <h3 class="tool-card-title">Can I buy?</h3>
        <p class="tool-card-desc">Five questions on permit, time in China, city and existing property. Get a verdict and the reason behind it.</p>
        <span class="tool-card-meta">Run the check</span>
      </a>
      <a class="tool-card" href="/tools/purchase-cost/">
        <span class="tool-icon">{svg.icon('chart', 22)}</span>
        <h3 class="tool-card-title">What will it really cost?</h3>
        <p class="tool-card-desc">Price, area and who pays the seller's taxes — the closing figure most buyers never compute.</p>
        <span class="tool-card-meta">Open the calculator</span>
      </a>
      <a class="tool-card" href="/tools/rent-vs-buy/">
        <span class="tool-icon">{svg.icon('scale', 22)}</span>
        <h3 class="tool-card-title">Rent or buy?</h3>
        <p class="tool-card-desc">Model your own horizon. At 1.5–2% gross yields, the arithmetic decides more cases than the advice does.</p>
        <span class="tool-card-meta">Compare</span>
      </a>
    </div>
  </div>
</section>"""

    latest = "".join(L.guide_card(g) for g in guides[:3])
    guides_block = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The fact base</p>
      <h2 class="section-title">Dated, sourced, and willing to say no</h2>
      <p class="section-sub">Every guide shows when it was last checked and who checked it. If a rule has moved, the page says so at the top rather than quietly ageing.</p>
    </div>
    <div class="grid grid-3">{latest}</div>
    <p class="mt-2">{L.btn('All guides', '/guides/', 'ghost')}</p>
  </div>
</section>"""

    pledge = f"""
<section class="section">
  <div class="wrap">
    <div class="pledge-band">
      <div>
        <p class="eyebrow">What this is not</p>
        <h2 class="section-title">No agents. No referrals. No fees.</h2>
      </div>
      <ul class="pledge-list">
        <li>{svg.icon('check', 16)}<span>No advertising, no sponsored content, no affiliate links</span></li>
        <li>{svg.icon('check', 16)}<span>No commissions from agents, lawyers, lenders or developers</span></li>
        <li>{svg.icon('check', 16)}<span>No forms, no newsletters, no accounts, no tracking</span></li>
        <li>{svg.icon('check', 16)}<span>No named recommendations — only how to vet people yourself</span></li>
      </ul>
    </div>
    <p class="pledge-close">The only thing we ask is that you use the framework before you use anyone else's advice. <a href="/about/">Why this exists</a>.</p>
  </div>
</section>"""

    body = hero + why + flow_block + layer_block + cities_block + tools + guides_block + pledge
    return L.page(
        title=C.SITE_NAME,
        description=C.SITE_DESCRIPTION,
        path="/",
        body=body,
        nav_active=None,
        body_class="page-home",
        jsonld=[ORG_LD, WEBSITE_LD],
    )


# -------------------------------------------------------------------- cities

def cities_index(cities: list[dict]) -> str:
    cards = "".join(L.city_card(c, i) for i, c in enumerate(cities))
    rows = "".join(
        f"""<tr>
      <td><a href="/cities/{c['slug']}/"><strong>{L.esc(c['name'])}</strong></a><br><span class="muted">{L.esc(c['name_zh'])}</span></td>
      <td>{L.esc(c['region'])}</td>
      <td class="nowrap">{L.esc(c['price_band'])}</td>
      <td class="nowrap">{L.esc(c['yield_band'])}</td>
      <td>{L.esc(c['best_for'])}</td>
    </tr>"""
        for c in cities
    )

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Cities', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 3 · City</p>
      <h1 class="section-title display">Twelve markets, one comparison</h1>
      <p class="section-sub">These are the cities where foreigners actually buy. Each one is assessed on the same seven dimensions, so a comparison between two of them means something — and so that a city can be ruled out for a reason better than "I liked it there".</p>
    </div>
    <div class="grid grid-4">{cards}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">At a glance</p>
      <h2 class="section-title">Compare on the numbers</h2>
      <p class="section-sub">Indicative secondary-market asking prices and gross yields, compiled from public listings. Yields are gross of management fees, heating and vacancy, which together remove roughly a third.</p>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>City</th><th>Region</th><th>Median asking</th><th>Gross yield</th><th>Best suited to</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    {L.editorial_note('Ranges, not appraisals. Check the specific unit against recent registered transactions in the same building before you use any number here in a negotiation.')}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="quote-block">
      <p class="quote-text">A city is not a market. It is a set of rules, a set of commutes, and a set of people who will one day buy from you.</p>
      <p class="quote-cite">The three things layer 3 asks you to judge</p>
    </div>
    <p class="mt-2">{L.btn('How to judge a city', '/framework/city/', 'primary')} {L.btn('How to verify what a seller tells you', '/verify/', 'ghost', icon_name=None)}</p>
  </div>
</section>"""

    return L.page(
        title="Cities",
        description="Twelve Chinese cities compared for foreign property buyers on one set of dimensions: prices, yields, eligibility practice, buyer pool and risk.",
        path="/cities/",
        body=body,
        nav_active="Cities",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Cities", "/cities/")])],
    )


def city_page(city: dict, cities: list[dict], guides: list[dict]) -> str:
    sky = svg.skyline(city["slug"], 1400, 130, "currentColor", 1, "skyline")
    intro = "".join(f"<p>{L.esc(p)}</p>" for p in city["intro"])
    districts = "".join(
        f"""<div class="district">
      <div><h3 class="district-name">{L.esc(d['name'])}<span class="district-zh">{L.esc(d['zh'])}</span></h3></div>
      <p>{L.esc(d['note'])}</p>
    </div>"""
        for d in city["districts"]
    )
    risks = "".join(f"<li>{L.esc(r)}</li>" for r in city["risks"])
    guide_cards = "".join(L.guide_card(g) for g in guides)

    body = f"""
<section class="city-hero">
  <div class="city-hero-sky">{sky}</div>
  <div class="wrap city-hero-inner">
    <div>
      {L.crumbs([('Home', '/'), ('Cities', '/cities/'), (city['name'], None)])}
      <h1 class="city-hero-title mt-2">{L.esc(city['name'])}<span class="city-hero-zh">{L.esc(city['name_zh'])} · {L.esc(city['pinyin'])}</span></h1>
      <p class="city-hero-sub">{L.esc(city['tagline'])}</p>
    </div>
    <dl class="city-facts">
      <div class="city-fact"><dt>Median asking</dt><dd>{L.esc(city['price_band'])}</dd></div>
      <div class="city-fact"><dt>Gross yield</dt><dd>{L.esc(city['yield_band'])}</dd></div>
      <div class="city-fact"><dt>Purchase cap</dt><dd>One self-use home</dd></div>
      <div class="city-fact"><dt>Land term</dt><dd>70 years, residential</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(2rem,5vw,4rem)">
      <div class="prose">
        {intro}
        {L.answer_box('Can a foreigner buy here?', f"<p>{L.esc(city['eligibility'])}</p>")}
        <p>{L.esc(city['foreign_note'])}</p>
      </div>
      <aside class="card side-card">
        <p class="eyebrow">Before you view anything here</p>
        <p>The paragraph above is a summary, not an answer. City practice is applied at district level and changes without much notice.</p>
        <p><strong>Take it to the counter:</strong> ask the district housing bureau to confirm your eligibility in writing, using the script in <a href="/verify/">how to verify</a>.</p>
        <a class="btn btn-primary btn-block mt-2" href="/verify/">How to check it</a>
      </aside>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Where to live</p>
      <h2 class="section-title">Districts that work for foreign buyers</h2>
      <p class="section-sub">Not every district is workable at every stage. These are the ones with the schools, services and resale liquidity foreigners actually need.</p>
    </div>
    <div class="district-list">{districts}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="gap:2.5rem">
      <div>
        <p class="eyebrow">The market</p>
        <h2 class="section-title">How {L.esc(city['name'])} actually trades</h2>
        <p class="section-sub">{L.esc(city['market'])}</p>
        <p class="eyebrow mt-2">Living here</p>
        <h2 class="section-title">Settling in</h2>
        <p class="section-sub">{L.esc(city['settling'])}</p>
      </div>
      <div class="card">
        <p class="eyebrow">Know before you offer</p>
        <h2 class="section-title" style="font-size:1.45rem">Three risks in this market</h2>
        <ul class="risk-list">{risks}</ul>
        <hr class="rule">
        <p class="eyebrow">Best suited to</p>
        <p class="mt-1">{L.esc(city['best_for'])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Before you commit</p>
      <h2 class="section-title">Read these first</h2>
    </div>
    <div class="grid grid-3">{guide_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="next-steps">
      <div>
        <p class="eyebrow">Carry on through the framework</p>
        <h2 class="section-title">A city is layer three. Two layers decide whether it matters.</h2>
      </div>
      <div class="next-steps-links">
        <a href="/framework/eligibility/">01 · Can you buy at all →</a>
        <a href="/framework/motive/">02 · Should you buy →</a>
        <a href="/framework/asset/">04 · Which property →</a>
        <a href="/framework/closing/">05 · How to close →</a>
      </div>
    </div>
  </div>
</section>"""

    return L.page(
        title=f"Buying property in {city['name']} as a foreigner",
        description=(f"{city['tagline']} Foreign-buyer rules, districts, price bands "
                     f"({city['price_band']}) and gross yields ({city['yield_band']}) in {city['name']}."),
        path=f"/cities/{city['slug']}/",
        body=body,
        nav_active="Cities",
        body_class="page-city",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Cities", "/cities/"), (city["name"], f"/cities/{city['slug']}/")]),
            {
                "@context": "https://schema.org",
                "@type": "Place",
                "name": city["name"],
                "alternateName": city["name_zh"],
                "address": {"@type": "PostalAddress", "addressCountry": "CN", "addressRegion": city["region"]},
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [{
                    "@type": "Question",
                    "name": f"Can a foreigner buy property in {city['name']}?",
                    "acceptedAnswer": {"@type": "Answer", "text": city["eligibility"]},
                }],
            },
        ],
    )


# -------------------------------------------------------------------- guides

def guides_index(guides: list[dict]) -> str:
    order = ["Legal & eligibility", "Money & tax", "Transaction", "Living"]
    buckets: dict[str, list[dict]] = {k: [] for k in order}
    for g in guides:
        buckets.setdefault(g["category"], []).append(g)

    blocks = []
    for cat in order:
        group = buckets.get(cat) or []
        if not group:
            continue
        cards = "".join(L.guide_card(g) for g in group)
        blocks.append(f"""
    <h2 class="section-title sub-head" id="{md.slugify(cat)}">{L.esc(cat)}</h2>
    <div class="grid grid-3 mt-2">{cards}</div>""")

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Guides', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">The fact base</p>
      <h1 class="section-title display">Guides, written to be finished</h1>
      <p class="section-sub">Each guide answers a question a foreign buyer actually asked, carries a review date, and has been checked against the rule it describes. They support the framework; they do not replace it.</p>
    </div>
    {''.join(blocks)}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="quote-block">
      <p class="quote-text">Read the framework first. Then use these pages to check a specific rule, not to find an opinion.</p>
      <p class="quote-cite">{L.btn('Open the framework', '/framework/', 'primary')}</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Guides",
        description="In-depth English guides to buying, financing, registering and owning property in China as a foreigner — dated and reviewed.",
        path="/guides/",
        body=body,
        nav_active="Guides",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Guides", "/guides/")])],
    )


def guide_page(post: dict, related: list[dict]) -> str:
    body_html = md.render(post["body"])
    toc_html = L.toc(md.headings(body_html))
    answer_html = L.answer_box("The short answer", md.render(post["answer_md"])) if post["answer_md"] else ""

    layer = post.get("layer")
    layer_html = ""
    if layer:
        l = C.LAYERS[layer - 1]
        layer_html = f"""
      <a class="layer-strip" href="/framework/{l['slug']}/">
        <span class="layer-strip-num">{l['n']:02d}</span>
        <span class="layer-strip-text">Part of Layer {l['n']} — {esc(l['name'])}: {esc(l['question'])}</span>
        {svg.icon('arrow', 16)}
      </a>"""

    body = f"""
<article>
  <header class="article-head">
    <div class="wrap">
      {L.crumbs([('Home', '/'), ('Guides', '/guides/'), (post['title'], None)])}
      <p class="eyebrow mt-2">{L.esc(post['category'])}</p>
      <h1 class="article-title">{L.esc(post['title'])}</h1>
      <p class="article-standfirst">{L.esc(post['description'])}</p>
      {L.byline(post)}
      {layer_html}
    </div>
  </header>
  <div class="wrap article-layout">
    <aside class="article-aside">
      <div class="card side-card">
        <p class="eyebrow">General information</p>
        <p>This page explains how a rule works. It cannot tell you how the rule applies to your file — that answer comes from a specific counter in a specific district, and we show you how to get it in writing.</p>
        <a class="btn btn-ghost btn-block mt-2" href="/verify/">How to verify</a>
      </div>
    </aside>
    <div class="prose">
      {answer_html}
      {body_html}
      {L.editorial_note('General information only — not legal, tax or investment advice. Rules change, and city practice varies. Confirm the position for your own file before acting.')}
    </div>
    <aside class="article-aside">
      {toc_html}
    </aside>
  </div>
</article>

{L.related(related)}"""

    return L.page(
        title=post["title"],
        description=post["description"],
        path=f"/guides/{post['slug']}/",
        body=body,
        nav_active="Guides",
        body_class="page-guide",
        og_type="article",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Guides", "/guides/"), (post["title"], f"/guides/{post['slug']}/")]),
            article_ld(post, f"/guides/{post['slug']}/"),
        ],
    )
