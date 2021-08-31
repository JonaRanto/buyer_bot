#!/usr/bin/python3
'''
Módulos de webs.
'''

# Importaciones
from datos import Producto, Comprador, Tarjeta
from mensajes import limpiar_consola, mensaje
from validaciones import validar_web
from bypass import saltar_bypass
from alertas import alerta_compra
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
tiempo_espera_elementos = 10
tarjeta = Tarjeta()

# Módulos


def bold(producto: Producto, numero_comprador: int, wd: WebDriver):
    '''
    Se ejecutan las instrucciones para la web de bold.
    '''
    while True:
        # Ingresar a la URL y limpia la consola
        if producto.busqueda_producto == 'None':
            wd.get(producto.url)
            limpiar_consola(producto, numero_comprador)
        else:
            producto.url = r'https://bold.cl/search/?text=' + producto.busqueda_producto
            wd.get(producto.url)
            limpiar_consola(producto, numero_comprador)

        # Verificar si es está en una cola de queue-it.net
        while True:
            if validar_web(str(wd.current_url))[1] == 'yaneken':
                limpiar_consola(producto, numero_comprador)
                mensaje(1, 'Esperando en cola...')
                # Buscar captcha
                mensaje(1, 'Buscando captcha...')
                if len(wd.find_elements_by_id('divChallenge')) != 0:
                    saltar_bypass(wd)
                else:
                    mensaje(1, 'Captcha no encontrado.')
                time.sleep(3)
            else:
                break

        # Buscar URL de producto a través de una palabra
        try:
            if producto.busqueda_producto != 'None':
                mensaje(1, 'Buscando producto...')
                grilla_productos = wd.find_element_by_xpath('//ul[@class="product__listing product__grid"]')
                lista_productos = grilla_productos.find_elements_by_class_name('name')
                producto_encontrado = False
                for index in range(len(lista_productos)):
                    if lista_productos[index].get_attribute('href').lower().find(producto.palabra_clave) != -1:
                        mensaje(1, 'Producto encontrado.')
                        lista_productos[index].click()
                        producto_encontrado = True
                        break
                if producto_encontrado:
                    producto.url = str(wd.current_url)
                    producto.busqueda_producto = 'None'
                else:
                    error('Producto no encontrado.')
        except Exception as e:
            error(e)

        # Inicia sesion si no está ya iniciada
        try:
            mensaje(1, 'Verificando inicio de sesión...')
            # Obtiene la grilla de sesion
            grilla_sesion = wd.find_element_by_class_name(
                'nav__links--shop_info')
            lista_opciones_sesion = grilla_sesion.find_elements_by_tag_name(
                'li')
            # Verifica si la sesión está iniciada
            if len(lista_opciones_sesion) > 2:
                mensaje(1, 'La sesión ya está iniciada.')
            else:
                mensaje(1, 'Sesión no iniciada. Iniciando sesión...')
                wd.get('https://bold.cl/login')
                user_email = wd.find_element_by_id('j_username')
                user_email.send_keys(Comprador(numero_comprador).email)
                user_pass = wd.find_element_by_id('j_password')
                user_pass.send_keys(Comprador(numero_comprador).pwd)
                boton_login = wd.find_element_by_xpath(
                    '//button[@data-test-login="login_button"]')
                boton_login.click()
                mensaje(1, 'Se ha iniciado la sesión.')
                wd.get(producto.url)
        except Exception as e:
            error(e)

        # Realizar la compra
        try:
            mensaje(1, 'Buscando talla...')
            # Obtiene la grilla de tallas
            grilla_tallas = wd.find_element_by_class_name('sizes-pdp-options')
            lista_tallas = grilla_tallas.find_elements_by_tag_name('a')
            tallas_disponibles = []
            # Recorre la grilla buscando las tallas aún disponibles
            for index in range(len(lista_tallas)):
                if not 'disabled' in lista_tallas[index].get_attribute('class'):
                    tallas_disponibles.append(lista_tallas[index])
            # Si encuentran tallas disponibles, se busca una talla especifica o seselecciona una al azar
            if len(tallas_disponibles) == 0:
                error('No se ha encontrado ninguna talla disponible.')
            else:
                if producto.talla_buscada == 'None':
                    talla_seleccionada = random.choice(tallas_disponibles)
                else:
                    talla_encontrada = False
                    for index in range(len(tallas_disponibles)):
                        if tallas_disponibles[index].text.split(' ')[1] == producto.talla_buscada:
                            talla_seleccionada = tallas_disponibles[index]
                            talla_encontrada = True
                    if not talla_encontrada:
                        error('No se ha encontrado la talla buscada.')
                mensaje(1, 'Se ha seleccionado la talla ' +
                        str(talla_seleccionada.text + '.'))
                talla_seleccionada.click()
                # Intentar añadir al carrito
                try:
                    mensaje(1, 'Añadiendo al carrito...')
                    WebDriverWait(wd, tiempo_espera_elementos).until(ec.presence_of_element_located((By.ID, 'addToCartForm')))
                    formulario_agregar_carro = wd.find_element_by_id(
                        'addToCartForm')
                    if formulario_agregar_carro.text == 'FUERA DE STOCK':
                        error('La talla está sin stock.')
                    else:
                        boton_agregar_carro = wd.find_element_by_id(
                            'addToCartButton')
                        boton_agregar_carro.click()
                        time.sleep(1.5)
                        producto_agregado = wd.find_element_by_xpath(
                            '//*[@id="addToCartLayer"]/div[2]/div[2]/div[1]')
                        # Verifica que el producto se haya añadido correctamente
                        if producto_agregado.text.split()[-1] == '0':
                            error(
                                'El producto no se añadió correctamente al carrito.')
                        else:
                            mensaje(
                                1, 'El producto se ha añadido al carrito correctamente!')
                            ir_carrito = wd.find_element_by_xpath(
                                '//*[@id="addToCartLayer"]/a[1]')
                            ir_carrito.click()
                            mensaje(1, 'Verificando carrito...')
                            # Verificar carrito de compras
                            while True:
                                cantidad_carrito = wd.find_elements_by_xpath(
                                    '//li[@class="item__list--item"]')
                                cantidad_carrito_flag = len(cantidad_carrito)
                                # Verificar si hay mas de un producto en el carrito y elimina todos menos el ultimo agregado
                                if len(cantidad_carrito) > 1:
                                    mensaje(
                                        1, 'Eliminando producto más antiguo...')
                                    eliminar_producto = wd.find_element_by_id(
                                        'actionEntry_0')
                                    eliminar_producto.click()
                                    # Esperar a que cambie la cantidad en el carrito
                                    while True:
                                        cantidad_carrito = wd.find_elements_by_xpath(
                                            '//li[@class="item__list--item"]')
                                        time.sleep(0.5)
                                        if cantidad_carrito_flag != len(cantidad_carrito):
                                            break
                                else:
                                    grilla_sesion = wd.find_element_by_class_name(
                                        'nav__links--shop_info')
                                    lista_opciones_sesion = grilla_sesion.find_elements_by_tag_name(
                                        'li')
                                    contador_carro = lista_opciones_sesion[5]
                                    # Verificar si hay mas de un producto en el carrito y elimina todos menos el ultimo agregado
                                    if int(contador_carro.text) > 1:
                                        WebDriverWait(wd, tiempo_espera_elementos).until(
                                            ec.presence_of_element_located((By.XPATH, '//button[@data-auto-id="label"]')))
                                        cantidad_mismo_producto = wd.find_element_by_id(
                                            'quantity_0')
                                        cantidad_mismo_producto.clear()
                                        cantidad_mismo_producto.send_keys(
                                            '1' + Keys.RETURN)
                                        # Esperar a que el contador del carro se actualice
                                        while True:
                                            contador_carro = wd.find_element_by_xpath(
                                                '//span[@data-auto-id="cart-count"]')
                                            time.sleep(0.5)
                                            if int(contador_carro.text) == 1:
                                                break
                                    mensaje(
                                        1, 'Carrito verificado correctamente!')
                                    break
                            mensaje(1, 'Rellenando datos de compra...')
                            # Intentar finalizar la compra
                            try:
                                boton_finalizar_compra = wd.find_element_by_xpath(
                                    '//div[@class="cart__actions"]/div/div[1]/button')
                                boton_finalizar_compra.click()
                                boton_libreta_direcciones = wd.find_element_by_class_name(
                                    'js-address-book')
                                boton_libreta_direcciones.click()
                                boton_usar_direccion = wd.find_element_by_xpath(
                                    '//*[@id="addressbook"]/div/form/button')
                                boton_usar_direccion.click()
                                boton_medio_pago = wd.find_element_by_id(
                                    'deliveryMethodSubmit')
                                boton_medio_pago.click()
                                seleccionar_tarjeta_credito = wd.find_element_by_id(
                                    'paymentModeCredit')
                                seleccionar_tarjeta_credito.click()
                                boton_datos_tarjeta = wd.find_element_by_id(
                                    'paymentModeSubmit')
                                boton_datos_tarjeta.click()
                                nombre_comprador = wd.find_element_by_id(
                                    'cardholderName')
                                nombre_comprador.send_keys(
                                    tarjeta.nombre_completo)
                                numero_tarjeta = wd.find_element_by_id(
                                    'cardNumber')
                                numero_tarjeta.send_keys(
                                    tarjeta.numero_tarjeta)
                                fecha_expiracion = wd.find_element_by_id(
                                    'expiracy')
                                fecha_expiracion.send_keys(
                                    tarjeta.fecha_expiracion_tarjeta)
                                mensaje(
                                    1, 'Se han llenado los datos de compra correctamente!')
                                alerta_compra(wd)
                                break
                            except Exception as e:
                                error(e)
                except Exception as e:
                    error(e)
        except Exception as e:
            time.sleep(2)
            error(e)


