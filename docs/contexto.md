# Contexto del proyecto — Blog

**Última actualización**: 2026-06-26
**Stack**: Astro 6.4 + Svelte 5 + Tailwind CSS 4.3
**Deploy**: Vercel (`blog-jorbencas.vercel.app`)
**Idioma**: Español
**Node**: >= 18

## Contenido

5 colecciones MDX en `src/content/`:
- `posts/` — posts del blog
- `auto-news/` — noticias automáticas (weekly reports)
- `auto-challenges/` — retos de programación (+140 guías)
- `myprojects/` — proyectos personales
- `tools/` — herramientas interactivas (listado en `/herramientas`)
- `weeklyPosts/` — resúmenes semanales (colección separada en `src/content.config.ts`)

Configuradas con Zod schemas en `src/content.config.ts` usando `astro/loaders` (glob) y `astro/zod`. Los schemas tipan `draft`, `title`, `description`, `pubDate` (transformado a Date), `tags`, `author`, `image` y campos específicos por colección.

`draft: true` filtra posts en desarrollo. `getSortedPosts()` en `src/utils.js`.

## Página de inicio (`src/pages/index.astro`)

Secciones en orden:
1. **Mis_Proyectos** — grid de ProjectCard (3 últimos)
2. **Mini_Herramientas** — grid de ToolCard (3 últimas, oculto si vacío)
3. **Retos** — grid de ChallengeCard (3 últimos)
4. **Últimos_Posts** — grid de PreviewPost (3 últimos)
5. **Resúmenes_Semanales** — grid Weekly (6 últimos, first card abarca 2 cols)

### Navbar (`src/components/Navbar.astro`)
- Menú responsive: hamburguesa → X animado en móvil, horizontal en lg+
- Body scroll lock con `position: fixed` + `scrollY` para evitar salto por scrollbar
- Escape cierra menú; resize >1024px lo cierra automáticamente
- 4 links: Proyectos, Retos, Blog, Mini Herramientas (cada uno con color de acento propio)

## Pipeline de imágenes

- `scripts/fix_images.py` (Python) — obtiene imágenes Unsplash + genera banners con Gemini
- Convierte a WebP/AVIF con compresión adaptativa SSIM
- Cache en `image_cache.json` — auto-pruning al cargar: descarta entradas >365 días, máximo 200
- Dependencias: `requirements.txt` (Pillow, aiohttp, google-genai)

## Tailwind v4

- Configuración CSS-first en `src/styles/global.css`
- `@plugin "@tailwindcss/typography"` para prose
- `@custom-variant dark (&:where(.dark, .dark *))`
- `html { scrollbar-gutter: stable; }` evita layout shift al abrir menú móvil
- Sin `tailwind.config.mjs` ni `postcss.config.mjs` (eliminados)
- Vite plugin: `@tailwindcss/vite` en `astro.config.mjs > vite.plugins`

## Componentes destacados

### ResponsiveImage (`src/components/ResponsiveImage.astro`)
Props: `fallback`, `avif`, `webp`, `blur` (LQIP), `fetchpriority`, `loading`, `aspectRatio`, `class`, `imgClass`

### VideoExtractor (`src/components/toolsmini/VideoExtractor.svelte`)
- Cortes de video con `captureStream()` + `MediaRecorder`
- Descarga WebM/MP4. Firefox: sin audio en captura. Máx 30s.

### Weekly (`src/components/Weekly.astro`)
- Card para resúmenes semanales con fecha y extracto

### SEO (`src/components/SEO.astro`)
- JSON-LD `BlogPosting`, OG tags, Twitter Cards, meta tags

### Recursos (`scripts/generate_resources.py`)
- Script Python que categoriza URLs en `src/content/posts/resources.mdx`
- 102+ recursos en 25 categorías con favicons y descripciones
- Idempotente: extrae URLs del MDX, clasifica y reconstruye

## TypeScript

`tsconfig.json` con `strict: true` y `noUncheckedIndexedAccess: true`.

## Archivos relevantes

### Config
- `astro.config.mjs`, `tsconfig.json`, `AGENTS.md`, `README.md`
- `.opencode/skills/update-context/SKILL.md`

### CI/CD
- `.github/workflows/spelling.yml`, `fixing_img.yml`, `issues_handel.yml`
- `.languagetool-ignore.txt`
- `docs/ci-cd.md`

### Layouts
- `src/layouts/PostLayout.astro`, `src/layouts/Layout.astro`, `src/layouts/ProjectLayout.astro`

### Componentes
- `src/components/Navbar.astro`, `ResponsiveImage.astro`, `SEO.astro`, `AudioPlayer.astro`, `TableOfContents.astro`, `PreviewPost.astro`, `Weekly.astro`
- `src/components/ChallengeCard.astro`, `ProjectCard.astro`, `ToolCard.astro`, `Information.astro`
- `src/components/ToggleButton.astro`, `NextPrevLinks.astro`, `Footer.astro`, `Buscador.astro`
- `src/components/toolsmini/VideoExtractor.svelte`

### Páginas
- `src/pages/posts/index.astro`, `src/pages/proyectos/index.astro`, `src/pages/herramientas/[slug].astro`

### Contenido y estilos
- `src/content.config.ts`, `src/styles/global.css`, `src/styles/solution.css`, `src/utils.js`

### Scripts y datos
- `scripts/fix_images.py`, `scripts/generate_resources.py`, `image_cache.json`
