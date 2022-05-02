# -*- coding: utf-8 -*-

import pandas as pd 
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
import tkinter as tk

class GUI(object):

    def __init__(self, parent):
        self.root = parent
        label = tk.Label(root, text="Nivel de humedad actual: ")
        label.pack()
        label = tk.Label(root, text="Estado: ")
        label.pack()
        self.root.title("Main")
        self.frame = tk.Frame(parent)
        self.frame.pack()
        btn = tk.Button(self.frame, text="Niveles de humedad",
                        command=self.humedadfrm)
        btn.pack()

    def humedadfrm(self):
        my_conn = mysql.connector.connect(user="root", password="ElCochaLoquis300",
                                          host="localhost",
                                          database="weatherdata")

        query = "SELECT * FROM humedadtb ORDER BY weatherDataID"
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



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = GUI(root)
    root.mainloop()
