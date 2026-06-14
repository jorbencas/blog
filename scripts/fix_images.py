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

# Verificación de soporte AVIF
try:
    import pillow_avif
except ImportError:
    pillow_avif = None

# ==============================================================================
# CONFIGURACIÓN FUSIONADA
# ==============================================================================
ACCESS_KEY = __import__('os').getenv("UNSPLASH_ACCESS_KEY")
GEMINI_KEY = __import__('os').getenv("GEMINI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

TARGET_DIR = ROOT_DIR / "src" / "content"
IMG_DIR = ROOT_DIR / "public" / "img"
CACHE_FILE = ROOT_DIR / "image_cache.json"

SIZES = [480, 768, 1200]
DEFAULT_IMAGE = "/img/default.jpg"

# Parámetros Algorítmicos de optimize.py
SSIM_THRESHOLD = 0.98      # Identidad perceptiva humana
QUALITY_START = 85
QUALITY_MIN = 50
QUALITY_STEP = 5
WEBP_METHOD = 6            # Máxima compresión por fuerza bruta en WebP

IMG_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# SISTEMA DE CACHÉ
# ==============================================================================
try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
except:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

# ==============================================================================
# ALGORITMO SSIM (Structural Similarity Index)
# ==============================================================================
def _channel_stats(pixels_a, pixels_b, width, height):
    n = width * height
    if n == 0: return 0, 0, 0, 0, 0
    sum_a = sum_b = sum_aa = sum_bb = sum_ab = 0
    for i in range(n):
        a, b = pixels_a[i], pixels_b[i]
        sum_a += a; sum_b += b
        sum_aa += a*a; sum_bb += b*b
        sum_ab += a*b
    m_a, m_b = sum_a/n, sum_b/n
    var_a = max((sum_aa/n) - (m_a**2), 0)
    var_b = max((sum_bb/n) - (m_b**2), 0)
    cov_ab = (sum_ab/n) - (m_a*m_b)
    return m_a, m_b, var_a, var_b, cov_ab

def compute_ssim(img1, img2):
    C1, C2 = (0.01*255)**2, (0.03*255)**2
    t_size = (160, 160)
    a = img1.convert("L").resize(t_size, Image.LANCZOS)
    b = img2.convert("L").resize(t_size, Image.LANCZOS)
    px_a, px_b = list(a.tobytes()), list(b.tobytes())
    m_a, m_b, v_a, v_b, c_ab = _channel_stats(px_a, px_b, 160, 160)
    num = (2*m_a*m_b + C1) * (2*c_ab + C2)
    den = (m_a**2 + m_b**2 + C1) * (v_a + v_b + C2)
    return num/den if den != 0 else 1.0

def find_optimal_quality(original, save_func, start=QUALITY_START, min_q=QUALITY_MIN):
    best_q = start
    for q in range(start, min_q - 1, -QUALITY_STEP):
        compressed = save_func(q)
        if compute_ssim(original, compressed) >= SSIM_THRESHOLD:
            best_q = q
        else:
            break
    return best_q

# ==============================================================================
# PREPARACIÓN DE IMAGEN (STRIP & CONSTRAIN)
# ==============================================================================
def strip_metadata(img):
    clean = Image.new(img.mode, img.size)
    clean.paste(img)
    return clean

def constrain_size(img, max_width=1200):
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    return img

# ==============================================================================
# OPERACIONES COMPLEMENTARIAS (GIF / SVG)
# ==============================================================================
def process_gif_fallback(input_path, out_dir, base_name):
    """Convierte un GIF a formatos de vídeo modernos optimizados para la web."""
    out_mp4 = out_dir / f"{base_name}.mp4"
    out_webm = out_dir / f"{base_name}.webm"
    
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

def process_svg_fallback(input_path, out_dir, filename):
    """Minifica código SVG eliminando metadatos irrelevantes de diseño."""
    out_path = out_dir / filename
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    content = re.sub(r"", "", content, flags=re.DOTALL)
    content = re.sub(r"\s+", " ", content).strip()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

# ==============================================================================
# IA EDITORIAL (GEMINI CONTEXT)
# ==============================================================================
def get_gemini_tech_context(title, content_snippet=""):
    if not GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
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
        response = model.generate_content(prompt)
        match = re.search(r'(\{.*\})', response.text, re.DOTALL)
        if match: return json.loads(match.group(1))
    except:
        pass
    return None

# ==============================================================================
# AUXILIARES DE TEXTO
# ==============================================================================
def clean_query(text):
    words = text.replace("/", "_").replace("\\", "_").replace("-", "_").split("_")
    return " ".join([w for w in words if w.lower() not in ["guia", "tutorial", "como", "de", "para", "en"] and len(w) > 2])

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def build_srcset(images, prefix):
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in images])

async def search_unsplash(session, query):
    if not ACCESS_KEY or not query.strip(): return None
    if query in cache: return cache[query]
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query + " technology code abstract", "per_page": 1, "orientation": "landscape"}
    headers = {"Authorization": f"Client-ID {ACCESS_KEY}"}
    try:
        async with session.get(url, params=params, headers=headers) as r:
            if r.status != 200: return None
            data = await r.json()
            if not data["results"]: return None
            photo = data["results"][0]
            cache[query] = photo; save_cache()
            return photo
    except: return None

