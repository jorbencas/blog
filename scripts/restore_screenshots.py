"""Restore and optimize flat screenshot files from beaa52e into subdirectories."""
import sys
sys.path.insert(0, '.')
from pathlib import Path
from PIL import Image
from scripts.fix_images import compress_and_save_adaptive

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "img"

# Map: (original_flat_file, slug_subdir, image_number)
# image_number is used for naming (e.g., slug_1, slug_2...)
entries = [
    ("arquitectura_web.webp", "arquitectura_web", "arquitectura_web", None),
    ("conectarse_del_cliente_al_servidor_mediante_ssh_1.png", "conectarse_del_cliente_al_servidor_mediante_ssh", "conectarse_del_cliente_al_servidor_mediante_ssh_1", 1),
    ("conectarse_del_cliente_al_servidor_mediante_ssh_2.png", "conectarse_del_cliente_al_servidor_mediante_ssh", "conectarse_del_cliente_al_servidor_mediante_ssh_2", 2),
    ("conectarse_del_cliente_al_servidor_mediante_ssh_3.png", "conectarse_del_cliente_al_servidor_mediante_ssh", "conectarse_del_cliente_al_servidor_mediante_ssh_3", 3),
    ("conexion_ssh_mediante_clave_publica_privada_1.png", "conexion_ssh_mediante_clave_publica_privada", "conexion_ssh_mediante_clave_publica_privada_1", 1),
    ("conexion_ssh_mediante_clave_publica_privada_2.png", "conexion_ssh_mediante_clave_publica_privada", "conexion_ssh_mediante_clave_publica_privada_2", 2),
    ("copiar_archivos_entre_diferentes_usuarios_y_archivos.png", "copiar_archivos_entre_diferentes_usuarios_y_archivos", "copiar_archivos_entre_diferentes_usuarios_y_archivos_1", 1),
    ("instalacion-y-configuracion-dhcp_1.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_1", 1),
    ("instalacion-y-configuracion-dhcp_2.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_2", 2),
    ("instalacion-y-configuracion-dhcp_3.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_3", 3),
    ("instalacion-y-configuracion-dhcp_4.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_4", 4),
    ("instalacion-y-configuracion-dhcp_5.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_5", 5),
    ("instalacion-y-configuracion-dhcp_6.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_6", 6),
    ("instalacion-y-configuracion-dhcp_7.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_7", 7),
    ("instalacion-y-configuracion-dhcp_8.png", "instalacion_y_configuracion_dhcp", "instalacion_y_configuracion_dhcp_8", 8),
]

formas_md = [
    ("formas_de_conerse_por_ssh.webp", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_1", None),
    ("formas_de_conerse_por_ssh_1.webp", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_2", None),
    ("formas_de_conerse_por_ssh_2.webp", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_3", None),
    ("formas_de_conerse_por_ssh_3.webp", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_4", None),
    ("formas_de_conectarse_con_ssh.png", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_5", None),
    ("formas_de_conectarse_con_ssh_1.png", "formas_de_conectarse_por_ssh", "formas_de_conectarse_por_ssh_6", None),
]

import pillow_avif  # noqa

for flat_name, slug, new_base, num in entries + formas_md:
    src = IMG / flat_name
    if not src.exists():
        print(f"❌ {flat_name} not found")
        continue
    folder = IMG / slug
    folder.mkdir(parents=True, exist_ok=True)
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    avif, webp, blur = compress_and_save_adaptive(img, new_base, folder)
    prefix = f"/img/{slug}"
    print(f"✅ {flat_name} → {prefix}/{new_base}-{{{','.join(str(s) for _,s in webp)}}}w")
    # Delete original flat file after optimization
    src.unlink()

print("\nDone!")
