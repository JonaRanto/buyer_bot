#!/usr/bin/python3
'''
Módulos de interfaz gráfica.
'''

# Importaciones
from datos import Producto, Comprador
from tkinter import *
from tkinter import messagebox
from validaciones import validar_formato_hora, validar_web
from tkcalendar import Calendar
import datetime as dt
import sys

# Metadatos
__author__ = 'Jonathan Navarro Vega'
__version__ = '1.0.0'
__email__ = 'jonathan@ranto.cl'
__status__ = 'developer'

# Variables
cantidad_compradores = Comprador().contar_compradores()
compradores = []
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
    url_producto = StringVar()
    url_producto.set(r'https://moredrops.cl/Drops/Men/Footwear/Sneakers-Men/Zapatilla-Nike-x-Undercover-Dunk-High-1985-%27UBA%27/p/NIDD9401600')
    compra_programada = BooleanVar()
    fecha_actual = dt.datetime.now()
    hora_evento = StringVar()
    comprador = StringVar()

    root.title('Interfaz gráfica buyer_bot')
    root.resizable(False, False)

    frame = Frame(root)
    frame.pack()

    label_descripcion_producto = Label(frame, text='Descripción: ')
    label_descripcion_producto.grid(row=0, column=0, sticky=E, pady=5, padx=10)
    input_descripcion_producto = Entry(
        frame, width=40, textvariable=descripcion_producto)
    input_descripcion_producto.grid(row=0, column=1, padx=10)

    label_url_producto = Label(frame, text='Url: ')
    label_url_producto.grid(row=1, column=0, sticky=E, pady=5, padx=10)
    input_url_producto = Entry(frame, width=40, textvariable=url_producto)
    input_url_producto.grid(row=1, column=1, padx=10)

    for i in range(cantidad_compradores):
        compradores.append(Comprador(i + 1).email)

    label_comprador = Label(frame, text='Comprador: ')
    label_comprador.grid(row=2, column=0, sticky=E, pady=5, padx=10)
    drop_comprador = OptionMenu(frame, comprador, *compradores)
    drop_comprador.grid(row=2, column=1, sticky=W, padx=10)
    comprador.set(compradores[0])

    def programar_compra():
        '''
        Activa y desactiva las opciones de compra programada.
        '''
        if compra_programada.get():
            label_programar_fecha.grid(
                row=4, column=0, sticky=E, pady=5, padx=10)
            input_programar_fecha.grid(row=4, column=1, padx=10)
            input_programar_fecha['mindate'] = fecha_actual
            label_programar_hora.grid(
                row=5, column=0, sticky=E, pady=5, padx=10)
            input_programar_hora.grid(row=5, column=1, sticky=W, padx=10)
        else:
            label_programar_fecha.grid_forget()
            input_programar_fecha.grid_forget()
            label_programar_hora.grid_forget()
            input_programar_hora.grid_forget()

    chk_box_compra_programada = Checkbutton(
        frame, text='Programar', variable=compra_programada, command=programar_compra)
    chk_box_compra_programada.grid(row=3, column=1, sticky=W, padx=10)

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
        Valida url y hora y en caso de pasar la validación, finaliza la interfaz gráfica.
        '''
        validacion_web = validar_web(url_producto.get())
        validado = False
        if not validacion_web[0]:
            messagebox.showerror('[ERROR]', 'La URL no es valida.')
        elif compra_programada.get():
            if not validar_formato_hora(hora_evento.get()):
                messagebox.showerror(
                    '[ERROR]', 'Formato de hora incorrecto. Ejemplo de formato: (08:30).')
            else:
                validado = True
        else:
            validado = True
        if validado:
            producto.url = url_producto.get()
            producto.nombre_web = validacion_web[1]
            producto.programado = compra_programada.get()
            producto.fecha_programada = input_programar_fecha.get_date()
            producto.hora_programada = hora_evento.get()
            producto.descripcion = descripcion_producto.get()
            for i in range(cantidad_compradores):
                if comprador.get() == Comprador(i + 1).email:
                    global comprador_flag 
                    comprador_flag = i + 1
                    break
            root.destroy()

    button_start = Button(frame, text='Comenzar', command=start)
    button_start.grid(row=6, column=0, columnspan=2, pady=5)

    def cerrar_ventana():
        sys.exit()

    root.protocol('WM_DELETE_WINDOW', cerrar_ventana)
    root.mainloop()

    return [producto, comprador_flag]
