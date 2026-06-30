# Blog — jorbencas

[![Vercel](https://img.shields.io/badge/deploy-vercel-black?logo=vercel)](https://blog-jorbencas.vercel.app/)
[![Astro](https://img.shields.io/badge/astro-6.4-BC52EE?logo=astro)](https://astro.build)
[![Svelte](https://img.shields.io/badge/svelte-5-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.3-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![Playwright](https://img.shields.io/badge/test-playwright-45ba4b?logo=playwright)](https://playwright.dev)
[![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python)](https://python.org)
[![Pagefind](https://img.shields.io/badge/search-pagefind-8A2BE2)](https://pagefind.app)

Blog personal de tecnología y desarrollo, construido con Astro 6, Svelte 5 y Tailwind CSS 4. Incluye artículos técnicos, retos de programación, proyectos personales, herramientas interactivas y un resumen semanal de noticias.

**[→ Abrir demo](https://blog-jorbencas.vercel.app/)**

---

## Características

- **5 colecciones de contenido** — posts, retos de programación (140+), proyectos personales, herramientas y noticias semanales
- **Búsqueda full‑text** — Pagefind indexa todo el sitio en el build; carga diferida solo en producción
- **SEO completo** — JSON‑LD, Open Graph, Twitter Cards, sitemap, RSS
- **OG images dinámicas** — generación con Satori + resvg
- **Tabla de contenidos** — scroll spy con IntersectionObserver; versión colapsable en móvil y sidebar fija en escritorio
- **Archive** — listado por años con colapso automático
- **Paginación** — navegación entre páginas de listados
- **Navegación entre posts** — enlaces anterior/siguiente con flechas de teclado
- **Barra de progreso de lectura** — indicador visual en la parte superior
- **Breadcrumbs** — miga de pan en todas las páginas de contenido
- **Modo oscuro** — conmutación manual, persistente en localStorage
- **Imágenes responsive** — pipeline automático con WebP/AVIF, compresión adaptativa SSIM y placeholder blur
- **Audio lazy** — reproductor con WaveSurfer se carga solo al hacer scroll al elemento
- **CodeTabs** — pestañas interactivas para código multi‑lenguaje (Python/JS/Java/TS) en retos
- **VideoExtractor** — herramienta para extraer cortes de video desde el navegador (WebM/MP4)
- **Tipado estricto** — TypeScript `strict` + `noUncheckedIndexedAccess`
- **Rendimiento** — imágenes con `fetchpriority="high"` para LCP, lazy loading, Astro islands
- **Pruebas E2E** — Playwright cubre navegación, páginas de listado, detalle, responsive, contraste, búsqueda y regresión visual

---

## Stack

| Categoría          | Tecnología |
| ------------------ | ---------- |
| Framework          | Astro 6.4 |
| Islas interactivas | Svelte 5 |
| Estilos            | Tailwind CSS 4.3 + `@tailwindcss/typography` + `@tailwindcss/vite` |
| Contenido          | MDX + Zod schemas (`astro/loaders`) |
| Despliegue         | Vercel (static output, `@astrojs/vercel`) |
| Búsqueda           | Pagefind |
| OG images          | Satori + resvg |
| Analítica          | Vercel Speed Insights |
| Fuentes            | Tipografía variable en `public/fonts/` |
| Iconos             | astro-icon + SVGs en `public/icons/` |
| E2E testing        | Playwright |
| Image pipeline     | Python 3.11 (Pillow, aiohttp, google-genai) |

---

## Estructura del proyecto

```
blog/
├── public/                     # Archivos estáticos
│   ├── audio/                  # Archivos de audio
│   ├── fonts/                  # Fuentes tipográficas
│   ├── icons/                  # Iconos SVG
│   ├── img/                    # Imágenes generadas (WebP/AVIF)
│   └── rss/                    # Feed RSS
├── src/
│   ├── components/             # Componentes reutilizables
│   │   ├── Archive.astro
│   │   ├── AudioPlayer.astro
│   │   ├── Breadcrumbs.astro
│   │   ├── Buscador.astro
│   │   ├── Card.astro
│   │   ├── Challenge.astro
│   │   ├── CodeEnhancer.astro
│   │   ├── CodeTabs.svelte
│   │   ├── CopyPost.astro
│   │   ├── Footer.astro
│   │   ├── header.astro
│   │   ├── Information.astro
│   │   ├── MoreProjects.astro
│   │   ├── Navbar.astro
│   │   ├── NextPrevLinks.astro
│   │   ├── PaginationLinks.astro
│   │   ├── ReadingProgress.astro
│   │   ├── ResponsiveImage.astro
│   │   ├── ScrollToTop.astro
│   │   ├── SearchOverlay.astro
│   │   ├── SEO.astro
│   │   ├── TableOfContents.astro
│   │   ├── TagsPosts.astro
│   │   ├── ToggleButton.astro
│   │   ├── VideoExtractor.svelte
│   │   └── Weekly.astro
│   ├── content/                # Colecciones MDX
│   │   ├── auto-challenges/    # Retos de programación
│   │   ├── auto-news/          # Noticias semanales
│   │   ├── myprojects/         # Proyectos personales
│   │   ├── posts/              # Artículos
│   │   └── tools/              # Herramientas interactivas
│   ├── content.config.ts       # Schemas Zod + loaders
│   ├── data/                   # Datos auxiliares (JSON)
│   ├── layouts/                # Layouts de página
│   │   ├── ChallengesLayout.astro
│   │   ├── Layout.astro
│   │   ├── PostLayout.astro
│   │   ├── ProjectLayout.astro
│   │   └── ToolLayout.astro
│   ├── pages/                  # Rutas y páginas
│   │   ├── 404.astro
│   │   ├── api/og/             # Endpoint OG image
│   │   ├── herramientas/       # Herramientas
│   │   ├── posts/              # Artículos
│   │   ├── proyectos/          # Proyectos
│   │   ├── retos/              # Retos
│   │   ├── tags/               # Páginas por etiqueta
│   │   ├── weekly/             # Noticias semanales
│   │   ├── index.astro
│   │   └── rss.xml.js
│   ├── styles/
│   │   └── global.css          # Config Tailwind v4
│   └── utils.js                # Funciones auxiliares
├── scripts/
│   ├── actualizar_recursos.py
│   ├── constants_retos.py
│   ├── fix_images.py           # Pipeline de imágenes
│   ├── generate_resources.py
│   ├── hunt_challenges.py      # Generación IA de retos
│   ├── make_cover_collage.py   # Collages de portada
│   ├── restore_screenshots.py
│   ├── rewrite_challenges.py
│   ├── screenshot_helper.mjs
│   ├── solutions_data.py
│   ├── solutions_db.py
│   └── utils_retos.py
├── tests/
│   ├── helpers/
│   │   ├── server.mjs
│   │   └── start-server.mjs
│   ├── python/
│   │   ├── test_constants_retos.py
│   │   ├── test_fix_images.py
│   │   ├── test_generate_resources.py
│   │   └── test_solutions_db.py
│   └── specs/
│       ├── code-enhancer.spec.mjs
│       ├── console-errors.spec.mjs
│       ├── content.spec.mjs
│       ├── contrast.spec.mjs
│       ├── detail-pages.spec.mjs
│       ├── interactive.spec.mjs
│       ├── listing-pages.spec.mjs
│       ├── navigation.spec.mjs
│       ├── navbar.spec.mjs
│       ├── responsive.spec.mjs
│       ├── search.spec.mjs
│       ├── visual-regression-full.spec.mjs
│       └── visual-regression.spec.mjs
├── .github/workflows/
│   ├── fixing_img.yml          # Pipeline de imágenes en CI
│   ├── hunt_challenges.yml     # Generación semanal de retos
│   ├── issues_handel.yml       # Gestor de feedback
│   ├── spelling.yml            # Corrector ortográfico
│   └── test.yml                # Tests automáticos
├── astro.config.mjs
├── pagefind.yml                # Config Pagefind
├── playwright.config.js        # Config Playwright
├── svelte.config.ts
├── pyproject.toml              # Config Python + pytest
├── requirements.txt            # Dependencias Python
├── tsconfig.json
├── .vercelignore
├── AGENTS.md                   # Guía para agentes IA
└── docs/contexto.md            # Contexto del proyecto
```

---

## Comandos

| Comando               | Acción |
| --------------------- | ------ |
| `npm run dev`         | Inicia servidor de desarrollo en `localhost:4321` |
| `npm run build`       | Build estático + indexado Pagefind |
| `npm run preview`     | Previsualiza el build localmente |
| `npm run cleaner`     | Reinstala dependencias desde cero |
| `npm test`            | Ejecuta tests E2E con Playwright |
| `npm run test:build`  | Build + tests E2E |
| `npm run test:update` | Actualiza snapshots de regresión visual |
| `npm run test:ui`     | Playwright en modo UI interactivo |

---

## Pipeline de imágenes

`scripts/fix_images.py` procesa automáticamente las imágenes del contenido:

1. Busca imágenes en Unsplash usando el título del post como query
2. Genera banners con Gemini (fondo oscuro + código + etiquetas)
3. Convierte a WebP/AVIF con compresión adaptativa basada en SSIM
4. Genera placeholders blur (LQIP) en base64
5. Sustituye las marcas `![]()` por `<ResponsiveImage>` en el MDX
6. Cachea resultados en `image_cache.json` (podado automáticamente a 200 entradas máx.)

Otros scripts complementarios:

| Script | Propósito |
| ------ | --------- |
| `make_cover_collage.py` | Genera collages de portada para posts |
| `hunt_challenges.py` | Genera nuevos retos de programación vía IA (Gemini) |
| `rewrite_challenges.py` | Reestructura retos con formato multi‑lenguaje |
| `generate_resources.py` | Genera páginas de recursos |
| `actualizar_recursos.py` | Actualiza recursos existentes |
| `restore_screenshots.py` | Restaura capturas de pantalla |
| `screenshot_helper.mjs` | Helper para capturas |

### Requisitos

```bash
pip install -r requirements.txt
export UNSPLASH_ACCESS_KEY="tu_clave"
export GEMINI_API_KEY="tu_clave"
```

---

## Tests

### E2E (Playwright)

14 suites que cubren navegación, páginas de listado, detalle, componentes interactivos, responsive, contraste, búsqueda y regresión visual.

```bash
npm test                    # Todos los tests
npm run test:build          # Build + tests
npm run test:update         # Actualizar snapshots
npm run test:ui             # Modo UI
```

### Python (pytest)

Tests unitarios para los scripts de pipeline y utilidades.

```bash
pytest tests/python/
```

---

## CI/CD

El repositorio incluye 5 GitHub Actions:

| Workflow | Disparador | Propósito |
| -------- | ---------- | --------- |
| **fixing_img** | Push a `main` con cambios en contenido | Pipeline de imágenes + collage de portada |
| **hunt_challenges** | Semanal (domingo) | Genera nuevos retos de programación con Gemini |
| **spelling** | PR contra `content` | LanguageTool en español |
| **test** | Push a `main` | Ejecuta `pytest` en `tests/python/` |
| **issues_handel** | Issues | Gestiona el formulario de feedback |

---

## Licencia

Uso personal — contenido original del autor.
