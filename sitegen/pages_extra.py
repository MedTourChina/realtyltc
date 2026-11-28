"""Framework chapters, tools, and long-form content pages."""

from __future__ import annotations

from . import config as C
from . import layout as L
from . import md, svg
from .pages import breadcrumb_ld, article_ld


# ------------------------------------------------------------------ framework

def framework_index() -> str:
    cards = "".join(L.layer_card(l) for l in C.LAYERS)

    body = f"""
<section class="section framework-hero">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">The framework</p>
      <h1 class="section-title display">Five decisions, in the order that saves you money</h1>
      <p class="section-sub">Everything a foreign buyer needs to settle before a price is discussed. Each layer has a stop condition: hit one and the purchase ends, which is usually the cheapest possible outcome.</p>
    </div>
    {L.flow([(l['name'], l['question']) for l in C.LAYERS])}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    {L.answer_box('How to use this', '<p>Read the five layers in order, once, before you look at any property. It takes about forty minutes. Then use the layer that matches where you actually are — most people discover they are on layer four while still undecided about layer one.</p>')}
    <div class="grid grid-3 layer-grid">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The stop conditions</p>
      <h2 class="section-title">What ends a purchase, and at which layer</h2>
      <p class="section-sub">These are the situations where the correct answer is to stop. Reading them first is faster than learning them at a signing table.</p>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <p class="eyebrow">Layer 1 — Eligibility</p>
        <ul class="risk-list">
          <li>Your residence permit is not work or study</li>
          <li>You cannot document twelve months in this city</li>
          <li>Your spouse already owns residential property in China</li>
          <li>The unit is 40- or 50-year commercial stock</li>
        </ul>
      </div>
      <div class="card">
        <p class="eyebrow">Layer 2 — Motive</p>
        <ul class="risk-list">
          <li>You expect to leave within three years</li>
          <li>You need the money to be liquid</li>
          <li>You are buying because prices might rise</li>
          <li>The rent you would pay is under 2% of the price</li>
        </ul>
      </div>
      <div class="card">
        <p class="eyebrow">Layer 4 — Asset</p>
        <ul class="risk-list">
          <li>Remaining land term is under 35 years</li>
          <li>The building has a heritage or demolition order</li>
          <li>The unit's registered use is not residential</li>
          <li>Management fees exceed 1.5% of price per year</li>
        </ul>
      </div>
      <div class="card">
        <p class="eyebrow">Layer 5 — Closing</p>
        <ul class="risk-list">
          <li>The seller cannot produce a clean title search</li>
          <li>Anyone asks you to pay a person, not an account</li>
          <li>The contract has no deposit-refund trigger</li>
          <li>The registered price is being understated</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="next-steps">
      <div>
        <p class="eyebrow">The companion page</p>
        <h2 class="section-title">Deciding is half of it. Checking is the other half.</h2>
      </div>
      <div class="next-steps-links">
        <a href="/verify/">How to verify anything you are told →</a>
        <a href="/tools/eligibility/">Run the eligibility check →</a>
        <a href="/tools/rent-vs-buy/">Model rent against buying →</a>
        <a href="/faq/">Common questions →</a>
      </div>
    </div>
  </div>
</section>"""

    return L.page(
        title="The framework",
        description="A five-layer decision framework for foreigners buying property in China: eligibility, motive, city, asset and closing — with a stop condition at every layer.",
        path="/framework/",
        body=body,
        nav_active="Framework",
        body_class="page-framework",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Framework", "/framework/")]),
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "The five layers",
                "itemListElement": [
                    {"@type": "ListItem", "position": l["n"], "name": l["question"],
                     "url": f"{C.SITE_URL}/framework/{l['slug']}/"}
                    for l in C.LAYERS
                ],
            },
        ],
    )


