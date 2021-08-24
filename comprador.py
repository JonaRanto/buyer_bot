#!/usr/bin/python3
'''
Control de objetos de tipo Comprador.
'''

# Importaciones

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Clase principal


class Comprador():
    def __init__(self, email: str, pwd: str, rut: str, nombre_completo: str, numero_tarjeta: str, fecha_expiracion_tarjeta: str):
        '''
        Crea un objeto de tipo Comprador.
        '''
        self.email = email
        self.pwd = pwd
        self.rut = rut
        self.nombre_completo = nombre_completo
        self.numero_tarjeta = numero_tarjeta
        self.fecha_expiracion_tarjeta = fecha_expiracion_tarjeta
