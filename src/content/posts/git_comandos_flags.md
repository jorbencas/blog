---
draft: false
title: "📕 Manual Maestro de Git: Flags y Comandos consolidado"
description: "Diccionario Consolidado de Comandos y Flags de Git con estrategias de limpieza y configuración global."
pubDate: "2026/03/10"
tags: ['git', 'terminal', 'desarrollo']
image: "/img/git_comandos_flags.png"
author: "Jorge Beneyto Castelló"
layout: "@layouts/PostLayout.astro"
---

## 1. Clonado y Configuración (Obtener proyectos)
* **`git clone`**:
    * `--depth <N>`: **Shallow clone**. Solo descarga los últimos N commits (ideal para ahorrar espacio y tiempo).
    * `--branch <nombre>` (`-b`): Clona una rama específica.
    * `--single-branch`: Descarga solo la rama indicada y no el resto de ramas del servidor.
    * `--filter=blob:none`: **Blobless clone**. Baja el historial pero no el contenido de archivos viejos hasta que los pidas.
    * `--recurse-submodules`: Clona el repo y todos sus submódulos automáticamente.
    * `--sparse`: Habilita el checkout parcial (para ver solo ciertas carpetas en monorepos).

---

## 2. Gestión de Cambios (El día a día)
* **`git commit`**:
    * `-m "mensaje"`: Añade el mensaje sin abrir el editor de texto.
    * `-a` (`--all`): Stage automático de archivos modificados/borrados (no incluye nuevos).
    * `--amend`: Edita el último commit (cambia el mensaje o añade archivos olvidados).
    * `--no-verify`: Salta los checks automáticos (hooks) de pre-commit.
    * `--reset-author`: Cambia la autoría del commit corregido al usuario actual.
    * `--date="now"`: Actualiza la marca de tiempo del commit.

* **`git diff`**:
    * `--staged` o `--cached`: Compara el stage contra el último commit.
    * `--stat`: Resumen numérico de líneas cambiadas por archivo.
    * `--name-only`: Muestra únicamente los nombres de los archivos afectados.
    * `-w`: Ignora cambios de espacios en blanco al comparar.

* **`git stash` (Guardado temporal)**:
    * `push -m "nombre"`: Guarda cambios actuales en una pila temporal.
    * `pop`: Recupera los cambios y los elimina de la pila.
    * `apply`: Aplica los cambios pero los mantiene en la pila.
    * `list`: Muestra todo lo guardado en el "limbo".
    * `-u` (`--include-untracked`): Guarda también los archivos nuevos no rastreados.

---

## 3. Sincronización y Remotos
* **`git push` / `git pull`**:
    * `-u` (`--set-upstream`): Vincula tu rama local con la remota.
    * `-f` (`--force`): Sobrescribe el historial remoto (peligroso).
    * `--force-with-lease`: Versión segura de force; no sobrescribe si hay cambios ajenos.
    * `--rebase` (en pull): Aplica tus cambios encima de los remotos (evita commits de merge).

* **`git remote`**:
    * `-v` (`--verbose`): Muestra las URLs de conexión.
    * `prune <nombre>`: Limpia ramas locales "fantasma" que ya no existen en el servidor.

---

## 4. Navegación e Historial
* **`git log`**:
    * `--oneline`: Resumen de un commit por línea.
    * `--graph`: Dibuja el árbol visual de ramas.
    * `--all`: Muestra el historial de todas las ramas.
    * `-p` (`--patch`): Muestra el código exacto que cambió.
    * `-S "<texto>"`: Busca texto específico dentro del código histórico.
    * `-L :<función>:<archivo>`: Rastrea la evolución de una función específica.
    * `--author="<nombre>"`: Filtra por autor.
    * `--no-merges`: Oculta los commits de fusión.

* **`git checkout` / `git switch`**:
    * `-b` / `-c`: Crea una rama nueva y salta a ella.
    * `-C`: Fuerza la creación/sobrescritura de la rama.
    * `-`: Vuelve a la rama anterior.
    * `-d` / `--detach`: Salta a un commit específico sin estar en ninguna rama.
    * `--discard-changes`: Cambia de rama borrando cambios locales sucios.

---

## 5. Reescritura y Recuperación (Avanzado)
* **`git rebase`**:
    * `-i` (`--interactive`): Interfaz para unir, renombrar o borrar commits.
    * `--continue` / `--abort`: Maneja el proceso en caso de conflictos.

* **`git reset`**:
    * `--soft`: Mueve HEAD pero mantiene cambios en el **Stage**.
    * `--mixed` (Default): Mueve HEAD y saca archivos del Stage al **Directorio**.
    * `--hard`: Borra todo. Vuelve al estado exacto del commit indicado.
    * `-p`: Reset interactivo para elegir partes específicas del archivo.

* **`git reflog`**: El historial de movimientos local para recuperar ramas o commits borrados.
* **`git cherry-pick <hash>`**: Copia un commit específico a tu rama actual.

---

## 6. Limpieza y Especialista
* **`git clean`**:
    * `-n`: Dry-run. Simulación de borrado.
    * `-f`: Fuerza la eliminación de archivos no rastreados.
    * `-fdx`: Borra archivos, directorios e ignorados por `.gitignore`.
    * `-X`: Borra **solo** los archivos ignorados por `.gitignore`.

* **`git blame`**:
    * `-L 10,20`: Analiza solo esas líneas.
    * `-w`: Ignora espacios en blanco.
    * `-M` / `-C`: Detecta si el código fue movido o copiado de otros archivos.

* **`git bisect`**: `start`, `bad`, `good`. Búsqueda binaria de commits con errores.
* **`git revert`**: `-n` (no commit), `-m 1` (para merges). Deshace cambios de forma segura.

---

## 7. Mantenimiento y Exportación
* **`git archive`**: `--format=zip -o salida.zip HEAD`. Exporta el código sin la carpeta `.git`.
* **`git worktree`**: `add <ruta> <rama>`. Permite tener varias ramas abiertas en carpetas distintas simultáneamente.
* **`git gc`**: `--prune=now --aggressive`. Comprime la DB y optimiza el repositorio.
* **`git bundle`**: Empaqueta el historial en un solo archivo para transferencias offline.

---

## 📂 Bonus: Configuración Global de `.gitignore`
Evita subir archivos basura de sistema o herramientas en todos tus proyectos locales:

```bash
# 1. Crear el archivo global
touch ~/.gitignore_global

# 2. Configurar Git para que lo use siempre
git config --global core.excludesfile ~/.gitignore_global

# 3. Ejemplo de contenido recomendado para ~/.gitignore_global:
# node_modules/
# .vscode/
# .idea/
# .DS_Store
# Thumbs.db

# .env
```  
