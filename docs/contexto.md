# Contexto del proyecto — Blog

**Última actualización**: 2026-06-24
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

## Mejoras implementadas

### 1. processVideoCuts() en VideoExtractor ✅
Implementar la función para exportar cortes como WebM/MP4 usando `captureStream()` + `MediaRecorder`.
Alerta para Firefox (sin audio capturable) y límite de 30s.

### 2. Hero y card images con ResponsiveImage ✅
- `PostLayout.astro` hero → `<ResponsiveImage fetchpriority="high" loading="eager" />`
- `PreviewPost.astro` card → `<ResponsiveImage imgClass="..." />`
- `ResponsiveImage.astro` modificado: props opcionales, `fetchpriority`, `imgClass`

### 3. TableOfContents + scroll spy ✅
Ya existía como componente independiente con `IntersectionObserver`. Sin cambios.

### 4. AudioPlayer con lazy loading ✅
WaveSurfer se importa y carga solo cuando el elemento entra en viewport (IntersectionObserver con 200px de margen). El HTML se renderiza siempre (ligero).

### 5. Migrar Tailwind v3 → v4 ✅
- Eliminados: `@astrojs/tailwind`, `postcss.config.mjs`, `tailwind.config.mjs`, `autoprefixer`
- Instalados: `tailwindcss@^4`, `@tailwindcss/vite`, `@tailwindcss/typography`
- Configuración CSS-first en `src/styles/global.css`
- `@apply` reemplazados por CSS plano en `PostLayout.astro` y `CodeEnhancer.astro`
- Build time significativamente más rápido

### 6. Validación frontmatter con Zod schemas ✅
- `src/content.config.ts` con schemas tipados para las 4 colecciones
- `pubDate` transformado a `Date` automáticamente
- Field `image` opcional, `draft` con default `false`
- Colección `auto-challenges` corregida (era `"challenges"` en rutas)
- Build detecta errores de frontmatter en tiempo de compilación

### 7. Metadatos SEO ✅
- JSON-LD: `mainEntityOfPage`, `image`, `dateModified`, `publisher`
- `article:modified_time` meta tag
- `twitter:creator` (@jorbencas)

### 8. TypeScript strict ✅
- `tsconfig.json` con `strict: true` y `noUncheckedIndexedAccess: true`
- Interfaces tipadas en `SEO.astro`, `Layout.astro`, `PostLayout.astro`
- Sin errores de compilación

### 9. Correcciones post-migración ✅
- **Navbar mobile**: menú cambiado de `hidden`/`absolute` a overlay `fixed` fullscreen con `bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm`, z-index 40, hamburguesa centrada con `mx-auto`
- **posts/index.astro**: corregidas clases duplicadas (ej. `text-gray-900 text-white` → `text-gray-900 dark:text-white`, `bg-slate-50/50 bg-slate-900/20` → `bg-slate-50/50 dark:bg-slate-900/20`, etc.)
- **AGENTS.md**: sección `Workflow` añadida — correr `npm run build` siempre, guardar contexto en `docs/contexto.md`, nota sobre Tailwind v4 `@apply` + dark mode
- Build verificado sin errores

### 10. CI/CD, documentación y auto-pruning de imágenes ✅
- **`scripts/fix_images.py`**: añadida `prune_cache()` — descarta entradas >365 días, máximo 200, ordenadas por `updated_at` descendente. Se ejecuta automáticamente al cargar el cache.
- **`README.md`**: rewrite completo en español — badges, demo link (`blog-jorbencas.vercel.app`), tabla de tecnologías, estructura real del proyecto, comandos, pipeline de imágenes, CI/CD y licencia MIT.
- **`docs/ci-cd.md`**: creado con documentación detallada de los 3 workflows (fix images, spelling, feedback wall) — triggers, pasos, secrets, beneficios.
- **`.github/workflows/tasks.txt`**: eliminado (no es YML, reemplazado por `docs/ci-cd.md`)
- **`spelling.yml`**: pre-step que reemplaza términos técnicos por "Sistema" en los archivos antes del chequeo, post-step que restaura originales con `git checkout`. Añadido `disabled_categories: CASING,STYLE,REDUNDANCY,CAPITALIZATION` para reducir ruido.
- **`.languagetool-ignore.txt`**: creado con 80+ términos técnicos (Astro, Svelte, Tailwind, Vite, Vercel, Pagefind, WebP, etc.) como referencia para el CI.
- **`scripts/lt-wrapper.sh`**: creado y luego eliminado (reemplazado por masking directo en el workflow).
- Build verificado sin errores tras todos los cambios.

### 11. Skill update-context ✅
- **`.opencode/skills/update-context/SKILL.md`**: creada skill que instruye al agente sobre el formato exacto de `docs/contexto.md` — secciones obligatorias, bullet points, verificación de build, categorías de archivos relevantes. Se dispara con "compact", "update context", "save context", "wrap up".
- **`AGENTS.md`**: paso 2 actualizado para referenciar la skill `update-context`.
- Build verificado sin errores.

## Archivos relevantes

### Config
- `astro.config.mjs`, `tsconfig.json`, `AGENTS.md`, `README.md`
- `.opencode/skills/update-context/SKILL.md`

### CI/CD
- `.github/workflows/spelling.yml`, `fixing_img.yml`, `issues_handel.yml`
- `.languagetool-ignore.txt`
- `docs/ci-cd.md`

### Layouts
- `src/layouts/PostLayout.astro`, `src/layouts/Layout.astro`

### Componentes
- `src/components/Navbar.astro`, `ResponsiveImage.astro`, `SEO.astro`, `AudioPlayer.astro`, `TableOfContents.astro`, `PreviewPost.astro`
- `src/components/toolsmini/VideoExtractor.svelte`

### Páginas
- `src/pages/posts/index.astro`

### Contenido y estilos
- `src/content.config.ts`, `src/styles/global.css`, `src/utils.js`

### Scripts y datos
- `scripts/fix_images.py`, `image_cache.json`
