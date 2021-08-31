from datos import Producto
import sys
import os
import json

producto = Producto()
producto.url = 'www.google.cl'

print(json.dumps(producto))

# def hola(producto: Producto):
#     print('Id-Proceso: ' + str(os.getpid()))
#     print('Hola, la url es ' + producto.url)
#     input('Presione cualquier tecla para finalizar.')




# if __name__== '__main__':
#     globals()[sys.argv[1]](producto)