import re
import json
import asyncio
import aiohttp
import base64
import unicodedata
import hashlib
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from typing import Dict, Any, List, Tuple, Optional, Callable

# Verificación y tipado seguro del soporte AVIF
pillow_avif: Optional[Any] = None
try:
    import pillow_avif  # type: ignore
except ImportError:
    pillow_avif = None

# ==============================================================================
# CONFIGURACIÓN FUSIONADA Y ENTORNO
# ==============================================================================
ACCESS_KEY: Optional[str] = __import__('os').getenv("UNSPLASH_ACCESS_KEY")
GEMINI_KEY: Optional[str] = __import__('os').getenv("GEMINI_API_KEY")

BASE_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = BASE_DIR.parent

TARGET_DIR: Path = ROOT_DIR / "src" / "content"
IMG_DIR: Path = ROOT_DIR / "public" / "img"
CACHE_FILE: Path = ROOT_DIR / "image_cache.json"

SIZES: List[int] = [480, 768, 1200]
DEFAULT_IMAGE: str = "/img/default.jpg"

# Parámetros Algorítmicos de compresión SSIM
SSIM_THRESHOLD: float = 0.98      # Identidad perceptiva humana
QUALITY_START: int = 85
QUALITY_MIN: int = 50
QUALITY_STEP: int = 5
WEBP_METHOD: int = 6               # Máxima compresión por fuerza bruta en WebP

# Límite de concurrencia de archivos para evitar TimeoutError en GitHub Actions
MAX_CONCURRENT_FILES: int = 3

IMG_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# SISTEMA DE CACHÉ
# ==============================================================================
MAX_CACHE_ENTRIES: int = 200

def _parse_date(date_str: str) -> Optional[Any]:
    try:
        from datetime import datetime
        return datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
    except Exception:
        return None

def prune_cache(cache_data: Dict[str, Any]) -> Dict[str, Any]:
    from datetime import datetime, timezone
    now: Any = datetime.now(timezone.utc)
    pruned: Dict[str, Any] = {}
    for key, val in cache_data.items():
        if not isinstance(val, dict):
            continue
        created = val.get("created_at", "")
        dt = _parse_date(created)
        # Descarta entradas con más de 365 días
        if dt and (now - dt).days > 365:
            continue
        pruned[key] = val
    # Si aún excede el límite, conserva las más recientes por updated_at
    if len(pruned) > MAX_CACHE_ENTRIES:
        pruned = dict(
            sorted(pruned.items(), key=lambda kv: kv[1].get("updated_at", ""), reverse=True)[:MAX_CACHE_ENTRIES]
        )
    return pruned

cache: Dict[str, Any] = {}
try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
except Exception:
    cache = {}
cache = prune_cache(cache)

def save_cache() -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

# ==============================================================================
# ALGORITMO SSIM (Structural Similarity Index)
# ==============================================================================
def _channel_stats(
    pixels_a: List[int], pixels_b: List[int], width: int, height: int
) -> Tuple[float, float, float, float, float]:
    n: int = width * height
    if n == 0: 
        return 0.0, 0.0, 0.0, 0.0, 0.0
    sum_a: float = 0.0
    sum_b: float = 0.0
    sum_aa: float = 0.0
    sum_bb: float = 0.0
    sum_ab: float = 0.0
    for i in range(n):
        a: int = pixels_a[i]
        b: int = pixels_b[i]
        sum_a += a
        sum_b += b
        sum_aa += a * a
        sum_bb += b * b
        sum_ab += a * b
    m_a: float = sum_a / n
    m_b: float = sum_b / n
    var_a: float = max((sum_aa / n) - (m_a ** 2), 0.0)
    var_b: float = max((sum_bb / n) - (m_b ** 2), 0.0)
    cov_ab: float = (sum_ab / n) - (m_a * m_b)
    return m_a, m_b, var_a, var_b, cov_ab

def compute_ssim(img1: Image.Image, img2: Image.Image) -> float:
    C1: float = (0.01 * 255) ** 2
    C2: float = (0.03 * 255) ** 2
    t_size: Tuple[int, int] = (160, 160)
    a: Image.Image = img1.convert("L").resize(t_size, Image.LANCZOS)
    b: Image.Image = img2.convert("L").resize(t_size, Image.LANCZOS)
    px_a: List[int] = list(a.tobytes())
    px_b: List[int] = list(b.tobytes())
    m_a, m_b, v_a, v_b, c_ab = _channel_stats(px_a, px_b, 160, 160)
    num: float = (2 * m_a * m_b + C1) * (2 * c_ab + C2)
    den: float = (m_a ** 2 + m_b ** 2 + C1) * (v_a + v_b + C2)
    return num / den if den != 0.0 else 1.0

