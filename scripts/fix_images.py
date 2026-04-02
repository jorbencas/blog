import os
import re
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

SIZES = [480, 768, 1200]

os.makedirs(IMG_DIR, exist_ok=True)

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

def clean_imports(content):
    if "<ResponsiveImage" not in content:
        return re.sub(
            r'import\s+ResponsiveImage.*\n',
            '',
            content
        )
    if "import ResponsiveImage" not in content:
        content = f'import ResponsiveImage from "@components/ResponsiveImage.astro";\n\n{content}'
    return content

# ========================
# URL FIXES
# ========================

def fix_url(src):
    if not src:
        return None

    # 🔥 /img/https:// → arreglar
    if src.startswith("/img/http"):
        src = src.replace("/img/", "")

    # 🔥 github blob → raw
    if "github.com" in src and "/blob/" in src:
        src = src.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    return src

def is_local(src):
    return src and src.startswith("/img/")

def local_exists(src):
    full = os.path.join(ROOT_DIR, src.lstrip("/"))
    return os.path.exists(full)

# ========================
# IMAGE
# ========================

async def fetch(session, url):
    try:
        async with session.get(url, timeout=15) as r:
            if r.status != 200:
                print(f"❌ HTTP {r.status} → {url}")
                return None
            return await r.read()
    except Exception as e:
        print(f"❌ Error descarga: {e}")
        return None

async def load_image(session, src):
    if not src:
        return None

    src = fix_url(src)

    if src.startswith("http"):
        print(f"🌐 Descargando: {src}")
        data = await fetch(session, src)
        if not data:
            return None
        return Image.open(BytesIO(data))

    if is_local(src):
        full = os.path.join(ROOT_DIR, src.lstrip("/"))
        if os.path.exists(full):
            print(f"📂 Cargando local: {full}")
            return Image.open(full)

    return None

def placeholder(img):
    small = img.copy()
    small.thumbnail((20, 20))
    buffer = BytesIO()
    small.save(buffer, format="JPEG", quality=30)
    return base64.b64encode(buffer.getvalue()).decode()

def generate(img, name, folder):
    os.makedirs(folder, exist_ok=True)

    avif = []
    webp = []
    blur = placeholder(img)

    for s in SIZES:
        w_name = f"{name}-{s}.webp"
        w_path = os.path.join(folder, w_name)

        copy = img.copy()
        copy.thumbnail((s, s))
        copy.save(w_path, "WEBP", quality=80)

        webp.append((w_name, s))

        try:
            a_name = f"{name}-{s}.avif"
            a_path = os.path.join(folder, a_name)
            copy.save(a_path, "AVIF", quality=50)
            avif.append((a_name, s))
        except:
            pass

    return avif, webp, blur

def srcset(data, prefix):
    return ", ".join([f"{prefix}/{n} {s}w" for n, s in data])

# ========================
# CORE
# ========================

async def process_file(session, path):
    print(f"\n📄 {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(path)
    is_md = filename.endswith(".md")

    new_path = path.replace(".md", ".mdx") if is_md else path

    base = slugify(os.path.splitext(filename)[0])

    title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
    title = title_match.group(1) if title_match else base

    md_imgs = extract_md_images(content)
    fm_img = extract_frontmatter_image(content)

    total = len(md_imgs) + (1 if fm_img else 0)

    if total == 0:
        print("⚠️ Sin imágenes → fallback Unsplash")
        fm_img = f"https://source.unsplash.com/1600x900/?{title}"
        content = content.replace("---", f"---\nimage: \"{fm_img}\"", 1)
        total = 1

    folder = IMG_DIR if total == 1 else os.path.join(IMG_DIR, base)
    prefix = "/img" if total == 1 else f"/img/{base}"

    # ========================
    # FRONTMATTER
    # ========================

    if fm_img:
        fm_img = fix_url(fm_img)

        if is_local(fm_img) and not local_exists(fm_img):
            print("♻️ Imagen rota → regenerar")
            fm_img = f"https://source.unsplash.com/1600x900/?{title}"

        img = await load_image(session, fm_img)

        if not img:
            print("⚠️ Fallback Unsplash")
            img = await load_image(session, f"https://source.unsplash.com/1600x900/?{title}")

        if img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            _, webp, _ = generate(img, f"{base}_cover", folder)
            fallback = f"{prefix}/{webp[-1][0]}"

            content = replace_frontmatter_image(content, fallback)

    # ========================
    # MARKDOWN
    # ========================

    for i, (alt, src) in enumerate(md_imgs):
        src = fix_url(src)

        img = await load_image(session, src)

        if not img:
            print("⚠️ fallback markdown → Unsplash")
            img = await load_image(session, f"https://source.unsplash.com/800x600/?{title}")

        if not img:
            continue

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        name = f"{base}_{i+1}" if total > 1 else base

        avif, webp, blur = generate(img, name, folder)

        comp = f"""
<ResponsiveImage
  avif="{srcset(avif, prefix)}"
  webp="{srcset(webp, prefix)}"
  fallback="{prefix}/{webp[-1][0]}"
  alt="{alt}"
  blur="{blur}"
/>
"""

        content = content.replace(f"![{alt}]({src})", comp)

    content = clean_imports(content)

    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)

    if is_md:
        os.remove(path)

    print(f"✅ OK → {new_path}")

# ========================
# MAIN
# ========================

async def main():
    print("🚀 REPAIR MODE ACTIVADO\n")

    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for root, _, files in os.walk(TARGET_DIR):
            for f in files:
                if f.endswith((".md", ".mdx")):
                    tasks.append(process_file(session, os.path.join(root, f)))

        await asyncio.gather(*tasks)

    print("\n🔥 TODO REPARADO")

if __name__ == "__main__":
    asyncio.run(main())