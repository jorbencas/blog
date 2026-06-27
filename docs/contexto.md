# Contexto del proyecto — Blog

**Última actualización**: 2026-06-27 (sesión: gitignore, vercelignore, reglas AGENTS.md unificadas)
**Stack**: Astro 6.4 + Svelte 5 + Tailwind CSS 4.3
**Deploy**: Vercel (`blog-jorbencas.vercel.app`)
**Idioma**: Español
**Node**: >= 18

## Mejoras implementadas

### 1. Recursos masivo + Hacking + Certificaciones ✅
- **`resources.mdx`**: reescrito completamente con 482+ tarjetas en 36 categorías. Diseño card grid con `not-prose`, favicons, hover effects. Categorías nuevas: Hacking/Ciberseguridad (24 tarjetas), Certificaciones (23 tarjetas), más las existentes expandidas.
- Summary box actualizado a "más de 500 recursos en más de 35 categorías".
- Build verificado sin errores.

### 2. Pagefind / Buscador fix ✅
- **`Buscador.astro`**: extraída función `initSearch()` llamada inmediatamente + registrada en `astro:page-load`. Eliminada inyección via `<script>`. Usa `import("/pagefind/pagefind.js")` directamente.
- Search tests actualizados: eliminada dependencia de `window.pagefind` (ya no existe). Tests usan solo DOM assertions.

### 3. Overflow safety + Navbar mobile ✅
- **`global.css`**: reglas overflow-safe para `iframe`, `video`, `pre`, `p`, `li`, `blockquote`, `td`, `th`. Añadido `.video-wrapper` utility.
- **`header.astro`**: `pr-14 lg:pr-0` + `text-sm sm:text-lg` para evitar solapamiento del hamburger.

### 4. Tags simplificado ✅
- **`tags.json`**: eliminado (estaba desactualizado, lógica de filtrado rota).
- **`TagsPosts.astro`**: simplificado, sin dependencia de tags.json.
- **`tags/index.astro`**: simplificado, eliminado import de `Information` y condicional vacío.

### 5. AGENTS.md reestructurado ✅
- Reglas críticas (pedir permiso antes de borrar/modificar) movidas al inicio.
- Testing rules movidas al final como referencia.

### 6. `.gitignore` y `.vercelignore` actualizados ✅
- **`.gitignore`**: añadidos `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.env.local`, `.env.*.local`
- **`.vercelignore`**: añadidos `tests/`, `node_modules/`, `.git/`, `.env`, `.env.production` (sin eliminar nada existente)

### 7. AGENTS.md — reglas unificadas ✅
- Reglas de modificar/borrar archivos, carpetas y configs fusionadas en un solo bloque
- Reglas de añadir dependencias (npm + Python) fusionadas en una sola
- Nueva regla: nunca borrar carpetas sin explicación + confirmación

## Contenido

5 colecciones MDX en `src/content/`:
- `posts/` — posts del blog (incluye `resources.mdx` con 482+ recursos, `n8n.mdx` con guía completa, etc.)
- `auto-news/` — noticias automáticas
- `auto-challenges/` — retos de programación (+140 guías)
- `myprojects/` — proyectos personales
- `tools/` — herramientas interactivas (listado en `/herramientas`)

Configuradas con Zod schemas en `src/content.config.ts` usando `astro/loaders` (glob) y `astro/zod`.

`draft: true` filtra posts en desarrollo. `getSortedPosts()` en `src/utils.js`.

## Página de inicio (`src/pages/index.astro`)

Secciones en orden:
1. **Mis_Proyectos** — grid de ProjectCard (3 últimos, primero abarca 2 cols en md+)
2. **Mini_Herramientas** — grid de ToolCard (3 últimas, oculto si vacío)
3. **Retos** — grid de ChallengeCard (3 últimos)
4. **Últimos_Posts** — grid de PreviewPost (3 últimos)
5. **Resúmenes_Semanales** — grid Weekly (6 últimos, first card abarca 2 cols)

