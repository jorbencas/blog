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

## Testing rules
Before writing a test, evaluate the following checklist. If a term is unclear at any point, ask the user if they want an explanation from official sources before proceeding.

### 1. Execution context
- Does the function have side effects (API calls, disk writes, global state mutation)?
- Does it depend on environment variables or external files?
- Does it run on the client (browser) or server (Node/Python)?
- Are there dependencies that need mocking to isolate the test?

### 2. Test type
- Pure function (same input → same output)? → *Unit test*
- Requires DOM interaction, user events, or browser APIs? → *E2E with Playwright*
- Renders UI and needs visual regression protection? → *Visual regression*
- Integrates multiple modules/systems (e.g. scraper + AI + local DB)? → *Integration test*

### 3. Functional coverage
- What edge cases are covered? (empty input, wrong types, boundary values, null/undefined)
- Does the test verify the expected output or just that no exception is thrown?
- Is there async behavior (promises, callbacks, streams) that needs `await` or `waitFor`?
- Would the test fail if someone changes the implementation but not the behavior? (i.e. it's a good test)

### 4. Code design
- Does the function do too many things (more than 3 clear responsibilities)?
- Does it have invisible side effects (mutates parameters, closes resources)?
- Would it be more testable if refactored into smaller functions?

### 5. Questions for the user
- What expected behavior do you have for this specific case?
- Does this test replace or complement existing tests?
- Is there documentation or usage examples that can serve as reference for the expected behavior?

### 6. Test file locations
- Python scripts → `tests/python/`
- Playwright E2E tests → `tests/specs/`

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

## File modification restrictions
Before deleting, changing permissions, or modifying any file, you must:
1. Explain exactly what you are going to do and why
2. Mention if there is a better alternative approach
3. Wait for explicit user confirmation before proceeding

## Git restrictions
- NEVER run `git push`, `git pull`, or `git fetch`. These operations must be done manually by the user.

## Python dependency rules
1. All Python libraries must be listed in `requirements.txt`, never hardcoded in workflow files.
2. When adding a new Python library to `requirements.txt`, you must:
   - Ask the user what the library is for and why it's needed
   - If the user doesn't know what the library does, provide a brief explanation of its purpose
   - Wait for explicit confirmation before adding it

## npm package use restrictions
1. Astro files don't use any npm package of node enviroment.
2. When adding a new npm package, you must:
   - Ask the user what the library is for and why it's needed
   - If the user doesn't know what the library does, provide a brief explanation of its purpose
   - Wait for explicit confirmation before adding it