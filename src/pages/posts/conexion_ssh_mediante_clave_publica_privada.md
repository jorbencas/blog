---
draft: false
title: "Conexión mediante clave pública privada"
description: "Practica para crear una conexión ssh mediante clave pública privada"
pubDate: "2015/12/09"
tags: ['sistemas']
slug: "conexion_ssh_mediante_clave_publica_privada.md"
image: "/img/conexion_ssh_mediante_clave_publica_privada.webp"
author: "Jorge Beneyto Castelló"
layout: "../../layouts/PostLayout.astro"
---
Hoy vamos ha ver como conectamos por ssh pero en lugar de usar la contraseña del usuario  servidor usaremos una autentificación de clave publica, o sea que nos pedirá una contraseña de clave pribada

Este ficherto es el que hay que copiar a nuestro servidor, que en este fichero es donde se guardan las claves publi8cas, para ello hay que abrir una terminal y mediante scp compiar este archivo a el servidor
![Webmin](/img/conexion_ssh_mediante_clave_publica_privada.png)

Estos son los 3 archivos que nos genera,
![Webmin](/img/conexion_ssh_mediante_clave_publica_privada_1.png)

Ahora nos vamos ha la maquina servidora y crear en tu carpeta pesonal un carpeta que se llame .ssh, ahora en la maquina cliente ay que ir a el servidor y copiar el fitxero id_rsa.pub a el servidor.
`scp ~/.ssh/id_rsa.pub jorge@192.168.101.1:~/.ssh`
Ahora hay un archivo en la carpeta `.ssh`
![Webmin](/img/conexion_ssh_mediante_clave_publica_privada.webp)

Ahora hay que crear un fitchero llamado authorized_krys despues hay que hacer una concatenación a el authorized_krys, para ello hay que abiri una terminal y poner:
`cat id_rsa.pub >> authorized_keys`
La clave  de uso de la clave publica peivada
![Webmin](/img/conexion_ssh_mediante_clave_publica_privada_2.png)

Ahora como vemos ia estamos conectados por ssh a la maquina , es igual que la misma forma que si hubieramos conectados por contraseña

Ahora le añadimos los permisos a el archivo authorized_keys para que se vaya actualizanso `chmod +x authorized_keys`.