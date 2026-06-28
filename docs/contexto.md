# Contexto del proyecto — Blog

**Última actualización**: 2026-06-28 (refactor retos + multi-lenguaje)
**Stack**: Astro 6.4 + Svelte 5 + Tailwind CSS 4.3 | Vercel static | Node >= 18
**Idioma**: Español
**Deploy**: `blog-jorbencas.vercel.app`
**Guía detallada de diseño/componentes**: `AGENTS.md` (Design System, Component Patterns, MDX Syntax, Build Verification)

## Timeline de cambios significativos

| Fecha | Cambio |
|---|---|
| 2025-04 | Recursos masivo (482+ cards), Pagefind, overflow safety, tags simplificado |
| 2025-04 | n8n integrado, TOC con fallback DOM, iconos SVG sin CDN |
| 2025-04 | Anti-flash dark mode, CopyPost dropdown→botones, light theme bg más suave |
| 2025-04 | Botones "Ver más" en móvil, Query Unsplash mejorada |
| 2025-05 | 15 guías 0-100 expandidas (~1500–3700 líneas c/u), skill de formato creada |
| 2025-05 | Errores MDX preexistentes fixeados (`<Fragment>`, `<1ms`, `<T>`, `<100ms`) |
| 2025-06 | **UI/UX audit**: Fase 1 (TOC colapsable mobile, breadcrumbs, max-w-4xl), Fase 2 (footer opacidad, cards sin quotes), Fase 3 (transición main, archive limitado), Fase 4 (buscador en hamburguesa, scroll-to-top desktop) |
| 2025-06 | **Retos multi-lenguaje**: 58 reformulados con 4 lenguajes (Python, JS, Java, TS), 85 archivados como draft. CodeTabs component |

## Mejoras implementadas

### 1. Refactor retos con multi-lenguaje ✅
- **scripts/constants_retos.py**: template actualizado de 1 a 4 lenguajes con CodeTabs
- **scripts/hunt_challenges.py**: adaptado para generar los 4 lenguajes + slug + `languages` field
- **scripts/rewrite_challenges.py**: nuevo script que procesa 143 retos — 58 reescritos con formato multi-lenguaje, 85 marcados como `draft: true`
- **src/components/CodeTabs.svelte**: nuevo componente con tabs interactivos para Python, JS, Java, TypeScript
- **src/content.config.ts**: schema extendido con campo `languages: string[]`
- **src/content/auto-challenges/**: 58 retos reformulados con descripciones, pasos, tests y código en 4 lenguajes
- Build verificado sin errores

## Contenido

5 colecciones MDX en `src/content/`:
- `posts/` — incluye `resources.mdx` (482+ recursos), `n8n.mdx`, 15 guías 0-100, etc.
- `auto-news/` — noticias automáticas
- `auto-challenges/` — +140 retos
- `myprojects/` — proyectos personales
- `tools/` — herramientas interactivas

`draft: true` filtra en desarrollo. Schemas con `astro/zod` en `src/content.config.ts`.

## Página de inicio (`index.astro`)

Orden de secciones: Mis_Proyectos → Mini_Herramientas → Retos → Últimos_Posts → Resúmenes_Semanales. Cada sección muestra 3-6 items con su card type correspondiente.

## Pipeline de imágenes

`scripts/fix_images.py`: Unsplash + Gemini banners → WebP/AVIF con compresión SSIM. Cachea en `image_cache.json` (auto-pruning: >365 días, max 200 entradas). `build_unsplash_query()` combina tags + título + tech hints contextuales.

## Tailwind v4 (notas clave)

- CSS-first: `src/styles/global.css` con `@plugin "@tailwindcss/typography"` + `@custom-variant dark`
- `html { scrollbar-gutter: stable }` evita layout shift en menú móvil
- Sin `tailwind.config.mjs` ni `postcss.config.mjs`
- `@apply` **no soportado** en `<style>` blocks de componentes

## Archivos relevantes

- **Layouts**: `PostLayout.astro` (TOC en grid), `Layout.astro` (tema, anti-flash), `ProjectLayout.astro`
- **Componentes clave**: `TableOfContents.astro` (mobile details + desktop sidebar), `Breadcrumbs.astro`, `Navbar.astro` (slot para buscador mobile), `Header.astro`, `Buscador.astro`, `CopyPost.astro` (3 botones), `ScrollToTop.astro`, `Archive.astro` (2 años + link completo)
- **Cards**: `PreviewPost`, `ChallengeCard`, `ToolCard`, `ProjectCard` — sin quotes/italics en descripciones
- **Guías**: 15 archivos `src/content/posts/guia-0-100-*.mdx`
- **Scripts**: `fix_images.py`, `image_cache.json`, `rewrite_challenges.py`, `solutions_db.py`, `constants_retos.py`, `hunt_challenges.py`
- **CI/CD**: `fixing_img.yml`, `spelling.yml`, `issues_handel.yml`
- **Skills**: `.opencode/skills/expand-guia-formato/SKILL.md`
- **Tests**: `tests/specs/search.spec.mjs`, `visual-regression.spec.mjs`
