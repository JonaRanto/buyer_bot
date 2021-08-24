#!/usr/bin/python3
'''
Módulos de bypass.
'''

# Importaciones
from mensajes import mensaje
from selenium.webdriver.chrome.webdriver import WebDriver


# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables


# Módulos

def saltar_bypass(wd: WebDriver):
    '''
    Verifica si en la página actual hay un captcha de google y lo resuelve.
    '''
    mensaje(1, 'Reconociendo ReCaptcha...')
    g_recaptcha = wd.find_element_by_xpath('//div[@id="challenge-container"]/div/div')
    # Dentro del elemento de g_recaptcha busca el elemento con el tag iframe y le hace click
    outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    outerIframe.click()
    mensaje(1, 'Resolviendo ReCaptcha...')
    wait = input('esperando...')