def framework_chapter(ch: dict, prev: dict | None, nxt: dict | None,
                      guides: list[dict], cities: list[dict] | None = None) -> str:
    body_html = md.render(ch["body"])
    toc_html = L.toc(md.headings(body_html))
    related_html = L.related(guides, title=f"Guides that support layer {ch['n']}")

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', '/framework/'), (f"Layer {ch['n']}", None)])}
    <p class="chapter-tag"><span class="chapter-num">{ch['n']:02d}</span> Layer {ch['n']} · {L.esc(ch['name'])}</p>
    <h1 class="chapter-title">{L.esc(ch['question'])}</h1>
    <p class="chapter-lede">{L.esc(ch['summary'])}</p>
  </div>
</header>

<div class="wrap chapter-layout">
  <aside class="chapter-rail">{L.rail(ch['slug'])}{toc_html}</aside>
  <div class="prose">
    {body_html}
    {L.tool_strip(ch['n'])}
    {L.city_strip(cities) if cities else ""}
  </div>
</div>

<div class="wrap">
  {L.pager(prev, nxt)}
</div>

{related_html}"""

    return L.page(
        title=f"Layer {ch['n']}: {ch['question']}",
        description=ch["description"],
        path=f"/framework/{ch['slug']}/",
        body=body,
        nav_active="Framework",
        body_class="page-chapter",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Framework", "/framework/"),
                           (f"Layer {ch['n']}", f"/framework/{ch['slug']}/")]),
            article_ld({
                "title": f"Layer {ch['n']}: {ch['question']}",
                "description": ch["description"],
                "updated": ch["updated"],
                "read": ch.get("read", 8),
            }, f"/framework/{ch['slug']}/"),
        ],
    )


# ---------------------------------------------------------------------- tools

def tools_index() -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Three tools</p>
      <h1 class="section-title display">Work it out before you ask anyone</h1>
      <p class="section-sub">These run entirely in your browser. Nothing is sent anywhere, nothing is stored, and there is no email field — because the point is your answer, not your address.</p>
    </div>
    <div class="grid grid-3">
      <a class="tool-card" href="/tools/eligibility/">
        <span class="tool-icon">{svg.icon('shield', 22)}</span>
        <h2 class="tool-card-title">Can I buy?</h2>
        <p class="tool-card-desc">Five questions on permit type, time in China, city and existing property. You get a verdict and the reasoning behind it.</p>
        <span class="tool-card-meta">Run the check</span>
      </a>
      <a class="tool-card" href="/tools/purchase-cost/">
        <span class="tool-icon">{svg.icon('chart', 22)}</span>
        <h2 class="tool-card-title">What will it really cost?</h2>
        <p class="tool-card-desc">Deed tax at the actual threshold, commission, notarisation and registration — plus the seller's taxes if they push them onto you.</p>
        <span class="tool-card-meta">Open the calculator</span>
      </a>
      <a class="tool-card" href="/tools/rent-vs-buy/">
        <span class="tool-icon">{svg.icon('scale', 22)}</span>
        <h2 class="tool-card-title">Rent or buy?</h2>
        <p class="tool-card-desc">A net-worth comparison over your own horizon, including the round-trip cost of buying and selling.</p>
        <span class="tool-card-meta">Compare</span>
      </a>
    </div>
    {L.editorial_note('These are models, not forecasts. They will not tell you what prices will do; they will tell you what a decision costs under assumptions you choose — which is the part you control.')}
  </div>
</section>"""

    return L.page(
        title="Tools",
        description="Three browser-based calculators for foreign property buyers in China: eligibility, full purchase cost, and rent versus buy.",
        path="/tools/",
        body=body,
        nav_active="Tools",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/")])],
    )


