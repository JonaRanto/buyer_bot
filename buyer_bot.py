#!/usr/bin/python3
'''
Bot de compras online automaticas.
'''
# Importaciones
from buyer_bot_gui import gui
import subprocess

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Código
respuesta_gui = gui()
producto = respuesta_gui[0]
numero_compradores = respuesta_gui[1]

# Ejecutar subprocesos
for i in range(numero_compradores):
    subprocess.Popen(['python', 'elegir_web.py', 'elegir_web', str(i + 1), str(producto.url), str(producto.busqueda_producto), str(producto.palabra_clave), str(producto.nombre_web), str(producto.talla_buscada), str(producto.programado), str(producto.fecha_programada), str(producto.hora_programada), str(producto.descripcion)], creationflags=subprocess.CREATE_NEW_CONSOLE)
