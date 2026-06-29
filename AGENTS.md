# Blog — Agent Guide

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

**Step 3 — WAIT**: You MUST stop and wait for the user to explicitly say "yes" or "adelante" or equivalent. The user's silence is NOT consent. Do not proceed unless the user gives a clear affirmative answer.

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
- TOC: `TableOfContents` component renderiza ambas versiones (mobile + desktop). Colocar en `lg:col-span-4` con `lg:sticky lg:top-24 lg:pl-8 h-fit`.
- Article prose: `max-w-4xl` (no `max-w-none`) para líneas de lectura cómodas.
- Breadcrumbs: colocar dentro del `<main>`, antes del `<header>`, en la misma columna.
- Max widths: `max-w-screen-xl` for post layout, `max-w-3xl` for description text.

## MDX Syntax — Critical Rules

MDX parses `<` and `{` as JSX/expression boundaries even in prose. **Never leave these unescaped outside code blocks:**

| Pattern | Problem | Fix |
|---|---|---|
| `<Fragment>` en heading | JSX tag en heading | Renombrar heading sin `<>` |
| `<1ms` en prosa | JSX tag inválido (`1` no es nombre válido) | `` `<1ms` `` o `&lt;1ms` |
| `Span<T>` en link text | `<T>` interpretado como JSX | `Span&lt;T&gt;` |
| `{variable}` fuera de code block | Interpretado como expresión JS | Escapar con `{'{variable}'}` |

**Regla de oro**: si ves `<` seguido de letra/número fuera de un bloque de código, escápalo. Siempre correr `npm run build` después de tocar MDX.

## Component Patterns (from UI audit)

### Card descriptions
- **NUNCA** usar comillas alrededor de `{description}`
- **NUNCA** usar `italic` ni `opacity-80` en descripciones
- Clase estándar: `text-sm sm:text-base text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed font-medium`

### Tabla de contenidos (TOC)
- Mobile: `<details>` colapsable con gradient badge `from-sky-800 to-cyan-500`, `lg:hidden`
- Desktop: sidebar sticky `hidden lg:block` con `IntersectionObserver` para highlight activo
- Ambos usan la misma clase `.toc-link` para que el observer resalte ambas listas
- El `<details>` debe tener `summary::-webkit-details-marker { display: none }` y `summary { list-style: none }`

### Breadcrumbs
- Colocar antes del `<header>` del post, dentro del `main` (no fuera del grid)
- Formato: `Inicio / Sección / Título` con `text-xs font-black uppercase tracking-[0.2em]`
- Separador: `/` en `text-slate-400 mx-2`
- Título truncado con `truncate max-w-[200px]` si es muy largo

### Header / Nav
- Buscador dentro del menú hamburguesa en mobile (`<slot />` en Navbar)
- Buscador visible en barra solo en desktop (`hidden lg:block`)
- ToggleButton siempre visible
- El `slot` en Navbar debe ir dentro de `#menu-items`, después de los nav links

### Scroll to top
- Sin `lg:hidden` — visible en desktop también tras 400px scroll
- `opacity-0 translate-y-4 pointer-events-none` → `opacity-100 translate-y-0 pointer-events-auto`

### Archive / Listados
- Mostrar solo últimos 2 años por defecto
- Link "Ver archivo completo (N años)" si hay más
- Usar `<details>` nativos para colapsar años
- Contador `Total_Entradas: {allPosts.length}` al final

## Mobile-first Responsive Patterns

| Componente | Mobile | Desktop |
|---|---|---|
| TOC | `<details>` colapsable encima del article | Sidebar sticky `lg:col-span-4` |
| Buscador | Dentro del menú hamburguesa | Barra header, al lado del toggle |
| Navbar | Overlay fullscreen con `fixed inset-0` | Horizontal, sin overlay |
| ScrollToTop | Visible tras 400px | Visible tras 400px |
| Archive | Plegado por defecto (2 años) | Plegado por defecto (2 años) |

## Build Verification

1. **Siempre** correr `npm run build` **antes de commitear**. Solo commitear si el build pasa.
2. Errores comunes de build:
   - `<` no escapado en MDX → buscar `<[A-Za-z0-9]` en prosa
   - `{ }` no escapados en MDX → buscar `{[a-zA-Z]` fuera de code blocks
   - Etiquetas JSX cerradas incorrectamente en headings (`<Fragment>`, `<Base>`)
3. Errores preexistentes conocidos (no tocar a menos que sea necesario):
   - `guia-0-100-csharp.mdx`: XML tags en code blocks son seguros
   - `guia-0-100-astro.mdx`: `<Base>`, `<Markdown>` en code blocks son seguros

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
