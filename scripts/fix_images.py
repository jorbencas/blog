import os
import re
import json
import requests
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO

# CONFIG
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, "src", "content")
IMG_DIR = os.path.join(BASE_DIR, "public", "img")

CACHE_FILE = os.path.join(BASE_DIR, "unsplash_cache.json")

SIZES = [480, 768, 1200]

os.makedirs(IMG_DIR, exist_ok=True)

# ------------------------
# CACHE
# ------------------------

try:
    with open(CACHE_FILE, "r") as f:
        unsplash_cache = json.load(f)
except:
    unsplash_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(unsplash_cache, f, indent=2)

# ------------------------
# HELPERS
# ------------------------

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)

def get_post_folder(base_name, multiple):
    if multiple:
        folder = os.path.join(IMG_DIR, base_name)
        os.makedirs(folder, exist_ok=True)
        return folder, f"/img/{base_name}"
    return IMG_DIR, "/img"

# ------------------------
# UNSPLASH
# ------------------------

def get_unsplash_image(query):
    if query in unsplash_cache:
        return unsplash_cache[query]

    url = f"https://api.unsplash.com/photos/random?query={query},tech&client_id={ACCESS_KEY}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            img_url = r.json()['urls']['regular']
            unsplash_cache[query] = img_url
            return img_url
    except:
        pass

    return None

# ------------------------
# IMÁGENES
# ------------------------

def generate_responsive(img, base_name, folder):
    outputs = []

    for size in SIZES:
        filename = f"{base_name}-{size}.webp"
        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            copy = img.copy()
            copy.thumbnail((size, size))
            copy.save(path, "WEBP", quality=80)

        outputs.append((filename, size))

    return outputs

def process_image(url_or_path, base_name, folder):
    try:
        if url_or_path.startswith("http"):
            r = requests.get(url_or_path, timeout=10)
            if r.status_code != 200:
                return None
            img = Image.open(BytesIO(r.content))
        else:
            full = os.path.join(BASE_DIR, url_or_path.lstrip("/"))
            if not os.path.exists(full):
                return None
            img = Image.open(full)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        return generate_responsive(img, base_name, folder)

    except:
        return None

# ------------------------
# MARKDOWN
# ------------------------

def extract_md_images(content):
    return re.findall(r'!\[.*?\]\((.*?)\)', content)

def replace_md_image(content, old, new):
    return content.replace(old, new)

def build_src(images, prefix):
    return f"{prefix}/{images[-1][0]}"

# ------------------------
# MAIN
# ------------------------

def process_posts():
    tasks = []

    with ThreadPoolExecutor(max_workers=5) as executor:

        for root, _, files in os.walk(TARGET_DIR):
            for file in files:

                if not file.endswith((".md", ".mdx")):
                    continue

                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                base_name = slugify(os.path.splitext(file)[0])

                md_images = extract_md_images(content)
                multiple = len(md_images) > 1

                folder, prefix = get_post_folder(base_name, multiple)

                def task(content=content, path=path):

                    new_content = content

                    for i, img in enumerate(md_images):

                        name = f"{base_name}_{i+1}" if multiple else base_name

                        images = process_image(img, name, folder)

                        if images:
                            new_path = f"{prefix}/{images[-1][0]}"
                            new_content = replace_md_image(new_content, img, new_path)

                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                tasks.append(executor.submit(task))

        for f in as_completed(tasks):
            f.result()

    save_cache()


if __name__ == "__main__":
    process_posts()