---
tittle: "Instalación y configuración de un servidor DHCP"
description: ""
date: "2015/11/03"
tags: ['web', 'sistemas']
slug: "instalacion-y-configuracion-dhcp.md"
image: "/img/instalacion-y-configuracion-dhcp.png"
author: "Jorge Beneyto Castelló"
layout: "../../layouts/PostLayout.astro"
---
Hoy vamos a instalar y configurar un servidor DHCP con Virtualbox, pero antes debemos saber que es y que hace el servicio DHCP.
El servicio DHCP permite la configuración de direcciones IP, máscaras, pasarelas por defecto y muchas otras opciones de configuración de manera totalmente dinámica.

## ¿Qué hace el DHCP?

Una forma campechana d’entender el DHCP es imaginar que los equipos de cliente al arrancar hacen un grito por la red y preguntan _«que hay algien?», «quien soy yo?»_. El servidor de DHCP les contesta proporcionándo les toda la información necesaria para que sepan quienes son y como deben configurar su configuración de red.
## Instalación y Configuración del Servidor DHCP

Vamos a proceder a la instal-lacion de un servidor DHCP. lo primero que debemos hacer es crear una maquina que actúe como servidor, en nuestro caso para crear el servidor vamos a utilizar Ubuntu Desktop 12.04 LTS:

[Pagina para descargar ISO de Ubuntu](https://ubuntu.com/download/alternative-downloads)

Una vez descargadas las ISO’s  es momento de crear la maquina virtual y instalar las ISO’s. Cuando ya tengamos las 2 maquinas virtuales instaladas la del cliente y la del servidor lo que debemos hacer es apagarlas y ir a configuracion red y habilitar en el servidor 2 adaptadores uno en Red Interna otro con NAT (Network Address Translation), aceptemos y encendemos la maquina Servidor.

Se debe de asignar una ip fija a el sevidor, concretamente a la tarjeta de red interna,para ello hay que ir a las conexiones y clicar en editar conexiones, luyego en IPV4 y poner manualmente, aqui sera donde pondremos la IP, la mascara y la puerta de enlace

<img title="Obtener dirección IP" alt="Obtener dirección IP" src="/img/instalacion-y-configuracion-dhcp_1.png">

Ahora debemos ir a el cliente i hacer lo mismo pero lo que hay que hacer es enves de manual hay que poner-lo automatico.
Para comprobar si nos la ha assignado, dedemos de abir una terminal y poner ifconfig

<img title="Obtener dirección IP" alt="Obtener dirección IP" src="/img/instalacion-y-configuracion-dhcp_2.png">

## Configuración con Webmin

Ahora debemos de instalar webmin que es una herramienta para configurar el servidor de forma grafica

[Para descargar webmin](https://www.webmin.com/download.html)

Una vez descargado webmin lo que se debe de hacer es instalar el paquete.deb de webmin, para ello debemos de abrir una terminal y poner:
`cd /ruta_donde_este_el_archivo_y_luego  sudo dpkg -i webmin_1.770_all.deb`
Una vez instalado webmin lo que se debe de hacer es abirir el navegador chorome, firefox, opera etc y pones https://localhost:10000/
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_3.png">

Luego lo que habra que hacer es entrar con un usuario que tenga permiso de adminitrador y cambiar el idioma ya que por defecto esta en inglés, para ello nos vamos a webmin, y cambiamos el idioma, luego hay que ir a donde dice **refresh modules** para que se apliquen los cambios una vez comprobado que podemos acceder y cambiar el idioma lo que hay que hacer es minimizar el navegador y ir a el centro de Sofware de ubuntu para ver si tenemos instalado un programita que se llama Avahi IPv4LL network address configuration daemon, es importante que el avahi este instalado ja que es necesario para activar el servidor DHCP, luego de instalar-lo se debe de comprobar que funciona el avahi.
<code>
    sudo avahi-autoipd eth1 && ping IP 
</code>
Cuando este configurado el Avahi para que se autoasigne a el adaptador eth1 que es el adaptador del cliente y por tanto es el adaptador de red interna que es la que debe de  comunicar-se con el cliente, luego se debe de instalar el servidor DHCP en el servidor, para ello se debe de abrir una terminal y poner:

<code>
    sudo apt-get install isc-dhcp-server
</code>

Después de haber instalado el DHCP server se debe de maximizar el navegador y poner refrescar modulos y ir a servidores y luego debe de aparecer **servidor DHCP**.
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_4.png">

Se pulsa y ya están todas las opciones para configurar un servidor DHCP, si hemos llegado hasta aquí ahora seria prudente cerrar todo y apagar la maquina virtual, luego nos vamos a donde pone archivo y exportar, asi si se nos estropea la maquina ya no hay que reinstalar-lo todo, solo la restauramos desde el archivo OVA que acabamos de exportar.

Encendemos la maquina y accedemos a webmin, a servidor DHCP y configuramos una nueva subred, para ello abra que configurar una serie de parametros en añadir una nueva subred como es el nombre de la red, el rango que quieres que abarque la asignación de IPs 192.168.101.200 - 192.168.101.205, la mascara 255.255.255.0 y ja podemos guardar.
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_5.png">

Ahora lo que hay que hacer es configurar el cliente, para ello hay que ir a **Editar opciones de el cliente**, dentro hay que poner el nombre del anfitrión, la mascara de subred 255.255.255.0, los enrutadores por defecto que ponemos la broadcast 192.168.202.255, luego ponemos otra vez la broadcast.
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_6.png">

Ahora ya esta configurado lo que hay que hacer es salvarlo que significa guardar, una vez echo esto hay que pulsar refresh moduls o abiri una terminal y poner 
<code>
    sudo /etc/init.d/dhcp3-server restart && sudo /etc/init.d/dhcp3-server stop 
</code>
para el servidor para que actualice la pagina.
Ahora es el momento de comprobar si el servidor dhcp nos a auto asignado una de las ip del rango que le hemos indicado, para ello hay que es encender la maquina virtual del cliente y nos vamos a editar las conexiones para ver si nos a auto asignado alguna ip, si nos la ha asignado es que ha funcionado, y ya tenemos configurado el cliente y el servidor.Ahora es recomendable comprobar que a ocurrido en los ficheros de configuración, para ello hay que ir ha
<code> 
    sudo gedit /etc/network/interfaces 
</code>
o otro fichero es el lesses que para acceder a el hay que poner 
<code> 
    sudo nano /etc/dhcp3/dhcpd.conf 
</code>

Ahora hay que comprobar que ha cambiado en  estos ficheros y asi entender que es lo quele a pasado en estos ficheros con lo que hemos echos en webmin.
También se puede hacer que se asigne a el cliente una ip fija, para ello debemos ir ha webmin y ir a servidor DHCP, y a **añadir nueva maquina**
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_7.png">

Una vez dentro habra que poner una dirección ip fija que sera la que se asignara a el cliente, una vez puesta la ip le damos a crear, luego hay que ir a editar manualmente, en este fichero abajo del todo y  hay que poner lo siguiente:
```
# internet
subnet 192.168.101.0 netmask 255.255.255.0 {
    range 192.168.101.200 192.168.101.205;
    host client {
        hardware ethernet 08:00:27:e9:ae:eb;
        fixed-address 192.168.101.202;
    }
}
```
<img title="Configuración Webmin" alt="Configuración Webmin" src="/img/instalacion-y-configuracion-dhcp_8.png">

Ahora salvamos y iniciamos la maquina cliente para ver si nos la a asignado, si nos la ha asignado es que si que ha funcionado.