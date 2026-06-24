# CI/CD — Flujos de GitHub Actions

El repositorio tiene tres flujos automatizados:

## 1. Fix Images — `fixing_img.yml`

**Disparador:** Push a `main` con cambios en `src/content/**/*.md*` (o manual via `workflow_dispatch`).

**Qué hace:**
1. Instala Python 3.11 + dependencias (`requirements.txt`)
2. Instala FFmpeg (para conversión GIF → MP4/WebM)
3. Ejecuta `scripts/fix_images.py`:
   - Busca imágenes Unsplash para cada post (cachea en `image_cache.json`)
   - Genera banners con Gemini si no encuentra en Unsplash
   - Convierte a WebP/AVIF con compresión adaptativa SSIM
   - Genera placeholders blur (LQIP) en base64
   - Sustituye `![]()` por `<ResponsiveImage>` en los MDX
4. Hace commit automático de los archivos generados (`[bot] update responsive images [skip ci]`)

**Requiere secrets:**
- `UNSPLASH_ACCESS_KEY`
- `GEMINI_API_KEY`

---

## 2. Spelling Check — `spelling.yml`

**Disparador:** Pull Request abierta contra cualquier rama con cambios en `src/content/**/*.md*`.

**Qué hace:**
1. Reemplaza temporalmente palabras técnicas (`.languagetool-ignore.txt`) por "Sistema" para evitar falsos positivos
2. Ejecuta [Reviewdog](https://github.com/reviewdog/action-languagetool) con LanguageTool en español
3. Comenta en la PR las sugerencias ortográficas y gramaticales directamente sobre las líneas del archivo (`github-pr-review`)
4. Solo revisa líneas añadidas (`filter_mode: added`), no todo el archivo
5. Restaura los archivos originales después del chequeo

**Diccionario personalizado:** editar `.languagetool-ignore.txt` en la raíz del repo — una palabra técnica por línea.

**Categorías desactivadas** para reducir ruido con código/markdown: `CASING`, `STYLE`, `REDUNDANCY`, `CAPITALIZATION`.

**Ventajas de este sistema:**
- **No rompe el sitio** — al usar PRs, el sitio sigue funcionando mientras decides si corriges o no
- **Aprendizaje** — las sugerencias aparecen en "Files changed" de la PR, mantienes el control total

**Sin requisitos extra** — LanguageTool se usa vía API pública gratuita. Sin claves ni suscripción.

---

## 3. Feedback Wall — `issues_handel.yml`

**Disparador:** Issue abierto o editado (o manual).

**Qué hace:**
1. Detecta si el issue es un feedback (título empieza por `Feedback:` o tiene label `anonymous-feedback`)
2. Extrae el texto del formulario (máximo 140 caracteres)
3. Filtra trolls con palabras prohibidas
4. Añade la línea de feedback al archivo correspondiente (no implementado en el script actual)
5. Cierra y bloquea el issue automáticamente

**Permisos necesarios:** `contents: write` e `issues: write`.