def _tool_epilogue(layer_n: int, links: list[tuple[str, str, str]],
                   terms: list[str] | None = None,
                   cities: list[dict] | None = None) -> str:
    """A calculator that ends in a number is a dead end. Hand the reader back to
    the reasoning the number sits inside, and to the checklist."""
    l = C.LAYERS[layer_n - 1]
    rows = [(f"Layer {l['n']} — {l['name']}: {l['question']}",
             f"/framework/{l['slug']}/",
             "The reasoning this figure sits inside.")]
    rows += list(links)
    rows.append(("Open the decision sheet", "/framework/decision-sheet/",
                 "Twenty-five checks and fifteen stop conditions, on one printable page."))
    items = "".join(
        '<a class="step-card" href="' + href + '">'
        '<span class="step-card-title">' + L.esc(title) + '</span>'
        '<span class="step-card-arrow">\u2192</span>'
        '<span class="step-card-reason">' + L.esc(reason) + '</span></a>'
        for title, href, reason in rows
    )
    strip = ""
    if terms:
        strip = L.term_chips_by_ids(terms, "The words this calculator is built on")
    city_html = L.city_strip(cities) if cities else ""
    return (
        '<section class="section"><div class="wrap">'
        '<p class="eyebrow">What a calculator cannot decide</p>'
        '<h2 class="section-title">The number is the start of the argument, not the end of it.</h2>'
        '<p class="section-sub">This tool answers one question. The framework is where '
        'that answer is tested against the other four.</p>'
        '<div class="tool-strip-grid mt-2">' + items + '</div>'
        + strip + city_html +
        '</div></section>'
    )


def eligibility_tool(cities: list[dict]) -> str:
    city_opts = "".join(f'<option value="{L.esc(c["name"])}">{L.esc(c["name"])}</option>' for c in cities)
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('Eligibility', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 1 · Eligibility</p>
      <h1 class="section-title display">Can you buy?</h1>
      <p class="section-sub">Five questions. The output is an indicative position, not a permission — the permission comes from a district housing bureau, in writing, and this tool tells you what to ask them.</p>
    </div>
    <div class="tool-shell">
      <div class="quiz" data-quiz="eligibility">
        <fieldset class="quiz-step">
          <legend><span class="quiz-n">1</span> What is your current residence permit for?</legend>
          <label class="opt"><input type="radio" name="permit" value="work"><span>Work or study (Z, X, or a work-type residence permit)</span></label>
          <label class="opt"><input type="radio" name="permit" value="family"><span>Family reunion or dependant</span></label>
          <label class="opt"><input type="radio" name="permit" value="other"><span>Tourist, business, or short stay</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">2</span> How long have you worked or studied in mainland China, with documents?</legend>
          <label class="opt"><input type="radio" name="tenure" value="long"><span>More than a year, continuously</span></label>
          <label class="opt"><input type="radio" name="tenure" value="short"><span>Less than a year</span></label>
          <label class="opt"><input type="radio" name="tenure" value="gap"><span>More than a year, but with gaps between employers</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">3</span> Will you buy in the city where you work or study?</legend>
          <label class="opt"><input type="radio" name="city" value="same"><span>Yes, same city</span></label>
          <label class="opt"><input type="radio" name="city" value="other"><span>No, a different city</span></label>
          <label class="opt"><input type="radio" name="city" value="unsure"><span>Not sure — my employer is registered elsewhere</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">4</span> Does anyone in your household already own residential property in China?</legend>
          <label class="opt"><input type="radio" name="existing" value="none"><span>No</span></label>
          <label class="opt"><input type="radio" name="existing" value="spouse"><span>Yes — my spouse does</span></label>
          <label class="opt"><input type="radio" name="existing" value="self"><span>Yes — I do</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">5</span> What kind of unit are you considering?</legend>
          <label class="opt"><input type="radio" name="type" value="residential"><span>Residential, 70-year land term</span></label>
          <label class="opt"><input type="radio" name="type" value="commercial"><span>40- or 50-year apartment, loft or office</span></label>
          <label class="opt"><input type="radio" name="type" value="unsure"><span>Not sure what it is</span></label>
        </fieldset>

        <button class="btn btn-primary btn-lg" type="button" data-quiz-run>Show my position</button>
        <div class="quiz-result" data-quiz-result hidden></div>
      </div>

      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">Then do this</p>
          <p>Whatever this says, the next step is the same: take your documents to the district housing bureau and ask for an eligibility confirmation in writing. The script is on the verification page.</p>
          <a class="btn btn-ghost btn-block mt-2" href="/verify/">How to verify</a>
        </div>
        <div class="card mt-2">
          <p class="eyebrow">Why five questions</p>
          <p>These are the five facts the housing bureau will actually establish. Everything else — budget, district, taste — comes later, and is irrelevant if any of these fails.</p>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="Can a foreigner buy? Eligibility check",
        description="Five questions that establish whether you can buy residential property in China, with the reasoning behind the verdict.",
        path="/tools/eligibility/",
        body=body + _tool_epilogue(1, [
            ("Read the one-year rule", "/guides/the-one-year-rule/", "What counts as a year of work or study, and what does not."),
            ("See how the twelve cities differ", "/cities/", "The same rule, administered twelve different ways."),
        ], terms=["purchase-restriction", "residence-registration", "online-contract-registration"],
           cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/calc.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("Eligibility", "/tools/eligibility/")])],
    )


