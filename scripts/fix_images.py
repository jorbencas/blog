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
    print(f"🖼️ Generando imágenes para: {base_name}")

    avif = []
    webp = []
    blur = generate_placeholder(img)

    os.makedirs(folder, exist_ok=True)

    for size in SIZES:
        try:
            webp_name = f"{base_name}-{size}.webp"
            webp_path = os.path.join(folder, webp_name)

            if not os.path.exists(webp_path):
                copy = img.copy()
                copy.thumbnail((size, size))
                copy.save(webp_path, "WEBP", quality=80)
                print(f"   ✅ WEBP creado: {webp_path}")
            else:
                print(f"   ⚡ WEBP ya existe: {webp_path}")

            webp.append((webp_name, size))

        except Exception as e:
            print(f"   ❌ Error WEBP ({size}): {e}")

        # ⚠️ AVIF puede fallar
        try:
            avif_name = f"{base_name}-{size}.avif"
            avif_path = os.path.join(folder, avif_name)

            if not os.path.exists(avif_path):
                copy = img.copy()
                copy.thumbnail((size, size))
                copy.save(avif_path, "AVIF", quality=50)
                print(f"   ✅ AVIF creado: {avif_path}")

            avif.append((avif_name, size))

        except Exception as e:
            print(f"   ⚠️ AVIF no soportado: {e}")

    return avif, webp, blur

async def fetch_image(session, url):
    print(f"🌐 Descargando: {url}")
    try:
        async with session.get(url, timeout=10) as r:
            if r.status != 200:
                print(f"❌ HTTP {r.status} en {url}")
                return None
            return await r.read()
    except Exception as e:
        print(f"❌ Error descargando {url}: {e}")
        return None

async def load_image(session, src):
    try:
        if src.startswith("http"):
            data = await fetch_image(session, src)
            if not data:
                print(f"❌ No se pudo descargar: {src}")
                return None
            print(f"✅ Imagen descargada")
            return Image.open(BytesIO(data))
        else:
            full = os.path.join(ROOT_DIR, src.lstrip("/"))
            if not os.path.exists(full):
                print(f"❌ No existe local: {full}")
                return None
            print(f"📂 Cargando local: {full}")
            return Image.open(full)
    except Exception as e:
        print(f"❌ Error cargando imagen {src}: {e}")
        return None

def build_srcset(images, prefix):
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in images])

# ========================
# PROCESS FILE
# ========================

async def process_file(session, old_path):

    print(f"\n📄 Procesando: {old_path}")

    file = os.path.basename(old_path)
    is_md = file.endswith(".md")

    new_filename = file.replace(".md", ".mdx") if is_md else file
    new_path = os.path.join(os.path.dirname(old_path), new_filename)

    with open(old_path, "r", encoding="utf-8") as f:
        content = f.read()

    if has_responsive_component(content):
        print("⚡ Ya procesado, skip")
        return

    base_name = slugify(os.path.splitext(new_filename)[0])

    md_images = extract_md_images(content)
    fm_image = extract_frontmatter_image(content)

    total_images = len(md_images) + (1 if fm_image else 0)
    print(f"🔍 Imágenes detectadas: {total_images}")

    if total_images == 0:
        print("⚠️ Sin imágenes")
        if is_md:
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(content)
            os.remove(old_path)
        return

    multiple = total_images > 1

    folder = IMG_DIR
    prefix = "/img"

    if multiple:
        folder = os.path.join(IMG_DIR, base_name)
        prefix = f"/img/{base_name}"

    used_component = False

    # FRONTMATTER
    if fm_image:
        print(f"🖼️ Frontmatter image: {fm_image}")

        img = await load_image(session, fm_image)

        if img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            _, webp, _ = generate_images(img, f"{base_name}_cover", folder)

            if webp:
                fallback = f"{prefix}/{webp[-1][0]}"
                content = replace_frontmatter_image(content, fallback)
                print(f"✅ Frontmatter actualizado: {fallback}")
            else:
                print("❌ No se generaron imágenes")

    # MARKDOWN
    for i, (alt, src) in enumerate(md_images):
        print(f"🖼️ Markdown image: {src}")

        img = await load_image(session, src)
        if not img:
            continue

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        name = f"{base_name}_{i+1}" if multiple else base_name

        avif, webp, blur = generate_images(img, name, folder)

        if not webp:
            print("❌ No se generaron imágenes markdown")
            continue

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

    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)

    if is_md:
        os.remove(old_path)

    print(f"✅ Guardado: {new_path}")

# ========================
# MAIN
# ========================

async def process_posts():

    print("🚀 Iniciando procesamiento...\n")

    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = []

        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                if not file.endswith((".md", ".mdx")):
                    continue

                path = os.path.join(root, file)
                tasks.append(process_file(session, path))

        await asyncio.gather(*tasks)

    save_cache()
    print("\n✅ DONE")

# ========================

if __name__ == "__main__":
    asyncio.run(process_posts())