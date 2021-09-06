#!/usr/bin/python3
'''
Módulos de mensajes.
'''

# Importaciones
from colorama.ansi import Style
from datos import Comprador, Producto
import colorama
import os

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.4'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Resetear colorama despues de utilizarlo
colorama.init()

# Módulos


def mensaje(tipo: int, mensaje: str):
    '''
    Recibe un tipo de mensaje 0:[-] | 1:[INFO] | 2:[ERROR] | 3:[IMPORTANTE] y el mensaje e imprime un mensaje formateado.
    '''
    if tipo == 1:
        print(colorama.Fore.YELLOW, ' [INFO] ' + mensaje + Style.RESET_ALL)
    elif tipo == 2:
        print(colorama.Fore.RED, ' [ERROR] ' + mensaje + Style.RESET_ALL)
    elif tipo ==3:
        print(colorama.Fore.CYAN, ' [IMPORTANTE] ' + mensaje + Style.RESET_ALL)
    else:
        print(colorama.Fore.WHITE, ' [-] ' + mensaje + Style.RESET_ALL)


def limpiar_consola(producto: Producto, numero_comprador: int):
    '''
    Recibe un objeto de tipo Producto, limpia la consola e imprime un texto por defecto.
    '''
    comando = 'clear'
    if os.name in ('nt', 'dos'):
        comando = 'cls'
    os.system(comando)
    mensaje(0, 'Comprador: ' + Comprador(numero_comprador).email)
    mensaje(0, 'Descripción: ' + producto.descripcion)
    mensaje(0, 'URL: ' + producto.url + '\n')
