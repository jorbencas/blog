---
draft: false
title: "Guia de consegos y utilidades de yt-dlp y ffmpeg"
description: ""
pubDate: "2026/03/30"
tags: ['web', 'sistemas']
image: "/img/guia_ffmpeg_y_ÿt_dlp.png"
author: "Jorge Beneyto Castelló"
---


En el dia de hoy vamos ha ver como usando FFMPEG que una aplicación para gestionar videos


Devolver audio a un vdeo con codecs de audio: 

```bash
ffmpeg -i SENDOKAI\ \(Episodios\ 13-26\)-v1853275809.mp4 -c:v copy -c:a aac -b:a 128k 13-26.mp4
```

Si quieres descargar solo un trozo de un video:
```bash
yt-dlp --external-downloader ffmpeg        --external-downloader-args "ffmpeg_i:-ss 00:30:00 -to 00:34:05"        -f "bestvideo+bestaudio/best" "https://kick.com/sendosama/videos/30573887-0d08-4a0f-b792-c579b66e7641"
```
Si quieres cortar un video:
```bash
ffmpeg -i DETECTIVE\ CONAN\ 👓\ ARCO\ DE\ VERMOUT\ ｜\ GENTA\ FISIOCULTURISTA\ CANADIENSE\ \[0f57ec75-6375-49ee-9a2d-53654406defd\].mp4 -ss 00:00:00 -to 00:55:43 -c copy 01.mp4
```
Descargar video completo: 
```bash
yt-dlp --impersonate chrome --no-update https://kick.com/sendosama/videos/00eaba49-966a-4349-ac1d-d4a2ea624bbf
```
para unir 2  videos en uno :
```bash
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1" output.mp4
```