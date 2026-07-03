# Blog — jorbencas

[![Vercel](https://img.shields.io/badge/deploy-vercel-black?logo=vercel)](https://blog-jorbencas.vercel.app/)
[![Astro](https://img.shields.io/badge/astro-6.4-BC52EE?logo=astro)](https://astro.build)
[![Svelte](https://img.shields.io/badge/svelte-5-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.3-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![Playwright](https://img.shields.io/badge/test-playwright-45ba4b?logo=playwright)](https://playwright.dev)
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
├── tests/
│   └── specs/                  # Tests E2E Playwright
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
│   ├── issues_handel.yml       # Gestor de feedback
│   ├── spelling.yml            # Corrector ortográfico
│   ├── test.yml                # Tests E2E
│   └── trigger-optimize.yml    # Dispatch optimización imágenes
├── astro.config.mjs
├── pagefind.yml                # Config Pagefind
├── playwright.config.js        # Config Playwright
├── svelte.config.ts
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

## Tests

14 suites E2E (Playwright) que cubren navegación, páginas de listado, detalle, componentes interactivos, responsive, contraste, búsqueda y regresión visual.

```bash
npm test                    # Todos los tests
npm run test:build          # Build + tests
npm run test:update         # Actualizar snapshots
npm run test:ui             # Modo UI
```

---

## CI/CD

| Workflow | Disparador | Propósito |
| -------- | ---------- | --------- |
| **trigger-optimize** | Push a `main` (imágenes o contenido) | Dispatch a test_githubActions para optimización |
| **spelling** | PR contra `content` | LanguageTool en español |
| **test** | Push a `main` | Tests E2E Playwright |
| **issues_handel** | Issues | Gestiona el formulario de feedback |

---

## Licencia

Uso personal — contenido original del autor.
