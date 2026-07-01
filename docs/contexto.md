# Contexto del proyecto — Blog

**Última actualización**: 2026-07-01 (refactor SOLID JS + externalización config en blog post Tech Pulse)
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
| 2025-06 | **E2E audit completo**: 94 tests — navegación, listados, detalle, interactivos, responsive, contraste, visual regression. CodeTabs language detection fix (Shiki `pre[data-language]`). Navbar backdrop click handler |
| 2025-06 | **GFM tables + Shiki + Archive + Navbar**: GFM fix (Astro 6.4.x regression), Shiki `github-light`/`github-dark`, Archive sin toggle, Navbar con botón X dedicado sin cierre por backdrop/Escape |
| 2025-06 | **Refactor cards**: PreviewPost, ToolCard, ChallengeCard, ProjectCard unificados en un solo `Card.astro` paramétrico por acento |
| 2025-06 | **TOC scroll tracking fix**: querySelector reemplazado por getAttribute("href") para IDs con U+FE0F; observer reinicializado en cada navigation; primer heading activo por defecto; rootMargin ajustado |
| 2025-06 | **TOC overflow-y-auto**: max-h + scroll interno cuando la lista de enlaces excede el viewport |

## Mejoras implementadas

### 1. Refactor retos con multi-lenguaje ✅
- **scripts/constants_retos.py**: template actualizado de 1 a 4 lenguajes con CodeTabs
- **scripts/hunt_challenges.py**: adaptado para generar los 4 lenguajes + slug + `languages` field
- **scripts/rewrite_challenges.py**: nuevo script que procesa 143 retos — 58 reescritos con formato multi-lenguaje, 85 marcados como `draft: true`
- **src/components/CodeTabs.svelte**: nuevo componente con tabs interactivos para Python, JS, Java, TypeScript
- **src/content.config.ts**: schema extendido con campo `languages: string[]`
- **src/content/auto-challenges/**: 58 retos reformulados con descripciones, pasos, tests y código en 4 lenguajes
- **85 drafts eliminados**: retos redundantes o boilerplate eliminados del repositorio
- Commit: `[retos] Refactor multi-lenguaje: 58 reformulados, 85 eliminados, CodeTabs component`
- Build verificado sin errores

### 2. E2E audit completo + CodeTabs/Navbar fixes ✅
- **CodeTabs.svelte (onMount)**: language detection cambiado de `code.className.match(/language-(\w+)/)` a `pre.getAttribute('data-language')` — Shiki no añade clases `language-` al `<code>`, usa `data-language` en `<pre>`
- **CodeTabs.svelte (switchTab)**: bug `:scope > .code-panels > pre` corregido a `codePanels.querySelectorAll('pre')` (Astro envuelve slotted content en `<astro-slot>`)
- **Navbar.astro**: backdrop `#menu-backdrop` con click listener que cierra el menú mobile
- **8 spec files E2E**: `navigation.spec.mjs`, `listing-pages.spec.mjs`, `detail-pages.spec.mjs`, `interactive.spec.mjs`, `responsive.spec.mjs`, `contrast.spec.mjs`, `visual-regression-full.spec.mjs`, más fixes en `content.spec.mjs` y `navbar.spec.mjs`
- 93/94 tests passing (1 flaky: Ctrl+K focus por timing de Pagefind async)
- Build verificado sin errores

### 3. Varios fixes: GFM tables, Shiki, Archive, Navbar ✅
- **astro.config.mjs**: añadido `gfm: true` — corrige regresión de Astro 6.4.x donde tablas GFM no se renderizaban en `.mdx` (cambio de schema `.default(true)` a `.optional()`)
- **astro.config.mjs**: Shiki themes cambiados a `github-light`/`github-dark`
- **CodeEnhancer.astro**: filtra `<pre>` dentro de `<th>`/`<td>` para no romper tablas con wrapper `my-6`/`border`
- **CodeEnhancer.astro**: eliminado filtro `brightness(1.4) saturate(1.25)` en dark mode (sobresaturaba texto)
- **global.css**: eliminadas reglas duplicadas de `::-webkit-scrollbar` en `.details-content pre`
- **Archive.astro**: eliminada toda la lógica de ocultar años (toggle "Ver archivo completo", `hidden-archive-year`, `data-year-archived`, JS asociado) — todos los años visibles siempre
- **Navbar.astro**: eliminada animación de spans del hamburguer (rotar/opacidad); añadido botón X dedicado `#menu-close` dentro del panel; menú solo se abre con hamburguer, solo se cierra con X. Eliminados handlers de backdrop click, Escape key y resize. JS simplificado
- **tests/navigation.spec.mjs**: tests actualizados — Escape ya no cierra el menú, resize ya no cierra, nuevo test para botón X
- 39 tests funcionales pasan + 4 visual regression snapshots actualizadas
- Build verificado sin errores

### 5. TOC scroll tracking fix ✅
- **TableOfContents.astro**: reemplazado `document.querySelector('.toc-link[href="#${id}"]')` por `link.getAttribute("href") === `#${id}`` para evitar fallos con caracteres unicode (U+FE0F) en IDs de headings
- Desconectado `observer.disconnect()` antes de crear nuevo observer en cada `initTOC()` para evitar acumulación en navegaciones con `astro:page-load`
- Primer heading ahora se activa siempre como estado por defecto (no solo cuando `scrollY < 100`)
- `rootMargin` cambiado de `"-100px 0px -70% 0px"` a `"-120px 0px -60% 0px"` para tracking más natural
- Eliminado plugin `remark-clean-headings` innecesario de `astro.config.mjs`
- Eliminado TOC inline manual de `src/content/posts/n8n.mdx`
- Añadido `max-h-[calc(100vh-8rem)] overflow-y-auto` al contenedor sticky del TOC para scroll interno cuando hay muchos headings
- Build verificado sin errores

### 6. Actualización blog post Tech Pulse Dashboard ✅
- **src/content/myprojects/tech-pulse-dashboard.mdx**: añadidas secciones "Refactor SOLID del Frontend JavaScript" (store observable, fábrica genérica de chips, helpers puros, filtros unificados) y "Externalización de Configuración" (prompts IA, plantillas, config JS, constantes de dict keys movidos a `constants_downloadfile.py`)
- Eliminadas todas las referencias a "Becas" (badges ahora Tech/RSS, categorías de 7 a 6)
- Añadida sección de "Referencia Tech" en el feature set
- Dashboard renderizado actualizado con store observable y config externalizada
- Build verificado sin errores

### 4. Refactor cards: PreviewPost + ToolCard + ChallengeCard + ProjectCard → Card.astro ✅
- **Card.astro**: nuevo componente unificado que reemplaza 4 cards anteriores. Acepta `accent` ("cyan" | "emerald" | "purple"), `aspectRatio`, `overlay`, `difficulty` (badge opcional), `repository` (icono GitHub opcional), `tags`, `pubDate`. Misma estructura `<a>` wrapping que PreviewPost
- **4 componentes eliminados**: `PreviewPost.astro`, `ToolCard.astro`, `ChallengeCard.astro`, `ProjectCard.astro` — 457 líneas eliminadas, 249 añadidas
- **9 páginas actualizadas**: `index.astro`, `posts/[page].astro`, `posts/index.astro`, `herramientas/index.astro`, `herramientas/[page].astro`, `retos/[page].astro`, `proyectos/[page].astro`, `tags/[tag]/[page].astro`
- **ToolCard y ProjectCard**: ahora con `<a>` wrapping (antes tenían link "Detalles_") — todo el card es clickeable, mismo comportamiento que PreviewPost
- 59 tests pasan (incluyendo visual regression — sin cambios visuales)
- Build verificado sin errores

## Contenido

5 colecciones MDX en `src/content/`:
- `posts/` — incluye `resources.mdx` (482+ recursos), `n8n.mdx`, 15 guías 0-100, etc.
- `auto-news/` — noticias automáticas
- `auto-challenges/` — 58 retos multi-lenguaje (Python, JS, Java, TS)
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
- **Componentes clave**: `TableOfContents.astro` (mobile details + desktop sidebar), `Breadcrumbs.astro`, `Navbar.astro` (slot para buscador mobile, botón X dedicado para cerrar menú, sin cierre por backdrop/Escape/resize), `Header.astro`, `Buscador.astro`, `CopyPost.astro` (3 botones), `ScrollToTop.astro`, `Archive.astro` (todos los años visibles, sin toggle), `CodeTabs.svelte` (4-lang tabs interactivos)
- **Cards**: `Card.astro` (unificado, paramétrico por acento: cyan/emerald/purple, aspectRatio, overlay, difficulty badge, repository icon)
- **Guías**: 15 archivos `src/content/posts/guia-0-100-*.mdx`
- **Scripts**: `fix_images.py`, `image_cache.json`, `rewrite_challenges.py`, `solutions_db.py`, `constants_retos.py`, `hunt_challenges.py`
- **CI/CD**: `fixing_img.yml`, `spelling.yml`, `issues_handel.yml`
- **Skills**: `.opencode/skills/expand-guia-formato/SKILL.md`
- **Tests**: `tests/specs/search.spec.mjs`, `visual-regression.spec.mjs`, `navigation.spec.mjs`, `listing-pages.spec.mjs`, `detail-pages.spec.mjs`, `interactive.spec.mjs`, `responsive.spec.mjs`, `contrast.spec.mjs`, `visual-regression-full.spec.mjs`
