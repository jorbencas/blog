import re
import asyncio
import aiohttp
import unicodedata
from pathlib import Path
import edge_tts
from typing import Dict, Any, List, Optional

# ==============================================================================
# CONFIGURACIÓN Y ENTORNO
# ==============================================================================
GEMINI_KEY: Optional[str] = __import__('os').getenv("GEMINI_API_KEY")

BASE_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = BASE_DIR.parent

TARGET_DIR: Path = ROOT_DIR / "src" / "content" / "posts"
AUDIO_DIR: Path = ROOT_DIR / "public" / "audio"

# Configuración de voz (es-ES-AlvaroNeural proporciona una entonación excelente)
VOZ_ELEGIDA: str = "es-ES-AlvaroNeural" 

# Control de concurrencia: procesa un máximo de 2 posts simultáneamente
MAX_CONCURRENT_POSTS: int = 2

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# AUXILIARES DE TEXTO & LIMPIEZA
# ==============================================================================
def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def limpiar_markdown_para_lectura(text: str) -> str:
    """Elimina bloques de código, tags y URLs para que el guion sea 100% natural."""
    # Eliminar bloques de código de triple comilla (```...```)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Eliminar código en línea (`code`)
    text = re.sub(r'`.*?`', '', text)
    # Enlaces Markdown: [Texto](URL) -> nos quedamos solo con el Texto
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Eliminar imágenes Markdown
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Eliminar componentes Astro o etiquetas HTML explícitas
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

# ==============================================================================
# INTELIGENCIA ARTIFICIAL: GENERACIÓN DEL LOCUTOR DE PODCAST
# ==============================================================================
def generar_guion_resumen(title: str, content: str) -> str:
    """Usa el nuevo SDK de Gemini para redactar un guion adaptado al oído humano."""
    if not GEMINI_KEY:
        return f"Resumen del artículo titulado: {title}. Por favor, lee el contenido completo en el blog."
        
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)
        
        texto_limpio: str = limpiar_markdown_para_lectura(content)
        
        prompt: str = f"""
        Actúa como un locutor de podcast tecnológico profesional, cercano y con ritmo dinámico.
        Quiero que hagas un resumen hablado de nuestro último artículo técnico titulado: "{title}".
        
        Contenido del post para resumir:
        \"\"\"{texto_limpio[:4000]}\"\"\"
        
        REGLAS CRÍTICAS DE LOCUCIÓN:
        1. Escribe en Español nativo de España.
        2. No uses NADA de formato Markdown (sin asteriscos, almohadillas, ni listas). Solo texto plano con comas y puntos bien colocados para estructurar las pausas de respiración.
        3. Explica los conceptos de código o arquitectura de forma abstracta (que se entienda perfectamente de oído). No deletrees comandos de consola ni menciones URLs.
        4. Empieza con un gancho directo (ej: "¡Hola! En este mini-podcast analizamos el artículo...") y despídete invitando a explorar la guía completa en la web.
        5. Longitud ideal: Entre 200 y 350 palabras (equivalente a 1 o 2 minutos de audio fluido).
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response.text:
            return response.text.strip()
    except Exception as e:
        print(f"⚠️ Error en Gemini GenAI al procesar '{title}': {e}")
    
    return f"Resumen de: {title}. Encuentra toda la información técnica detallada en el cuerpo del artículo."

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

            # Extraer el título del Frontmatter
            title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
            title: str = title_match.group(1).strip() if title_match else path.stem

            # Verificación cruzada (Idempotencia)
            has_audio_frontmatter: bool = "audioSrc:" in content
            audio_file_exists: bool = dest_audio_path.exists()

            # 🛠️ DETECCIÓN SÓLIDA: Si tiene el frontmatter PERO el archivo físico no existe,
            # forzamos su regeneración cambiando este flag a False.
            if has_audio_frontmatter and not audio_file_exists:
                print(f"⚠️ Alerta: Se detectó frontmatter de audio en '{title}', pero el archivo .mp3 ha desaparecido.")
                # Permitimos que continúe el script para volver a crear el archivo binario

            # Si el frontmatter está puesto y el archivo físico existe, pasamos de largo
            if has_audio_frontmatter and audio_file_exists:
                return

            print(f"🎙️ Generando audio-resumen para: '{title}'")

            # Paso 1: Si no existe el .mp3 físico en public/audio/, lo creamos
            if not audio_file_exists:
                guion_podcast: str = generar_guion_resumen(title, content)
                
                communicate = edge_tts.Communicate(guion_podcast, VOZ_ELEGIDA)
                await communicate.save(str(dest_audio_path))
                print(f"  ✅ Audio binario creado correctamente: /audio/{audio_filename}")

            # Paso 2: Si falta inyectar la línea en el frontmatter, la insertamos
            if not has_audio_frontmatter:
                fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if fm_match:
                    frontmatter_original = fm_match.group(1)
                    # Añadimos la propiedad de forma limpia antes de cerrar el bloque YAML
                    nuevo_frontmatter = f"{frontmatter_original}\naudioSrc: \"/audio/{audio_filename}\""
                    
                    content = content.replace(frontmatter_original, nuevo_frontmatter, 1)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  ✍️ Frontmatter actualizado con audioSrc en '{path.name}'")

        except Exception as e:
            print(f"❌ Error al procesar audio en el archivo {path.name}: {e}")

# ==============================================================================
# ORQUESTADOR RECURSIVO
# ==============================================================================
async def main() -> None:
    target_path: Path = Path(TARGET_DIR)
    if not target_path.exists():
        print(f"❌ Error: El directorio {TARGET_DIR} no existe.")
        return

    # Buscar recursivamente todos los artículos .md y .mdx
    files: List[Path] = list(target_path.rglob("*.md")) + list(target_path.rglob("*.mdx"))
    if not files:
        print("📭 No hay artículos para procesar.")
        return

    print(f"🚀 Ejecutando Pipeline TTS sobre {len(files)} posts...")
    
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_POSTS)
    tasks = [process_audio_file(file_path, semaphore) for file_path in files]
    await asyncio.gather(*tasks)
    print("🏁 Pipeline de audio completado de forma segura.")

if __name__ == "__main__":
    asyncio.run(main())