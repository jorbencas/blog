# Contexto del proyecto — Blog

**Última actualización**: 2026-06-27 (sesión: grid proyectos, navbar aportaciones)
**Stack**: Astro 6.4 + Svelte 5 + Tailwind CSS 4.3
**Deploy**: Vercel (`blog-jorbencas.vercel.app`)
**Idioma**: Español
**Node**: >= 18

## Mejoras implementadas

### 1. Grid de proyectos rediseñado + navbar Aportaciones/Bugs ✅
- **`src/pages/proyectos/index.astro`**: grid cambiado a 2 columnas con primer proyecto destacado (md:col-span-2)
- **`src/components/Navbar.astro`**: añadido enlace "Aportaciones/Bugs" con color ámbar, apunta a GitHub Issues
- **`src/components/Buscador.astro`**: pagefind.js cargado dinámicamente via `<script>` en lugar de `import()` para evitar error de Vite en dev
- **`package.json`**: build script cross-platform (Node.js fs en vez de rm/cp)
- Build verificado sin errores

## Contenido

5 colecciones MDX en `src/content/`:
- `posts/` — posts del blog (incluye `n8n.mdx` con guía completa: servidor, cloud, precios, ejemplos prácticos, seguridad, logs, HTML node, errores comunes, comparativa Zapier/Make, tips)
- `auto-news/` — noticias automáticas (weekly reports)
- `auto-challenges/` — retos de programación (+140 guías)
- `myprojects/` — proyectos personales
- `tools/` — herramientas interactivas (listado en `/herramientas`)
- `weeklyPosts/` — resúmenes semanales (colección separada en `src/content.config.ts`)

Configuradas con Zod schemas en `src/content.config.ts` usando `astro/loaders` (glob) y `astro/zod`. Los schemas tipan `draft`, `title`, `description`, `pubDate` (transformado a Date), `tags`, `author`, `image` y campos específicos por colección.

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
- Botón hamburguesa/X en móvil: `fixed top-3 right-3 z-50` (esquina superior derecha)
- Escape cierra menú; resize >1024px lo cierra automáticamente
- 5 links: Proyectos, Retos, Blog, Mini Herramientas, Aportaciones/Bugs (cada uno con color de acento propio; Aportaciones/Bugs usa ámbar y apunta a GitHub Issues)

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
- Siempre con borde degradado `from-cyan-500 via-purple-500 to-blue-500` + badge "RESUMEN_SEMANAL"
- Hover: glow sobre el wrapper + imagen más brillante

### CopyPost (`src/components/CopyPost.astro`)
- Botón "COPIAR" con dropdown: Markdown, Texto plano (strip MD), Para IA (con metadatos)
- Datos pasados via `<script type="application/json">` para evitar HTML-escape de Astro
- Estilo: `border-2 sky-500`, uppercase, tracking-widest, hover/active effects (mismo estilo que botones proyecto)
- Ubicado en el header de PostLayout, tras AudioPlayer

### PreviewPost (`src/components/PreviewPost.astro`)
- Card para posts del blog
- Hover: `hover:border-cyan-500/50`

### ChallengeCard (`src/components/ChallengeCard.astro`)
- Card para retos de programación
- Dificultad con badge de color (Iniciación=emerald, Intermedio=cyan, Avanzado=rose)
- Hover: `hover:border-cyan-500/50`

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
- `.opencode/skills/update-timeline/SKILL.md` — instrucciones para actualizar `linea_temporal_blog.mdx` tras cambios significativos

### CI/CD
- `.github/workflows/spelling.yml`, `fixing_img.yml`, `issues_handel.yml`
- `.languagetool-ignore.txt`
- `docs/ci-cd.md`

### Layouts
- `src/layouts/PostLayout.astro`, `src/layouts/Layout.astro`, `src/layouts/ProjectLayout.astro` (grid 8+4 con sidebar MoreProjects)

### Componentes
- `src/components/Navbar.astro` (5 links: Proyectos, Retos, Blog, Mini Herramientas, Aportaciones/Bugs), `ResponsiveImage.astro`, `SEO.astro`, `AudioPlayer.astro`, `TableOfContents.astro`, `PreviewPost.astro`, `CopyPost.astro`, `Weekly.astro`, `MoreProjects.astro`
- `src/components/ChallengeCard.astro`, `ProjectCard.astro`, `ToolCard.astro`, `Information.astro`
- `src/components/ToggleButton.astro`, `NextPrevLinks.astro`, `Footer.astro`, `Buscador.astro`
- `src/components/toolsmini/VideoExtractor.svelte`

### Páginas
- `src/pages/posts/index.astro`, `src/pages/proyectos/index.astro`, `src/pages/herramientas/[slug].astro`

### Contenido y estilos
- `src/content.config.ts`, `src/styles/global.css`, `src/styles/solution.css`, `src/utils.js`

### Cards hover pattern (unificado)
Todas las cards usan el mismo hover: `hover:border-<color>-500/50` (el borde cambia al color de acento en hover):
- **ProjectCard** → `hover:border-purple-500/50`
- **ToolCard** → `hover:border-emerald-500/50`
- **PreviewPost** → `hover:border-cyan-500/50`
- **ChallengeCard** → `hover:border-cyan-500/50`
- **Weekly** → wrapper gradient con `hover:shadow-[0_0_40px_rgba(6,182,212,0.25)]`

Además: overlay de imagen se desvanece (`opacity-70 → opacity-40`) y la imagen gana opacidad (`opacity-80 → opacity-100`) en hover en todas las cards.

### Temas claro/oscuro
- `.astro-code` tiene `border` + `padding` en tema claro (además del dark existente)
- `prose-code` tiene `background` + `padding` + `rounded` + `font-semibold` en todos los layouts
- `prose-pre` tiene `border` en tema claro en todos los layouts

### solution.css
- `details` sin padding propio; solo `summary` (1rem) y `.details-content` (izq/der/abajo) manejan espaciado
- Botón DESCIFRAR con gradient en lugar de color sólido

### Scripts y datos
- `scripts/fix_images.py`, `scripts/generate_resources.py`, `image_cache.json`
