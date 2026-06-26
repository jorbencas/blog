import os
import json
import re
import random
import asyncio
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from google import genai
from slugify import slugify

from scripts.constants_retos import (
    CONFIG,
    WEBS_RETOS,
    RETO_MD_TEMPLATE,
    PROMPT_IMAGEN_TEMPLATE_RETO
)
from scripts.utils_retos import obtener_solucion_ia, generar_imagen_noticia, traducir_titulos_ia
from scripts.solutions_db import lookup as db_lookup, generate_generic

logger = logging.getLogger("scraper")


def clean_challenges(folder="./auto-challenges"):
    print(f"Limpiando {folder}...")
    if not os.path.exists(folder): return

    archivos = [f for f in os.listdir(folder) if f.endswith(('.md', '.mdx'))]
    borrados = 0
    titulos_vistos = set()

    for archivo in archivos:
        path = os.path.join(folder, archivo)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if len(content) < 300 or "{codigo_solucion}" in content or "{lenguaje_lower}" in content:
                os.remove(path)
                borrados += 1
                continue

            match = re.search(r'title:\s*["\'](.*?)["\']', content)
            if match:
                titulo = match.group(1).replace("RETO: ", "").lower().strip()
                if titulo in titulos_vistos:
                    os.remove(path)
                    borrados += 1
                    continue
                titulos_vistos.add(titulo)

            if "```" not in content:
                os.remove(path)
                borrados += 1
        except Exception as e:
            print(f"Error limpiando {archivo}: {e}")

    print(f"Se eliminaron {borrados} archivos.")


async def generar_retos_ia_puros(client, folder):
    if not client:
        print("Modo offline activo. No se pueden generar retos creativos con IA.")
        return []

    print("No se encontraron retos nuevos. Activando generación creativa de IA...")
    lenguajes = ["Svelte", "Python (FastAPI/Django)", "Go", "C#", "Astro (JS/TS)"]
    retos_generados = []

    for idx, lang in enumerate(lenguajes):
        try:
            prompt_inventar = f"""
            Eres un creador de retos de programación. Inventa un título atractivo para un reto técnico en {lang}.

            REQUISITOS:
            - El reto debe resolverse en ~30-60 minutos
            - Debe tener aplicación en el mundo real (no solo algoritmia abstracta)
            - El título debe ser descriptivo pero conciso (max 10 palabras)
            - Evita: "Calculadora de...", "Hola Mundo", ejercicios de clase repetidos
            - Prefiere: procesamiento de datos, APIs, automatización, parsing, optimización

            Responde SOLO el título, sin explicaciones ni formato.
            """
            modelo_actual = (CONFIG.get("AI_MODELS") or ["gemini-2.5-flash"])[0]
            res_titulo = await asyncio.to_thread(
                client.models.generate_content,
                model=modelo_actual,
                contents=prompt_inventar
            )
            titulo_inventado = res_titulo.text.strip()

            if await solve_and_save(titulo_inventado, "IA Creativa", client, folder, index_hint=idx):
                retos_generados.append(titulo_inventado)
                print(f"Reto IA Generado ({lang}): {titulo_inventado}")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"Error generando reto IA para {lang}: {e}")

    return retos_generados


CODEEMBER_LANGS = [
    ("python", "Python"),
    ("javascript", "JavaScript"),
    ("typescript", "TypeScript"),
    ("go", "Go"),
    ("rust", "Rust"),
    ("java", "Java"),
    ("csharp", "C#"),
    ("kotlin", "Kotlin"),
    ("swift", "Swift"),
    ("php", "PHP"),
    ("ruby", "Ruby"),
    ("dart", "Dart"),
]

