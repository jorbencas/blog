# Blog — jorbencas

[![Vercel](https://img.shields.io/badge/deploy-vercel-black?logo=vercel)](https://blog-jorbencas.vercel.app/)
[![Astro](https://img.shields.io/badge/astro-6.4-BC52EE?logo=astro)](https://astro.build)
[![Svelte](https://img.shields.io/badge/svelte-5-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.3-06B6D4?logo=tailwindcss)](https://tailwindcss.com)

Blog personal de tecnología y desarrollo, construido con Astro 6, Svelte 5 y Tailwind CSS 4. Incluye artículos técnicos, retos de programación, proyectos personales y un resumen semanal de noticias.

**[→ Abrir demo](https://blog-jorbencas.vercel.app/)**

---

## Características

- **4 colecciones de contenido** — posts, retos de programación (140+), proyectos personales y noticias semanales
- **Imágenes responsive** — pipeline automático con WebP/AVIF, compresión adaptativa SSIM y placeholder blur
- **Modo oscuro** — conmutación manual, persistente en localStorage
- **Búsqueda** — Pagefind indexa todo el sitio en el build
- **SEO** — JSON-LD, Open Graph, Twitter Cards, sitemap, RSS
- **OG images** — generación dinámica con Satori + resvg
- **VideoExtractor** — herramienta para extraer cortes de video desde el navegador (WebM/MP4)
- **Audio lazy** — WaveSurfer se carga solo cuando el elemento entra en viewport
- **Tabla de contenidos** — con scroll spy via IntersectionObserver
- **Tipado estricto** — TypeScript strict + `noUncheckedIndexedAccess`
- **Rendimiento** — imágenes con `fetchpriority="high"` para LCP, lazy loading, Astro islands

---

## Stack

| Categoría      | Tecnología |
| -------------- | ---------- |
| Framework      | Astro 6.4 |
| Islas interactivas | Svelte 5 |
| Estilos        | Tailwind CSS 4.3 + `@tailwindcss/typography` |
| Contenido      | MDX + Zod schemas (`astro/loaders`) |
| Despliegue     | Vercel (static output, `@astrojs/vercel`) |
| Búsqueda       | Pagefind |
| OG images      | Satori + resvg |
| Fuentes        | Tipografía variable en `public/fonts/` |
| Iconos         | astro-icon + SVGs en `public/icons/` |

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
│   │   ├── toolsmini/          # Herramientas (VideoExtractor, etc.)
│   │   ├── Navbar.astro
│   │   ├── ResponsiveImage.astro
│   │   ├── SEO.astro
│   │   ├── AudioPlayer.astro
│   │   ├── TableOfContents.astro
│   │   ├── PreviewPost.astro
│   │   └── ...
│   ├── content/                # Colecciones MDX
│   │   ├── posts/
│   │   ├── auto-news/
│   │   ├── auto-challenges/
│   │   └── myprojects/
│   ├── content.config.ts       # Schemas Zod + loaders
│   ├── data/                   # Datos auxiliares (JSON)
│   ├── layouts/                # Layouts de página
│   │   ├── Layout.astro
│   │   ├── PostLayout.astro
│   │   └── ChallengesLayout.astro
│   ├── pages/                  # Rutas y páginas
│   │   ├── api/og/             # Endpoint OG image
│   │   ├── posts/
│   │   ├── proyectos/
│   │   ├── retos/
│   │   ├── toolsmini/
│   │   └── ...
│   ├── styles/
│   │   └── global.css          # Config Tailwind v4
│   └── utils.js                # Funciones auxiliares
├── scripts/
│   └── fix_images.py           # Pipeline de imágenes (Python)
├── astro.config.mjs
├── tsconfig.json
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

---

## Pipeline de imágenes

`scripts/fix_images.py` procesa automáticamente las imágenes del contenido:

1. Busca imágenes en Unsplash usando el título del post como query
2. Genera banners合成 con Gemini (fondo oscuro + código + etiquetas)
3. Convierte a WebP/AVIF con compresión adaptativa basada en SSIM
4. Genera placeholders blur (LQIP) en base64
5. Sustituye las marcas `![]()` por `<ResponsiveImage>` en el MDX
6. Cachea resultados en `image_cache.json` (podado automáticamente a 200 entradas máx.)

### Requisitos

```bash
pip install -r requirements.txt
export UNSPLASH_ACCESS_KEY="tu_clave"
export GEMINI_API_KEY="tu_clave"
```

---

## CI/CD

El repositorio incluye GitHub Actions para:

- **Image fixing** — se ejecuta automáticamente al hacer push a main con cambios en contenido
- **Spelling check** — LanguageTool en español para PRs contra la rama `content`
- **Feedback handler** — gestión de issues del formulario de feedback

---

## Licencia

Uso personal — contenido original del autor.
