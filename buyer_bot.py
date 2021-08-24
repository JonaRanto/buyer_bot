'''
Bot de compras online automaticas.
'''
# Importaciones
from buyer_bot_gui import gui
from programacion import programar_compra
from conexion import conectar_wd
import webs

# Código
producto = gui()

# Programar compra
if producto.programado:
    programar_compra(producto)

# Elegir web
if producto.nombre_web == 'moredrops' or producto.nombre_web == 'yaneken':
    # Conexion WebDriver
    wd = conectar_wd()
    webs.moredrops(producto, wd)
elif producto.nombre_web == 'adidas':
    # Conexion WebDriver
    wd = conectar_wd()
    webs.adidas(producto, wd)