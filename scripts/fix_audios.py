import re
import asyncio
import unicodedata
from pathlib import Path
import edge_tts
from typing import Dict, Any, List, Optional

# ==============================================================================
# CONFIGURACIÓN Y ENTORNO
# ==============================================================================
BASE_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = BASE_DIR.parent

TARGET_DIR: Path = ROOT_DIR / "src" / "content" / "posts"
AUDIO_DIR: Path = ROOT_DIR / "public" / "audio"

# Configuración de voz humana nativa de España
VOZ_ELEGIDA: str = "es-ES-AlvaroNeural" 

# Procesamos de 2 en 2 para que la red de GitHub Actions vaya fluida
MAX_CONCURRENT_POSTS: int = 2

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# LIMPIEZA QUIRÚRGICA DEL POST (Para que la lectura sea perfecta)
# ==============================================================================
def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def extraer_texto_puro_del_post(raw_content: str) -> str:
    """Quita el frontmatter y limpia el Markdown para que el lector lea el artículo real."""
    # 1. Separar el Frontmatter (quitamos la cabecera entre '---')
    partes = re.split(r'^---\s*$', raw_content, maxsplit=2, flags=re.MULTILINE)
    cuerpo_post: str = partes[2] if len(partes) >= 3 else raw_content

    # 2. Eliminar bloques de código de triple comilla por completo (```...```)
    # No queremos que el lector lea líneas de código sueltas que aburrirían al oyente
    cuerpo_post = re.sub(r'```.*?```', '', cuerpo_post, flags=re.DOTALL)
    
    # 3. Eliminar código en línea (`mi_variable`)
    cuerpo_post = re.sub(r'`.*?`', '', cuerpo_post)
    
    # 4. Limpiar enlaces de Markdown manteniendo el texto: [Mi Enlace](https://...) -> Mi Enlace
    cuerpo_post = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cuerpo_post)
    
    # 5. Eliminar imágenes Markdown por completo
    cuerpo_post = re.sub(r'!\[.*?\]\(.*?\)', '', cuerpo_post)
    
    # 6. Eliminar componentes Astro inyectados o etiquetas HTML (ej: <ResponsiveImage />)
    cuerpo_post = re.sub(r'<.*?>', '', cuerpo_post)
    
    # 7. Limpiar exceso de saltos de línea y almohadillas de los títulos (# Título -> Título)
    cuerpo_post = re.sub(r'#+\s+', '', cuerpo_post)
    
    return cuerpo_post.strip()

# ==============================================================================
# PIPELINE ASÍNCRONO E IDEMPOTENTE
# ==============================================================================
async def process_audio_file(path: Path, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content: str = f.read()

            base_name: str = slugify(path.stem)
            audio_filename: str = f"{base_name}.mp3"
            dest_audio_path: Path = AUDIO_DIR / audio_filename

            # Extraer el título del Frontmatter solo para el log de consola
            title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
            title: str = title_match.group(1).strip() if title_match else path.stem

            # Comprobación de Idempotencia pura
            has_audio_frontmatter: bool = "audioSrc:" in content
            audio_file_exists: bool = dest_audio_path.exists()

            # Si ya se hizo en el pasado y el archivo está ahí, saltamos de largo
            if has_audio_frontmatter and audio_file_exists:
                return

            print(f"🎙️ Convirtiendo Post Completo a Audio: '{title}'")

            # Paso 1: Si falta el archivo físico, lo generamos leyendo el post real
            if not audio_file_exists:
                # Extraemos el texto real del artículo sin código ni sintaxis Markdown
                texto_lectura: str = extraer_texto_puro_del_post(content)
                
                if not texto_lectura:
                    print(f"  ⚠️ El post '{title}' no tiene texto suficiente para leer.")
                    return

                # Inyectamos una introducción muy breve y natural para abrir el artículo
                texto_final: str = f"Artículo titulado: {title}. ... {texto_lectura}"
                
                # Generamos el audio directamente del texto del post
                communicate = edge_tts.Communicate(texto_final, VOZ_ELEGIDA)
                await communicate.save(str(dest_audio_path))
                print(f"  ✅ Audio completo generado: /audio/{audio_filename}")

            # Paso 2: Si falta inyectar la línea en el frontmatter, la insertamos
            if not has_audio_frontmatter:
                fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if fm_match:
                    frontmatter_original = fm_match.group(1)
                    nuevo_frontmatter = f"{frontmatter_original}\naudioSrc: \"/audio/{audio_filename}\""
                    
                    content = content.replace(frontmatter_original, nuevo_frontmatter, 1)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  ✍️ Frontmatter actualizado con audioSrc")

        except Exception as e:
            print(f"❌ Error al procesar audio en {path.name}: {e}")

# ==============================================================================
# ORQUESTADOR RECURSIVO
# ==============================================================================
async def main() -> None:
    target_path: Path = Path(TARGET_DIR)
    if not target_path.exists():
        return

    files: List[Path] = list(target_path.rglob("*.md")) + list(target_path.rglob("*.mdx"))
    if not files:
        return

    print(f"🚀 Iniciando TTS del contenido en {len(files)} posts...")
    
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_POSTS)
    tasks = [process_audio_file(file_path, semaphore) for file_path in files]
    await asyncio.gather(*tasks)
    print("🏁 Proceso completado.")

if __name__ == "__main__":
    asyncio.run(main())