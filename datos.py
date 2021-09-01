#!/usr/bin/python3
'''
Control de datos.
'''

# Importaciones
from configparser import ConfigParser
import os

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
configuracion_file = os.getcwd() + '\\config.ini'

# Leer el archivo de configuracion
config = ConfigParser(interpolation=None)
config.read(configuracion_file)

# Clase principal


class Producto():
    def __init__(self, url: str = None, busqueda_producto: str = None, palabra_clave: str = None, nombre_web: str = None, talla_buscada: str = None, programado: bool = False, fecha_programada: str = None,  hora_programada: str = None, descripcion: str = None):
        '''
        Crea un objeto de tipo Producto.
        '''
        self.url = url
        self.busqueda_producto = busqueda_producto
        self.palabra_clave = palabra_clave
        self.nombre_web = nombre_web
        self.talla_buscada = talla_buscada
        self.programado = programado
        self.fecha_programada = fecha_programada
        self.hora_programada = hora_programada
        self.descripcion = descripcion


class Comprador():
    def __init__(self, numero_comprador: int = 1):
        '''
        Crea un objeto de tipo Comprador obteniendo el numero identificatorio de la configuración.
        '''
        self.email = config.get('comprador-' + str(numero_comprador), 'email')
        self.pwd = config.get('comprador-' + str(numero_comprador), 'pass')

    def contar_compradores(self):
        '''
        Devuelve un int con la cantidad de compradores en la configuración.
        '''
        index = 1
        while True:
            try:
                config.get('comprador-' + str(index), 'email')
                index += 1
            except:
                break
        return index - 1


class Tarjeta():
    def __init__(self):
        '''
        Crea un objeto de tipo Tarjeta con los datos de la configuración.
        '''
        self.nombre_completo = config.get('tarjeta', 'nombre_completo')
        self.rut = config.get('tarjeta', 'rut')
        self.numero_tarjeta = config.get('tarjeta', 'numero_tarjeta')
        self.fecha_expiracion_tarjeta = config.get(
            'tarjeta', 'fecha_expiracion')
