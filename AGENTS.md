# Blog — Agent Guide

## Commands
- `npm run dev` — dev server (localhost:4321)
- `npm run build` — `astro build && npx pagefind --site dist` (build + search index)
- `npm run cleaner` — rm node_modules + reinstall (use if deps are broken)
- `npm run preview` — preview production build locally

## Stack
- Astro 6.4 + Svelte 5 + Tailwind CSS 4.3 (dark mode via `class`)
- Vercel adapter, static output, deployed at `https://blog-jorbencas.vercel.app/`
- Node >= 18

## Content (all in Spanish)
5 collections in `src/content/` — `posts/`, `auto-news/`, `auto-challenges/`, `myprojects/`, `tools/`
Content is MDX. Frontmatter includes `draft` (filtered by `getSortedPosts` in `src/utils.js`).
Schemas in `src/content.config.ts` using `astro/loaders` (glob) + `astro/zod`.

## Tools collection (`src/content/tools/`)
- Listings at `/herramientas` with pagination (page size 12), cards via `ToolCard.astro`, layout via `ToolLayout.astro`.
- Interactive Svelte components live at `src/components/` and are embedded in `[slug].astro` via slug-based conditional.
- Adding a new tool: (1) create MDX in `src/content/tools/`, (2) if it needs an interactive component, create it in `src/components/` and add the import + conditional in `src/pages/herramientas/[slug].astro`, (3) add a banner image to `public/img/`.

## Path aliases
`@components/*`, `@layouts/*`, `@pages/*`, `@styles/*`, `@audios/*`, `@data/*`

## Non-obvious tooling
- **Image pipeline**: `scripts/fix_images.py` (Python) fetches Unsplash images + generates banners via Gemini. Requires `UNSPLASH_ACCESS_KEY` and `GEMINI_API_KEY` env vars. Converts to WebP/AVIF with SSIM-based adaptive compression. Cached in `image_cache.json`.
- **Search**: Pagefind indexes `dist/` — runs automatically during build.
- **OG images**: Custom endpoint `src/pages/api/og/og.png.ts` using satori + resvg.
- **Reading time**: Custom remark plugin `remark-reading-time.mjs` adds `minutesRead` to frontmatter.
- **Python deps**: `requirements.txt` (Pillow, aiohttp, google-genai) — needed to run image fixer.
- **Svelte components**: live alongside `.astro` files in `src/components/` (e.g., `VideoExtractor.svelte`).
- **CI**: GitHub Actions — image fixing on push to main (content changes), spelling check (LanguageTool, Spanish) on PRs to content, feedback wall issue handler.

## Workflow
0. **Read `docs/contexto.md` first** — always start by reading the full context file to understand project state.
   - If running `fix_images.py`, `image_cache.json` is pruned automatically (max 200 entries, discards >365 days).
1. **Always run `npm run build` after any change** to verify no errors.
2. **Save project context** in `docs/contexto.md` — update it with each change. Load the `update-context` skill for the exact format.
3. **Update timeline post** after significant changes — load the `update-timeline` skill.
4. **Tailwind v4 note**: `@apply` is NOT supported in component `<style>` blocks. Use plain CSS instead.
5. **Dark mode**: Always pair light/dark classes explicitly (e.g. `text-slate-900 dark:text-white`). Never stack conflicting classes without `dark:` prefix.

## Notes
- `image_cache.json` is auto-generated; treat as cache.
- Posts with `draft: true` are filtered out at runtime.
- Content is in Spanish — prefer Spanish in new content.

## PR instructions
- Title format: [<project_name>] <Title>
- Always run `npm lint` and `npm test` before committing.

## Git conventions
- Commits in Spanish (castellano).
- Scope prefix: `[blog]`, `[retos]`, `[herramientas]`, `[estilos]`, `[infra]`, etc.
- Format: `[scope] Short description in Spanish`

## Git restrictions
- NEVER run `git push`, `git pull`, or `git fetch`. These operations must be done manually by the user.

## npm package use restrictions
1. **Astro files** don't use any npm package of node enviroment.