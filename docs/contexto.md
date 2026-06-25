# Contexto del proyecto — Blog

**Última actualización**: 2026-06-25
**Stack**: Astro 6.4 + Svelte 5 + Tailwind CSS 4.3
**Deploy**: Vercel (`blog-jorbencas.vercel.app`)
**Idioma**: Español
**Node**: >= 18

## Contenido

4 colecciones MDX en `src/content/`:
- `posts/` — posts del blog
- `auto-news/` — noticias automáticas (weekly reports)
- `auto-challenges/` — retos de programación (+140 guías)
- `myprojects/` — proyectos personales

Configuradas con Zod schemas en `src/content.config.ts` usando `astro/loaders` (glob) y `astro/zod`. Los schemas tipan `draft`, `title`, `description`, `pubDate` (transformado a Date), `tags`, `author`, `image` y campos específicos por colección.

`draft: true` filtra posts en desarrollo. `getSortedPosts()` en `src/utils.js`.

## Pipeline de imágenes

- `scripts/fix_images.py` (Python) — obtiene imágenes Unsplash + genera banners con Gemini
- Convierte a WebP/AVIF con compresión adaptativa SSIM
- Cache en `image_cache.json` — auto-pruning al cargar: descarta entradas >365 días, máximo 200
- Dependencias: `requirements.txt` (Pillow, aiohttp, google-genai)

## Tailwind v4

- Configuración CSS-first en `src/styles/global.css`
- `@plugin "@tailwindcss/typography"` para prose
- `@custom-variant dark (&:where(.dark, .dark *))`
- Sin `tailwind.config.mjs` ni `postcss.config.mjs` (eliminados)
- Vite plugin: `@tailwindcss/vite` en `astro.config.mjs > vite.plugins`

## Componente ResponsiveImage

`src/components/ResponsiveImage.astro`

Props:
- `fallback` (string) — imagen por defecto (obligatorio)
- `avif`, `webp` (opcional) — rutas a variantes AVIF/WebP
- `blur` (opcional) — base64 para LQIP con efecto blur
- `fetchpriority` (opcional) — `"high"` para LCP candidates
- `loading` (opcional) — `"lazy"` (default) o `"eager"`
- `aspectRatio` (opcional) — string CSS (ej. `"16/9"`)
- `class` / `imgClass` — clases para wrapper y `<img>` respectivamente

## VideoExtractor

`src/components/toolsmini/VideoExtractor.svelte`

- Procesa cortes de video con `captureStream()` + `MediaRecorder`
- Cada segmento "keep" se descarga como WebM (o MP4 si está disponible)
- Firefox: sin audio en captura, se muestra alerta
- Duración máxima advertida: 30s total
- Deshabilitado durante procesamiento

## SEO

`src/components/SEO.astro`

- JSON-LD completo: `BlogPosting` con headline, description, keywords, url, `mainEntityOfPage`, `image`, `datePublished`, `dateModified`, `author`, `publisher`
- OG tags: type, url, title, description, image (1200x630 PNG), site_name, locale
- Twitter Cards: `summary_large_image`, site, creator (@jorbencas), url, title, description, image
- Meta: canonical, description, theme-color, `article:published_time`, `article:modified_time`, `article:author`, `article:tag`

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
- `src/components/Navbar.astro`, `ResponsiveImage.astro`, `SEO.astro`, `AudioPlayer.astro`, `TableOfContents.astro`, `PreviewPost.astro`
- `src/components/ChallengeCard.astro`, `ProjectCard.astro`, `Information.astro`
- `src/components/ToggleButton.astro`, `NextPrevLinks.astro`, `Footer.astro`, `Buscador.astro`
- `src/components/toolsmini/VideoExtractor.svelte`

### Páginas
- `src/pages/posts/index.astro`, `src/pages/proyectos/index.astro`

### Contenido y estilos
- `src/content.config.ts`, `src/styles/global.css`, `src/styles/solution.css`, `src/utils.js`

### Scripts y datos
- `scripts/fix_images.py`, `image_cache.json`