def moredrops(producto: Producto, numero_comprador: int, wd: WebDriver):
    '''
    Se ejecutan las instrucciones para la web de moredrops.
    '''
    while True:
        # Ingresar a la URL y limpia la consola
        if producto.busqueda_producto == 'None':
            wd.get(producto.url)
            limpiar_consola(producto, numero_comprador)
        else:
            producto.url = r'https://moredrops.cl/search/?text=' + producto.busqueda_producto
            wd.get(producto.url)
            limpiar_consola(producto, numero_comprador)

        # Verificar si es está en una cola de queue-it.net
        while True:
            if validar_web(str(wd.current_url))[1] == 'yaneken':
                limpiar_consola(producto, numero_comprador)
                mensaje(1, 'Esperando en cola...')
                # Buscar captcha
                mensaje(1, 'Buscando captcha...')
                if len(wd.find_elements_by_id('divChallenge')) != 0:
                    saltar_bypass(wd)
                else:
                    mensaje(1, 'Captcha no encontrado.')
                time.sleep(3)
            else:
                break

        # Buscar URL de producto a través de una palabra
        try:
            if producto.busqueda_producto != 'None':
                mensaje(1, 'Buscando producto...')
                grilla_productos = wd.find_element_by_xpath('//ul[@class="product__listing product__grid"]')
                lista_productos = grilla_productos.find_elements_by_class_name('name')
                producto_encontrado = False
                for index in range(len(lista_productos)):
                    if lista_productos[index].get_attribute('href').lower().find(producto.palabra_clave) != -1:
                        mensaje(1, 'Producto encontrado.')
                        lista_productos[index].click()
                        producto_encontrado = True
                        break
                if producto_encontrado:
                    producto.url = str(wd.current_url)
                    producto.busqueda_producto = 'None'
                else:
                    error('Producto no encontrado.')
        except Exception as e:
            error(e)

        # Inicia sesion si no está ya iniciada
        try:
            mensaje(1, 'Verificando inicio de sesión...')
            # Obtiene la grilla de sesion
            grilla_sesion = wd.find_element_by_class_name(
                'nav__links--shop_info')
            lista_opciones_sesion = grilla_sesion.find_elements_by_tag_name(
                'li')
            # Verifica si la sesión está iniciada
            if len(lista_opciones_sesion) > 2:
                mensaje(1, 'La sesión ya está iniciada.')
            else:
                mensaje(1, 'Sesión no iniciada. Iniciando sesión...')
                wd.get('https://moredrops.cl/login')
                user_email = wd.find_element_by_id('j_username')
                user_email.send_keys(Comprador(numero_comprador).email)
                user_pass = wd.find_element_by_id('j_password')
                user_pass.send_keys(Comprador(numero_comprador).pwd)
                boton_login = wd.find_element_by_xpath(
                    '//button[@data-test-login="login_button"]')
                boton_login.click()
                mensaje(1, 'Se ha iniciado la sesión.')
                wd.get(producto.url)
        except Exception as e:
            error(e)

        # Realizar la compra
        try:
            mensaje(1, 'Buscando talla...')
            # Obtiene la grilla de tallas
            grilla_tallas = wd.find_element_by_class_name('sizes-pdp-options')
            lista_tallas = grilla_tallas.find_elements_by_tag_name('a')
            tallas_disponibles = []
            # Recorre la grilla buscando las tallas aún disponibles
            for index in range(len(lista_tallas)):
                if not 'disabled' in lista_tallas[index].get_attribute('class'):
                    tallas_disponibles.append(lista_tallas[index])
            # Si encuentran tallas disponibles, se busca una talla especifica o seselecciona una al azar
            if len(tallas_disponibles) == 0:
                error('No se ha encontrado ninguna talla disponible.')
            else:
                if producto.talla_buscada == 'None':
                    talla_seleccionada = random.choice(tallas_disponibles)
                else:
                    talla_encontrada = False
                    for index in range(len(tallas_disponibles)):
                        if tallas_disponibles[index].text.split(' ')[1] == producto.talla_buscada:
                            talla_seleccionada = tallas_disponibles[index]
                            talla_encontrada = True
                    if not talla_encontrada:
                        error('No se ha encontrado la talla buscada.')
                mensaje(1, 'Se ha seleccionado la talla ' +
                        str(talla_seleccionada.text + '.'))
                talla_seleccionada.click()
                # Intentar añadir al carrito
                try:
                    mensaje(1, 'Añadiendo al carrito...')
                    WebDriverWait(wd, tiempo_espera_elementos).until(ec.presence_of_element_located((By.ID, 'addToCartForm')))
                    formulario_agregar_carro = wd.find_element_by_id(
                        'addToCartForm')
                    if formulario_agregar_carro.text == 'FUERA DE STOCK':
                        error('La talla está sin stock.')
                    else:
                        boton_agregar_carro = wd.find_element_by_id(
                            'addToCartButton')
                        boton_agregar_carro.click()
                        time.sleep(1.5)
                        producto_agregado = wd.find_element_by_xpath(
                            '//*[@id="addToCartLayer"]/div[2]/div[2]/div[1]')
                        # Verifica que el producto se haya añadido correctamente
                        if producto_agregado.text.split()[-1] == '0':
                            error(
                                'El producto no se añadió correctamente al carrito.')
                        else:
                            mensaje(
                                1, 'El producto se ha añadido al carrito correctamente!')
                            ir_carrito = wd.find_element_by_xpath(
                                '//*[@id="addToCartLayer"]/a[1]')
                            ir_carrito.click()
                            mensaje(1, 'Verificando carrito...')
                            # Verificar carrito de compras
                            while True:
                                cantidad_carrito = wd.find_elements_by_xpath(
                                    '//li[@class="item__list--item"]')
                                cantidad_carrito_flag = len(cantidad_carrito)
                                # Verificar si hay mas de un producto en el carrito y elimina todos menos el ultimo agregado
                                if len(cantidad_carrito) > 1:
                                    mensaje(
                                        1, 'Eliminando producto más antiguo...')
                                    eliminar_producto = wd.find_element_by_id(
                                        'actionEntry_0')
                                    eliminar_producto.click()
                                    # Esperar a que cambie la cantidad en el carrito
                                    while True:
                                        cantidad_carrito = wd.find_elements_by_xpath(
                                            '//li[@class="item__list--item"]')
                                        time.sleep(0.5)
                                        if cantidad_carrito_flag != len(cantidad_carrito):
                                            break
                                else:
                                    grilla_sesion = wd.find_element_by_class_name(
                                        'nav__links--shop_info')
                                    lista_opciones_sesion = grilla_sesion.find_elements_by_tag_name(
                                        'li')
                                    contador_carro = lista_opciones_sesion[5]
                                    # Verificar si hay mas de un producto en el carrito y elimina todos menos el ultimo agregado
                                    if int(contador_carro.text) > 1:
                                        WebDriverWait(wd, tiempo_espera_elementos).until(
                                            ec.presence_of_element_located((By.XPATH, '//button[@data-auto-id="label"]')))
                                        cantidad_mismo_producto = wd.find_element_by_id(
                                            'quantity_0')
                                        cantidad_mismo_producto.clear()
                                        cantidad_mismo_producto.send_keys(
                                            '1' + Keys.RETURN)
                                        # Esperar a que el contador del carro se actualice
                                        while True:
                                            contador_carro = wd.find_element_by_xpath(
                                                '//span[@data-auto-id="cart-count"]')
                                            time.sleep(0.5)
                                            if int(contador_carro.text) == 1:
                                                break
                                    mensaje(
                                        1, 'Carrito verificado correctamente!')
                                    break
                            mensaje(1, 'Rellenando datos de compra...')
                            # Intentar finalizar la compra
                            try:
                                boton_finalizar_compra = wd.find_element_by_xpath(
                                    '//div[@class="cart__actions"]/div/div[1]/button')
                                boton_finalizar_compra.click()
                                boton_libreta_direcciones = wd.find_element_by_class_name(
                                    'js-address-book')
                                boton_libreta_direcciones.click()
                                boton_usar_direccion = wd.find_element_by_xpath(
                                    '//*[@id="addressbook"]/div/form/button')
                                boton_usar_direccion.click()
                                boton_medio_pago = wd.find_element_by_id(
                                    'deliveryMethodSubmit')
                                boton_medio_pago.click()
                                seleccionar_tarjeta_credito = wd.find_element_by_id(
                                    'paymentModeCredit')
                                seleccionar_tarjeta_credito.click()
                                boton_datos_tarjeta = wd.find_element_by_id(
                                    'paymentModeSubmit')
                                boton_datos_tarjeta.click()
                                nombre_comprador = wd.find_element_by_id(
                                    'cardholderName')
                                nombre_comprador.send_keys(
                                    tarjeta.nombre_completo)
                                numero_tarjeta = wd.find_element_by_id(
                                    'cardNumber')
                                numero_tarjeta.send_keys(
                                    tarjeta.numero_tarjeta)
                                fecha_expiracion = wd.find_element_by_id(
                                    'expiracy')
                                fecha_expiracion.send_keys(
                                    tarjeta.fecha_expiracion_tarjeta)
                                mensaje(
                                    1, 'Se han llenado los datos de compra correctamente!')
                                alerta_compra(wd)
                                break
                            except Exception as e:
                                error(e)
                except Exception as e:
                    error(e)
        except Exception as e:
            error(e)