def find_optimal_quality(
    original: Image.Image, save_func: Callable[[int], Image.Image], start: int = QUALITY_START, min_q: int = QUALITY_MIN
) -> int:
    best_q: int = start
    for q in range(start, min_q - 1, -QUALITY_STEP):
        compressed: Image.Image = save_func(q)
        if compute_ssim(original, compressed) >= SSIM_THRESHOLD:
            best_q = q
        else:
            break
    return best_q

# ==============================================================================
# PREPARACIÓN DE IMAGEN (STRIP & CONSTRAIN)
# ==============================================================================
def strip_metadata(img: Image.Image) -> Image.Image:
    clean: Image.Image = Image.new(img.mode, img.size)
    clean.paste(img)
    return clean

def constrain_size(img: Image.Image, max_width: int = 1200) -> Image.Image:
    if img.width > max_width:
        ratio: float = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    return img

# ==============================================================================
# OPERACIONES COMPLEMENTARIAS (GIF / SVG)
# ==============================================================================
def process_gif_fallback(input_path: Path, out_dir: Path, base_name: str) -> None:
    """Convierte un GIF a formatos de vídeo modernos optimizados para la web."""
    out_mp4: Path = out_dir / f"{base_name}.mp4"
    out_webm: Path = out_dir / f"{base_name}.webm"
    
    if not out_mp4.exists():
        subprocess.run([
            "ffmpeg", "-y", "-i", str(input_path),
            "-movflags", "faststart", "-pix_fmt", "yuv420p",
            "-vf", "scale='trunc(iw/2)*2:trunc(ih/2)*2'",
            "-c:v", "libx264", "-crf", "23", "-an", str(out_mp4)
        ], capture_output=True)
        
    if not out_webm.exists():
        subprocess.run([
            "ffmpeg", "-y", "-i", str(input_path),
            "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-an", str(out_webm)
        ], capture_output=True)
        
    shutil.copy2(input_path, out_dir / f"{base_name}.gif")

def process_svg_fallback(input_path: Path, out_dir: Path, filename: str) -> None:
    """Minifica código SVG eliminando metadatos irrelevantes de diseño."""
    out_path: Path = out_dir / filename
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        content: str = f.read()
    content = re.sub(r"<metadata>.*?</metadata>", "", content, flags=re.DOTALL)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    content = re.sub(r"\s+", " ", content).strip()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

# ==============================================================================
# IA EDITORIAL (MIGRADO AL NUEVO SDK GOOGLE-GENAI)
# ==============================================================================
def get_gemini_tech_context(title: str, content_snippet: str = "") -> Optional[Dict[str, Any]]:
    if not GEMINI_KEY:
        return None
    try:
        # Migración al nuevo cliente de la librería unificada google-genai
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)
        
        prompt: str = f"""
        Analiza este artículo de blog tecnológico. Título: "{title}". Fragmento: "{content_snippet[:400]}"
        Devuelve estrictamente un objeto JSON válido con la siguiente estructura:
        {{
          "color_bg": "Un color hexadecimal CSS muy oscuro adecuado para fondo de IDE (ej: #0d1117, #0f141c)",
          "color_accent": "Un color hexadecimal vibrante neón tipo sintaxis (ej: #00f2fe, #38bdf8)",
          "keywords": ["3 palabras clave tecnológicas"],
          "mock_filename": "Un nombre de archivo simulado (ej: index.tsx, server.js, deploy.yaml)",
          "tech_stack": "Nombre de la tecnología principal en mayúsculas (ej: ASTRO, REACT, DOCKER)"
        }}
        """
        # Llamada estructurada nativa para gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response.text:
            match = re.search(r'(\{.*\})', response.text, re.DOTALL)
            if match: 
                return json.loads(match.group(1))  # type: ignore
    except Exception as e:
        print(f"⚠️ Aviso en el cliente Gemini GenAI: {e}")
    return None

# ==============================================================================
# AUXILIARES DE TEXTO
# ==============================================================================
def clean_query(text: str) -> str:
    words: List[str] = text.replace("/", "_").replace("\\", "_").replace("-", "_").split("_")
    return " ".join([w for w in words if w.lower() not in ["guia", "tutorial", "como", "de", "para", "en"] and len(w) > 2])

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def build_srcset(images: List[Tuple[str, int]], prefix: str) -> str:
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in images])

