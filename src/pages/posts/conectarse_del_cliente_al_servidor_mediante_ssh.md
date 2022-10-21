---
draft: false
tittle: "Conectarse del cliente al servidor mediante ssh"
description: "Descubre con un ejemplo la forma de conectarse del cliente a un servidor mediante ssh"
date: "2015/12/02"
tags: ['sistemas']
slug: "conectarse_del_cliente_al_servidor_mediante_ssh.md"
image: "/img/conectarse_del_cliente_al_servidor_mediante_ssh.webp"
author: "Jorge Beneyto Castelló"
layout: "../../layouts/PostLayout.astro"
---

Lo que hoy vamos ha intentar es  tener internet en un odenador cliente, conectando nos  através del servidor, ya que este es el que tiene una tarjeta NAT y por ello es el que tiene internet,gracias a la tarjeta NAT, y nosotros lo que vamos a hacer es que el cliente através de su tarjeta que esta en red interna, que es común en los 2 ordenadores se conecte a el servidor y coja el internet de su tarjeta NAT.

Para ello hay que tener en cuenta que hay que tener las 2 maquinas o ordenadores conectados en red y hay que tener instalado el ssh,

Lo primero que debemos hacer es iniciar el servidor,una vez iniciado ahora ahy que crear un script para que haga el renviamiento de puertos, abrimos un editor de texto plano (nano, gedit…) y una vez abierto hay que poner lo siguiente:

```
    echo «1» > /proc/sys/net/ipv4/ip_forward
    iptables -A FORWARD -j ACCEPT
    iptables -t nat -A POSTROUTING -s 192.168.101.0/24 -o eth0 -j MASQUERADE
```

NOTA: En la dirección  IP debemos adaptarla a la nuestra, para ello hay que abrir una terminal y  poner  ifconfig y ver cual es tu dirección IP.

NOTA2: Es importante que el script, que es funchero lo guardemos en sh , ya que si lo guardamos en otro formato no lo ejecutara.

Ahora hay que abrir una terminal y poner:

`sudo nano  /etc/rc.local`

(donde pone nano da igual que sea el gedit, el caso es que sea un editor de texto plano )

Una vez dentro del fichero rc.local , lo que hay que  hacer ex en la ultima linea comentada antes del exit 0 hay que poner:

`sh /home/jorge/Baixades/iptables.sh`

Osea sh por que es un script, y en linux los scripts se ejecutan con la extensión sh y la ruta donde esta el fichero , logicamente hay que incluir el nombre del fichero para que nos lo ejecute, ersto lo estamos haciendo por que si lo hubie semos hecho en los comando sueltos

```
    echo «1» > /proc/sys/net/ipv4/ip_forward

    iptables -A FORWARD -j ACCEPT

    iptables -t nat -A POSTROUTING -s 192.168.101.0/24 -o eth0 -j MASQUERADE
```

Hubiera funcionado pero cuando hubiesemos reiniciado el equipo toda la configuración del iptables se abria borrado, por eso hay que ejecutarlo en un script con extensión sh y luego guardar-lo en `/etc/rc.local`.

Ya es el momento de cerrrar la terminal y el editor de tecto y abrir el navegador y entrar a el gestor webmin, ir a servidores>servidor dhcp>cliente>editar opciones de cliente
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh.webp)

Ademas de poner de la IP de DNS que hay poner otra por si acaso en esa que hay no esta, que pueda ir a buscar-la ala otra dirección IP de DNS.
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh_1.png)

Ahora salvamos y ya podemos iniciar el cliente y hacer un túnel para que se conecta a la tarjeta en red interna que tienen en común el servidor y el cliente, para así luego que se conecte a la NAT y que le devuelva a el cliente la conexión a internet.

Para ello hay que abrir una terminal en el cliente y poner el siguente comando:

`ssh -D 8080 -p 22 -N jorge@192.168.101.1`

Nos conectamos por ssh .

- La opción D lo que hace es el redireccionamiento de puertos, lo cual implica que el puerto de entrada sera el 8080 .

- la opció p lo que hace es decirle que lo haga por el puerto 22, que es el puerto del ssh, portanto un puerto seguro.

- La opción N lo que hace es que sea invisible a el usuario, osea que no abre la terminal del servidor y lo ejecuta, sino que lo ejecuta de forma transparente a los ojos del usuario.

Luego ponemos el usuario y la dirección IP y se nos quedara así:
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh_2.png)

Como vemos hay que tener cuidado con escribir bien la contraseña del servidor, sino nos la vuelve a preguntar, un máximo de 3 veces

Ahora ya nos esta haciendo el puente a la maquina servidora, pero si queremos que salga a internet, debemos especificar en el navegador web una serie de parametros.

Para ello abrimos el navegador web, nos vamos a editar>preferencias>avanzado>red>Configuración.
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh_1.webp)

Aqui es donde  los datos, hay que marcar la opción «Configuración manual del proxy», ya que por defecto nos pone sin proxy, ahora ya le pondremos que el servidor SOCKS sea el localhost, osea la maquina local que es el servidor y le indicaremos el puerto que es el 8080, ya no hay que tocar nada mas
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh_3.png)

Asi es como debe quedar nuestra configuración, luego le damos a aceptar, cerramos y ya podremos navegar con el cliente.
![Webmin](/img/conectarse_del_cliente_al_servidor_mediante_ssh_2.webp)

Como vemos ya nos podemos conectar a internet con el cliente atraves del servidor, si quisieramos dejarlo como estava, nos vamos otravez a edita >preferencias>avanzado>red>configuración y ponemos «sin proxy»