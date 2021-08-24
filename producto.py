#!/usr/bin/python3
'''
Control de objetos de tipo Producto.
'''

# Importaciones

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Clase principal


class Producto():
    def __init__(self, url: str = None, nombre_web: str = None, programado: bool = False, fecha_programada: str = None,  hora_programada: str = None, descripcion: str = None):
        '''
        Crea un objeto de tipo Producto.
        '''
        self.url = url
        self.nombre_web = nombre_web
        self.programado = programado
        self.fecha_programada = fecha_programada
        self.hora_programada = hora_programada
        self.descripcion = descripcion