async def search_unsplash(session: aiohttp.ClientSession, query: str) -> Optional[Dict[str, Any]]:
    if not ACCESS_KEY or not query.strip(): 
        return None
    if query in cache: 
        return cache[query]  # type: ignore
    url: str = "https://api.unsplash.com/search/photos"
    params: Dict[str, str] = {"query": query + " technology code abstract", "per_page": "1", "orientation": "landscape"}
    headers: Dict[str, str] = {"Authorization": f"Client-ID {ACCESS_KEY}"}
    try:
        async with session.get(url, params=params, headers=headers, timeout=15) as r:
            if r.status != 200: 
                return None
            data: Dict[str, Any] = await r.json()
            if not data.get("results"): 
                return None
            photo: Dict[str, Any] = data["results"][0]
            cache[query] = photo
            save_cache()
            return photo
    except Exception: 
        return None

# ==============================================================================
# MOTOR GRÁFICO (IDE VECTOR CANVAS)
# ==============================================================================
def generate_local_banner(title: str, tech_context: Optional[Dict[str, Any]] = None) -> Image.Image:
    try:
        width: int = 1200
        height: int = 630
        ctx: Dict[str, Any] = tech_context or {}
        bg_dark: str = ctx.get("color_bg", "#0f141c")
        accent: str = ctx.get("color_accent", "#00f2fe")
        mock_file: str = ctx.get("mock_filename", "main.tsx")
        tech_label: str = ctx.get("tech_stack", "DEV WORKSPACE")
        keywords: List[str] = ctx.get("keywords", ["code", "system"])
        
        img: Image.Image = Image.new('RGB', (width, height), bg_dark)
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img, "RGBA")
        
        for i in range(width):
            alpha: int = int(40 * (i / width))
            r_a: int = int(accent[1:3], 16)
            g_a: int = int(accent[3:5], 16)
            b_a: int = int(accent[5:7], 16)
            draw.line([(i, 0), (i, height)], fill=(r_a, g_a, b_a, alpha))

        grid_size: int = 40
        for x in range(0, width, grid_size): 
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 5))
        for y in range(0, height, grid_size): 
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 5))

        random.seed(title)
        syntax_colors: List[Tuple[int, int, int, int]] = [(56, 189, 248, 25), (244, 63, 94, 25), (52, 211, 153, 25)]
        for line_idx in range(12):
            y_pos: int = 140 + (line_idx * 32)
            indent: int = random.choice([60, 90, 120])
            block_len: int = random.randint(80, 300)
            draw.rounded_rectangle([indent, y_pos, indent + block_len, y_pos + 12], radius=4, fill=random.choice(syntax_colors))

        draw.ellipse([45, 45, 59, 59], fill="#ff5f56")
        draw.ellipse([67, 45, 81, 59], fill="#ffbd2e")
        draw.ellipse([89, 45, 103, 59], fill="#27c93f")

        font_paths: List[str] = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"]
        font_main: Optional[ImageFont.FreeTypeFont] = None
        font_sub: Optional[ImageFont.FreeTypeFont] = None
        font_tag: Optional[ImageFont.FreeTypeFont] = None
        
        for p in font_paths:
            if Path(p).exists():
                font_main = ImageFont.truetype(p, 52)
                font_sub = ImageFont.truetype(p, 18)
                font_tag = ImageFont.truetype(p, 14)
                break
                
        # Cast seguro a tipado básico si no se encuentran las fuentes ttf
        f_main = font_main if font_main else ImageFont.load_default()
        f_sub = font_sub if font_sub else ImageFont.load_default()
        f_tag = font_tag if font_tag else ImageFont.load_default()

        draw.text((130, 43), f"~/projects/blog/src/content/posts/{mock_file}", font=f_sub, fill=(255, 255, 255, 90))
        draw.rounded_rectangle([width - 250, 38, width - 60, 70], radius=6, fill=(255, 255, 255, 15), outline=accent, width=1)
        draw.text((width - 235, 46), tech_label, font=f_tag, fill=accent)

        clean_title: str = title.replace("_", " ").replace("-", " ").upper()
        words: List[str] = clean_title.split()
        lines: List[str] = []
        curr_line: List[str] = []
        for word in words:
            curr_line.append(word)
            if (draw.textbbox((0, 0), " ".join(curr_line), font=f_main)[2]) > 850:
                curr_line.pop()
                lines.append(" ".join(curr_line))
                curr_line = [word]
        if curr_line: 
            lines.append(" ".join(curr_line))

        y_offset: float = (height - (len(lines) * 65)) / 2 + 20
        for line in lines:
            tw: float = draw.textbbox((0, 0), line, font=f_main)[2]
            draw.text(((width - tw) / 2 + 4, y_offset + 4), line, font=f_main, fill=(0, 0, 0, 160))
            draw.text(((width - tw) / 2, y_offset), line, font=f_main, fill="#ffffff")
            y_offset += 70

        x_tag_offset: int = 60
        for kw in keywords:
            draw.text((x_tag_offset, height - 50), f"#{kw.lower()}", font=f_sub, fill=(255, 255, 255, 120))
            x_tag_offset += 200

        draw.rectangle([0, height - 10, width, height], fill=accent)
        return img
    except Exception as e:
        print(f"⚠️ Error en canvas: {e}")
        return Image.new('RGB', (1200, 630), "#0f172a")

