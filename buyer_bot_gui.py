#!/usr/bin/python3
'''
Módulos de interfaz gráfica.
'''

# Importaciones
from archivos import cargar_json
from datos import Producto, Comprador
from tkinter import *
from tkinter import messagebox
from validaciones import validar_formato_hora, validar_web, validar_talla
from tkcalendar import Calendar
import datetime as dt
import os
import sys

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.4.3'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
webs_disponibles_file = os.getcwd() + '\\webs_disponibles.json'
webs = []
lista_cantidad_compradores = []
global comprador_flag

# Módulos


def gui():
    '''
    Muestra la interfaz gráfica del buyer_bot y devuelve una lista con un objeto de tipo Producto y el numero del comprador.
    '''
    root = Tk()

    producto = Producto()

    # Variables locales
    descripcion_producto = StringVar()
    buscar_producto = BooleanVar()
    busqueda_producto = StringVar()
    palabra_clave = StringVar()
    web_name = StringVar()
    url_producto = StringVar()
    talla_unica = BooleanVar()
    talla_buscada = StringVar()
    compra_programada = BooleanVar()
    fecha_actual = dt.datetime.now()
    hora_evento = StringVar()
    compradores = StringVar()

    root.title('Interfaz gráfica buyer_bot')
    root.resizable(False, False)

    frame = Frame(root)
    frame.pack()

    label_descripcion_producto = Label(frame, text='Descripción: ')
    label_descripcion_producto.grid(row=0, column=0, sticky=E, pady=5, padx=10)
    input_descripcion_producto = Entry(
        frame, width=40, textvariable=descripcion_producto)
    input_descripcion_producto.grid(row=0, column=1, padx=10)

    def buscar_producto_sin_url():
        '''
        Activa y desactiva la opción de buscar un producto sin URL.
        '''
        if buscar_producto.get():
            label_url_producto.grid_forget()
            input_url_producto.grid_forget()
            label_buscar_producto.grid(row=2, column=0, sticky=E, pady=5, padx=10)
            input_buscar_producto.grid(row=2, column=1, padx=10)
            label_palabra_clave.grid(row=3, column=0, sticky=E, pady=5, padx=10)
            input_palabra_clave.grid(row=3, column=1, sticky=W, padx=10)
            label_web.grid(row=4, column=0, sticky=E, pady=5, padx=10)
            drop_web.grid(row=4, column=1, sticky=W, padx=10)
        else:
            label_url_producto.grid(row=2, column=0, sticky=E, pady=5, padx=10)
            input_url_producto.grid(row=2, column=1, padx=10)
            label_buscar_producto.grid_forget()
            input_buscar_producto.grid_forget()
            label_palabra_clave.grid_forget()
            input_palabra_clave.grid_forget()
            label_web.grid_forget()
            drop_web.grid_forget()
            
    chk_box_buscar_producto = Checkbutton(
        frame, text='Buscar producto sin url', variable=buscar_producto, command=buscar_producto_sin_url)
    chk_box_buscar_producto.grid(row=1, column=1, sticky=W, padx=10)

    label_buscar_producto = Label(frame, text='Buscar por por texto: ')
    input_buscar_producto = Entry(frame, width=40, textvariable=busqueda_producto)

    label_palabra_clave = Label(frame, text='Palabra clave: ')
    input_palabra_clave = Entry(frame, width=20, textvariable=palabra_clave)

    for i in cargar_json(webs_disponibles_file):
        if i.get('web_name') != 'yaneken' and i.get('web_name') != 'adidas':
            webs.append(str(i.get('web_name')))

    label_web = Label(frame, text='Web: ')
    drop_web = OptionMenu(frame, web_name, *webs)
    web_name.set(webs[0])

    label_url_producto = Label(frame, text='Url: ')
    label_url_producto.grid(row=2, column=0, sticky=E, pady=5, padx=10)
    input_url_producto = Entry(frame, width=40, textvariable=url_producto)
    input_url_producto.grid(row=2, column=1, padx=10)

    for i in range(Comprador().contar_compradores()):
        lista_cantidad_compradores.append(i + 1)

    label_comprador = Label(frame, text='Cantidad de compradores: ')
    label_comprador.grid(row=5, column=0, sticky=E, pady=5, padx=10)
    drop_comprador = OptionMenu(frame, compradores, *lista_cantidad_compradores)
    drop_comprador.grid(row=5, column=1, sticky=W, padx=10)
    compradores.set(lista_cantidad_compradores[0])

    def buscar_talla_unica():
        '''
        Activa y desactiva la opción de buscar por una talla unica.
        '''
        if talla_unica.get():
            label_talla_buscada.grid(row=7, column=0, sticky=E, pady=5, padx=10)
            input_talla_buscada.grid(row=7, column=1, sticky=W, padx=10)
            label_no_disponible_adidas.grid(row=7, column=1, pady=5, padx=10)
        else:
            label_talla_buscada.grid_forget()
            input_talla_buscada.grid_forget()
            label_no_disponible_adidas.grid_forget()

    chk_box_buscar_talla_unica = Checkbutton(
        frame, text='Buscar talla única', variable=talla_unica, command=buscar_talla_unica)
    chk_box_buscar_talla_unica.grid(row=6, column=1, sticky=W, padx=10)
    label_no_disponible_adidas = Label(frame, text='ⓘ No disponible en Adidas')

    label_talla_buscada = Label(frame, text='Talla buscada: ')
    label_talla_buscada.grid_forget()
    input_talla_buscada = Entry(frame, width=4, textvariable=talla_buscada)
    input_talla_buscada.grid_forget()

    def programar_compra():
        '''
        Activa y desactiva las opciones de compra programada.
        '''
        if compra_programada.get():
            label_programar_fecha.grid(
                row=9, column=0, sticky=E, pady=5, padx=10)
            input_programar_fecha.grid(row=9, column=1, padx=10)
            input_programar_fecha['mindate'] = fecha_actual
            label_programar_hora.grid(
                row=10, column=0, sticky=E, pady=5, padx=10)
            input_programar_hora.grid(row=10, column=1, sticky=W, padx=10)
        else:
            label_programar_fecha.grid_forget()
            input_programar_fecha.grid_forget()
            label_programar_hora.grid_forget()
            input_programar_hora.grid_forget()

    chk_box_compra_programada = Checkbutton(
        frame, text='Programar', variable=compra_programada, command=programar_compra)
    chk_box_compra_programada.grid(row=8, column=1, sticky=W, padx=10)

    label_programar_fecha = Label(
        frame, text='Fecha programada: ')
    input_programar_fecha = Calendar(
        frame, selectmode='day', showweeknumbers=False, date_pattern='dd-mm-y')
    input_programar_fecha.grid_forget()

    label_programar_hora = Label(frame, text='Hora: ')
    input_programar_hora = Entry(frame, width=5, textvariable=hora_evento)
    input_programar_hora.insert(END, '08:30')
    input_programar_hora.grid_forget()

    def start():
        '''
        Valida url, hora y talla, en caso de pasar la validación, finaliza la interfaz gráfica.
        '''
        validacion_web = validar_web(url_producto.get())
        validacion_talla = validar_talla(talla_buscada.get())
        validado = False
        if not validacion_web[0] and not buscar_producto.get():
            messagebox.showerror('[ERROR]', 'La URL no es valida.')
        elif talla_unica.get() and not validacion_talla:
            messagebox.showerror('[ERROR]', 'Formato de la talla incorrecto. Ejemplo de formato: (11.5).')
        elif compra_programada.get() and not validar_formato_hora(hora_evento.get()):
            messagebox.showerror('[ERROR]', 'Formato de hora incorrecto. Ejemplo de formato: (08:30).')
        else:
            validado = True
        if validado:
            if buscar_producto.get():
                producto.busqueda_producto = busqueda_producto.get()
                producto.palabra_clave = palabra_clave.get()
                producto.nombre_web = web_name.get()
            else:
                producto.url = url_producto.get()
                producto.nombre_web = validacion_web[1]
            if talla_unica.get():
                producto.talla_buscada = talla_buscada.get()
            producto.programado = compra_programada.get()
            producto.fecha_programada = input_programar_fecha.get_date()
            producto.hora_programada = hora_evento.get()
            producto.descripcion = descripcion_producto.get()
            root.destroy()

    button_start = Button(frame, text='Comenzar', command=start)
    button_start.grid(row=11, column=0, columnspan=2, pady=5)

    def cerrar_ventana():
        '''
        Cierra la aplicación.
        '''
        sys.exit()

    root.protocol('WM_DELETE_WINDOW', cerrar_ventana)
    root.mainloop()

    return [producto, int(compradores.get())]
