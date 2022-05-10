import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk

mydb = mysql.connector.connect(user="root", password="NuevaContrasenia123",
                                host="localhost", database="weatherdata2")

cursor = mydb.cursor()

sql = "SELECT * FROM temphumdb"
cursor.execute(sql)
rows = cursor.fetchall()
total = cursor.rowcount
print("total data entries:"+str(total))



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
win.mainloop()