async def solve_and_save(titulo, fuente, client, folder, difficulty_override=None, index_hint=0):
    print(f"Procesando: {titulo}")

    week_seed = datetime.now().isocalendar()[1]
    rng = random.Random(week_seed)
    langs_shuffled = list(CODEEMBER_LANGS)
    rng.shuffle(langs_shuffled)
    lang_id, lang_display = langs_shuffled[index_hint % len(langs_shuffled)]

    sol = db_lookup(titulo, lang_id)
    if sol:
        print(f"   Solución local encontrada ({lang_display}), sin llamada a IA")
    else:
        if client:
            sol = await obtener_solucion_ia(titulo, fuente, client, lang=lang_display)

        if not sol:
            print(f"   IA falló o modo offline. Usando código genérico ({lang_display})")
            sol = generate_generic(titulo, lang_id)

    if sol:
        titulo_es = sol.get('titulo', titulo)
        slug = f"reto-{slugify(titulo_es)[:40]}"
        path = os.path.join(folder, f"{slug}.mdx")

        img_url = ""
        if client:
            img_url = await generar_imagen_noticia(titulo_es, client, prompt_template=PROMPT_IMAGEN_TEMPLATE_RETO)

        dificultad = difficulty_override or sol.get('dificultad', 'Intermedio')

        taxonomia = {
            "Fácil": "Iniciación", "Iniciación": "Iniciación", "Junior": "Iniciación",
            "Intermedio": "Intermedio", "Medio": "Intermedio", "Mid": "Intermedio",
            "Difícil": "Avanzado", "Avanzado": "Avanzado", "Senior": "Avanzado"
        }
        dificultad_blog = taxonomia.get(dificultad, "Intermedio")
        tags_seo = json.dumps([lang_id, 'retos', dificultad_blog.lower()])

        try:
            test_cases = sol.get('test_cases', 'entrada_ejemplo | salida_ejemplo')
            tabla_casos = '\n'.join(
                f'| `{c.split("|")[0].strip()}` | `{c.split("|")[1].strip()}` |'
                for c in test_cases.split(';') if '|' in c
            ) or '| `ejemplo` | `resultado` |'

            res = RETO_MD_TEMPLATE.format(
                titulo=titulo_es.replace('"', "'"),
                resumen_corto=sol.get('descripcion', '')[:140].replace('"', "'"),
                fecha_pub=datetime.now().strftime("%Y-%m-%d"),
                slug_name=slug,
                tags_seo=tags_seo,
                descripcion_ia=sol.get('descripcion', ''),
                ruta_imagen=img_url,
                dificultad=dificultad_blog,
                paso_1=sol.get('paso1', ''),
                paso_2=sol.get('paso2', ''),
                paso_3=sol.get('paso3', ''),
                big_o_time=sol.get('big_o_time', 'O(n)'),
                big_o_space=sol.get('big_o_space', 'O(n)'),
                tabla_casos=tabla_casos,
                lenguaje_lower=lang_id,
                lenguaje_display=lang_display,
                codigo_solucion=sol.get('codigo', '')
            )

            await asyncio.to_thread(lambda: open(path, "w", encoding="utf-8").write(res))
            return True
        except KeyError as e:
            print(f"Error de formato en el Template: Olvidaste escapar una llave en tu constante: {e}")
            return False
    return False


async def hunt(offline=False):
    folder = CONFIG.get("CHALLENGES_DIR", "../src/content/auto-challenges")
    os.makedirs(folder, exist_ok=True)

    api_key = CONFIG.get("GEMINI_KEY")
    if not api_key:
        print("Sin API KEY. Entrando en modo Estático/Offline...")
        offline = True

    client = genai.Client(api_key=api_key) if not offline else None
    retos_nuevos = []

    if offline:
        print("Modo Offline: El script solo buscará soluciones en la base de datos local (solutions_db.py).")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    reto_idx = 0

    for nombre, config in WEBS_RETOS.items():
        try:
            print(f"Buscando en: {nombre}...")

            r = await asyncio.to_thread(
                lambda: requests.get(config["url"], timeout=15, headers=headers)
            )

            if r.status_code != 200: continue

            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.select(config["selector"])[:5]

            items_validos = []
            for i in items:
                t_raw = i.get_text(strip=True)
                if len(t_raw) >= 5:
                    items_validos.append({"obj": i, "titulo": t_raw})

            if items_validos and not offline and client:
                logger.info(f"Traduciendo {len(items_validos)} títulos de {nombre}...")
                items_validos = await traducir_titulos_ia(items_validos, client)

            for item_data in items_validos:
                titulo_es = item_data["titulo"]
                if await solve_and_save(titulo_es, nombre, client, folder, index_hint=reto_idx):
                    retos_nuevos.append(titulo_es)
                    reto_idx += 1
                    await asyncio.sleep(5)
        except Exception as e:
            print(f"Error en {nombre}: {e}")

    if not retos_nuevos and not offline and client:
        retos_nuevos = await generar_retos_ia_puros(client, folder)

    if retos_nuevos:
        print(f"{len(retos_nuevos)} nuevos retos.")

    clean_challenges(folder)


if __name__ == "__main__":
    import sys
    is_offline = "--offline" in sys.argv
    asyncio.run(hunt(offline=is_offline))
