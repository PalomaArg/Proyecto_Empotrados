# -*- coding: utf-8 -*-

import pandas as pd 
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
import tkinter as tk
from tkinter import *
from tkinter import ttk


class GUI(object):

    def __init__(self, parent):
        self.root = parent
        
        
        datos= self.info()
        label = tk.Label(root, text="Nivel de humedad actual: "+ datos[0])
        label.pack()
        label = tk.Label(root, text="Estado: "+datos[1])
        label.pack()
           
        self.root.title("Main")
        self.frame = tk.Frame(parent)
        self.frame.pack()
    
        btnHumedad = tk.Button(self.frame, text="Niveles de humedad",
                        command=self.humedadfrm)
        btnHumedad.pack()
        
        btnTemperatura = tk.Button(self.frame, text="Niveles de temperatura",
                        command=self.temperaturafrm)
        btnTemperatura.pack()
        
        btnEstado = tk.Button(self.frame, text="Estados de la bomba",
                        command=self.estadosfrm)
        btnEstado.pack()
        
        btnPastel = tk.Button(self.frame, text="Estados",
                        command=self.grafica_pastel)
        btnPastel.pack()
        


    def estadosfrm(self):
        '''
        Función que muestra una tabla con los datos de id, humedad, temperatura,
        tiempoRegistro y estadoBomba.

        '''
        
        my_conn = mysql.connector.connect(user="root", password="NuevaContrasenia123",
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
        win.geometry("1000x400")
        win.resizable(False, False)
        my_conn.close()
        win.mainloop()

    def temperaturafrm(self):
        '''
        Función que displiega una pantalla con una gráfica de barra mostrando las niveles
        de temperaturas de cada registro
        '''
        my_conn = mysql.connector.connect(user="root", password="NuevaContrasenia123",
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

    def humedadfrm(self):
        '''
        Función que despliega una pantalla con una gráfica de barra que muestra la humedad
        de cada registro.
        '''
        my_conn = mysql.connector.connect(user="root", password="NuevaContrasenia123",
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
        
        
    def grafica_pastel(self):
        '''
        Función que despliega una pantalla con una gráfica de pastel con los datos
        del estadoBomba
        '''
        contadorPositivo=0
        contadorNegativo=0
        root= tk.Tk()
        my_conn = mysql.connector.connect(user="root", password="NuevaContrasenia123",
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
        
    def info(self):
        
        my_conn = mysql.connector.connect(user="root", password="NuevaContrasenia123",
                                          host="localhost",
                                          database="weatherdata2")
        sql="SELECT humedad, estadoBomba from temphumdb ORDER BY weatherDataID DESC LIMIT 1"
        cursor=my_conn.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        data = rows[0]
        my_conn.close()
        return str(data[0]),str(data[1])
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = GUI(root)
    root.mainloop()

    
