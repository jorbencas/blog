import os
import re
import json
import asyncio
import aiohttp
import base64
import hashlib
import unicodedata
import urllib.parse
from PIL import Image
from io import BytesIO

# ========================
# PATHS
# ========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

TARGET_DIR = os.path.join(ROOT_DIR, "src", "content")
IMG_DIR = os.path.join(ROOT_DIR, "public", "img")

CACHE_FILE = os.path.join(ROOT_DIR, "image_cache.json")

SIZES = [480, 768, 1200]

os.makedirs(IMG_DIR, exist_ok=True)

# ========================
# CACHE
# ========================

try:
    with open(CACHE_FILE, "r") as f:
        CACHE = json.load(f)
except:
    CACHE = {
        "url_map": {},   # url → base_name
        "hash_map": {}   # hash → base_name
    }

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f, indent=2)

# ========================
# HELPERS
# ========================

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\W_]+', '_', text.lower()).strip('_')

def hash_bytes(data):
    return hashlib.md5(data).hexdigest()

def build_unsplash_url(query):
    clean = re.sub(r'[^a-z0-9\s]', '', query.lower())
    clean = " ".join(clean.split()[:5])
    return f"https://source.unsplash.com/1600x900/?{urllib.parse.quote(clean)}"

def fallback_image():
    return "https://picsum.photos/1600/900"

def fix_url(src):
    if not src:
        return None

    if src.startswith("/img/http"):
        src = src.replace("/img/", "")

    if "github.com" in src and "/blob/" in src:
        src = src.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    return src

# ========================
# NETWORK
# ========================

async def fetch(session, url, retries=3):
    for i in range(retries):
        try:
            async with session.get(url, timeout=15) as r:
                if r.status == 200:
                    return await r.read()
        except:
            pass
        await asyncio.sleep(1)
    return None

# ========================
# IMAGE
# ========================

def generate_placeholder(img):
    small = img.copy()
    small.thumbnail((20, 20))
    buffer = BytesIO()
    small.save(buffer, format="JPEG", quality=30)
    return base64.b64encode(buffer.getvalue()).decode()

def generate_images(img, base_name):
    webp = []
    avif = []

    for size in SIZES:
        copy = img.copy()
        copy.thumbnail((size, size))

        w_name = f"{base_name}-{size}.webp"
        w_path = os.path.join(IMG_DIR, w_name)

        if not os.path.exists(w_path):
            copy.save(w_path, "WEBP", quality=80)

        webp.append((w_name, size))

        try:
            a_name = f"{base_name}-{size}.avif"
            a_path = os.path.join(IMG_DIR, a_name)

            if not os.path.exists(a_path):
                copy.save(a_path, "AVIF", quality=50)

            avif.append((a_name, size))
        except:
            pass

    return avif, webp, generate_placeholder(img)

def build_srcset(data):
    return ", ".join([f"/img/{n} {s}w" for n, s in data])

# ========================
# CORE CACHE LOGIC
# ========================

async def get_or_create_image(session, url, base_name):

    url = fix_url(url)

    # 🔁 URL cache
    if url in CACHE["url_map"]:
        print(f"⚡ Cache URL hit: {url}")
        return CACHE["url_map"][url]

    data = await fetch(session, url)

    if not data:
        print("⚠️ fallback")
        data = await fetch(session, build_unsplash_url(base_name))

    if not data:
        data = await fetch(session, fallback_image())

    if not data:
        print("💀 fallo total imagen")
        return None

    h = hash_bytes(data)

    # 🔁 HASH cache (deduplicación)
    if h in CACHE["hash_map"]:
        print(f"♻️ Imagen duplicada detectada")
        base = CACHE["hash_map"][h]
        CACHE["url_map"][url] = base
        return base

    # 🆕 nueva imagen
    img = Image.open(BytesIO(data))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    generate_images(img, base_name)

    CACHE["url_map"][url] = base_name
    CACHE["hash_map"][h] = base_name

    return base_name

# ========================
# PROCESS FILE
# ========================

async def process_file(session, path):
    print(f"\n📄 {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(path)
    base = slugify(os.path.splitext(filename)[0])

    title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
    title = title_match.group(1) if title_match else base

    fm_match = re.search(r'image:\s*["\']?(.*?)["\']?\n', content)
    fm_img = fm_match.group(1) if fm_match else None

    if not fm_img:
        fm_img = build_unsplash_url(title)

    base_img = await get_or_create_image(session, fm_img, f"{base}_cover")

    if not base_img:
        return

    fallback = f"/img/{base_img}-1200.webp"

    content = re.sub(
        r'image:\s*["\']?(.*?)["\']?\n',
        f'image: "{fallback}"\n',
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ OK → {path}")

# ========================
# MAIN
# ========================

async def main():
    print("🚀 CACHE + DEDUP MODE\n")

    connector = aiohttp.TCPConnector(limit=3)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for root, _, files in os.walk(TARGET_DIR):
            for f in files:
                if f.endswith((".md", ".mdx")):
                    tasks.append(process_file(session, os.path.join(root, f)))

        await asyncio.gather(*tasks)

    save_cache()
    print("\n🔥 DONE (cache optimizada)")

if __name__ == "__main__":
    asyncio.run(main())