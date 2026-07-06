# Blog — jorbencas

[![Astro](https://img.shields.io/badge/astro-6.4-BC52EE?logo=astro)](https://astro.build)
[![Svelte](https://img.shields.io/badge/svelte-5-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.3-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![Pagefind](https://img.shields.io/badge/search-pagefind-8A2BE2)](https://pagefind.app)
[![Vercel](https://img.shields.io/badge/deploy-vercel-black?logo=vercel)](https://vercel.com)

Personal tech & development blog built with Astro 6, Svelte 5 and Tailwind CSS 4. Features technical articles, programming challenges, personal projects, interactive tools, and a weekly AI-generated news recap.

**[→ blog-jorbencas.vercel.app](https://blog-jorbencas.vercel.app/)** · [RSS](/rss.xml)

---

## Features

- **5 content collections** — posts, challenges (140+), projects, tools, weekly news
- **Full‑text search** — Pagefind indexes the entire site at build, lazy-loaded in production
- **Complete SEO** — JSON‑LD, Open Graph, Twitter Cards, sitemap, RSS
- **Dynamic OG images** — generated with Satori + resvg
- **Table of Contents** — IntersectionObserver scroll spy, collapsible on mobile, sticky sidebar on desktop
- **Dark mode** — manual toggle, persisted in localStorage
- **Responsive images** — WebP/AVIF pipeline with SSIM-based adaptive compression and blur placeholder
- **CodeTabs** — interactive multi-language code tabs (Python/JS/Java/TS) in challenges
- **VideoExtractor** — browser-based video clip extraction (WebM/MP4)
- **Strict TypeScript** — `strict` + `noUncheckedIndexedAccess`

---

## Tech Stack

| Category       | Technology |
| -------------- | ---------- |
| Framework      | Astro 6.4 (static output) |
| Interactive    | Svelte 5 (runes, snippets) |
| Styles         | Tailwind CSS 4.3 + `@tailwindcss/typography` |
| Content        | MDX + Zod schemas (`astro/loaders`) |
| Deployment     | Vercel (`@astrojs/vercel`) |
| Search         | Pagefind |
| OG images      | Satori + resvg |
| Analytics      | Vercel Speed Insights |
| Typography     | Self-hosted variable fonts |
| Icons          | astro-icon + SVGs |

---

## Project Structure

```
blog/
├── public/                     # Static assets
│   ├── audio/  fonts/  icons/  img/  rss/
├── src/
│   ├── components/             # 25+ Astro + Svelte components
│   ├── content/                # 5 MDX collections
│   │   ├── auto-challenges/    # 46 programming challenges
│   │   ├── auto-news/          # Weekly news recaps
│   │   ├── myprojects/         # Personal projects
│   │   ├── posts/              # Technical articles
│   │   └── tools/              # Interactive tools
│   ├── content.config.ts       # Zod schemas + loaders
│   ├── data/  layouts/  pages/  styles/  utils.js
├── .github/workflows/
│   ├── issues_handel.yml       # Feedback management
│   ├── spelling.yml            # LanguageTool (Spanish)
│   └── trigger-optimize.yml    # Dispatch image optimization
├── astro.config.mjs / pagefind.yml
├── svelte.config.ts / tsconfig.json
└── AGENTS.md / docs/contexto.md
```

---

## Commands

| Command                | Action |
| ---------------------- | ------ |
| `npm run dev`          | Dev server on `localhost:4321` |
| `npm run build`        | Static build + Pagefind indexing |
| `npm run preview`      | Preview production build |
| `npm run cleaner`      | Reinstall dependencies |

---

## Resource Management API

Resources (`resources.mdx`, `resources2.mdx`) use **ResourceCard** and **ResourceCategory** components. They are auto-maintained by the [test_githubActions](https://github.com/jorbencas/test_githubActions) pipeline via `manage_resources.py`, which runs daily at 06:00 UTC.

### Pipeline (`daily_resources.yml`)

1. **Scrape** — GitHub Trending + Product Hunt → `herramientas.json`
2. **Add new tools** — inserts new resources into the `#nuevas-herramientas` section
3. **Deduplicate** (`--dedup`) — merges sections with the same ID, removes duplicate cards by URL
4. **Paginate** — splits into `resources2.mdx` if a file exceeds 500 cards
5. **Push** — commits changes directly to the blog

### CLI flags (`manage_resources.py` on test_githubActions)

| Flag | Purpose |
| ---- | ------- |
| `--dedup` | Merge duplicate sections + remove duplicate cards by URL |
| `--translate` | Translate English descriptions → Spanish via Gemini |
| `--reorder` | Sort all sections alphabetically across files |
| `--fix-spacing` | Fix missing blank lines between sections |
| `--clean` | Check resource URLs and remove dead links |
| `--convert` | Convert legacy inline HTML to ResourceCard components |
| `--max-cards N` | Max cards per file before pagination (default: 500) |

### Components

- `ResourceCard.astro` — individual card with favicon, title, description
- `ResourceCategory.astro` — section wrapper with ID anchor and title

Both live in `src/components/` and follow the blog's design system.

---

## CI/CD

| Workflow | Trigger | Purpose |
| -------- | ------- | ------- |
| **trigger-optimize** | Push to `main` (images or content) | Dispatch optimization to test_githubActions |
| **spelling** | PR against `content` | LanguageTool (Spanish) |
| **issues_handel** | Issues | Feedback form handler |

---

## License

Personal use — original content by the author.