def cost_tool(cities: list[dict]) -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('Purchase cost', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 2 · Motive, and the arithmetic</p>
      <h1 class="section-title display">What will it really cost?</h1>
      <p class="section-sub">The price is the number you negotiate. This is the number you pay. Adjust the assumptions and watch the 140m² threshold and the seller's taxes do their work.</p>
    </div>
    <div class="tool-shell">
      <div class="calc" data-calc="cost">
        <div class="calc-row">
          <div class="field">
            <label for="c-price">Purchase price (¥)</label>
            <input id="c-price" type="number" data-in="price" value="10000000" min="0" step="100000">
          </div>
          <div class="field">
            <label for="c-area">Registered area (m²)</label>
            <input id="c-area" type="number" data-in="area" value="118" min="10" step="1">
          </div>
          <div class="field">
            <label for="c-home">Your position</label>
            <select id="c-home" data-in="home">
              <option value="first">First home</option>
              <option value="second">Second home</option>
              <option value="third">Third home or more</option>
            </select>
          </div>
          <div class="field">
            <label for="c-use">Land use of the unit</label>
            <select id="c-use" data-in="use">
              <option value="residential">Residential (70-year)</option>
              <option value="commercial">Commercial (40 or 50-year)</option>
            </select>
          </div>
          <div class="field">
            <label for="c-agency">Agency commission (%)</label>
            <input id="c-agency" type="number" data-in="agency" value="1" min="0" max="5" step="0.1">
          </div>
          <div class="field">
            <label for="c-seller">Who pays the seller's taxes?</label>
            <select id="c-seller" data-in="seller">
              <option value="seller">Seller pays (clean deal)</option>
              <option value="buyer">Pushed onto me</option>
            </select>
          </div>
        </div>
        <div class="calc-out">
          <div class="calc-total">
            <span>All-in, on top of price</span>
            <strong data-out="total">—</strong>
          </div>
          <ul class="calc-breakdown">
            <li><span>Deed tax</span><b data-out="deed">—</b></li>
            <li><span>Agency commission</span><b data-out="agency">—</b></li>
            <li><span>Notarisation</span><b data-out="notary">—</b></li>
            <li><span>Registration</span><b data-out="reg">—</b></li>
            <li><span>Legal due diligence</span><b data-out="legal">—</b></li>
            <li><span>Seller-side taxes</span><b data-out="sellerTax">—</b></li>
            <li class="calc-sum"><span>Total purchase cost</span><b data-out="grand">—</b></li>
          </ul>
          <p class="calc-note" data-out="note"></p>
        </div>
      </div>
      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">The rules behind it</p>
          <ul class="risk-list">
            <li>Deed tax is 1% up to 140m² for a first or second home, 1.5–2% above that</li>
            <li>Commercial stock is charged at 3% regardless of area</li>
            <li>VAT and income tax are the seller's, but are often pushed onto the buyer</li>
            <li>140m² is a cliff, not a gradient</li>
          </ul>
          <a class="btn btn-ghost btn-block mt-2" href="/guides/the-full-cost-of-buying-a-home-in-china/">Read the cost guide</a>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="Purchase cost calculator",
        description="Work out the true all-in cost of buying property in China: deed tax at the 140m² threshold, commission, notarisation, registration and seller-side taxes.",
        path="/tools/purchase-cost/",
        body=body + _tool_epilogue(2, [
            ("Why the exit costs more than the entry", "/guides/exit-and-repatriation/", "The channel your money came in through decides whether it can leave."),
            ("Compare renting and buying", "/tools/rent-vs-buy/", "The same flat, the same horizon, held as an asset or as a payment."),
        ], terms=["deed-tax", "value-added-tax", "individual-income-tax", "five-years-only-home"],
           cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/calc.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("Purchase cost", "/tools/purchase-cost/")])],
    )


