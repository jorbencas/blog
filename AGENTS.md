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

**New Astro/Svelte components**: before implementing a new component, review how existing ones are developed to follow the same pattern and maximize consistency. If there are doubts about the implementation, prepare a set of questions for the user before writing code.

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

## Design System — do not deviate from these patterns

### Colors by card/section type
- **Projects**: purple accent (`purple-500/50` border hover)
- **Tools**: emerald accent (`emerald-500/50` border hover)
- **Blog posts / Challenges / Retos**: cyan accent (`cyan-500/50`)
- **Weekly**: cyan gradient glow (`hover:shadow-[0_0_40px_rgba(6,182,212,0.25)]`)
- **Image overlays**: `opacity-70 → opacity-40`, image `opacity-80 → opacity-100`

### Gradient badge (section headers h2/h3)
- **h2**: `<h2 class="inline-flex items-center gap-2 bg-gradient-to-r from-sky-800 to-cyan-500 dark:from-sky-600 dark:to-cyan-400 px-5 py-2.5 text-xs sm:text-sm font-black uppercase tracking-[0.25em] text-white dark:text-slate-900 shadow-[4px_4px_0px_0px_rgba(6,182,212,0.3)]">` — always use **actual `<h2>` element** (not `<span>`) so Astro extracts it for TableOfContents.
- **h3**: same but smaller: `<h3 class="...from-sky-700 to-cyan-600... px-4 py-2 text-[11px] sm:text-xs ...">` — use actual `<h3>` element.

### Resource cards (resources.mdx)
- `rounded-xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 hover:shadow-xl hover:-translate-y-1 transition-all`
- Favicon: `<img class="rounded bg-slate-100 dark:bg-slate-800 p-0.5 w-5 h-5" />`
- Title: `font-bold text-slate-900 dark:text-white`
- Description: `text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-snug`

### Navigation links (link grid at top of resources.mdx)
- `inline-flex items-center gap-2.5 px-4 py-3 rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:border-cyan-400 hover:shadow-lg hover:-translate-y-0.5 transition-all no-underline text-xs font-black uppercase tracking-wider text-slate-700 dark:text-slate-300 hover:text-cyan-600 dark:hover:text-cyan-400`
- Always `font-black uppercase tracking-wider`, 2-column grid on mobile, 4-column on md+.

### Typography
- **Body headings (prose)**: `uppercase italic tracking-tighter font-black` — applied globally via prose config in PostLayout.
- **Navbar links**: `text-sm font-black uppercase tracking-[0.2em] italic`
- **Body text**: `leading-[1.8]` in prose.
- **Card titles**: `font-bold` (not `font-semibold` or `font-medium`).
- **Numbers / counts**: cyan accent `text-cyan-600 dark:text-cyan-400`.

### Icons / Emojis
- Every section header starts with an emoji: 🔒 Hacking, 🎓 Certificaciones, 🤖 IA, etc.
- Resource cards use favicons from Google S2 (`https://www.google.com/s2/favicons?domain=...`).
- Navigation links use emojis.
- Always place emoji first in the text, no extra space before it.

### Cards with lists inside (grid of items)
- Always use `not-prose` wrapper div to prevent prose list styling.
- Grid: `grid grid-cols-1 sm:grid-cols-2 gap-4` for resource cards (2 columns on sm+, 1 on mobile).
- For dense sections, `gap-3` instead of `gap-4`.

### Prose overrides (PostLayout article)
- Headings: `uppercase italic tracking-tighter font-black`
- Links: `text-cyan-600 dark:text-cyan-400 no-underline hover:underline`
- Strong: `text-cyan-600 dark:text-cyan-400`
- Code: `text-cyan-700 dark:text-cyan-300`
- Pre/code blocks: `border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-transparent rounded-lg`
- Images: `shadow-2xl rounded-sm max-w-full h-auto`

### Layout
- Post pages: 12-column grid, `lg:col-span-8` main + `lg:col-span-4` sidebar (TOC).
- Sidebar TOC: `hidden lg:block` on desktop, `lg:hidden` collapsible above article on mobile.
- Max widths: `max-w-screen-xl` for post layout, `max-w-3xl` for description text.

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
