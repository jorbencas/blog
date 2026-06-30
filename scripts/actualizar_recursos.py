#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


SECTION_ID = "nuevas-herramientas"
SECTION_TITLE = "🆕 Nuevas Herramientas Descubiertas"

SECTION_HEADER = (
    '<div class="not-prose mt-12 mb-6"><h2 '
    'class="inline-flex items-center gap-2 bg-gradient-to-r from-sky-800 to-cyan-500 '
    'dark:from-sky-600 dark:to-cyan-400 px-5 py-2.5 text-xs sm:text-sm font-black '
    'uppercase tracking-[0.25em] text-white dark:text-slate-900 '
    'shadow-[4px_4px_0px_0px_rgba(6,182,212,0.3)]"'
    f' id="{SECTION_ID}">{SECTION_TITLE}</h2></div>'
)

GRID_OPEN = '<div class="not-prose grid grid-cols-1 md:grid-cols-2 gap-4 my-6">'
GRID_CLOSE = "</div>"


def domain_from(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")


def extract_existing_urls(text: str) -> set:
    seen = set()
    for u in re.findall(r"https?://[^\s\n<>\"\'\)]+", text):
        u = u.rstrip(".,;:)!?")
        if "google.com/s2/favicons" in u or "googleusercontent.com" in u:
            continue
        seen.add(u)
    return seen


def build_card(name: str, url: str, description: str) -> str:
    dom = domain_from(url)
    favicon = f"https://www.google.com/s2/favicons?domain={dom}&sz=32"
    desc_escaped = description.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    name_escaped = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return (
        f'<a href="{url}" '
        'class="flex items-start gap-4 p-4 rounded-xl border border-slate-200 '
        'dark:border-slate-700 bg-white dark:bg-slate-900 '
        'hover:border-cyan-400 dark:hover:border-cyan-400 '
        'hover:shadow-xl hover:-translate-y-1 transition-all no-underline group">'
        f'\n  <img src="{favicon}" width="20" height="20" '
        'class="mt-1 shrink-0 rounded bg-slate-100 dark:bg-slate-800 p-0.5"'
        f' alt="{name_escaped}" loading="lazy" />'
        "\n  <div>"
        f'\n    <span class="font-bold text-slate-900 dark:text-white '
        "group-hover:text-cyan-600 dark:group-hover:text-cyan-400 "
        'transition-colors">{name_escaped}</span>'
        f'\n    <p class="text-sm text-slate-500 dark:text-slate-400 '
        f'mt-0.5 leading-snug">{desc_escaped}</p>'
        "\n  </div>"
        "\n</a>"
    )


def find_section_bounds(content: str, section_id: str) -> tuple[int, int] | None:
    """Return (start_line_in_content, end_line_in_content) of the grid div for a section."""
    id_pattern = f'id="{section_id}"'
    idx = content.find(id_pattern)
    if idx == -1:
        return None

    grid_start = content.find(GRID_OPEN, idx)
    if grid_start == -1:
        return None

    grid_end = content.find(GRID_CLOSE, grid_start)
    if grid_end == -1:
        return None

    return grid_start, grid_end + len(GRID_CLOSE)


def main():
    parser = argparse.ArgumentParser(description="Merge tools into blog's resources.mdx")
    parser.add_argument("--blog-path", default="..", help="Path to the blog checkout directory")
    args = parser.parse_args()

    blog_path = Path(args.blog_path).resolve()
    resources_file = blog_path / "src" / "content" / "posts" / "resources.mdx"
    herramientas_file = blog_path.parent / "files" / "herramientas.json"

    if not herramientas_file.exists():
        print("No se encuentra files/herramientas.json. Sin herramientas nuevas.")
        sys.exit(2)

    with open(herramientas_file, "r", encoding="utf-8") as f:
        herramientas = json.load(f)

    if not herramientas:
        print("No hay herramientas nuevas para añadir.")
        sys.exit(2)

    if not resources_file.exists():
        print(f"No se encuentra {resources_file}")
        sys.exit(1)

    current_content = resources_file.read_text(encoding="utf-8")
    existing_urls = extract_existing_urls(current_content)

    new_tools = []
    for h in herramientas:
        url = h.get("enlace", "")
        if url and url not in existing_urls:
            new_tools.append(h)
            existing_urls.add(url)

    if not new_tools:
        print("Todas las herramientas descubiertas ya están en resources.mdx.")
        sys.exit(2)

    cards = []
    for t in new_tools:
        name = t.get("titulo", domain_from(t.get("enlace", "")))
        desc = t.get("descripcion", "")
        url = t.get("enlace", "")
        cards.append(build_card(name, url, desc))

    cards_block = "\n\n".join(cards)

    bounds = find_section_bounds(current_content, SECTION_ID)

    if bounds:
        grid_start, grid_end = bounds
        before = current_content[:grid_end]
        after = current_content[grid_end:]
        updated = before + "\n\n" + cards_block + "\n" + after
    else:
        separator = "\n\n---\n\n" if current_content.rstrip().endswith("</div>") else "\n\n"
        block = (
            separator
            + SECTION_HEADER
            + "\n"
            + GRID_OPEN
            + "\n\n"
            + cards_block
            + "\n\n"
            + GRID_CLOSE
            + "\n"
        )
        updated = current_content.rstrip() + block

    resources_file.write_text(updated, encoding="utf-8")
    print(
        f"{len(new_tools)} herramientas añadidas a "
        f"{resources_file.relative_to(blog_path) if resources_file.is_relative_to(blog_path) else resources_file}"
    )

    recipe_script = blog_path / "scripts" / "generate_resources.py"
    if recipe_script.exists():
        print("Re-categorizando con generate_resources.py...")
        result = subprocess.run(
            [sys.executable, str(recipe_script)],
            cwd=str(blog_path),
            capture_output=True, text=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"generate_resources.py terminó con código {result.returncode}")
            if result.stderr:
                print(result.stderr[:500])
    else:
        print("generate_resources.py no encontrado. Las herramientas se añadieron en la sección 'Nuevas herramientas'.")

    print("Hecho.")


if __name__ == "__main__":
    main()