### Navbar (`src/components/Navbar.astro`)
- Menú responsive: hamburguesa → X animado en móvil, horizontal en lg+
- Body scroll lock con `position: fixed` + `scrollY` para evitar salto por scrollbar
- Botón hamburguesa/X en móvil: `fixed top-3 right-3 z-50`
- Escape cierra menú; resize >1024px lo cierra automáticamente
- 5 links: Proyectos, Retos, Blog, Mini Herramientas, Aportaciones/Bugs

### Header (`src/components/header.astro`)
- Título con `pr-14 lg:pr-0` para evitar solapamiento con hamburger en móvil
- `text-sm sm:text-lg` en el h2 del título

## Pipeline de imágenes

- `scripts/fix_images.py` (Python) — obtiene imágenes Unsplash + genera banners con Gemini
- Convierte a WebP/AVIF con compresión adaptativa SSIM
- Cache en `image_cache.json` — auto-pruning: descarta entradas >365 días, máximo 200
- Dependencias: `requirements.txt` (Pillow, aiohttp, google-genai)

## Tailwind v4

- Configuración CSS-first en `src/styles/global.css`
- `@plugin "@tailwindcss/typography"` para prose
- `@custom-variant dark (&:where(.dark, .dark *))`
- `html { scrollbar-gutter: stable; }` evita layout shift al abrir menú móvil
- Sin `tailwind.config.mjs` ni `postcss.config.mjs`
- Vite plugin: `@tailwindcss/vite` en `astro.config.mjs > vite.plugins`

## Componentes destacados

### Buscador (`src/components/Buscador.astro`)
- Pagefind importado via `import("/pagefind/pagefind.js")` directo (no `<script>`)
- `initSearch()` se ejecuta inmediatamente y también en `astro:page-load`

### TagsPosts (`src/components/TagsPosts.astro`)
- Renderiza tags como links, recibe JSON string via prop `tagsList`
- Sin dependencia de `tags.json` (eliminado)

### CopyPost (`src/components/CopyPost.astro`)
- Botón "COPIAR" con dropdown: Markdown, Texto plano, Para IA
- Datos via `<script type="application/json">`
- Ubicado en el header de PostLayout, tras AudioPlayer

### Cards hover pattern (unificado)
- **ProjectCard** → `hover:border-purple-500/50`
- **ToolCard** → `hover:border-emerald-500/50`
- **PreviewPost** → `hover:border-cyan-500/50`
- **ChallengeCard** → `hover:border-cyan-500/50`
- **Weekly** → wrapper gradient con `hover:shadow-[0_0_40px_rgba(6,182,212,0.25)]`
- Overlay imagen: `opacity-70 → opacity-40`, imagen: `opacity-80 → opacity-100`

### solution.css
- `details` sin padding propio; `summary` (1rem) y `.details-content` manejan espaciado
- Botón DESCIFRAR con gradient

## Archivos relevantes

### Config
- `astro.config.mjs`, `tsconfig.json`, `AGENTS.md`
- `.opencode/skills/customize-opencode/SKILL.md`

### CI/CD
- `.github/workflows/spelling.yml`, `fixing_img.yml`, `issues_handel.yml`
- `.languagetool-ignore.txt`
- `docs/ci-cd.md`

### Layouts
- `src/layouts/PostLayout.astro`, `src/layouts/Layout.astro`, `src/layouts/ProjectLayout.astro`

### Páginas
- `src/pages/posts/index.astro`, `src/pages/proyectos/index.astro`, `src/pages/herramientas/[slug].astro`
- `src/pages/tags/index.astro` (simplificado, sin componente Information)

### Scripts
- `scripts/fix_images.py`, `image_cache.json`

### Tests
- `tests/specs/search.spec.mjs` (sin dependencia de window.pagefind)
- `tests/specs/visual-regression.spec.mjs`
- `.gitignore` incluye `test-results/`
