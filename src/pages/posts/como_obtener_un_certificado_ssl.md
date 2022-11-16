---
draft: false
title: "Cómo obtener un certificado SSL"
description: ""
pubDate: "2016/01/19"
tags: ['sistemas', 'web']
slug: "como_obtener_un_certificado_ssl.md"
image: "/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl.webp"
author: "Jorge Beneyto Castelló"
layout: "../../layouts/PostLayout.astro"
---

Hoy vamos ha ver como configurar un certificado ssl, para ello hay que ir a nuestro servidor Webmin, desde la maquina servidora, hay que iniciar nuestro servidor web, irnos a Servidor web apache, una vez en el servidor  web apache , hay que ir ha Global Configuration, una vez allí ahi que ir a configuración de apache modules, una vez allí hay que ir ha la opción de ssl

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_1.png)

Una vez activada esta opción hay que ir a enable select para que asi podamos activar, una vez hecho esto hay que abrir una terminal y instalar el ssl, para ello hay que poner

<code>sudo apt-get install openssl</code>

Una vez hecho esto hay que crear una carpeta en la cual se guardaran los 2 certificados, para ello hay que hacer un sudo `mkdir /etc/http`, luego hay que situarse en dicha carpeta para ello hay que hacer un cd /etc/http una vez allí ahí que hacer el comando que nos generara los 2 certificados

<code>sudo openssl req -newkey rsa:512 -x509 -nodes -out cert.pen -keyout key.pen</code>

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_2.png)

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_3.png)

Despues ahi que darle permisos a los 2 ficheros para ello hay que hacer el siguiente comando:

<code>sudo chmod +x key.gen</code>

Ahora ya tenemos creados nuestros certificados ssl, para comprovar si se ha hecho hay que hacer un listado de los archivos que hay en esta carpeta, para comprovar que estan los 2 archivos hay que hacer un `ls`.
Una vez hecho esto ahora es momento de volver al Webmin, ir a servidor web Apache, ir a nuestra zona virtual, y luego clicar a nuestra zona, una vez allí hay que ir a Opciones SSL, debtro hay que ir a archivo de Certificado/clave publica, y archivo de clave privada, aqui hay que poner la ruta de los 2 archivos, como se ve en la imagen:

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_4.png)

Ahora hay que hacer que el puerto sea el 443

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_1.webp)

Una vez hecho esto hay que ir ha el cliente y probar si funciona.

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_5.png)

Y ahora como vemos ya nos funciuona y nos apareze, ahora para acceder a la pagina lo que hay que hacer es clicar en `understand`:

![carpeta var](/img/como_obtener_un_certificado_ssl/como_obtener_un_certificado_ssl_6.png)

Y en haz una excepción, al hacer esto nos deja entrar.

Espero que hos haya servido este tutorial