def rentbuy_tool(cities: list[dict]) -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('Rent vs buy', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 2 · Motive</p>
      <h1 class="section-title display">Rent or buy, over your horizon</h1>
      <p class="section-sub">At gross yields of 1.4–2% in the major cities, renting is not the financially irrational choice it is often presented as. Model your own numbers before anyone models them for you.</p>
    </div>
    <div class="tool-shell">
      <div class="calc" data-calc="rentbuy">
        <div class="calc-row">
          <div class="field">
            <label for="r-price">Purchase price (¥)</label>
            <input id="r-price" type="number" data-in="price" value="10000000" step="100000">
          </div>
          <div class="field">
            <label for="r-rent">Comparable monthly rent (¥)</label>
            <input id="r-rent" type="number" data-in="rent" value="12000" step="500">
          </div>
          <div class="field">
            <label for="r-down">Down payment (%)</label>
            <input id="r-down" type="number" data-in="down" value="40" min="10" max="100" step="5">
          </div>
          <div class="field">
            <label for="r-rate">Mortgage rate (%)</label>
            <input id="r-rate" type="number" data-in="rate" value="3.2" min="0" max="10" step="0.1">
          </div>
          <div class="field">
            <label for="r-years">Your horizon (years)</label>
            <input id="r-years" type="number" data-in="years" value="7" min="1" max="30" step="1">
          </div>
          <div class="field">
            <label for="r-growth">Annual price growth (%)</label>
            <input id="r-growth" type="number" data-in="growth" value="0" min="-10" max="10" step="0.5">
          </div>
        </div>
        <div class="calc-out">
          <div class="calc-total">
            <span>Net worth difference at year <span data-out="horizon">7</span></span>
            <strong data-out="delta">—</strong>
          </div>
          <ul class="calc-breakdown">
            <li><span>Buying: cash out over the period</span><b data-out="buyOut">—</b></li>
            <li><span>Buying: equity if you sell</span><b data-out="buyEquity">—</b></li>
            <li><span>Renting: rent paid over the period</span><b data-out="rentPaid">—</b></li>
            <li><span>Renting: deposit invested at 4%</span><b data-out="rentInvest">—</b></li>
            <li class="calc-sum"><span>Verdict</span><b data-out="verdict">—</b></li>
          </ul>
          <p class="calc-note" data-out="note"></p>
        </div>
      </div>
      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">What this model assumes</p>
          <ul class="risk-list">
            <li>25-year amortising mortgage, no early repayment</li>
            <li>Round-trip transaction cost of 8% on purchase and sale</li>
            <li>Rent grows 3% a year; a 40% down payment is invested at 4% if you rent</li>
            <li>No tax on the invested deposit, no maintenance, no vacancy</li>
          </ul>
          <p class="calc-note">The assumptions are deliberately plain. Change them to match your own situation — the conclusion should be robust to the ones you are unsure about.</p>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="Rent vs buy calculator",
        description="Compare renting and buying property in China over your own horizon, including transaction costs and the opportunity cost of a down payment.",
        path="/tools/rent-vs-buy/",
        body=body + _tool_epilogue(2, [
            ("Read the full cost of buying", "/guides/the-full-cost-of-buying-a-home-in-china/", "The eight to eleven percent round trip, itemised."),
            ("Work out the purchase cost", "/tools/purchase-cost/", "Deed tax, commission and the seller's taxes."),
        ], terms=["property-management-fee", "maintenance-fund", "shared-floor-area"],
           cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/calc.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("Rent vs buy", "/tools/rent-vs-buy/")])],
    )


