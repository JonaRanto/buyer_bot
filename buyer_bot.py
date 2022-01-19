#!/usr/bin/python3
'''
Bot de compras online automaticas.
'''
# Importaciones
from os import getcwd
import pathlib
import requests
from buyer_bot_gui import gui
import subprocess
from configparser import ConfigParser

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.3.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Código
respuesta_gui = gui()
producto = respuesta_gui[0]
numero_compradores = respuesta_gui[1]

# def verificar_version():
#     config_auto_update_file = getcwd() + r'/config-auto-update.ini'
#     config = ConfigParser(interpolation=None)
#     config.read(config_auto_update_file)
#     url_last_readme = r'https://github.com/JonaRanto/' + config.get('File', 'id') + r'/raw/main/README.md'
#     print('Verificando versión')
#     page = requests.get(url_last_readme)
#     last_version = page.text.split('\n')[1].split('=')[1]
#     if not pathlib(getcwd() + r'/README.md').is_file():
#         resp = False
#     else:
#         my_readme = open('README.md', 'r')
#         my_version = my_readme.read().split('\n')[1].split('=')[1]
#         my_readme.close()
#         resp = False
#         if my_version == last_version: resp = True
#     return resp

# if not verificar_version():
#     subprocess.Popen(['python', 'autoupdate.py'])

# Ejecutar subprocesos
for i in range(numero_compradores):
    subprocess.Popen(['python', 'elegir_web.py', 'elegir_web', str(i + 1), str(producto.url), str(producto.busqueda_producto), str(producto.palabra_clave), str(producto.nombre_web), str(producto.talla_buscada), str(producto.programado), str(producto.fecha_programada), str(producto.hora_programada), str(producto.descripcion)], creationflags=subprocess.CREATE_NEW_CONSOLE)
