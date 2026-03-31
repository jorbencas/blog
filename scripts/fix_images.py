import os
import re
import json
import asyncio
import aiohttp
import base64
import unicodedata
from PIL import Image
from io import BytesIO

# ========================
# PATHS
# ========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

TARGET_DIR = os.path.join(ROOT_DIR, "src", "content")
IMG_DIR = os.path.join(ROOT_DIR, "public", "img")

CACHE_FILE = os.path.join(ROOT_DIR, "unsplash_cache.json")

SIZES = [480, 768, 1200]

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
# HELPERS
# ========================

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def extract_md_images(content):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', content)

def ensure_component_import(content):
    if "ResponsiveImage" in content:
        return content
    return f'import ResponsiveImage from "@components/ResponsiveImage.astro";\n\n{content}'

# ========================
# IMAGE GENERATION
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

    for size in SIZES:

        # WEBP
        webp_name = f"{base_name}-{size}.webp"
        webp_path = os.path.join(folder, webp_name)

        if not os.path.exists(webp_path):
            copy = img.copy()
            copy.thumbnail((size, size))
            copy.save(webp_path, "WEBP", quality=80)

        webp.append((webp_name, size))

        # AVIF
        avif_name = f"{base_name}-{size}.avif"
        avif_path = os.path.join(folder, avif_name)

        if not os.path.exists(avif_path):
            copy = img.copy()
            copy.thumbnail((size, size))
            copy.save(avif_path, "AVIF", quality=50)

        avif.append((avif_name, size))

    return avif, webp, blur

# ========================
# LOAD IMAGE
# ========================

async def fetch_image(session, url):
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                return None
            return await resp.read()
    except:
        return None

async def load_image(session, source):
    try:
        if source.startswith("http"):
            data = await fetch_image(session, source)
            if not data:
                return None
            return Image.open(BytesIO(data))
        else:
            full = os.path.join(ROOT_DIR, source.lstrip("/"))
            if not os.path.exists(full):
                return None
            return Image.open(full)
    except:
        return None

# ========================
# SRCSET
# ========================

def build_srcset(images, prefix):
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in images])

# ========================
# PROCESS FILE
# ========================

async def process_file(session, old_path):

    file = os.path.basename(old_path)
    is_md = file.endswith(".md")

    new_filename = file.replace(".md", ".mdx")
    new_path = os.path.join(os.path.dirname(old_path), new_filename)

    with open(old_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = ensure_component_import(content)

    base_name = slugify(os.path.splitext(new_filename)[0])
    images = extract_md_images(content)

    multiple = len(images) > 1

    folder = IMG_DIR
    prefix = "/img"

    if multiple:
        folder = os.path.join(IMG_DIR, base_name)
        os.makedirs(folder, exist_ok=True)
        prefix = f"/img/{base_name}"

    for i, (alt, src) in enumerate(images):

        name = f"{base_name}_{i+1}" if multiple else base_name

        img = await load_image(session, src)
        if not img:
            continue

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        avif, webp, blur = generate_images(img, name, folder)

        avif_srcset = build_srcset(avif, prefix)
        webp_srcset = build_srcset(webp, prefix)

        fallback = f"{prefix}/{webp[-1][0]}"

        md_pattern = f"![{alt}]({src})"

        component = f'''
<ResponsiveImage
  avif="{avif_srcset}"
  webp="{webp_srcset}"
  fallback="{fallback}"
  alt="{alt}"
  blur="{blur}"
/>
'''

        content = content.replace(md_pattern, component)

    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)

    if is_md and old_path != new_path:
        os.remove(old_path)

# ========================
# MAIN
# ========================

async def process_posts():
    tasks = []

    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:

        for root, _, files in os.walk(TARGET_DIR):
            for file in files:

                if not file.endswith((".md", ".mdx")):
                    continue

                path = os.path.join(root, file)
                tasks.append(process_file(session, path))

        await asyncio.gather(*tasks)

    save_cache()

# ========================

if __name__ == "__main__":
    asyncio.run(process_posts())