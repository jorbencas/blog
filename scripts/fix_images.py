import os
import re
import requests

# CONFIGURACIÓN
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
TARGET_DIR = "src/content/*"
OLD_IMAGE = "public/img/arquitectura_web.webp"

def get_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query},tech&orientation=landscape&client_id={ACCESS_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()['urls']['regular']
    except: return None
    return None

def enhance_metadata(content, title):
    # 1. Autogenerar tags si hay pocos
    tags_match = re.search(r'tags:\s*\[(.*?)\]', content)
    if tags_match:
        current_tags = [t.strip().replace('"', '').replace("'", "") for t in tags_match.group(1).split(',')]
        if len(current_tags) < 3:
            # Añadimos tags genéricos basados en palabras del título
            extra_tags = ["tech", "innovation", "development"]
            new_tags = list(set(current_tags + extra_tags))
            content = content.replace(f"tags: [{tags_match.group(1)}]", f"tags: {str(new_tags)}")

    # 2. Arreglar descripción si es muy genérica o corta
    desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\n', content)
    if desc_match and len(desc_match.group(1)) < 30:
        new_desc = f"Análisis profundo sobre {title}. Descubre las últimas novedades en el ecosistema tecnológico."
        content = content.replace(desc_match.group(1), new_desc)
    
    return content

def process_posts():
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".md") or filename.endswith(".mdx"):
            path = os.path.join(TARGET_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
            title = title_match.group(1) if title_match else "technology"

            # Mejorar metadatos (Tags y Desc)
            content = enhance_metadata(content, title)

            # Cambiar imagen si es la repetida
            if OLD_IMAGE in content:
                new_img = get_unsplash_image(title)
                if new_img:
                    content = content.replace(OLD_IMAGE, new_img)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    process_posts()