def adidas(producto: Producto, numero_comprador: int, wd: WebDriver):
    '''
    Se ejecutan las instrucciones para la web de adidas.
    '''
    while True:
        # Ingresar a la URL y limpia la consola
        wd.get(producto.url)
        limpiar_consola(producto, numero_comprador)

        # Inicia sesion si no está ya iniciada
        try:
            mensaje(1, 'Verificando inicio de sesión...')
            time.sleep(1)
            # Obtiene la grilla de sesion
            grilla_sesion = wd.find_element_by_xpath(
                '//div[@data-auto-id="glass-header-top-desktop"]')
            lista_opciones_sesion = grilla_sesion.find_elements_by_tag_name(
                'a')
            # Verifica si la sesión está iniciada
            if not lista_opciones_sesion[-1].text == 'iniciar sesión':
                mensaje(1, 'La sesión ya está iniciada')
            else:
                mensaje(1, 'Sesión no iniciada. Iniciando sesión...')
                lista_opciones_sesion[-1].click()
                WebDriverWait(wd, tiempo_espera_elementos).until(
                    ec.presence_of_element_located((By.ID, 'login-email')))
                user_name = wd.find_element_by_id('login-email')
                user_name.send_keys(Comprador(numero_comprador).email)
                user_pass = wd.find_element_by_id('login-password')
                user_pass.send_keys(Comprador(numero_comprador).pwd)
                boton_login = wd.find_element_by_xpath(
                    '//button[@data-auto-id="login-form-login"]')
                boton_login.click()
                # Esperar que termine de iniciar sesión
                while True:
                    if str(wd.current_url) == 'https://www.adidas.cl/my-account':
                        break
                mensaje(1, 'Se ha iniciado la sesión.')
                wd.get(producto.url)
        except Exception as e:
            error(e)

        # Verificar si se está en una sala de espera
        while True:
            mensaje(1, 'Verificando si se encuentra en una sala de espera...')
            if len(wd.find_elements_by_xpath('//h1[@data-auto-id="product-title"]')) == 0:
                limpiar_consola(producto, numero_comprador)
                mensaje(1, 'Esperando en cola...')
                time.sleep(3)
            else:
                break

        # Realizar la compra
        try:
            mensaje(1, 'Buscando talla con más unidades...')
            # Obtiene la grilla de tallas
            WebDriverWait(wd, tiempo_espera_elementos).until(ec.presence_of_element_located(
                (By.XPATH, '//div[@data-auto-id="size-selector"]')))
            grilla_tallas = wd.find_element_by_xpath(
                '//div[@data-auto-id="size-selector"]')
            lista_tallas = grilla_tallas.find_elements_by_tag_name('span')
            talla_mas_unidades = 0
            selector_talla_flag = 0
            selector_talla = wd.find_element_by_xpath(
                '//div[@data-auto-id="pdp"]/div[2]/div[2]/section/div[1]')
            # Recorre la grilla buscando la talla con mas unidades disponibles y la selecciona
            for i in range(len(lista_tallas)):
                lista_tallas[i].click()
                if (selector_talla.text.split(' ')[-1] == 'almacenes'):
                    if (int(selector_talla.text.split(' ')[-4]) >= talla_mas_unidades):
                        talla_mas_unidades = int(
                            selector_talla.text.split(' ')[-4])
                        selector_talla_flag = i
                elif (selector_talla.text.split(' ')[-1] == 'unidades'):
                    if (10 >= talla_mas_unidades):
                        talla_mas_unidades = 10
                        selector_talla_flag = i
                else:
                    if (20 >= talla_mas_unidades):
                        talla_mas_unidades = 20
                        selector_talla_flag = i
            lista_tallas[selector_talla_flag].click()
            mensaje(1, 'Se ha seleccionado la talla ' +
                    lista_tallas[selector_talla_flag].text + '.')
            # Intentar añadir al carrito
            try:
                mensaje(1, 'Añadiendo al carrito...')
                boton_agregar_carro = wd.find_element_by_xpath(
                    '//button[@data-auto-id="add-to-bag"]')
                boton_agregar_carro.click()
                WebDriverWait(wd, tiempo_espera_elementos).until(ec.presence_of_element_located(
                    (By.XPATH, '//a[@data-auto-id="view-bag-desktop"]')))
                boton_ir_carrito = wd.find_element_by_xpath(
                    '//a[@data-auto-id="view-bag-desktop"]')
                boton_ir_carrito.click()
                mensaje(1, 'Verificando carrito...')
                # Verificar carrito de compras
                while True:
                    cantidad_carrito = wd.find_elements_by_xpath(
                        '//div[@data-auto-id="glass-cart-item-list"]/div/div/div/div/div/div/div/div[2]/div/button')
                    cantidad_carrito_flag = len(cantidad_carrito)
                    # Verificar si hay mas de un producto en el carrito y elimina el más antiguo
                    if len(cantidad_carrito) > 1:
                        mensaje(1, 'Eliminando producto más antiguo...')
                        eliminar_producto = wd.find_element_by_xpath(
                            '//div[@data-auto-id="glass-cart-item-list"]/div/div/div[1]/div/div/div[2]/div/div[2]/div/button')
                        eliminar_producto.click()
                        # Esperar a que cambie la cantidad en el carrito
                        while True:
                            cantidad_carrito = wd.find_elements_by_xpath(
                                '//div[@data-auto-id="glass-cart-item-list"]/div/div/div/div/div/div/div/div[2]/div/button')
                            time.sleep(0.5)
                            if cantidad_carrito_flag != len(cantidad_carrito):
                                break
                    else:
                        contador_carro = wd.find_element_by_xpath(
                            '//span[@data-auto-id="cart-count"]')
                        if int(contador_carro.text) > 1:
                            WebDriverWait(wd, tiempo_espera_elementos).until(
                                ec.presence_of_element_located((By.XPATH, '//button[@data-auto-id="label"]')))
                            boton_cantidad_mismo_producto = wd.find_element_by_xpath(
                                '//button[@data-auto-id="label"]')
                            boton_cantidad_mismo_producto.click()
                            boton_cantidad_mismo_producto.send_keys(
                                '1' + Keys.RETURN)
                            # Esperar a que el contador del carro se actualice
                            while True:
                                contador_carro = wd.find_element_by_xpath(
                                    '//span[@data-auto-id="cart-count"]')
                                time.sleep(0.5)
                                if int(contador_carro.text) == 1:
                                    break
                        mensaje(1, 'Carrito verificado correctamente!')
                        break
                boton_ir_pagar = wd.find_element_by_xpath(
                    '//button[@data-auto-id="glass-checkout-button-bottom"]')
                boton_ir_pagar.click()
                # Intentar finalizar la compra
                mensaje(1, 'Rellenando datos de compra...')
                WebDriverWait(wd, tiempo_espera_elementos).until(ec.presence_of_element_located(
                    (By.XPATH, '//div[@data-auto-id="billingAddress-fiscalDocument"]')))
                tipo_documento = wd.find_element_by_xpath(
                    '//div[@data-auto-id="billingAddress-fiscalDocument"]')
                tipo_documento.click()
                selector_documento = wd.find_element_by_xpath(
                    '//select[@data-auto-id="billingAddress-fiscalDocument"]')
                lista_documento = selector_documento.find_elements_by_tag_name(
                    'option')
                for index in range(len(lista_documento)):
                    if (lista_documento[index].text.find('Boleta') != -1):
                        lista_documento[index].click()
                        break
                rut = wd.find_element_by_id('billingAddress-documentValue')
                rut.send_keys(tarjeta.rut)
                mensaje(1, 'Se ha seleccionado el tipo de documento correctamente.')
                boton_finalizar_compra = wd.find_element_by_xpath(
                    '//button[@data-auto-id="review-and-pay-button"]')
                boton_finalizar_compra.click()
                # Rellenar datos de tarjeta
                WebDriverWait(wd, tiempo_espera_elementos).until(
                    ec.presence_of_element_located((By.ID, 'card-number')))
                numero_tarjeta = wd.find_element_by_id('card-number')
                numero_tarjeta.send_keys(tarjeta.numero_tarjeta)
                nombre_comprador = wd.find_element_by_id('name')
                nombre_comprador.send_keys(tarjeta.nombre_completo)
                fecha_expiracion = wd.find_element_by_id('expiryDate')
                fecha_expiracion.send_keys(tarjeta.fecha_expiracion_tarjeta)
                mensaje(1, 'Se han llenado los datos de compra correctamente!')
                alerta_compra(wd)
                break
            except Exception as e:
                error(e)
        except Exception as e:
            error(e)


def error(msg):
    '''
    Recibe un mensaje, se imprime junto a un mensaje de recargar pagina y espera un segundo.
    '''
    mensaje(2, str(msg))
    mensaje(1, 'Recargando página...')
    time.sleep(1)
