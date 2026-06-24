---
name: update-context
description: |
  Use ONLY when the user says "compact", "update context", "save context",
  "wrap up", "actualiza el context", or explicitly asks to save progress
  in docs/contexto.md.
  Updates docs/contexto.md with the latest changes while preserving the
  established format. Run `npm run build` before saving and only mark
  changes that build successfully.
---

# Update Context — docs/contexto.md

Always read the current `docs/contexto.md` first and preserve **all existing
content and sections**. Only append, insert, or modify the specific parts that
changed.

## Format rules

### Header block
Keep the YAML-like header at the top. Update `Última actualización` to today's
date (YYYY-MM-DD). Preserve all other fields (Stack, Deploy, Idioma, Node).

### Mejoras implementadas
Each work cycle becomes a new numbered section under `## Mejoras implementadas`.

```
### N. Short Spanish title ✅
- bullet per change: **File/area**: what changed (why if non-obvious)
- Build verificado sin errores
```

- Use `✅` after the title.
- One bullet per logical change. Use `**bold**` for the file/area name.
- End with `- Build verificado sin errores` (or explain any warnings).

### Archivos relevantes
Update this section to add/move/remove files. Organized by category:

```
### Config
- `astro.config.mjs`, `tsconfig.json`, `AGENTS.md`, `README.md`

### CI/CD
- `.github/workflows/spelling.yml`, `fixing_img.yml`, `issues_handel.yml`
- `.languagetool-ignore.txt`
- `docs/ci-cd.md`

### Layouts
### Componentes
### Páginas
### Contenido y estilos
### Scripts y datos
```

Only edit the relevant category. If a file was deleted, remove it. If a file is
new, add it. If a new category makes sense, create it.

### Main sections
Preserve these top-level sections untouched unless the changes directly affect
them:
- `## Contenido`
- `## Pipeline de imágenes`
- `## Tailwind v4`
- `## Componente ResponsiveImage`
- `## VideoExtractor`
- `## SEO`
- `## TypeScript`

If a change modifies one of these areas (e.g. the image pipeline), update the
corresponding section.

## Verification

1. Run `npm run build` before touching `docs/contexto.md`.
2. If build fails, do NOT update context — fix the error first.
3. Only write "Build verificado sin errores" if exit code is 0.
4. If there are pre-existing warnings (e.g. `weeklyPosts` empty, deprecation
   notices), note them but still consider the build valid.
