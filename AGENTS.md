# Blog — Agent Guide

## ⚠️ Critical Rules (Priority Order)

**Files, folders, and config files (`.gitignore`, `.vercelignore`)**
Before modifying, adding entries to, or deleting any file, folder, or config file:
1. Explain exactly what you are going to do and why
2. For deletions: explain why it and its contents should be removed
3. Mention if there is a better alternative approach
4. Wait for explicit user confirmation before proceeding

**Dependencies (npm, Python, or any tool)**
When adding or changing a dependency:
1. Ask the user what it is for and why they need it
2. If the user doesn't know what it does, give a brief explanation
3. If changing a version: search for all references across the project, report findings, and summarize impact
4. Wait for explicit confirmation before proceeding

**Git**: NEVER run `git push`, `git pull` or `git fetch`. These must be done manually.

## Workflow
0. **Read `docs/contexto.md` first** — always start by reading the full context.
1. **Run `npm run build` after every change** to verify no errors.
2. **Save context** to `docs/contexto.md` — load the `update-context` skill for the exact format.
3. **Update timeline** after significant changes — load the `update-timeline` skill.

## Commands
- `npm run dev` — dev server (localhost:4321)
- `npm run build` — `astro build && npx pagefind --site dist`
- `npm run cleaner` — rm node_modules + reinstall
- `npm run preview` — preview the production build

## Stack
- Astro 6.4 + Svelte 5 + Tailwind CSS 4.3 (dark mode via `class`)
- Vercel adapter, static, deployed at `https://blog-jorbencas.vercel.app/`
- Node >= 18

## Content (all in Spanish)
5 collections in `src/content/` — `posts/`, `auto-news/`, `auto-challenges/`, `myprojects/`, `tools/`
Content is MDX. Frontmatter includes `draft` (filtered by `getSortedPosts` in `src/utils.js`).
Schemas in `src/content.config.ts` using `astro/loaders` (glob) + `astro/zod`.

## Tools Collection (`src/content/tools/`)
- Listings at `/herramientas` with pagination (12 per page), cards via `ToolCard.astro`, layout via `ToolLayout.astro`.
- Interactive Svelte components live in `src/components/`, embedded in `[slug].astro` via slug-based conditional.
- Adding a new tool: (1) create MDX, (2) if it needs an interactive component, create it and import it in `src/pages/herramientas/[slug].astro`, (3) add a banner to `public/img/`.

## Path Aliases
`@components/*`, `@layouts/*`, `@pages/*`, `@styles/*`, `@audios/*`, `@data/*`

## Non-obvious Tooling
- **Image pipeline**: `scripts/fix_images.py` (Python) fetches Unsplash images + generates banners via Gemini. Requires `UNSPLASH_ACCESS_KEY` and `GEMINI_API_KEY`. Converts to WebP/AVIF with SSIM-based adaptive compression. Cached in `image_cache.json`.
- **Search**: Pagefind indexes `dist/` — runs automatically during the build.
- **OG images**: Custom endpoint `src/pages/api/og/og.png.ts` using satori + resvg.
- **Reading time**: Custom remark plugin `remark-reading-time.mjs` adds `minutesRead` to frontmatter.
- **Python deps**: `requirements.txt` (Pillow, aiohttp, google-genai).
- **Svelte components**: live alongside `.astro` files in `src/components/`.
- **CI**: GitHub Actions — image fixing on push to main (content changes), spelling check (LanguageTool, Spanish) on PRs to content, feedback wall issue handler.
- **Tailwind v4**: `@apply` is NOT supported in component `<style>` blocks. Use plain CSS instead.
- **Dark mode**: Always pair light/dark classes explicitly (e.g. `text-slate-900 dark:text-white`).

## Notes
- `image_cache.json` is auto-generated; treat as cache.
- Posts with `draft: true` are filtered at runtime.
- Content is in Spanish — prefer Spanish for new content.

## Git Conventions
- Commits in Spanish (castellano).
- Scope prefix: `[blog]`, `[retos]`, `[herramientas]`, `[estilos]`, `[infra]`, etc.
- Format: `[scope] Short description in Spanish`

## PR Instructions
- Title: `[<project_name>] <Title>`
- Always run `npm lint` and `npm test` before committing.

## Testing Rules (reference)
Before writing a test, evaluate:

1. **Execution context**: does it have side effects? depends on env/files? client or server?
2. **Test type**: pure → unit, DOM → E2E (Playwright), UI → visual regression, multiple modules → integration
3. **Functional coverage**: edge cases, output assertions, async, should fail if implementation changes
4. **Code design**: does it do too many things? invisible side effects? refactorable?
5. **Ask the user**: expected behavior, whether it replaces or complements existing tests
6. **Location**: Python → `tests/python/`, Playwright → `tests/specs/`