# ------------------------------------------------------------- content pages

def _next_step_html(post: dict) -> str:
    """Every guide ends by handing the reader to a tool, not by trailing off."""
    layer = post.get("layer")
    if not layer:
        return ""
    return L.next_step(int(layer))


def content_page(post: dict, *, nav_active: str | None = None,
                 cities: list[dict] | None = None) -> str:
    body_html = md.render(post["body"])
    toc_html = L.toc(md.headings(body_html))
    kicker = post.get("kicker", "")
    terms_html = L.term_chips_by_ids(post.get("terms") or [], "The words this page turns on")
    city_html = L.city_strip(cities) if (post.get("want_cities") and cities) else ""

    body = f"""
<header class="article-head">
  <div class="wrap">
    {L.crumbs(post["crumbs"])}
    {f'<p class="eyebrow mt-2">{L.esc(kicker)}</p>' if kicker else ''}
    <h1 class="article-title">{L.esc(post['title'])}</h1>
    <p class="article-standfirst">{L.esc(post['description'])}</p>
  </div>
</header>
<div class="wrap article-layout article-layout-content">
  <div class="prose">{body_html}{terms_html}{city_html}{_next_step_html(post)}</div>
  <aside class="article-aside">{toc_html}</aside>
</div>"""

    return L.page(
        title=post["title"],
        description=post["description"],
        path=post["path"],
        body=body,
        nav_active=nav_active,
        body_class="page-content",
        jsonld=[breadcrumb_ld(post["crumbs"])],
    )


def _faq_item(x: dict) -> str:
    """An answer that ends the conversation is a wasted answer. Every entry
    carries the two places to go next."""
    see = x.get("see") or []
    links = "".join(
        f'<a href="{L.esc(s["href"])}">{L.esc(s["label"])}</a>' for s in see
    )
    more = (f'<p class="faq-see"><span class="faq-see-label">Go deeper</span>{links}</p>'
            if links else "")
    return (f'<details class="faq-item"><summary>{L.esc(x["q"])}</summary>'
            f'<div class="faq-a"><p>{L.esc(x["a"])}</p>{more}</div></details>')


