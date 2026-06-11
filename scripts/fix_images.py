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
GEMINI_KEY = os.getenv("GEMINI_API_KEY") # Shared key for AI conceptualization

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
    if not ACCESS_KEY:
        return None

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
        "Authorization": f"Client-ID {ACCESS_KEY}",
        "User-Agent": "AstroBlogImageFixer/1.0"
    }

    try:
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
    except Exception as e:
        print(f"⚠️ Unsplash request error: {e}")
        return None

def generate_local_banner(title, theme=None):
    try:
        width, height = 1200, 630
        
        # Default theme
        c1 = theme.get("color1", "#1a1a2e") if theme else "#1a1a2e"
        c2 = theme.get("color2", "#16213e") if theme else "#16213e"
        
        # Create gradient background
        base = Image.new('RGB', (width, height), c1)
        top = Image.new('RGB', (width, height), c2)
        mask = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                mask.putpixel((x, y), int(255 * (x / width)))
        
        img = Image.composite(base, top, mask)
        draw = ImageDraw.Draw(img)
        
        # Draw simple tech patterns (dots)
        for _ in range(200):
            x, y = random.randint(0, width), random.randint(0, height)
            draw.ellipse([x, y, x+2, y+2], fill="#ffffff22")

        # Text rendering
        try:
            # Preferred fonts on Linux
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
            ]
            font = None
            for p in font_paths:
                if os.path.exists(p):
                    font = ImageFont.truetype(p, 60)
                    break
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Draw centered text
        text = title.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width-tw)/2, (height-th)/2), text, font=font, fill="white")
        
        # Add branding
        try:
            small_font = ImageFont.truetype(font_paths[0], 24) if os.path.exists(font_paths[0]) else font
            draw.text((50, height-60), "BLOG RETOS", font=small_font, fill="#ffffff88")
        except:
            pass

        return img
    except Exception as e:
        print(f"⚠️ Error generating local banner: {e}")
        # Final emergency fallback: open default image
        try:
            return Image.open(os.path.join(ROOT_DIR, "public", DEFAULT_IMAGE.lstrip("/")))
        except:
            return None

async def search_all_providers(session, query):
    # 1. Unsplash
    photo = await search_unsplash(session, query)
    if photo:
        return {"url": photo["urls"]["raw"], "source": "unsplash", "data": photo}

    # 2. Local Generation (Conceptualized by Gemini if possible)
    print(f"🎨 Generating local creative banner for: {query}")
    theme = get_gemini_theme(query)
    
    return {
        "source": "local_gen",
        "title": query,
        "theme": theme
    }

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with session.get(url, headers=headers, timeout=15) as r:
            if r.status != 200:
                print(f"⚠️ Failed to fetch image: {url} (Status: {r.status})")
                return None
            return await r.read()
    except Exception as e:
        print(f"❌ Error fetching {url}: {str(e)}")
        return None

async def load_image(session, src, query=None):

    if src.startswith("http"):

        data = await fetch_image(session, src)

        if data:
            try:
                return Image.open(BytesIO(data))
            except Exception as e:
                print(f"❌ Error decoding image from {src}: {str(e)}")
                return None

        if query:
            result = await search_all_providers(session, query)

            if result:
                if result["source"] == "local_gen":
                    return generate_local_banner(result["title"], result["theme"])
                
                img_data = await fetch_image(session, result["url"])

                if img_data:
                    try:
                        return Image.open(BytesIO(img_data))
                    except Exception as e:
                        print(f"❌ Error decoding image from {result['source']}: {str(e)}")
                        return None

    else:
        full = os.path.join(ROOT_DIR, src.lstrip("/"))
        if os.path.exists(full):
            try:
                return Image.open(full)
            except Exception as e:
                print(f"❌ Error opening local image {full}: {str(e)}")
                return None

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

    result = await search_all_providers(session, query)

    if not result:
        return

    if result["source"] == "local_gen":
        img = generate_local_banner(result["title"], result["theme"])
    else:
        img_data = await fetch_image(session, result["url"])
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

    base_name = slugify(os.path.splitext(os.path.basename(path))[0])
    
    # We always check the file now to ensure all images (FM and MD) exist.
    await generate_cover_if_missing(session, base_name)

    md_images = extract_md_images(content)
    fm_image = extract_frontmatter_image(content)

    prefix = "/img"
    folder = IMG_DIR

    used_component = False

    # FRONTMATTER
    if fm_image:
        fm_image = fix_broken_url(fm_image)
        img = await load_image(session, fm_image, base_name)

        if img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            _, webp, _ = generate_images(img, f"{base_name}_cover", folder)

            if webp:
                fallback = f"{prefix}/{webp[-1][0]}"
                content = replace_frontmatter_image(content, fallback)
        else:
            # Fallback for frontmatter
            content = replace_frontmatter_image(content, DEFAULT_IMAGE)

    # MARKDOWN
    for i, (alt, original_src) in enumerate(md_images):

        src = fix_broken_url(original_src)

        query = alt or base_name
        img = await load_image(session, src, query=query)

        if not img:
            # If we fixed a broken URL, or if it's completely missing, use the default image
            replacement = f"![{alt}]({DEFAULT_IMAGE})"
            content = content.replace(f"![{alt}]({original_src})", replacement)
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
