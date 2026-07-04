# Blog — Agent Guide

## Language
All communication, comments, documentation, and agents must be written in English.

## Engineering Principles

- **Clean & Readable**: Write code for humans first, computers second. Deep believer in KISS and SOLID.
- **Automation First**: If a manual task has to be done more than thrice, it deserves a script or a GitHub Action.
- **Architecture Mindset**: Focus on decoupled systems, scalability, and predictable state management.
- **Refactor Iteratively**: When code works, refactor it toward clean, testable design. Replace hardcoded mappings with data-driven structures. Eliminate long if/elif chains. Each change should leave the codebase more maintainable than before.

Apply these principles when writing code. First make it work correctly, then improve the design.

## 🔴 CRITICAL RULES — Zero Tolerance (Priority Order)

### 🚫 ABSOLUTELY NEVER DELETE FILES WITHOUT EXPLICIT CONFIRMATION

You MUST ask before running **ANY** command that modifies or removes files/folders:
- `rm`, `rmdir`, `rm -rf`, `del`
- `git rm` (even though allowed, still needs confirmation)
- `mv` / `rename` (moving = removing from original location)
- `cp` with `--remove-source-files`
- Any script or tool call that deletes files

The rule applies to **ALL** files regardless of type: generated, cached, snapshots, logs, temp, node_modules, build output, `.gitignore` entries, etc. There are no exceptions.

**Mandatory workflow — every single time:**

**Step 1 — STOP and EXPLAIN**: Say exactly which files/folders you want to delete, how many, their total size, and why.

**Step 2 — EXPLAIN alternatives**: Mention if there is a better approach (e.g. adding to `.gitignore` instead of deleting, or keeping the folder structure and only deleting contents).

**Step 3 — WAIT**: You MUST stop and wait for the user to explicitly say "yes" or equivalent. The user's silence is NOT consent. Do not proceed unless the user gives a clear affirmative answer.

**Step 4 — EXECUTE**: Only after receiving explicit confirmation, run the command.

### ⚠️ Other modification rules

**Config files (`.gitignore`, `.vercelignore`, `astro.config.*`, etc.)**
Before modifying:
1. Explain exactly what you are going to do and why
2. Wait for explicit user confirmation before proceeding

**Dependencies (npm, Python, or any tool)**
When adding or changing a dependency:
1. Ask the user what it is for and why they need it
2. If the user doesn't know what it does, give a brief explanation
3. If changing a version: search for all references across the project, report findings, and summarize impact
4. Wait for explicit confirmation before proceeding

**New Astro/Svelte components**: before implementing a new component, review how existing ones are developed to follow the same pattern and maximize consistency. If there are doubts about the implementation, prepare a set of questions for the user before writing code.

**Git — allowed commands only**: `git pull`, `git add`, `git rm`, `git commit`. Everything else (push, fetch, merge, rebase, stash, branch, checkout, reset, revert, etc.) must be done manually by the user. For `git rm`, always explain what is being removed and why, then wait for explicit confirmation before executing.

**Commit ordering**: If told to commit and then asked to change something, postpone the commit until all requested changes are done. Commit is always the last step.

## Workflow
0. **Read `docs/contexto.md` first** — always start by reading the full context.
1. **Run `npm run build` before every commit** to verify no errors. Only commit if the build passes.
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
- **Blog posts**: cyan accent (`cyan-500/50`)
- **Retos / Challenges**: amber accent (`amber-500/50`)
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
- TOC: `TableOfContents` component renders both versions (mobile + desktop). Place in `lg:col-span-4` with `lg:sticky lg:top-24 lg:pl-8 h-fit`.
- Article prose: `max-w-4xl` (not `max-w-none`) for comfortable reading lines.
- Breadcrumbs: place inside `<main>`, before `<header>`, in the same column.
- Max widths: `max-w-screen-xl` for post layout, `max-w-3xl` for description text.

## MDX Syntax — Critical Rules

MDX parses `<` and `{` as JSX/expression boundaries even in prose. **Never leave these unescaped outside code blocks:**

| Pattern | Problem | Fix |
|---|---|---|
| `<Fragment>` in heading | JSX tag in heading | Rename heading without `<>` |
| `<1ms` in prose | Invalid JSX tag (`1` is not a valid name) | `` `<1ms` `` or `&lt;1ms` |
| `Span<T>` in link text | `<T>` interpreted as JSX | `Span&lt;T&gt;` |
| `{variable}` outside code block | Interpreted as JS expression | Escape with `{'{variable}'}` |

**Golden rule**: if you see `<` followed by a letter/number outside a code block, escape it. The build will catch these errors before commit anyway.

## Component Patterns (from UI audit)

### Card descriptions
- **NEVER** use quotes around `{description}`
- **NEVER** use `italic` or `opacity-80` in descriptions
- Standard class: `text-sm sm:text-base text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed font-medium`

### Table of Contents (TOC)
- Mobile: `<details>` collapsible with gradient badge `from-sky-800 to-cyan-500`, `lg:hidden`
- Desktop: sticky sidebar `hidden lg:block` with `IntersectionObserver` for active highlight
- Both use the same `.toc-link` class so the observer highlights both lists
- `<details>` must have `summary::-webkit-details-marker { display: none }` and `summary { list-style: none }`

### Breadcrumbs
- Place before the post `<header>`, inside `<main>` (not outside the grid)
- Format: `Home / Section / Title` with `text-xs font-black uppercase tracking-[0.2em]`
- Separator: `/` in `text-slate-400 mx-2`
- Title truncated with `truncate max-w-[200px]` if too long

### Header / Nav
- Search inside hamburger menu on mobile (`<slot />` in Navbar)
- Search visible in header bar only on desktop (`hidden lg:block`)
- ToggleButton always visible
- The `slot` in Navbar must go inside `#menu-items`, after nav links

### Scroll to top
- No `lg:hidden` — visible on desktop too after 400px scroll
- `opacity-0 translate-y-4 pointer-events-none` → `opacity-100 translate-y-0 pointer-events-auto`

## Mobile-first Responsive Patterns

| Component | Mobile | Desktop |
|---|---|---|
| TOC | `<details>` collapsible above article | Sticky sidebar `lg:col-span-4` |
| Search | Inside hamburger menu | Header bar, next to toggle |
| Navbar | Fullscreen overlay `fixed inset-0` | Horizontal, no overlay |
| ScrollToTop | Visible after 400px | Visible after 400px |
| Archive | Collapsed by default (2 years) | Collapsed by default (2 years) |

## Build Verification

1. **Always** run `npm run build` **before committing**. Only commit if the build passes.
2. Common build errors:
   - `<` not escaped in MDX → search for `<[A-Za-z0-9]` in prose
   - `{ }` not escaped in MDX → search for `{[a-zA-Z]` outside code blocks
   - Incorrectly closed JSX tags in headings (`<Fragment>`, `<Base>`)
3. Any MDX file may contain `<` or `{` inside code blocks (fenced with ```). These are safe and should NOT be escaped — only unescaped `<`/`{` in prose need fixing.

## Git Conventions
- Commits in Spanish (castellano).
- Scope prefix: `[blog]`, `[retos]`, `[herramientas]`, `[estilos]`, `[infra]`, etc.
- Format: `[scope] Short description in Spanish`

## PR Instructions
- Title: `[<project_name>] <Title>`
