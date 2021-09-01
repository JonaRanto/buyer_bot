#!/usr/bin/python3
'''
Módulos de alertas.
'''

# Importaciones
from mensajes import mensaje
from selenium.webdriver.chrome.webdriver import WebDriver
import winsound
import os

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.1'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
repeticiones_alarma = 3

# Módulos


def alerta_compra(wd: WebDriver):
    '''
    Recibe un WebDriver y lanza una alerta que reproduce un sonido, envia un mensaje por consola y maximiza la ventana.
    '''
    mensaje(1, 'Reproduciendo alarma!')
    wd.minimize_window()
    wd.maximize_window()
    for i in range(repeticiones_alarma):
        winsound.PlaySound(os.getcwd() + '\\alarm', winsound.SND_FILENAME)
