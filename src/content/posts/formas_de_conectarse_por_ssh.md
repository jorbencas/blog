---
draft: false
title: "Formas de conectarse por SSH"
description: "Descubre las distintas formas de conectarse con ssh"
pubDate: "2015/11/25"
tags: ['sistemas']
slug: "formas_de_conectarse_por_ssh.md"
image: "/img/html5.png"
author: "Jorge Beneyto Castelló"
layout: "@layouts/PostLayout.astro"
---

### Instalación del SSH

Hoy vamos a ver como instalar y las 4 formas que hay de conectar-se por ssh de un cliente a un servidor, lo primero que hay que hacer es instalar el ssh en el equipo que queramos utilizar como servidor, osea al cual queramos conectarnos para ello abriremos una terminal y pondremos el siguiente comando:`sudo apt-get install openSSH-server`

Una vez que ya este instalado, lo que se debe de hacer es iniciar el cliente, abrir una terminal y conectarse a el servidor, que es el equipo donde hemos instalado el servicio de ssh, para ello debemos saber el nom de usuario y la dirección ip del servidor, una vez que sepamos esto, lo  que se debe de hacer es ir a la terminal y escribir el siguiente comando:
### Conectarse utilizando un usuario y una IP
Primera Forma: ssh jorge@192.168.101.1 (usuario@dirección IP)

(En usuario pondremos nuestro nombre de usuario y en IP, la dirección IP a la cual queremos conectarnos) esta es la forma tradicional de conectarse a otro equipo, que es el servidor, el servicio ssh es un servicio cliente/servidor, nos conectamos des del cliente al servidor,

Dentro de esta forma, existe la posibilidad de poner un parámetro con la instrucción que se quiere realizar para que la realiza y después se desconecte de forma automática, esto se utiliza cuando se querer realizar una acción concreta en el servidor y des pues desconectarse, para ello abriremos una terminal y pondremos:
### Conectarse para utilizar un comando
`ssh jorge@192.168.101.1 ls -l`   (usuario@dirección IP Comando)

<img title="Formas de conectarse con ssh" alt="Obtener dirección IP" src="/img/formas_de_conerse_por_ssh.webp
">

### Conectarse utilizando la dirección IP
Segunda Forma: `ssh 192.168.101.1` (Dirección IP)

De esta forma solo hay que poner la dirección IP del servidor al cual queremos conectarnos, y se conectara, si es la primera vez que nos conectamos no pedirá que si es este host/ordenador al que queremos conectarnos.

<img title="Formas de conectarse con ssh" alt="Obtener dirección IP" src="/img/formas_de_conerse_por_ssh_1.webp
">

Esta forma de conexión es posible por que en el servidor hay un usuario con el mismo nombre de usuario que en el cliente (no debe de ser un usuario administrador) por tanto lo que esta haciendo es conectarse a el nombre de usuario cliente de la maquina servidora

Como hemos instalado un servidor DNS, también podemos hacerlo poniendo solo el dominio de nuestro servidor

### Conectarse utilizando el domínio
`ssh www.jorge.com` (nombre de dominio)

Mediante esta forma lo podemos hacer ya que previamentre hemos configurado nuestro servidor DNS con webmin.

### Conectarse utilizando el SCP
Tercera Forma: `scp /home/jorge/pajaritos.txt client@192.168.101.1:/home/client/`

<img title="Formas de conectarse con ssh" alt="Obtener dirección IP" src="/img/formas_de_conerse_por_ssh_2.webp
">

Esta forma se llama protocolo de copia de archivos segura, por ello las siglas SCP (Service Copia Protocol), donde pone ruta hay que opner la ruta del fichero que queremos copias, y luego la ruta del destino de ese fichero.

### Conectarse por SFTP
Curta Forma: `sftp://jorge@192.168.101.1`  (usuario@dirección IP)

Abrimos una terminal y ponemos sudo nautilus ( se pone sudo para que nos abra el nautilus con privilegios de adminstrador)esta instrucción lo que hace es iniciar el nautilus que es un gestor de carpetas, una vez allí  ahi que ir a la barra de busqueda y poner control l , ahora  se nos abre la barra de busqueda, en la cual hay que poner, el siguiente comando

### Conectarse utilizando el Nautilus
`sftp://jorge@192.168.101.1` (usuario@dirección IP)

Nos pedirá la contraseña de dicho usuario, cuando ya la hayamos puesto se nos abre el Nautilus de la maquina servidora

![Formas de conectarse con ssh](/img/formas_de_conerse_por_ssh_3.webp)

Tambien nos podemos conectar por ssh utilizabdi el nautilus, iendo a la carpeta personal, ha archivo, a conectarse con el servidor y dentro hay que poner los datos, que son el tipo de conexión que en este caso es ssh , la IP del servidro, el puerto que es el 22, la carpeta a la cual queremos conectar-nos que en mi casdo es /home/jorge y ponemos el usuario y contraseña de este usuario, despues te pide la contraseña

![Formas de conectarse con ssh](/img/formas_de_conectarse_con_ssh.png)

Como podemos ver nos la monta como una unidad de red

![Formas de conectarse con ssh](/img/formas_de_conectarse_con_ssh_1.png)