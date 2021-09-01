#!/usr/bin/python3
'''
Módulos de conexion.
'''

# Importaciones
from mensajes import mensaje
from selenium.common.exceptions import SessionNotCreatedException
import os

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.1'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
chromedriver_file = os.getcwd() + '\\chromedriver.exe'

# Módulos


def conectar_wd():
    '''
    Realiza la conexion entre WebDriver y Chrome.
    '''
    # Importaciones locales
    from selenium import webdriver as wd

    # Configuracion de WebDriver
    config_chrome = wd.ChromeOptions()
    # Forzar el inicio de la web para un dispositivo compatible.
    config_chrome.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    config_chrome.add_argument('--disable-notifications')
    config_chrome.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    try:
        # Ejecuta el controlador de chrome ubicado en la raiz y le pasa las opciones configuradas
        wd = wd.Chrome(executable_path=chromedriver_file,
                       options=config_chrome)
    except SessionNotCreatedException:
        mensaje(2, 'Version de ChromeDriver y Chrome no compatibles,')
    return wd
