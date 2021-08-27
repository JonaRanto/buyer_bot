#!/usr/bin/python3
'''
Bot de compras online automaticas.
'''
# Importaciones
import sys
from buyer_bot_gui import gui
from programacion import programar_compra
from conexion import conectar_wd
import webs

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Código
respuesta_gui = gui()
producto = respuesta_gui[0]
numero_comprador = respuesta_gui[1]

print('Si finalizó')
sys.exit()

# Programar compra
if producto.programado:
    programar_compra(producto)

# Elegir web
if producto.nombre_web == 'bold':
    # Conexion WebDriver
    wd = conectar_wd()
    webs.bold(producto, numero_comprador, wd)
elif producto.nombre_web == 'moredrops':
    # Conexion WebDriver
    wd = conectar_wd()
    webs.moredrops(producto, numero_comprador, wd)
elif producto.nombre_web == 'adidas':
    # Conexion WebDriver
    wd = conectar_wd()
    webs.adidas(producto, numero_comprador, wd)
