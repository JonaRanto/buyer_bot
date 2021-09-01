#!/usr/bin/python3
'''
Módulos de validaciones.
'''

# Importaciones
from archivos import cargar_json
from urllib.parse import urlparse
import re
import os

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.2'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
webs_disponibles_file = os.getcwd() + '\\webs_disponibles.json'

# Módulos


def validar_formato_hora(hora: str):
    '''
    Recibe una hora y devuelve un bool con la validación.
    '''
    hora_re = re.compile(r'^(?:[01]?\d|2[0-3]):[0-5]\d$')
    validacion = bool(hora_re.search(hora))
    return validacion


def validar_web(url: str):
    '''
    Recibe una url y devuelve una lista con la validación y el nombre de la web.
    '''
    url_parse = urlparse(url)
    archivo_json = cargar_json(webs_disponibles_file)
    validacion = False
    for index in archivo_json:
        if (url_parse.hostname == index.get('web_hostname')):
            validacion = True
            nombre_web = str(index.get('web_name'))
            break
    if validacion:
        return list([validacion, nombre_web])
    else:
        return list([validacion])


def validar_talla(talla_buscada: str):
    '''
    Recibe una talla y devuelve un bool con la validación.
    '''
    talla_re = re.compile(r'^(1\d|[5-9])(.[05]|)$')
    validacion = bool(talla_re.search(talla_buscada))
    return validacion