def faq_page(items: list[dict], cities: list[dict] | None = None) -> str:
    order = ["Eligibility", "Money", "Transaction", "Living"]
    blocks = []
    for cat in order:
        group = [x for x in items if x["category"] == cat]
        if not group:
            continue
        qs = "".join(_faq_item(x) for x in group)
        blocks.append(f'<h2 class="section-title sub-head" id="{md.slugify(cat)}">{L.esc(cat)}</h2><div class="faq-group">{qs}</div>')

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": x["q"],
             "acceptedAnswer": {"@type": "Answer", "text": x["a"]}}
            for x in items
        ],
    }

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('FAQ', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Straight answers</p>
      <h1 class="section-title display">Questions people actually ask</h1>
      <p class="section-sub">Short answers, with the guide or framework layer that goes deeper linked from most of them. Nothing here is a substitute for a written answer from your district bureau.</p>
    </div>
    {''.join(blocks)}
    {L.term_chips_by_ids(["residence-registration", "online-contract-registration", "deposit", "deed-tax"], "The words in these answers")}
    {L.city_strip(cities) if cities else ""}
  </div>
</section>"""

    return L.page(
        title="FAQ",
        description="Short, direct answers to the questions foreign buyers ask most often about property in China.",
        path="/faq/",
        body=body,
        nav_active="About",
        jsonld=[breadcrumb_ld([("Home", "/"), ("FAQ", "/faq/")]), faq_ld],
    )


def decision_sheet(sheet_layers: list[dict]) -> str:
    by_n = {l["n"]: l for l in C.LAYERS}
    blocks = []

    for entry in sheet_layers:
        n = int(entry["layer"])
        meta = by_n.get(n)
        if not meta:
            continue

        checks = "".join(
            '<li><label class="sheet-opt">'
            f'<input type="checkbox" data-check="{L.esc(c["id"])}">'
            '<span class="sheet-mark" aria-hidden="true"></span>'
            f'<span class="sheet-text">{L.esc(c["text"])}</span>'
            "</label></li>"
            for c in entry["checks"]
        )
        stops = "".join(
            '<li><label class="sheet-opt sheet-opt-stop">'
            f'<input type="checkbox" data-stop="{L.esc(c["id"])}">'
            '<span class="sheet-mark" aria-hidden="true"></span>'
            f'<span class="sheet-text">{L.esc(c["text"])}</span>'
            "</label></li>"
            for c in entry["stops"]
        )

        tools = C.LAYER_TOOLS.get(n, [])
        tool_links = " · ".join(f'<a href="{h}">{L.esc(lbl)}</a>' for lbl, h, _ in tools)
        tool_html = (f'<p class="sheet-layer-tools">Work this layer out first: {tool_links}</p>'
                     if tool_links else "")

        blocks.append(f"""
<section class="sheet-layer" data-layer="{n}" data-slug="{meta['slug']}" data-name="{L.esc(meta['name'])}">
  <div class="sheet-layer-head">
    <span class="sheet-layer-num">{n:02d}</span>
    <div class="sheet-layer-title-wrap">
      <h2 class="sheet-layer-title">{L.esc(meta['name'])}</h2>
      <p class="sheet-layer-q">{L.esc(meta['question'])}</p>
    </div>
    <a class="sheet-layer-link" href="/framework/{meta['slug']}/">Read layer {n}</a>
  </div>
  <p class="sheet-group-label">Tick each line that is true</p>
  <ul class="sheet-list">{checks}</ul>
  <p class="sheet-group-label sheet-group-stop">Stop conditions — any one of these ends the purchase</p>
  <ul class="sheet-list">{stops}</ul>
  {tool_html}
</section>""")

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', '/framework/'), ('Decision sheet', None)])}
    <p class="eyebrow">Layers 1 to 5, in order</p>
    <h1 class="chapter-title display">The decision sheet</h1>
    <p class="chapter-lede">Twenty-five things to confirm and fifteen things that end the purchase, arranged so that failure stays cheap.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="sheet-intro prose">
      <p>This is the framework as a working document. Answer layer 1 before doing anything else: if a stop condition there is true, none of the rest of this page applies to you. Each layer is meant to be settled before you spend money on the next one.</p>
      <p>Your ticks are stored in this browser and nowhere else. There is no account, no form and no submission — if you want a record, print the page and keep it with your notes.</p>
    </div>

    <div class="sheet" data-sheet>
      <div class="sheet-top">
        <div class="sheet-meter">
          <p class="sheet-progress" data-progress>0 of 5 layers cleared</p>
          <div class="sheet-bar" aria-hidden="true"><span data-bar style="width:0%"></span></div>
        </div>
        <div class="sheet-actions">
          <button type="button" class="sheet-print" data-sheet-print>Print my results</button>
          <button type="button" class="sheet-reset" data-sheet-reset>Clear all</button>
        </div>
      </div>
      <div class="sheet-verdict" data-verdict hidden></div>
      <div class="sheet-print-report" data-print-report aria-live="polite"></div>
      <p class="sheet-print-hint">Print my results opens your browser's print dialog. Choose “Save as PDF” to keep a dated snapshot; the full checklist can still be printed below.</p>
      {''.join(blocks)}
      <p class="sheet-foot">Print this page and take it to your lawyer. A ticked box is your own answer, not evidence — the sheet exists to show you which answers you have not actually checked.</p>
    </div>

    <div class="sheet-intro prose">
      <p><strong>What this sheet is not.</strong> It is not a legal opinion, a valuation, or a prediction. It does not tell you whether prices will rise. It is a way of finding out, in ten minutes and for nothing, whether a purchase you are considering fails on the first two layers — which is where most purchases by foreign buyers actually fail.</p>
      <p>If you want the reasoning behind any line, follow it back to <a href="/framework/">the framework</a>. If you want the vocabulary you will hear at the counter, the <a href="/glossary/">glossary</a> has the twenty-four terms that come up most often, with the characters you will see on paper.</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="The decision sheet",
        description="The five-layer framework as a working checklist: twenty-five checks and fifteen stop conditions for foreign buyers of property in China.",
        path="/framework/decision-sheet/",
        body=body,
        nav_active="Framework",
        body_class="page-chapter",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Framework", "/framework/"),
                               ("Decision sheet", "/framework/decision-sheet/")])],
        extra_scripts=f'<script src="/js/decision.js?v={C.ASSET_V}" defer></script>',
    )


def glossary(entries: list[dict], guides: list[dict]) -> str:
    titles = {g["slug"]: g["title"] for g in guides}
    ordered = sorted(entries, key=lambda e: e["english"].lower())

    by_letter: dict[str, list[dict]] = {}
    for e in ordered:
        by_letter.setdefault(e["english"][0].upper(), []).append(e)

    def card(e: dict) -> str:
        gid = md.slugify(e["english"])
        see = "".join(
            f'<a href="/guides/{L.esc(s)}/">{L.esc(titles.get(s, s.replace("-", " ")))}</a>'
            for s in e.get("see", []) if s
        )
        see_html = f'<p class="gterm-see">Where this matters: {see}</p>' if see else ""
        return f"""
<li class="gterm" id="{gid}">
  <div class="gterm-head">
    <h3 class="gterm-zh">{L.esc(e['term'])}</h3>
    <p class="gterm-py">{L.esc(e['pinyin'])}</p>
    <p class="gterm-en">{L.esc(e['english'])}</p>
  </div>
  <p class="gterm-def">{L.esc(e['def'])}</p>
  {see_html}
</li>"""

    jump = "".join(f'<a href="#letter-{k}">{k}</a>' for k in by_letter)
    sections = "".join(
        f'<h2 class="g-letter" id="letter-{k}">{k}</h2>'
        f'<ul class="g-list">{"".join(card(e) for e in group)}</ul>'
        for k, group in by_letter.items()
    )

    term_set = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Glossary of Chinese property terms",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": e["english"],
             "alternateName": e["term"], "description": e["def"]}
            for e in ordered
        ],
    }

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Glossary', None)])}
    <p class="eyebrow">{len(entries)} terms</p>
    <h1 class="chapter-title display">The words on the paperwork</h1>
    <p class="chapter-lede">Every term you are likely to meet at a counter or on a certificate, with the characters, the pinyin, and what it actually decides.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="glossary-intro prose">
      <p>Property in China is discussed in a vocabulary that carries legal weight and is almost never translated in the room. Knowing the four characters on a certificate is the difference between understanding what you own and being told what you own.</p>
      <p>The pinyin is included because you will hear these words spoken long before you see them written. Say the term out loud once; it is the fastest way to stop a conversation that has moved past you.</p>
    </div>
    <nav class="g-jump" aria-label="Jump to letter">{jump}</nav>
    {sections}
    <div class="glossary-intro prose">
      <p>If a term you met is missing, that is a gap worth reporting — <a href="/about/">tell us</a> and it will be added with the same treatment.</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Glossary",
        description="Twenty-four Chinese property terms with characters, pinyin and plain-English definitions, from 契税 to 资金监管.",
        path="/glossary/",
        body=body,
        body_class="page-chapter",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Glossary", "/glossary/")]), term_set],
    )


def not_found() -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    <div class="notfound">
      <p class="eyebrow">404</p>
      <h1 class="section-title display">That page does not exist</h1>
      <p class="section-sub">It may have been renamed when the site moved from a commercial model to a purely editorial one. The framework is a good place to pick up again.</p>
      <p class="mt-2">{L.btn('The framework', '/framework/', 'primary')} {L.btn('All cities', '/cities/', 'ghost', icon_name=None)}</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Page not found",
        description="Page not found.",
        path="/404.html",
        body=body,
        noindex=True,
    )
