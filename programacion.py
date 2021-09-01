#!/usr/bin/python3
'''
Módulos de programacion.
'''

# Importaciones
from mensajes import limpiar_consola, mensaje
from datos import Producto
import datetime as dt
import time

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.2'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Módulos


def programar_compra(producto: Producto, numero_comprador: int):
    '''
    Recibe un objeto de tipo Producto y espera en un bucle hasta llegar a la hora indicada.
    '''
    # Variables locales
    lista_fecha = [int(n) for n in producto.fecha_programada.split('-')]
    lista_hora = [int(n) for n in producto.hora_programada.split(':')]
    fecha_actual = dt.datetime.now().strftime('%d-%m-%Y %H:%M')
    fecha_programada = dt.datetime(
        lista_fecha[2], lista_fecha[1], lista_fecha[0], lista_hora[0], lista_hora[1]).strftime('%d-%m-%Y %H:%M')
    while True:
        if fecha_actual < fecha_programada:
            limpiar_consola(producto, numero_comprador)
            mensaje(1, 'Esperando evento... (' + fecha_programada + ')')
            fecha_actual = dt.datetime.now().strftime('%d-%m-%Y %H:%M')
            time.sleep(3)
        else:
            break
