---
draft: false
title: "Scripts"
description: "Post de Scripts"
pubDate: "2023/12/16"
tags: ['sistemas', 'linux', 'bash']
slug: "scripts"
image: "/img/resources.webp"
author: "Jorge Beneyto Castelló"
layout: "@layouts/PostLayout.astro"
---

# ar 1
``` bash
#!/bin/bash

# Ruta de las carpetas de videos y audios
videos_folder="./VIDEOS "
audios_folder="./Audios"
unidos_folder="./UNIDOS"

# Iterar sobre los archivos de video
for video_file in "$videos_folder"/*.mp4; do
    # Extraer el número de T del nombre del video
    t_number=$(echo "$video_file" | grep -oP 'T\d+' | cut -c2-)

    # Construir la ruta del archivo de audio correspondiente en biolo1
    audio_file_1="$audios_folder/biolo1/Psicobio 1 T${t_number}-audio.mp4"

    # Construir la ruta del archivo de audio correspondiente en biolo2
    audio_file_2="$audios_folder/biolo2/Psicobio 2 T${t_number}-audio.mp4"

    # Verificar si existen archivos de video y audio
    if [ -f "$video_file" ]; then
        if [ -f "$audio_file_1" ]; then
            audio_file="$audio_file_1"
        elif [ -f "$audio_file_2" ]; then
            audio_file="$audio_file_2"
        else
            echo "No se encontró el archivo de audio correspondiente para $video_file"
            continue
        fi
    else
        echo "No se encontró el archivo de video $video_file"
        continue
    fi

    # Crear la carpeta de salida si no existe
    mkdir -p "$unidos_folder"
    
    # Crear la carpeta en la que se colocarán los archivos unidos
    output_folder="$unidos_folder/$(basename "$video_file" .mp4)"
    mkdir -p "$output_folder"

    v_file="$output_folder/01.mp4"
    a_file="$output_folder/01-audio.mp4"
 # Verificar si "$output_folder/01.mp4" ya existe antes de copiar
                if [ ! -f "$v_file" ] && [ ! -f "$a_file" ]; then
    # Copiar los archivos y renombrarlos a "01.mp4" y "01-audio.mp4"
    cp "$(realpath "$video_file")" "$v_file"
    cp "$(realpath "$audio_file")" "$a_file"
	echo "CARPETA: $v_file" 
    echo "Unión completa para $video_file"
    
     else
                    echo "El archivo \"$v_file\" ya existe. No se hizo nada."
                fi

 # Verificar si se encontraron archivos de video y audio
            if [ -f "$v_file" ] && [ -f "$a_file" ]; then
                # Ejecutar el comando ffmpeg con los nombres reales de los archivos
# Obtener la ruta absoluta del directorio de salida
output_folder_absolute=$(realpath "$output_folder")

# Ejecutar el comando ffmpeg con rutas absolutas
ar_videos_command="ffmpeg -i \"$output_folder_absolute/01.mp4\" -i \"$output_folder_absolute/01-audio.mp4\" -c:v copy -c:a aac -strict experimental \"$output_folder_absolute/001.mp4\""

# Ejecutar ffmpeg
eval "$ar_videos_command"
ffmpeg_exit_code=$?

# ...


        # Verificar si el archivo se generó correctamente antes de renombrar
        if [ $ffmpeg_exit_code -eq 0 ] && [ -f "$output_folder/001.mp4" ]; then
            # Renombrar el archivo resultante con el nombre de la carpeta
            mv "$output_folder/001.mp4" "$output_folder/$(basename "$output_folder").mp4"

            echo "Conversión completa para la carpeta $(basename "$output_folder")"
            
            
              # Mover el archivo resultante una carpeta arriba
                    mv "$output_folder/$(basename "$output_folder").mp4" "$unidos_folder"

                    # Borrar la carpeta de salida
                    rm -r "$output_folder"

                    echo "Movido y borrado correctamente."
                    
        else
            echo "Error: No se generó el archivo de salida correctamente."
        fi
            else
                echo "No se encontraron archivos de video y audio en la carpeta $output_folder"
            fi
done
```
# ar 2
```bash
#!/bin/bash

# Ruta de las carpetas de videos y audios
videos_folder="./VIDEOS "
audios_folder="./Audios"
unidos_folder="./UNIDOS"

# Iterar sobre los archivos de video
for video_file in "$videos_folder"/*.mp4; do
    # Extraer el número de T del nombre del video
    t_number=$(echo "$video_file" | grep -oP 'T\d+' | cut -c2-)

    # Construir la ruta del archivo de audio correspondiente en biolo1
    audio_file_1="$audios_folder/biolo1/Psicobio 1 T${t_number}-audio.mp4"

    # Construir la ruta del archivo de audio correspondiente en biolo2
    audio_file_2="$audios_folder/biolo2/Psicobio 2 T${t_number}-audio.mp4"

    # Verificar si existen archivos de video y audio
    if [ -f "$video_file" ]; then
        if [ -f "$audio_file_1" ]; then
            audio_file="$audio_file_1"
        elif [ -f "$audio_file_2" ]; then
            audio_file="$audio_file_2"
        else
            echo "No se encontró el archivo de audio correspondiente para $video_file"
            continue
        fi
    else
        echo "No se encontró el archivo de video $video_file"
        continue
    fi

    # Crear la carpeta de salida si no existe
    mkdir -p "$unidos_folder"
    
    # Crear la carpeta en la que se colocarán los archivos unidos
    output_folder="$unidos_folder/$(basename "$video_file" .mp4)"
    mkdir -p "$output_folder"

    v_file="$output_folder/01.mp4"
    a_file="$output_folder/01-audio.mp4"
 # Verificar si "$output_folder/01.mp4" ya existe antes de copiar
                if [ ! -f "$v_file" ] && [ ! -f "$a_file" ]; then
    # Copiar los archivos y renombrarlos a "01.mp4" y "01-audio.mp4"
    cp "$video_file" "$v_file"
    cp "$audio_file" "$a_file"

    echo "Unión completa para $video_file"
    
     else
                    echo "El archivo \"$v_file\" ya existe. No se hizo nada."
                fi

 # Verificar si se encontraron archivos de video y audio
            if [ -f "$v_file" ] && [ -f "$a_file" ]; then
                # Ejecutar el comando ffmpeg con los nombres reales de los archivos
# Obtener la ruta absoluta del directorio de salida
output_folder_absolute=$(realpath "$output_folder")

# Ejecutar el comando ffmpeg con rutas absolutas
ar_videos_command="ffmpeg -i \"$output_folder_absolute/01.mp4\" -i \"$output_folder_absolute/01-audio.mp4\" -c:v copy -c:a aac -strict experimental \"$output_folder_absolute/001.mp4\""

# Ejecutar ffmpeg
eval "$ar_videos_command"
ffmpeg_exit_code=$?

# ...


        # Verificar si el archivo se generó correctamente antes de renombrar
        if [ $ffmpeg_exit_code -eq 0 ] && [ -f "$output_folder/001.mp4" ]; then
            # Renombrar el archivo resultante con el nombre de la carpeta
            mv "$output_folder/001.mp4" "$output_folder/$(basename "$output_folder").mp4"

            echo "Conversión completa para la carpeta $(basename "$output_folder")"
            
            
              # Mover el archivo resultante una carpeta arriba
                    mv "$output_folder/$(basename "$output_folder").mp4" "$unidos_folder"

                    # Borrar la carpeta de salida
                    rm -r "$output_folder"

                    echo "Movido y borrado correctamente."
        else
            echo "Error: No se generó el archivo de salida correctamente."
        fi
            else
                echo "No se encontraron archivos de video y audio en la carpeta $output_folder"
            fi
done
```
# ar 3
```bash
#!/bin/bash

# Rutas de la carpeta que contiene videos y audios, y la carpeta de salida
source_folder="./VIDEOCLASES SOCIAL"
unidos_folder="./UNIDOS"

# Iterar sobre los archivos de video
for video_file in "$source_folder"/*.mp4; do
    # Extraer el número de T del nombre del video
    t_number=$(echo "$video_file" | grep -oP 'T\d+' | cut -c2-)

    # Construir la ruta del archivo de audio correspondiente
    audio_file="$source_folder/Social T${t_number}-audio.mp4"

    # Verificar si existen archivos de video y audio
    if [ -f "$video_file" ]; then
        if [ -f "$audio_file" ]; then
            # Crear la carpeta de salida si no existe
            mkdir -p "$unidos_folder"

            # Crear la carpeta en la que se colocarán los archivos unidos
            output_folder="$unidos_folder/$(basename "$video_file" .mp4)"
            mkdir -p "$output_folder"

            # Verificar si "$output_folder/01.mp4" ya existe antes de copiar
            if [ ! -f "$output_folder/01.mp4" ]; then
                # Copiar los archivos y renombrarlos a "01.mp4" y "01-audio.mp4"
                cp "$video_file" "$output_folder/01.mp4"
                cp "$audio_file" "$output_folder/01-audio.mp4"

                echo "Unión completa para $video_file"
            else
                echo "El archivo \"$output_folder/01.mp4\" ya existe. No se hizo nada."
            fi

            # Ejecutar el comando ffmpeg con los nombres reales de los archivos
            # Obtener la ruta absoluta del directorio de salida
    output_folder_absolute=$(realpath "$output_folder")

    # Ejecutar el comando ffmpeg con rutas absolutas
    ar_videos_command="ffmpeg -i \"$output_folder_absolute/01.mp4\" -i \"$output_folder_absolute/01-audio.mp4\" -c:v copy -c:a aac -strict experimental \"$output_folder_absolute/001.mp4\""

    # Ejecutar ffmpeg
    eval "$ar_videos_command"
    ffmpeg_exit_code=$?

            # Verificar si el archivo se generó correctamente antes de renombrar
            if [ $ffmpeg_exit_code -eq 0 ] && [ -f "$output_folder/001.mp4" ]; then
                # Renombrar el archivo resultante con el nombre de la carpeta
                mv "$output_folder/001.mp4" "$output_folder/$(basename "$output_folder").mp4"

                echo "Conversión completa para la carpeta $(basename "$output_folder")"
                
                  # Mover el archivo resultante una carpeta arriba
                    mv "$output_folder/$(basename "$output_folder").mp4" "$unidos_folder"

                    # Borrar la carpeta de salida
                    rm -r "$output_folder"

                    echo "Movido y borrado correctamente."
            else
                echo "Error: No se generó el archivo de salida correctamente."
            fi
        else
            echo "No se encontró el archivo de audio correspondiente para $video_file"
        fi
    else
        echo "No se encontró el archivo de video $video_file"
    fi
done
```