# ==============================================================================
# MOTOR GRÁFICO (IDE VECTOR CANVAS)
# ==============================================================================
def generate_local_banner(title, tech_context=None):
    try:
        width, height = 1200, 630
        ctx = tech_context or {}
        bg_dark = ctx.get("color_bg", "#0f141c")
        accent = ctx.get("color_accent", "#00f2fe")
        mock_file = ctx.get("mock_filename", "main.tsx")
        tech_label = ctx.get("tech_stack", "DEV WORKSPACE")
        keywords = ctx.get("keywords", ["code", "system"])
        
        img = Image.new('RGB', (width, height), bg_dark)
        draw = ImageDraw.Draw(img, "RGBA")
        
        for i in range(width):
            alpha = int(40 * (i / width))
            r_a, g_a, b_a = int(accent[1:3],16), int(accent[3:5],16), int(accent[5:7],16)
            draw.line([(i, 0), (i, height)], fill=(r_a, g_a, b_a, alpha))

        grid_size = 40
        for x in range(0, width, grid_size): draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 5))
        for y in range(0, height, grid_size): draw.line([(0, y), (width, y)], fill=(255, 255, 255, 5))

        random.seed(title)
        syntax_colors = [(56, 189, 248, 25), (244, 63, 94, 25), (52, 211, 153, 25)]
        for line_idx in range(12):
            y_pos = 140 + (line_idx * 32)
            indent = random.choice([60, 90, 120])
            block_len = random.randint(80, 300)
            draw.rounded_rectangle([indent, y_pos, indent + block_len, y_pos + 12], radius=4, fill=random.choice(syntax_colors))

        draw.ellipse([45, 45, 59, 59], fill="#ff5f56")
        draw.ellipse([67, 45, 81, 59], fill="#ffbd2e")
        draw.ellipse([89, 45, 103, 59], fill="#27c93f")

        font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"]
        font_main = font_sub = font_tag = None
        for p in font_paths:
            if Path(p).exists():
                font_main = ImageFont.truetype(p, 52); font_sub = ImageFont.truetype(p, 18); font_tag = ImageFont.truetype(p, 14)
                break
        if not font_main:
            font_main = font_sub = font_tag = ImageFont.load_default()

        draw.text((130, 43), f"~/projects/blog/src/content/posts/{mock_file}", font=font_sub, fill=(255, 255, 255, 90))
        draw.rounded_rectangle([width - 250, 38, width - 60, 70], radius=6, fill=(255, 255, 255, 15), outline=accent, width=1)
        draw.text((width - 235, 46), tech_label, font=font_tag, fill=accent)

        clean_title = title.replace("_", " ").replace("-", " ").upper()
        words = clean_title.split()
        lines, curr_line = [], []
        for word in words:
            curr_line.append(word)
            if (draw.textbbox((0, 0), " ".join(curr_line), font=font_main)[2]) > 850:
                curr_line.pop(); lines.append(" ".join(curr_line)); curr_line = [word]
        if curr_line: lines.append(" ".join(curr_line))

        y_offset = (height - (len(lines) * 65)) / 2 + 20
        for line in lines:
            tw = draw.textbbox((0, 0), line, font=font_main)[2]
            draw.text(((width - tw) / 2 + 4, y_offset + 4), line, font=font_main, fill=(0, 0, 0, 160))
            draw.text(((width - tw) / 2, y_offset), line, font=font_main, fill="#ffffff")
            y_offset += 70

        x_tag_offset = 60
        for kw in keywords:
            draw.text((x_tag_offset, height - 50), f"#{kw.lower()}", font=font_sub, fill=(255, 255, 255, 120))
            x_tag_offset += 200

        draw.rectangle([0, height - 10, width, height], fill=accent)
        return img
    except Exception as e:
        print(f"⚠️ Error en canvas: {e}")
        return Image.new('RGB', (1200, 630), "#0f172a")

# ==============================================================================
# PIPELINE DE COMPRESIÓN AVANZADA CON SSIM AUTOMÁTICO
# ==============================================================================
def compress_and_save_adaptive(img, base_name, folder):
    avif, webp = [], []
    blur = generate_placeholder(img)
    folder.mkdir(parents=True, exist_ok=True)

    img = constrain_size(img)
    img = strip_metadata(img)

    for size in SIZES:
        copy = img.copy()
        copy.thumbnail((size, size))
        
        # 1. Compresión Adaptativa WebP vía SSIM
        w_name = f"{base_name}-{size}.webp"
        w_path = folder / w_name
        if not w_path.exists():
            def save_webp_test(q):
                copy.save(w_path, "WEBP", quality=q, method=WEBP_METHOD)
                return Image.open(w_path)
            opt_q = find_optimal_quality(copy, save_webp_test)
            copy.save(w_path, "WEBP", quality=opt_q, method=WEBP_METHOD)
        webp.append((w_name, size))

        # 2. Compresión Adaptativa AVIF vía SSIM (Si está disponible)
        if pillow_avif:
            a_name = f"{base_name}-{size}.avif"
            a_path = folder / a_name
            if not a_path.exists():
                def save_avif_test(q):
                    copy.save(a_path, "AVIF", quality=q, speed=6)
                    return Image.open(a_path)
                opt_a = find_optimal_quality(copy, save_avif_test)
                copy.save(a_path, "AVIF", quality=opt_a, speed=6)
            avif.append((a_name, size))

    return avif, webp, blur

