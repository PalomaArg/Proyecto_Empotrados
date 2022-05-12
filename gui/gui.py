import webbrowser
import re
import sys
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from pathlib import Path
import pandas as pd 
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
import tkinter as tk
from tkinter import *
from tkinter import ttk


# Path usados para el diseño, error mostrado 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tkdesigner.designer import Designer
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add tkdesigner to the PATH.")


ASSETS_PATH = Path(__file__).resolve().parent / "assets"

path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label

def estadosfrm():
        '''
        Función que muestra una tabla con los datos de id, humedad, temperatura,
        tiempoRegistro y estadoBomba.

        '''
        
        my_conn = mysql.connector.connect(user="root", password="1234",
                                           host="localhost",
                                           database="weatherdata2")
        cursor = my_conn.cursor()

        sql = "SELECT * FROM temphumdb"
        cursor.execute(sql)
        rows = cursor.fetchall()
        total = cursor.rowcount

        win = Tk()
        frm = Frame(win)
        frm.pack(side=tk.LEFT, padx=5)

        tv = ttk.Treeview(frm, columns=(1,2,3,4,5), show="headings", height="8")
        tv.pack()
        tv.heading(1, text="weatherDataID")
        tv.heading(2, text="humedad")
        tv.heading(3, text="temperatura")
        tv.heading(4, text="tiempoRegistro")
        tv.heading(5, text="estadoBomba")
        
        for i in rows:
            tv.insert('',tk.END,values=i)

        win.title("Datos")
        win.geometry("1000x200")
        win.resizable(False, False)
        my_conn.close()
        win.mainloop()
        
def temperaturafrm():
        '''
        Función que displiega una pantalla con una gráfica de barra mostrando las niveles
        de temperaturas de cada registro
        '''
        my_conn = mysql.connector.connect(user="root", password="1234",
                                          host="localhost",
                                          database="weatherdata2")

        query = "SELECT * FROM temphumdb ORDER BY weatherDataID"
        df = pd.read_sql(query, my_conn)

        df1 = DataFrame(df, columns=['weatherDataID', 'temperatura'])
        root = tk.Tk()

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = df1[['weatherDataID', 'temperatura']].groupby('weatherDataID').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Niveles de temperatura')
        
        root.mainloop()
        my_conn.close()

def humedadfrm():
        '''
        Función que despliega una pantalla con una gráfica de barra que muestra la humedad
        de cada registro.
        '''
        my_conn = mysql.connector.connect(user="root", password="1234",
                                          host="localhost",
                                          database="weatherdata2")

        query = "SELECT * FROM temphumdb ORDER BY weatherDataID"
        df = pd.read_sql(query, my_conn)

        df1 = DataFrame(df, columns=['weatherDataID', 'humedad'])
        root = tk.Tk()

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = df1[['weatherDataID', 'humedad']].groupby('weatherDataID').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Niveles de humedad')
        
        root.mainloop()
        my_conn.close()

def info():
        '''
        Función que despliega la información al inicio
        del último registro.
        '''
        my_conn = mysql.connector.connect(user="root", password="1234",
                                          host="localhost",
                                          database="weatherdata2")
        sql="SELECT humedad, estadoBomba from temphumdb ORDER BY weatherDataID DESC LIMIT 1"
        cursor=my_conn.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        data = rows[0]
        my_conn.close()
        return str(data[0]),str(data[1])
        
datos= info()
window = tk.Tk()
logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
window.title("Sistema automático")

window.geometry("862x519")
window.configure(bg="#3A7FF6")
canvas = tk.Canvas(
    window, bg="#3A7FF6", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")


token_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)

URL_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)

path_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)


canvas.create_text(
    573.5, 88.0, text=" Seleccione un botón",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="Sistema de riego automático", bg="#3A7FF6",
    fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(
    text="Para conocer más información\n"
    "sobre el estado de su planta\n"
    "haga click en los botones\n"
    "que se encuentran de lado izquierdo.\n\n"

    "Estado actual: "+ datos[1],
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=200.0)


info_text = tk.Label(
    text=""

    "Nivel de humedad: "+ datos[0],
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=400.0)

generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=humedadfrm)
generate_btn.place(x=557, y=350, width=180, height=55)

generate_btn_img2 = tk.PhotoImage(file=ASSETS_PATH / "generate2.png")
generate_btn = tk.Button(
    image=generate_btn_img2, borderwidth=0, highlightthickness=0,
    command=temperaturafrm, relief="flat")
generate_btn.place(x=557, y=250, width=180, height=55)

generate_btn_img3 = tk.PhotoImage(file=ASSETS_PATH / "generate3.png")
generate_btn = tk.Button(
    image=generate_btn_img3, borderwidth=0, highlightthickness=0,
    command=estadosfrm, relief="flat")
generate_btn.place(x=557, y=150, width=180, height=55)

window.resizable(False, False)
window.mainloop()

        
def grafica_pastel(self):
        '''
        Función que despliega una pantalla con una gráfica de pastel con los datos
        del estadoBomba
        '''
        contadorPositivo=0
        contadorNegativo=0
        root= tk.Tk()
        my_conn = mysql.connector.connect(user="root", password="1234",
                                          host="localhost",
                                          database="weatherdata2")
        sql="SELECT estadoBomba FROM temphumdb"
        cursor=my_conn.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        for i in datos:
            if i[0]=="ACTIVADO":
                contadorPositivo=contadorPositivo+1
            elif i[0]=="DESACTIVADO":
                contadorNegativo=contadorNegativo+1

        estado = [contadorPositivo,contadorNegativo]
        nombres = ["Estado Activo","Estado inactivo"]
        colores = ["#60D394","#EE6055"]
        plt.pie(estado, labels=nombres, autopct="%0.1f %%", colors=colores)
        plt.show()
        
        root.mainloop()
        my_conn.close()
        
