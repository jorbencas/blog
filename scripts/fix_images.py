import os
import re
import json
import asyncio
import aiohttp
import base64
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

# ========================
# CONFIG
# ========================

ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

TARGET_DIR = os.path.join(ROOT_DIR, "src", "content")
IMG_DIR = os.path.join(ROOT_DIR, "public", "img")

CACHE_FILE = os.path.join(ROOT_DIR, "image_cache.json")

SIZES = [480, 768, 1200]
DEFAULT_IMAGE = "/img/default.jpg"

os.makedirs(IMG_DIR, exist_ok=True)

# ========================
# CACHE
# ========================

try:
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
except:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

# ========================
# GEMINI (Optional)
# ========================

def get_gemini_theme(query):
    if not GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Define a visual tech theme for a blog post titled "{query}".
        Provide only a JSON with:
        {{
          "color1": "CSS Hex color (dark)",
          "color2": "CSS Hex color (vibrant)",
          "concept": "One word tech concept (e.g. circuit, code, neural)"
        }}
        """
        response = model.generate_content(prompt)
        match = re.search(r'(\{.*\})', response.text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except:
        pass
    return None

# ========================
# HELPERS
# ========================

STOPWORDS = ["guia", "tutorial", "como", "ejemplo", "simple", "introduccion", "png", "jpg", "jpeg", "webp"]

def clean_query(text):
    # Reemplaza guiones y barras para limpiar nombres de archivos rotos
    text = text.replace("/", "_").replace("\\", "_").replace("-", "_")
    words = text.split("_")
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return " ".join(words)

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def extract_md_images(content):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', content)

def extract_frontmatter_image(content):
    match = re.search(r'image:\s*["\']?(.*?)["\']?\n', content)
    return match.group(1).strip() if match else None

def replace_frontmatter_image(content, new_value):
    return re.sub(
        r'image:\s*["\']?(.*?)["\']?\n',
        f'image: "{new_value}"\n',
        content
    )

def fix_broken_url(src):
    if src.startswith("/img/http"):
        return src.replace("/img/", "")
    return src

def build_srcset(images, prefix):
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in images])

# ========================
# UNSPLASH
# ========================

async def search_unsplash(session, query):
    if not ACCESS_KEY or not query.strip():
        return None

    if query in cache:
        return cache[query]

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }
    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}",
        "User-Agent": "AstroBlogImageFixer/1.0"
    }

    try:
        async with session.get(url, params=params, headers=headers) as r:
            if r.status != 200:
                return None
            data = await r.json()
            if not data["results"]:
                return None
            photo = data["results"][0]
            cache[query] = photo
            save_cache()
            return photo
    except:
        return None

# ========================
# GENERACIÓN DE BANNER CON PILLOW
# ========================
def generate_local_banner(title, theme=None):
    try:
        width, height = 1200, 630
        c1 = theme.get("color1", "#0f172a") if theme else "#0f172a"
        
        img = Image.new('RGB', (width, height), c1)
        draw = ImageDraw.Draw(img, "RGBA")
        
        grid_spacing = 40
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 6))
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 6))
            
        for r in range(350, 0, -8):
            alpha = int(30 * (1 - r/350))
            draw.ellipse([width-r, height-r, width+r, height+r], fill=(56, 189, 248, alpha))

        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
        ]
        font = None
        for p in font_paths:
            if os.path.exists(p):
                font = ImageFont.truetype(p, 52)
                break
        if not font:
            font = ImageFont.load_default()

        text = title.replace("_", " ").replace("-", " ").upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        draw.text(((width-tw)/2 + 3, (height-th)/2 + 3), text, font=font, fill=(0, 0, 0, 100))
        draw.text(((width-tw)/2, (height-th)/2), text, font=font, fill="white")
        
        draw.ellipse([50, 50, 62, 62], fill="#ef4444")
        draw.ellipse([70, 50, 82, 62], fill="#f59e0b")
        draw.ellipse([90, 50, 102, 62], fill="#10b981")

        return img
    except Exception as e:
        print(f"⚠️ Error generando banner en Pillow: {e}")
        return cargar_imagen_por_defecto_segura()

def cargar_imagen_por_defecto_segura():
    try:
        ruta_defecto = os.path.join(ROOT_DIR, "public", DEFAULT_IMAGE.lstrip("/"))
        if os.path.exists(ruta_defecto):
            return Image.open(ruta_defecto)
    except:
        pass
    return Image.new('RGB', (1200, 630), "#1e293b")

async def search_all_providers(session, query):
    photo = await search_unsplash(session, query)
    if photo:
        return {"url": photo["urls"]["raw"], "source": "unsplash", "data": photo}

    theme = get_gemini_theme(query)
    return {
        "source": "local_gen",
        "title": query,
        "theme": theme
    }

# ========================
# IMAGE PROCESSING
# ========================

def generate_placeholder(img):
    small = img.copy()
    small.thumbnail((20, 20))
    buffer = BytesIO()
    small.save(buffer, format="JPEG", quality=30)
    return base64.b64encode(buffer.getvalue()).decode()

def generate_images(img, base_name, folder):
    avif = []
    webp = []
    blur = generate_placeholder(img)

    os.makedirs(folder, exist_ok=True)

    for size in SIZES:
        copy = img.copy()
        copy.thumbnail((size, size))

        webp_name = f"{base_name}-{size}.webp"
        webp_path = os.path.join(folder, webp_name)

        if not os.path.exists(webp_path):
            copy.save(webp_path, "WEBP", quality=80)

        webp.append((webp_name, size))

        try:
            avif_name = f"{base_name}-{size}.avif"
            avif_path = os.path.join(folder, avif_name)

            if not os.path.exists(avif_path):
                copy.save(avif_path, "AVIF", quality=50)

            avif.append((avif_name, size))
        except:
            pass

    return avif, webp, blur

async def fetch_image(session, url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers, timeout=15) as r:
            if r.status != 200:
                return None
            return await r.read()
    except:
        return None

async def load_image(session, src, query=None):
    # 1. Si es remota, se descarga
    if src.startswith("http"):
        data = await fetch_image(session, src)
        if data:
            try: return Image.open(BytesIO(data))
            except: pass
    else:
        # 2. Si es local, se comprueba si de verdad existe el archivo en disco
        full = os.path.join(ROOT_DIR, src.lstrip("/"))
        if os.path.exists(full) and os.path.isfile(full):
            try: return Image.open(full)
            except: pass

    # 3. 🚨 PLAN DE RESCATE: Si el archivo no existe o está corrupto, buscamos/generamos uno nuevo
    print(f"🔍 Archivo ausente o roto ({src}). Activando protocolo de rescate...")
    
    # Intentamos buscar usando el texto alternativo (alt) o el nombre del archivo roto limpiado
    search_term = clean_query(query or os.path.basename(src))
    result = await search_all_providers(session, search_term)
    
    if result:
        if result["source"] == "local_gen":
            return generate_local_banner(result["title"], result["theme"])
        
        img_data = await fetch_image(session, result["url"])
        if img_data:
            try: return Image.open(BytesIO(img_data))
            except: pass

    return cargar_imagen_por_defecto_segura()

# ========================
# COVER
# ========================

async def generate_cover_if_missing(session, base_name, current_folder):
    name = f"{base_name}_cover"
    expected = os.path.join(current_folder, f"{name}-1200.webp")
    if os.path.exists(expected):
        return

    query = clean_query(base_name)
    result = await search_all_providers(session, query)

    if not result:
        return

    if result["source"] == "local_gen":
        img = generate_local_banner(result["title"], result["theme"])
    else:
        img_data = await fetch_image(session, result["url"])
        if not img_data:
            img = cargar_imagen_por_defecto_segura()
        else:
            img = Image.open(BytesIO(img_data))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    generate_images(img, name, current_folder)

# ========================
# CONTROL DE IMPORTS
# ========================

def fix_imports_and_clean(content):
    import_statement = 'import ResponsiveImage from "@components/ResponsiveImage.astro";'
    content = re.sub(r'import\s+ResponsiveImage\s+from\s+["\']@components/ResponsiveImage\.astro["\'];?\n*', '', content)
    
    if "<ResponsiveImage" in content:
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            end_of_frontmatter = frontmatter_match.end()
            header = content[:end_of_frontmatter]
            body = content[end_of_frontmatter:]
            return f"{header}{import_statement}\n\n{body}"
        else:
            return f"{import_statement}\n\n{content}"
    return content

# ========================
# PROCESS FILE
# ========================

async def process_file(session, path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    base_name = slugify(os.path.splitext(os.path.basename(path))[0])
    md_images = extract_md_images(content)
    fm_image = extract_frontmatter_image(content)

    # Selección dinámica de carpetas según tu criterio de volumen de imágenes
    if len(md_images) > 1:
        current_folder = os.path.join(IMG_DIR, base_name)
        prefix = f"/img/{base_name}"
    else:
        current_folder = IMG_DIR
        prefix = "/img"

    os.makedirs(current_folder, exist_ok=True)

    await generate_cover_if_missing(session, base_name, current_folder)

    # FRONTMATTER COVER
    if fm_image:
        fm_image = fix_broken_url(fm_image)
        portada_optimizada_existe = os.path.exists(os.path.join(current_folder, f"{base_name}_cover-1200.webp"))
        
        if not portada_optimizada_existe:
            # Aquí load_image rescatará la portada si la ruta original de la metadata está rota
            img = await load_image(session, fm_image, query=base_name)
            if img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                _, webp, _ = generate_images(img, f"{base_name}_cover", current_folder)
                if webp:
                    fallback = f"{prefix}/{webp[-1][0]}"
                    content = replace_frontmatter_image(content, fallback)
            else:
                content = replace_frontmatter_image(content, DEFAULT_IMAGE)
        else:
            content = replace_frontmatter_image(content, f"{prefix}/{base_name}_cover-1200.webp")

    # MARKDOWN IMAGES
    for i, (alt, original_src) in enumerate(md_images):
        src = fix_broken_url(original_src)
        name = f"{base_name}_{i+1}"
        
        rutas_resoluciones = [os.path.join(current_folder, f"{name}-{size}.webp") for size in SIZES]
        archivos_existen = all(os.path.exists(r) for r in rutas_resoluciones)

        if not archivos_existen:
            # Mandamos el término de búsqueda 'alt' o el 'base_name' por si la ruta física del mdx está rota
            query_fallback = alt if alt.strip() else base_name
            img = await load_image(session, src, query=query_fallback)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            avif, webp, blur = generate_images(img, name, current_folder)
        else:
            avif = [(f"{name}-{size}.avif", size) for size in SIZES]
            webp = [(f"{name}-{size}.webp", size) for size in SIZES]
            blur = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAAUABQBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="

        component = f'''
<ResponsiveImage
  avif="{build_srcset(avif, prefix)}"
  webp="{build_srcset(webp, prefix)}"
  fallback="{prefix}/{webp[-1][0]}"
  alt="{alt}"
  blur="{blur}"
/>
'''
        content = content.replace(f"![{alt}]({original_src})", component)
        content = content.replace(f"![{alt}]({src})", component)

    content = fix_imports_and_clean(content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ========================
# MAIN
# ========================

async def process_posts():
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        if os.path.exists(TARGET_DIR):
            for root, _, files in os.walk(TARGET_DIR):
                for file in files:
                    if file.endswith((".md", ".mdx")):
                        path = os.path.join(root, file)
                        tasks.append(process_file(session, path))
            if tasks:
                await asyncio.gather(*tasks)

    save_cache()

if __name__ == "__main__":
    asyncio.run(process_posts())