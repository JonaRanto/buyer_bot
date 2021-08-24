#!/usr/bin/python3
'''
Módulos de archivos.
'''

# Importaciones
import json

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Módulos


def cargar_json(ubicacion_json: str):
    '''
    Recibe el path de un archivo y devuelve una lista de diccionarios.
    '''
    with open(ubicacion_json) as contenido:
        web_options = json.load(contenido)
        return web_options
