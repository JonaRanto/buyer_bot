from conexion import conectar_wd
from programacion import programar_compra
from mensajes import mensaje
from datos import Producto
import webs
import sys

def elegir_web(numero_comprador: int, url, busqueda_producto, palabra_clave, nombre_web, talla_buscada, programado, fecha_programada,  hora_programada, descripcion):
    '''
    Recibe el numero del comprador los datos para crear un objeto de tipo Producto y ejecuta el código correspondiente a la web del producto.
    '''
    producto = Producto()
    producto.url = url
    producto.busqueda_producto = busqueda_producto
    producto.palabra_clave = palabra_clave
    producto.nombre_web = nombre_web
    producto.talla_buscada = talla_buscada
    producto.programado = bool(programado)
    producto.fecha_programada = fecha_programada
    producto.hora_programada = hora_programada
    producto.descripcion = descripcion

    # Programar compra
    if producto.programado:
        programar_compra(producto, numero_comprador)

    if producto.nombre_web == 'bold':
        # Conexion WebDriver
        wd = conectar_wd()
        webs.bold(producto, numero_comprador, wd)
    elif producto.nombre_web == 'moredrops':
        # Conexion WebDriver
        wd = conectar_wd()
        webs.moredrops(producto, numero_comprador, wd)
    elif producto.nombre_web == 'adidas':
        # Conexion WebDriver
        wd = conectar_wd()
        webs.adidas(producto, numero_comprador, wd)
    else:
        mensaje(2, 'Se ha recibido un nombre de web invalido: ' + str(producto.nombre_web))

    mensaje(3, 'No cerrar esta consola hasta terminar la venta...')
    input('Presione ENTER para cerrar la consola.')

if __name__== '__main__':
    globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
