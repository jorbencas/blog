# Blog — jorbencas

[![Astro](https://img.shields.io/badge/astro-6.4-BC52EE?logo=astro)](https://astro.build)
[![Svelte](https://img.shields.io/badge/svelte-5-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.3-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![Pagefind](https://img.shields.io/badge/search-pagefind-8A2BE2)](https://pagefind.app)
[![Vercel](https://img.shields.io/badge/deploy-vercel-black?logo=vercel)](https://vercel.com)

Personal tech & development blog built with Astro 6, Svelte 5 and Tailwind CSS 4. Features technical articles, programming challenges, personal projects, interactive tools, and a weekly AI-generated news recap.

**[→ blog-jorbencas.vercel.app](https://blog-jorbencas.vercel.app/)** · [RSS](https://blog-jorbencas.vercel.app/rss.xml)

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
- **View Transitions** — ClientRouter for instant navigation between pages
- **Audio player** — WaveSurfer-based with Vercel Blob storage
- **Security headers** — CSP, X-Frame-Options, X-Content-Type-Options via vercel.json
- **Rate limiting** — API endpoints protected (views counter, OG images)
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
├── scripts/
│   ├── generate_puzzles.py     # Puzzle generator for JuegosLogicos
│   └── upload-audio.ts         # Upload MP3s to Vercel Blob
├── src/
│   ├── components/             # 30+ Astro + Svelte components
│   │   └── home/               # Homepage sections (Hero, Stats, Ticker, etc.)
│   ├── content/                # 5 MDX collections
│   │   ├── auto-challenges/    # 46 programming challenges
│   │   ├── auto-news/          # Weekly news recaps
│   │   ├── myprojects/         # Personal projects
│   │   ├── posts/              # Technical articles
│   │   └── tools/              # Interactive tools
│   ├── content.config.ts       # Zod schemas + loaders
│   ├── data/
│   │   ├── audio-map.json      # Blob URL mapping for audio files
│   │   └── views.json          # Page view counters
│   ├── layouts/  pages/  styles/  utils.js
├── .github/workflows/
│   ├── issues_handel.yml       # Feedback management
│   ├── spelling.yml            # LanguageTool (Spanish)
│   └── trigger-optimize.yml    # Dispatch image optimization
├── vercel.json                 # Security headers (CSP, X-Frame-Options, etc.)
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
| `npm run upload-audio` | Upload MP3s to Vercel Blob |

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

## Audio — Vercel Blob

Los archivos de audio (`public/audio/*.mp3`) se almacenan en **Vercel Blob Storage** para no sobrecargar el build con 59MB de MP3.

### Variables de entorno necesarias

| Variable | Descripción | Dónde obtenerla |
|----------|-------------|-----------------|
| `BLOB_READ_WRITE_TOKEN` | Token de acceso a Vercel Blob | Vercel Dashboard (ver abajo) |
| `BUTTONDOWN_API_KEY` | API key de Buttondown (newsletter) | Buttondown → Settings → API |

### Cómo obtener BLOB_READ_WRITE_TOKEN

1. Ve a [vercel.com/dashboard](https://vercel.com/dashboard)
2. Selecciona el proyecto **blog**
3. Menú lateral → **Settings**
4. Pestaña **Environment Variables**
5. Haz clic en **Add**:
   - Key: `BLOB_READ_WRITE_TOKEN`
   - Value: (ver paso 6)
6. **Crear el token:**
   - Menú lateral → **Storage**
   - Haz clic en **Create Store** → selecciona **Blob**
   - Nómbralo (ej: `blog-audio`) → **Create**
   - En la página del store → pestaña **Tokens**
   - **Create Token** → cópialo
7. Vuelve a **Settings → Environment Variables** y pega el token

### Cómo obtener BUTTONDOWN_API_KEY

1. Ve a [buttondown.com](https://buttondown.com/) y crea cuenta
2. Settings → API Keys → **Create API Key**
3. Copia la key
4. En Vercel Dashboard → **Settings → Environment Variables**:
   - Key: `BUTTONDOWN_API_KEY`
   - Value: (la key copiada)

### Añadir las variables en Vercel

En el dashboard de Vercel:

```
Settings → Environment Variables → Add

┌─────────────────────────┬──────────────────────────────┐
│ Key                     │ Value                        │
├─────────────────────────┼──────────────────────────────┤
│ BLOB_READ_WRITE_TOKEN   │ vercel_blob_rw_xxxxx...      │
│ BUTTONDOWN_API_KEY      │ 2fe6df88-xxxx...             │
└─────────────────────────┴──────────────────────────────┘
```

Seleccionar: **Production**, **Preview**, **Development** (las 3)

### Subir audios a Blob

```bash
npm run upload-audio
```

Este script:
- Lee todos los `.mp3` de `public/audio/`
- Los sube a Vercel Blob bajo el prefijo `audio/`
- Genera `data/audio-map.json` con el mapping `{ "/audio/file.mp3": "https://..." }`
- El `audio-map.json` **debe commitearse** al repo

### Cómo funciona la resolución

Los posts definen `audioSrc` en frontmatter con rutas locales:

```yaml
---
audioSrc: "/audio/pdf_ninja.mp3"
---
```

`ContentLayout.astro` resuelve automáticamente la URL:
1. Lee `data/audio-map.json`
2. Si la ruta `/audio/xxx.mp3` existe en el map → usa la URL de Blob
3. Si no existe (fallback) → usa la ruta local de `public/audio/`

Esto permite que funcione tanto en desarrollo (sin Blob) como en producción (con Blob).

### Añadir un nuevo audio

1. Colocar el `.mp3` en `public/audio/`
2. Ejecutar `npm run upload-audio`
3. Hacer commit del `data/audio-map.json` generado
4. Referenciar en el MDX: `audioSrc: "/audio/nuevo_audio.mp3"`

### Eliminar audios locales (opcional)

Una vez subidos a Blob, puedes borrar `public/audio/` para reducir el tamaño del repo:

```bash
rm -rf public/audio/
```

El blog seguirá funcionando porque resuelve las URLs desde `audio-map.json`.

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
