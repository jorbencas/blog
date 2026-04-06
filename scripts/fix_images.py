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
# CONFIG
# ========================

ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

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

STOPWORDS = ["guia", "tutorial", "como", "ejemplo", "simple", "introduccion"]

def clean_query(text):
    words = text.split("_")
    words = [w for w in words if w not in STOPWORDS]
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

def has_responsive_component(content):
    return "<ResponsiveImage" in content

def add_import_if_needed(content, used):
    if not used:
        return content
    if "ResponsiveImage" in content:
        return content
    return f'import ResponsiveImage from "@components/ResponsiveImage.astro";\n\n{content}'

def clean_unused_import(content):
    if "<ResponsiveImage" in content:
        return content
    return re.sub(
        r'import\s+ResponsiveImage\s+from\s+["\']@components/ResponsiveImage\.astro["\'];?\n?',
        '',
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

    if query in cache:
        print(f"⚡ Cache hit: {query}")
        return cache[query]

    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }

    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }

    async with session.get(url, params=params, headers=headers) as r:
        if r.status != 200:
            print(f"❌ Unsplash error: {r.status}")
            return None

        data = await r.json()

        if not data["results"]:
            print(f"❌ Sin resultados: {query}")
            return None

        photo = data["results"][0]

        cache[query] = photo
        save_cache()

        return photo

# ========================
# IMAGE
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

        # WEBP
        webp_name = f"{base_name}-{size}.webp"
        webp_path = os.path.join(folder, webp_name)

        if not os.path.exists(webp_path):
            copy.save(webp_path, "WEBP", quality=80)

        webp.append((webp_name, size))

        # AVIF (opcional)
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
    try:
        async with session.get(url, timeout=10) as r:
            if r.status != 200:
                return None
            return await r.read()
    except:
        return None

async def load_image(session, src, query=None):

    if src.startswith("http"):

        data = await fetch_image(session, src)

        if data:
            return Image.open(BytesIO(data))

        if query:
            photo = await search_unsplash(session, query)

            if photo:
                headers = {
                    "Authorization": f"Client-ID {ACCESS_KEY}"
                }

                await session.get(photo["links"]["download_location"], headers=headers)

                img_data = await fetch_image(session, photo["urls"]["raw"])

                if img_data:
                    return Image.open(BytesIO(img_data))

    else:
        full = os.path.join(ROOT_DIR, src.lstrip("/"))
        if os.path.exists(full):
            return Image.open(full)

    return None

# ========================
# COVER
# ========================

async def generate_cover_if_missing(session, base_name):

    name = f"{base_name}_cover"
    expected = os.path.join(IMG_DIR, f"{name}-1200.webp")

    if os.path.exists(expected):
        return

    query = clean_query(base_name)

    photo = await search_unsplash(session, query)

    if not photo:
        return

    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }

    await session.get(photo["links"]["download_location"], headers=headers)

    img_data = await fetch_image(session, photo["urls"]["raw"])

    if not img_data:
        return

    img = Image.open(BytesIO(img_data))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    generate_images(img, name, IMG_DIR)

# ========================
# PROCESS FILE
# ========================

async def process_file(session, path):

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if has_responsive_component(content):
        return

    base_name = slugify(os.path.splitext(os.path.basename(path))[0])

    await generate_cover_if_missing(session, base_name)

    md_images = extract_md_images(content)
    fm_image = extract_frontmatter_image(content)

    prefix = "/img"
    folder = IMG_DIR

    used_component = False

    # FRONTMATTER
    if fm_image:
        img = await load_image(session, fm_image, base_name)

        if img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            _, webp, _ = generate_images(img, f"{base_name}_cover", folder)

            if webp:
                fallback = f"{prefix}/{webp[-1][0]}"
                content = replace_frontmatter_image(content, fallback)

    # MARKDOWN
    for i, (alt, src) in enumerate(md_images):

        src = fix_broken_url(src)

        query = alt or base_name
        img = await load_image(session, src, query=query)

        if not img:
            continue

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        name = f"{base_name}_{i+1}"

        avif, webp, blur = generate_images(img, name, folder)

        component = f'''
<ResponsiveImage
  avif="{build_srcset(avif, prefix)}"
  webp="{build_srcset(webp, prefix)}"
  fallback="{prefix}/{webp[-1][0]}"
  alt="{alt}"
  blur="{blur}"
/>
'''

        content = content.replace(f"![{alt}]({src})", component)
        used_component = True

    content = add_import_if_needed(content, used_component)
    content = clean_unused_import(content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ========================
# MAIN
# ========================

async def process_posts():

    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = []

        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                if file.endswith((".md", ".mdx")):
                    path = os.path.join(root, file)
                    tasks.append(process_file(session, path))

        await asyncio.gather(*tasks)

    save_cache()

# ========================

if __name__ == "__main__":
    asyncio.run(process_posts())
