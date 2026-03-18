---
draft: false
title: "Como crear un servidor virtual"
description: ""
pubDate: "2016/01/17"
tags: ['sistemas', 'web']
image: "/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual.png"
author: "Jorge Beneyto Castelló"
---


Hoy vamos ha hacer que podamos acceder a una pagina web alogadaen un usuario en el servidor desde el cliente, para ello debemos de tener instalado el apache.

Primero de todo, lo que vamos ha hacer es ir ha el servidor y abrir una terminal y poner

<code>sudo apt-get install apache2</code>

ahora hay que abrir una terminal, poner

<code>sudo nautilus</code>

Una vez hecho esto se nos abrirar el nautilus peor como root, una vez alli hay que ir a el directorio `/var/www` y dentro de este directorio abra un archivo que se llama index.html , ese es el indice de nuestra pagina web, pero no esta donde nosotros que remos que este ja que nosotros queremos que otro usuario sea el que pueda subir esa pagina web.

![carpeta var](/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual_1.png)

Para ello hay que ir a `/` y una vez allí hay que ir a `/home/client (Client es nuestro usuario lo que se trata es de ir a la carpeta del usuario)`, una vez allí hay que pegar la carpeta www que hemos copiado de `/var/www` 

![archivo index](/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual_2.png)

Luego hay que ir a nuestro Webmin y ver si esta instalado el modulo de apache, si esta instalado, es hora poner-se manos a la obra, hay que crear un host virtual, pero primero hay que crear un nombre de dominio que asociaremos a este host virtual, en mi caso el nombre de dominio que he elegido es `beneyto.com` 

### Recordatorio
Para crear un nombre de dominio hay que ir en nuestro servidor Webmin a DHCP NIND a donde dice crear zona maestra, una vez allí hay que poner en nombre de domino, laIP asociada a ese nombre de dominio, que siempre sera la del servidor y una dirección de correo, luego aceptar y ja esta creada nuestra nueva zona maestra o lo que es lo mismo nuestro nuevo nombre de dominio

![webmin](/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual_1.webp)

Es ahora cuando ya podemos crear nuestro host virtual, para ello hay que ir  a Servidor Web apache, a crear virtual hosts, una vez dentro solo hay que completar con la IP del servidor, la ruta donde esta el archivo de nuestra pagina web, osea el index.html, luego hay que poner el nombre de nuestro nuevo dominio que en mi caso es beneyto.com, es muy importante poner antes del dominio `http://www.beneyto.com`, una vez hecho esto ja tenemos nuestro hosts virtual creado.

![webmin](/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual_3.png)

Ahora ya nuestro usuario client puede subir paginas web, para comprobarlo hay que ir a la maquina cliente, abrir el navegador y poner la dirección IP o el nombre de dominio especificado para ese host virtual, que en mi caso es `http://www.beneyto.com`

![webmin](/img/como_crear_un_servidor_virtual/como_crear_un_servidor_virtual_4.png)

Es importante que si utilizáis el nombre de domino para verificar que ha funcionado pongáis www si no no estáis escribiendo correctamente el dominio y no funcionara