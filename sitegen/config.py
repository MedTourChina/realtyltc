"""Site-wide configuration.

This project is deliberately non-commercial: there is no company behind it,
no advertising, no referral fees and no data collection. Nothing in the
configuration should imply otherwise.
"""

from __future__ import annotations

SITE_NAME = "Lantern"
SITE_TAGLINE = "China property, made clear."
SITE_DESCRIPTION = (
    "A free, independent framework for foreigners buying property in China — "
    "the five decisions that come before the price, and how to verify each one yourself."
)

SITE_URL = "https://lanternchina.com"

# Corrections only. There is no sales inbox, because there is no sales.
CORRECTIONS_EMAIL = "notes@lanternchina.com"

LEGAL_ENTITY = "An independent editorial project"
LAST_UPDATED = "March 2026"

AUTHOR_NAME = "Maya Chen"
AUTHOR_ROLE = "Editor"
REVIEWER_NAME = "Wei Lian"
REVIEWER_ROLE = "Property counsel, Shanghai"

# The five layers are the spine of the site. Order matters: each layer can
# veto the purchase before the next one is reached.
LAYERS = [
    {
        "n": 1,
        "slug": "eligibility",
        "name": "Eligibility",
        "question": "Can you buy at all?",
        "summary": "One self-use home, in the city where you work, after a documented year in China.",
    },
    {
        "n": 2,
        "slug": "motive",
        "name": "Motive",
        "question": "Should you buy?",
        "summary": "At 1.4–2% gross yields, this is a consumption decision before it is an investment one.",
    },
    {
        "n": 3,
        "slug": "city",
        "name": "City",
        "question": "Which city?",
        "summary": "The same seven dimensions applied to twelve markets, so the comparison is honest.",
    },
    {
        "n": 4,
        "slug": "asset",
        "name": "Asset",
        "question": "Which property?",
        "summary": "70, 50 and 40 years are three different asset classes, not three ages of building.",
    },
    {
        "n": 5,
        "slug": "closing",
        "name": "Closing",
        "question": "How do you verify and settle?",
        "summary": "Money moves against documents, never against promises.",
    },
]

NAV = [
    ("Framework", "/framework/"),
    ("Cities", "/cities/"),
    ("Guides", "/guides/"),
    ("Tools", "/tools/"),
    ("About", "/about/"),
]

FOOTER_NAV = [
    (
        "The framework",
        [("Overview", "/framework/")] + [
            (f"{l['n']}. {l['name']}", f"/framework/{l['slug']}/") for l in LAYERS
        ],
    ),
    (
        "Explore",
        [
            ("Cities", "/cities/"),
            ("Guides", "/guides/"),
            ("Tools", "/tools/"),
            ("How to verify", "/verify/"),
        ],
    ),
    (
        "About",
        [
            ("What this is", "/about/"),
            ("Questions", "/faq/"),
            ("Disclaimer", "/legal/disclaimer/"),
        ],
    ),
]

# Shown on every page footer. It is the whole business model.
PLEDGE = (
    "No advertising. No commissions. No accounts. No forms. "
    "This site collects nothing about you and sells nothing to anyone."
)

USD_CNY = 7.15
