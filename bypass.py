#!/usr/bin/python3
'''
Módulos de bypass.
'''

# Importaciones
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from mensajes import mensaje
import time
import os
import urllib.request


# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
speetch_to_text_url = "https://speech-to-text-demo.ng.bluemix.net/"
audioFile = "\\payload.mp3"

# Módulos

def saltar_bypass(wd: WebDriver):
    '''
    Verifica si en la página actual hay un captcha de google y lo resuelve.
    '''
    mensaje(1, 'Reconociendo ReCaptcha...')
    # Busca el elemento que contiene el iframe del captcha
    g_recaptcha = wd.find_element_by_xpath('//div[@id="challenge-container"]/div/div')
    # Dentro del elemento de g_recaptcha busca el elemento con el tag iframe y le hace click
    outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    outerIframe.click()

    mensaje(1, 'Resolviendo ReCaptcha...')
    # Guarda una lista de elementos con la clase iframe
    iframes = wd.find_elements_by_tag_name('iframe')
    
    audioBtnFound = False
    audioBtnIndex = -1

    # Repite la cantidad de elementos iframes que se encontraron
    for index in reversed(range(len(iframes))):
        # Switch_to cambia algunas opciones del objeto obtenido
        wd.switch_to.default_content()
        iframe = wd.find_elements_by_tag_name('iframe')[index]
        # Se ubica en el frame (Los frames son marcos incrustados por otras páginas)
        wd.switch_to.frame(iframe)
        try:
            WebDriverWait(wd, 2).until(ec.presence_of_element_located((By.ID, 'recaptcha-audio-button')))
            audioBtn = wd.find_element_by_id("recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception:
            pass
    
    if audioBtnFound:
        try:
            while True:
                mensaje(1, 'Obteniendo Url del audio...')
                # Obtiene la url del audio
                WebDriverWait(wd, 2).until(ec.presence_of_element_located((By.ID, 'audio-source')))
                src = wd.find_element_by_id("audio-source").get_attribute("src")
                mensaje(1, 'Audio src: %s' % src)

                # Descarga el audio (payload.mp3)
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Conversor de voz a texto
                key = AudioToText(os.getcwd() + audioFile, wd)
                mensaje(1, 'Recaptcha Key: %s' % key)

                # Vuelve a ubicarse en el frame del recaptcha
                wd.switch_to.default_content()
                iframe = wd.find_elements_by_tag_name('iframe')[audioBtnIndex]
                wd.switch_to.frame(iframe)

                # Introduce la key en el input y presiona enter
                inputField = wd.find_element_by_id("audio-response")
                inputField.send_keys(key)
                time.sleep(2)
                inputField.send_keys(Keys.ENTER)

                # Si no hay error avanza
                time.sleep(5)
                try:
                    help_button = wd.find_element_by_id('recaptcha-help-button')
                    help_button.click()
                except ElementClickInterceptedException:
                    mensaje(1, 'Se ha resuelto el captcha!')
                    break
                    
        except Exception as e:
            mensaje(2, e)
            mensaje(2, 'Posiblemente ha sido bloqueado por google')
            pass
    else:
        mensaje(2, 'No se encuentra el botón de reproduccion de audio')
        pass


def AudioToText(audioFile, wd):
    '''
    Recibe un archivo de audio y devuelve un str con la transcripción
    '''
    # Ejecuta un script que abre una nueva pestaña
    wd.execute_script('''window.open("","_blank")''')
    # Se cambia a la nueva pestaña
    wd.switch_to.window(wd.window_handles[1])
    # Entra a la url para el cambio de voz a texto
    wd.get(speetch_to_text_url)

    time.sleep(2)
    # Ubica el elemento de subida de archivo mp3 y le envia la ubicacion del payload.mp3
    audioInput = wd.find_element_by_xpath('//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(10)

    text = wd.find_element_by_xpath(
        '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = wd.find_element_by_xpath(
            '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    # Cierra la pestaña actual
    wd.close()
    # Cambia a la primera pestaña
    wd.switch_to.window(wd.window_handles[0])

    # Retorna un string con la key
    return result
