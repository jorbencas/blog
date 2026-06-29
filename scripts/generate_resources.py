#!/usr/bin/env python3
"""Generate enhanced resources.mdx with categories, favicons, names, and descriptions.

Idempotent: skips already-known favicon URLs and doesn't re-process own output.
"""

import json
import re
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_FILE = BASE_DIR / "src" / "content" / "posts" / "resources.mdx"
BACKUP_FILE = BASE_DIR / "src" / "content" / "posts" / "resources.mdx.bak"
ENTRIES_FILE = BASE_DIR / "data" / "herramientas.json"

FAVICON_BASE = "https://www.google.com/s2/favicons?domain={domain}&sz=32"

with open(ENTRIES_FILE, encoding="utf-8") as _f:
    ENTRIES: dict = json.load(_f)

CATEGORY_ORDER = [
    "Componentes UI", "Iconos", "Frameworks", "State Management",
    "Hosting / Nube", "APIs", "CMS", "Testing", "Rendimiento", "Monorepos",
    "Utilidades Dev", "Herramientas Dev", "Herramientas Terminal",
    "Herramientas Multimedia", "Extensiones",
    "Aprendizaje", "Documentación", "Comunidad", "Blogs / Referencias",
    "Diseño", "Programación Reactiva",
    "AI", "Productividad", "Desarrollo UI", "Juegos",
]

CAT_ICON = {
    "Iconos": "🎨", "Componentes UI": "🧩", "Utilidades Dev": "🛠️",
    "Aprendizaje": "📚", "APIs": "🔌", "Diseño": "✨",
    "CMS": "📝", "Herramientas Multimedia": "🎬",
    "Comunidad": "💬", "Documentación": "📖",
    "Frameworks": "⚙️", "Herramientas Terminal": "💻",
    "Hosting / Nube": "☁️", "Herramientas Dev": "🔧",
    "State Management": "📦", "Rendimiento": "⚡",
    "Monorepos": "🏗️", "Testing": "🧪",
    "Desarrollo UI": "🎯", "Programación Reactiva": "🔄",
    "Blogs / Referencias": "📝", "Productividad": "⏱️",
    "AI": "🤖", "Juegos": "🎮", "Extensiones": "🧩",
}

FM = """\
---
draft: false
title: "Recursos para desarrolladores"
description: "Colección curada de herramientas, librerías, plataformas, APIs y referencias para el desarrollo web y de software."
pubDate: "2025-04-01"
tags: ['recursos', 'herramientas', 'desarrollo-web', 'ui', 'hosting', 'aprendizaje', 'referencias', 'api']
image: "img/resources_cover-1200.webp"
author: "Jorge Beneyto Castelló"
---"""


def domain_from(url: str) -> str:
    return urlparse(url).netloc.replace('www.', '')


def classify(url: str) -> dict | None:
    domain = domain_from(url)
    # path-specific first (e.g. github.com/pmndrs/zustand before github.com)
    for key, entry in ENTRIES.items():
        if '/' in key and key in url:
            return entry
    # exact domain
    if domain in ENTRIES:
        return ENTRIES[domain]
    # base domain (last 2 parts)
    parts = domain.split('.')
    if len(parts) >= 2:
        base = '.'.join(parts[-2:])
        if base in ENTRIES:
            return ENTRIES[base]
    # substring fallback (only for keys without '/')
    for key, entry in ENTRIES.items():
        if '/' not in key and key in url:
            return entry
    return None


def extract_clean_urls(text: str) -> list[str]:
    """Extract URLs, excluding favicon URLs and already-generated content."""
    seen = set()
    result = []
    for u in re.findall(r'https?://[^\s\n<>"\'\)]+', text):
        u = u.rstrip('.,;:)!?')
        # Skip favicon URLs / google services
        if 'google.com/s2/favicons' in u or 'googleusercontent.com' in u:
            continue
        if u in seen:
            continue
        seen.add(u)
        result.append(u)
    return result


def build_new_content(all_urls: list[str]) -> str:
    """Build the full MDX content from a clean list of URLs."""
    seen_entry = set()
    by_cat: dict[str, list[tuple[str, str, str, str]]] = {}  # cat → [(name, url, desc, domain)]

    for url in all_urls:
        cls = classify(url)
        if cls:
            key = (cls["name"], cls["cat"])
            if key not in seen_entry:
                seen_entry.add(key)
                dom = domain_from(url)
                by_cat.setdefault(cls["cat"], []).append((cls["name"], url, cls["desc"], dom))
        else:
            dom = domain_from(url)
            by_cat.setdefault("_uncat", []).append((url, dom))

    lines = [
        "¡Bienvenido a mi colección curada de recursos! Aquí encontrarás herramientas, librerías, plataformas y referencias",
        "que uso o he usado en mi día a día como desarrollador. Cada recurso incluye una breve descripción y posibles",
        "casos de uso para que sepas cuándo puede serte útil.\n",
    ]

    # Categorised
    for cat in sorted((c for c in by_cat if c != "_uncat"), key=lambda c: CATEGORY_ORDER.index(c) if c in CATEGORY_ORDER else 999):
        items = sorted(by_cat[cat], key=lambda x: x[0].lower())
        icon = CAT_ICON.get(cat, "📌")
        lines.append(f"## {icon} {cat}\n")
        for name, url, desc, dom in items:
            fv = FAVICON_BASE.format(domain=dom)
            lines.append(
                f'- <img src="{fv}" width="16" height="16" '
                f'style="vertical-align:middle;margin-right:6px" alt="{name}" /> '
                f'**[{name}]({url})** — {desc}'
            )
        lines.append("")

    # Uncategorised
    if "_uncat" in by_cat:
        lines.append("## 📌 Sin categorizar\n")
        for url, dom in sorted(set(by_cat["_uncat"])):
            fv = FAVICON_BASE.format(domain=dom)
            lines.append(f'- <img src="{fv}" width="16" height="16" style="vertical-align:middle;margin-right:6px" /> {url}')
        lines.append("")

    return FM + "\n\n" + "\n".join(lines) + "\n"


def main():
    raw = RESOURCES_FILE.read_text(encoding='utf-8').lstrip('\n\r ')

    # Strip frontmatter
    body = re.sub(r'^---\n.*?\n---\n*', '', raw, count=1, flags=re.DOTALL).strip()

    urls = extract_clean_urls(body)
    new_content = build_new_content(urls)

    # Backup original
    BACKUP_FILE.write_text(raw, encoding='utf-8')

    RESOURCES_FILE.write_text(new_content, encoding='utf-8')
    # Stats
    cats = set()
    uncat = 0
    for url in urls:
        cls = classify(url)
        if cls:
            cats.add(cls["cat"])
        else:
            uncat += 1
    print(f"✅ {RESOURCES_FILE} actualizado")
    print(f"   Categorías: {len(cats)}")
    print(f"   Recursos listados: {len(set((classify(u)['name'], classify(u)['cat']) for u in urls if classify(u)))}")
    print(f"   Sin clasificar: {uncat}")
    print(f"   Backup guardado en {BACKUP_FILE}")


if __name__ == "__main__":
    main()
