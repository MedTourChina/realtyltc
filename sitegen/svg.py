"""Inline SVG assets: icon set, procedural city skylines, brand mark.

The site ships zero raster images. Skylines are generated deterministically
from a per-city seed so each city card has a distinct silhouette while the
whole set stays visually consistent.
"""

from __future__ import annotations

import random

_PATHS = {
    "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-up": '<path d="M7 17 17 7M8 7h9v9"/>',
    "check": '<path d="M4 12.5 9 17.5 20 6.5"/>',
    "pin": '<path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "scale": '<path d="M12 4v16M7 20h10M4 8h16M4 8l-2 5a3 3 0 0 0 6 0L6 8M20 8l-2 5a3 3 0 0 0 6 0l-2-5"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "key": '<circle cx="8" cy="8" r="4"/><path d="m11 11 9 9M17 14l3-3M20 17l2-2"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16V11M12.5 16V7M17 16v-4"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "phone": '<path d="M6.5 3.5 9 3l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2 .5 2.5A2 2 0 0 1 19.4 20C11 19.5 4.5 13 4 4.6a2 2 0 0 1 2.5-1.1z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.3 3.8 5.3 3.8 8.5S14.5 18.2 12 20.5C9.5 18.2 8.2 15.2 8.2 12S9.5 5.8 12 3.5z"/>',
    "home": '<path d="m3.5 10.5 8.5-7 8.5 7V20a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1v-9.5z"/><path d="M9.5 21v-6h5v6"/>',
    "file": '<path d="M13 3.5H7a1.5 1.5 0 0 0-1.5 1.5v14A1.5 1.5 0 0 0 7 20.5h10a1.5 1.5 0 0 0 1.5-1.5V9l-5.5-5.5z"/><path d="M13 3.5V9h5.5M8.5 13h7M8.5 16.5h4.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "chevron": '<path d="m6 9.5 6 6 6-6"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c0-3 2.5-5.2 5.5-5.2s5.5 2.2 5.5 5.2"/><path d="M16 5.2a3.2 3.2 0 0 1 0 6.2M17.5 14.9c1.8.6 3 2.3 3 4.4"/>',
    "spark": '<path d="M12 3.5 13.9 9l5.6 1.9-5.6 1.9L12 18.5l-1.9-5.7L4.5 10.9 10.1 9 12 3.5z"/>',
}


def icon(name: str, size: int = 20, cls: str = "icon") -> str:
    path = _PATHS.get(name, _PATHS["spark"])
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{path}</svg>'
    )


def skyline(seed: str, width: int = 340, height: int = 104, fill: str = "currentColor",
            opacity: float = 1.0, cls: str = "skyline") -> str:
    """Deterministic procedural skyline for a city card."""
    rnd = random.Random(seed)
    parts: list[str] = []
    x = 0.0
    while x < width:
        w = min(rnd.randint(13, 33), width - x)
        if w < 7:
            break
        h = rnd.randint(int(height * 0.22), int(height * 0.94))
        y = height - h
        parts.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="{h}"/>')
        roll = rnd.random()
        cx = x + w / 2
        if roll < 0.16:
            parts.append(f'<rect x="{cx - 1:.0f}" y="{max(y - 14, 0)}" width="2" height="14"/>')
        elif roll < 0.30:
            inner = round(w * 0.56)
            parts.append(
                f'<rect x="{x + (w - inner) / 2:.0f}" y="{max(y - 9, 0)}" width="{inner}" height="9"/>'
            )
        elif roll < 0.40:
            parts.append(
                f'<path d="M{x:.0f} {y:.0f} L{cx:.0f} {max(y - h * 0.22, 0):.0f} '
                f'L{x + w:.0f} {y:.0f} Z"/>'
            )
        x += w + rnd.choice([1, 2, 2, 3, 5])

    return (
        f'<svg class="{cls}" viewBox="0 0 {width} {height}" preserveAspectRatio="none" '
        f'fill="{fill}" opacity="{opacity}" aria-hidden="true" focusable="false">'
        + "".join(parts)
        + "</svg>"
    )


BRAND_MARK = (
    '<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
    '<circle cx="16" cy="17" r="13" fill="currentColor" opacity=".08"/>'
    '<rect x="13" y="1.5" width="6" height="2.6" rx="1.3" fill="currentColor"/>'
    '<path d="M16 4v2.4" stroke="currentColor" stroke-width="1.6"/>'
    '<rect x="7.5" y="6.4" width="17" height="4" rx="2" fill="currentColor" opacity=".9"/>'
    '<path d="M9.6 10.4h12.8c1.1 3.4 1.1 12.2 0 15.2H9.6c-1.1-3-1.1-11.8 0-15.2z" '
    'fill="var(--amber)"/>'
    '<rect x="14.4" y="12.6" width="3.2" height="11" rx="1.6" fill="#fff" opacity=".75"/>'
    '<rect x="7.8" y="25.7" width="16.4" height="2.6" rx="1.3" fill="currentColor"/>'
    "</svg>"
)

FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="7" fill="#12192b"/>'
    '<rect x="13" y="5" width="6" height="2.4" rx="1.2" fill="#faf8f4"/>'
    '<rect x="8" y="9" width="16" height="3.4" rx="1.7" fill="#faf8f4"/>'
    '<path d="M10 12.4h12c1 3.2 1 11 0 13.6H10c-1-2.6-1-10.4 0-13.6z" fill="#d98a3a"/>'
    '<rect x="14.6" y="14.4" width="2.8" height="9.6" rx="1.4" fill="#fff" opacity=".8"/>'
    '<rect x="8.4" y="25.6" width="15.2" height="2.4" rx="1.2" fill="#faf8f4"/>'
    "</svg>"
)