# ==============================================================================
# PROCESAMIENTO DE ARCHIVOS INDIVIDUALES
# ==============================================================================
async def process_file(session, path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    base_name = slugify(path.stem)
    md_images = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    fm_image = re.search(r'image:\s*["\']?(.*?)["\']?\n', content)
    fm_image = fm_image.group(1).strip() if fm_image else None

    current_folder = (IMG_DIR / base_name) if len(md_images) > 1 else IMG_DIR
    current_folder.mkdir(parents=True, exist_ok=True)

    # Resolución adaptativa de portadas
    if fm_image:
        portada_existe = (current_folder / f"{base_name}_cover-1200.webp").exists()
        if not portada_existe:
            res = await search_all_providers(session, base_name, content)
            if res["source"] == "local_gen":
                img = generate_local_banner(res["title"], res["theme"])
            else:
                async with session.get(res["url"], headers={"User-Agent": "Mozilla"}) as r:
                    img = Image.open(BytesIO(await r.read())) if r.status == 200 else Image.new('RGB', (1200,630), "#0f141c")
            
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            _, webp, _ = compress_and_save_adaptive(img, f"{base_name}_cover", current_folder)
            if webp:
                content = re.sub(r'image:\s*["\']?(.*?)["\']?\n', f'image: "{current_folder.name}/{webp[-1][0]}"\n', content)

    # Inyección y mutación inteligente del cuerpo Markdown
    for i, (alt, original_src) in enumerate(md_images):
        name = f"{base_name}_{i+1}"
        ext = original_src.lower().split(".")[-1]
        
        # Intercepción de formatos alternativos de optimize.py
        if ext == "gif":
            process_gif_fallback(ROOT_DIR / original_src.lstrip("/"), current_folder, name)
            continue
        elif ext == "svg":
            process_svg_fallback(ROOT_DIR / original_src.lstrip("/"), current_folder, f"{name}.svg")
            continue

        archivos_existen = all((current_folder / f"{name}-{s}.webp").exists() for s in SIZES)
        if not archivos_existen:
            full_local_path = ROOT_DIR / original_src.lstrip("/")
            if full_local_path.exists() and full_local_path.is_file():
                img = Image.open(full_local_path)
            else:
                res = await search_all_providers(session, alt if alt.strip() else base_name, content)
                async with session.get(res["url"], headers={"User-Agent": "Mozilla"}) as r:
                    img = Image.open(BytesIO(await r.read())) if r.status == 200 else Image.new('RGB', (1200,630), "#0f141c")

            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            avif, webp, blur = compress_and_save_adaptive(img, name, current_folder)
        else:
            avif = [(f"{name}-{size}.avif", size) for size in SIZES]
            webp = [(f"{name}-{size}.webp", size) for size in SIZES]
            blur = "data:image/jpeg;base64,/9j/4AAQSkZJRgA="

        prefix = f"/img/{base_name}" if len(md_images) > 1 else "/img"
        component = f'<ResponsiveImage avif="{build_srcset(avif, prefix)}" webp="{build_srcset(webp, prefix)}" fallback="{prefix}/{webp[-1][0]}" alt="{alt}" blur="{blur}" />'
        content = content.replace(f"![{alt}]({original_src})", component)

    # Inyección limpia del componente Astro
    import_stmt = 'import ResponsiveImage from "@components/ResponsiveImage.astro";'
    content = re.sub(r'import\s+ResponsiveImage\s+from\s+["\']@components/ResponsiveImage\.astro["\'];?\n*', '', content)
    if "<ResponsiveImage" in content:
        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match: content = content[:fm_match.end()] + import_stmt + "\n\n" + content[fm_match.end():]

    with open(path, "w", encoding="utf-8") as f: f.write(content)

async def search_all_providers(session, query, content_snippet=""):
    photo = await search_unsplash(session, query)
    if photo: return {"url": photo["urls"]["raw"], "source": "unsplash"}
    return {"source": "local_gen", "title": query, "theme": get_gemini_tech_context(query, content_snippet)}

# ==============================================================================
# ORQUESTADOR (BÚSQUEDA RECURSIVA CON PATHLIB O(N))
# ==============================================================================
async def process_posts():
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        target_path = Path(TARGET_DIR)
        if not target_path.exists(): return
        
        files = list(target_path.rglob("*.md")) + list(target_path.rglob("*.mdx"))
        tasks = [process_file(session, file_path) for file_path in files]
        if tasks: await asyncio.gather(*tasks)
    save_cache()

if __name__ == "__main__":
    asyncio.run(process_posts())
