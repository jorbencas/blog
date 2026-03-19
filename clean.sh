#!/bin/bash

# Directorio de búsqueda
TARGET_DIR="./src"

echo "Iniciando limpieza de estilos en $TARGET_DIR..."

# 1. Eliminar efectos de Glassmorphism (blurs)
# Busca 'backdrop-blur-md', 'backdrop-blur-sm', 'backdrop-blur', etc.
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/backdrop-blur-[a-z0-4]\{1,2\}//g' {} +
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/backdrop-blur//g' {} +

# 2. Eliminar Bordes específicos que no quieres
# Esto quita las clases 'border', 'border-white/10', 'border-slate-200', etc.
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/border-white\/[0-9]\{1,2\}//g' {} +
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/border-slate-[0-9]\{3\}//g' {} +
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/border-cyan-500\/[0-9]\{2\}//g' {} +

# 3. Limpiar espacios dobles que hayan quedado tras borrar clases
find "$TARGET_DIR" -type f -name "*.astro" -exec sed -i 's/  */ /g' {} +

echo "Limpieza completada. Revisa tus componentes."