# ==============================================================================
# PIPELINE DE COMPRESIÓN AVANZADA CON SSIM AUTOMÁTICO
# ==============================================================================
def generate_placeholder(img: Image.Image) -> str:
    """Genera una miniatura de 20x20 píxeles comprimida en Base64 para el efecto blur."""
    try:
        small: Image.Image = img.copy()
        small.thumbnail((20, 20))
        buffer: BytesIO = BytesIO()
        small.save(buffer, format="JPEG", quality=30)
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        print(f"⚠️ Error al generar el placeholder blur: {e}")
        return "data:image/jpeg;base64,/9j/4AAQSkZJRgA="

def compress_and_save_adaptive(
    img: Image.Image, base_name: str, folder: Path
) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]], str]:
    avif: List[Tuple[str, int]] = []
    webp: List[Tuple[str, int]] = []
    blur: str = generate_placeholder(img)
    folder.mkdir(parents=True, exist_ok=True)

    img = constrain_size(img)
    img = strip_metadata(img)

    for size in SIZES:
        copy: Image.Image = img.copy()
        copy.thumbnail((size, size))
        
        # 1. Compresión Adaptativa WebP vía SSIM
        w_name: str = f"{base_name}-{size}.webp"
        w_path: Path = folder / w_name
        if not w_path.exists():
            def save_webp_test(q: int) -> Image.Image:
                copy.save(w_path, "WEBP", quality=q, method=WEBP_METHOD)
                return Image.open(w_path)
            opt_q: int = find_optimal_quality(copy, save_webp_test)
            copy.save(w_path, "WEBP", quality=opt_q, method=WEBP_METHOD)
        webp.append((w_name, size))

        # 2. Compresión Adaptativa AVIF vía SSIM (Si está disponible)
        if pillow_avif:
            a_name: str = f"{base_name}-{size}.avif"
            a_path: Path = folder / a_name
            if not a_path.exists():
                def save_avif_test(q: int) -> Image.Image:
                    copy.save(a_path, "AVIF", quality=q, speed=6)
                    return Image.open(a_path)
                opt_a: int = find_optimal_quality(copy, save_avif_test)
                copy.save(a_path, "AVIF", quality=opt_a, speed=6)
            avif.append((a_name, size))

    return avif, webp, blur

# ==============================================================================
# PROCESAMIENTO DE ARCHIVOS INDIVIDUALES
# ==============================================================================
async def process_file(session: aiohttp.ClientSession, path: Path, semaphore: asyncio.Semaphore) -> None:
    # Usamos el semáforo para adquirir un espacio bloqueante y controlar los hilos asíncronos
    async with semaphore:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content: str = f.read()

            base_name: str = slugify(path.stem)
            md_images: List[Tuple[str, str]] = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
            
            fm_image_match = re.search(r'image:\s*["\']?(.*?)["\']?\n', content)
            fm_image: Optional[str] = fm_image_match.group(1).strip() if fm_image_match else None

            current_folder: Path = (IMG_DIR / base_name) if len(md_images) > 1 else IMG_DIR
            current_folder.mkdir(parents=True, exist_ok=True)

            # Resolución adaptativa de portadas
            if fm_image:
                portada_existe: bool = (current_folder / f"{base_name}_cover-1200.webp").exists()
                if not portada_existe:
                    res: Dict[str, Any] = await search_all_providers(session, base_name, content)
                    if res["source"] == "local_gen":
                        img: Image.Image = generate_local_banner(res["title"], res["theme"])
                    else:
                        async with session.get(res["url"], headers={"User-Agent": "Mozilla"}, timeout=15) as r:
                            img = Image.open(BytesIO(await r.read())) if r.status == 200 else Image.new('RGB', (1200,630), "#0f141c")
                    
                    if img.mode in ("RGBA", "P"): 
                        img = img.convert("RGB")
                    _, webp, _ = compress_and_save_adaptive(img, f"{base_name}_cover", current_folder)
                    if webp:
                        content = re.sub(r'image:\s*["\']?(.*?)["\']?\n', f'image: "{current_folder.name}/{webp[-1][0]}"\n', content)

            # Inyección del cuerpo Markdown (Procesa imágenes internas)
            for i, (alt, original_src) in enumerate(md_images):
                name: str = f"{base_name}_{i+1}"
                ext: str = original_src.lower().split(".")[-1]
                
                if ext == "gif":
                    process_gif_fallback(ROOT_DIR / original_src.lstrip("/"), current_folder, name)
                    continue
                elif ext == "svg":
                    process_svg_fallback(ROOT_DIR / original_src.lstrip("/"), current_folder, f"{name}.svg")
                    continue

                archivos_existen: bool = all((current_folder / f"{name}-{s}.webp").exists() for s in SIZES)
                if not archivos_existen:
                    full_local_path: Path = ROOT_DIR / original_src.lstrip("/")
                    if full_local_path.exists() and full_local_path.is_file():
                        img = Image.open(full_local_path)
                    else:
                        res = await search_all_providers(session, alt if alt.strip() else base_name, content)
                        async with session.get(res["url"], headers={"User-Agent": "Mozilla"}, timeout=15) as r:
                            img = Image.open(BytesIO(await r.read())) if r.status == 200 else Image.new('RGB', (1200,630), "#0f141c")

                    if img.mode in ("RGBA", "P"): 
                        img = img.convert("RGB")
                    avif, webp, blur = compress_and_save_adaptive(img, name, current_folder)
                else:
                    avif = [(f"{name}-{size}.avif", size) for size in SIZES]
                    webp = [(f"{name}-{size}.webp", size) for size in SIZES]
                    blur = "data:image/jpeg;base64,/9j/4AAQSkZJRgA="

                prefix: str = f"/img/{base_name}" if len(md_images) > 1 else "/img"
                component: str = f'<ResponsiveImage avif="{build_srcset(avif, prefix)}" webp="{build_srcset(webp, prefix)}" fallback="{prefix}/{webp[-1][0]}" alt="{alt}" blur="{blur}" />'
                content = content.replace(f"![{alt}]({original_src})", component)

            # Inyección limpia del componente Astro en la sección frontmatter
            import_stmt: str = 'import ResponsiveImage from "@components/ResponsiveImage.astro";'
            content = re.sub(r'import\s+ResponsiveImage\s+from\s+["\']@components/ResponsiveImage\.astro["\'];?\n*', '', content)
            if "<ResponsiveImage" in content:
                fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if fm_match: 
                    content = content[:fm_match.end()] + import_stmt + "\n\n" + content[fm_match.end():]

            with open(path, "w", encoding="utf-8") as f: 
                f.write(content)
        except Exception as e:
            print(f"❌ Error al procesar el archivo {path.name}: {e}")

async def search_all_providers(session: aiohttp.ClientSession, query: str, content_snippet: str = "") -> Dict[str, Any]:
    photo: Optional[Dict[str, Any]] = await search_unsplash(session, query)
    if photo: 
        return {"url": photo["urls"]["raw"], "source": "unsplash"}
    return {"source": "local_gen", "title": query, "theme": get_gemini_tech_context(query, content_snippet)}

# ==============================================================================
# ORQUESTADOR (BÚSQUEDA RECURSIVA CONTROLADA POR SEMÁFORO)
# ==============================================================================
async def process_posts() -> None:
    # Agregamos timeouts estrictos a nivel sesión HTTP
    timeout_config = aiohttp.ClientTimeout(total=30, connect=10, sock_read=10)
    connector = aiohttp.TCPConnector(limit=10)
    
    # Creamos el semáforo para racionar la ejecución asíncrona de archivos
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_FILES)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout_config) as session:
        target_path: Path = Path(TARGET_DIR)
        if not target_path.exists(): 
            return
        
        files: List[Path] = list(target_path.rglob("*.md")) + list(target_path.rglob("*.mdx"))
        
        # Pasamos el semáforo a cada corrutina
        tasks = [process_file(session, file_path, semaphore) for file_path in files]
        if tasks: 
            await asyncio.gather(*tasks)
    save_cache()

if __name__ == "__main__":
    asyncio.run(process_posts())
