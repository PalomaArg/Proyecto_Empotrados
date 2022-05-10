# -*- coding: utf-8 -*-

import pandas as pd  # import Pandas library from sqlalchemy 
 
import mysql.connector

my_conn = mysql.connector.connect(user="root", password="1234",
                                 host="localhost",
                                 database="weatherdata2")

query = "SELECT * FROM temphumdb ORDER BY weatherDataID"
df = pd.read_sql(query, my_conn)
lb = [row for row in df['humedad']]  # Labels of graph

plot=df.plot.bar(title="Niveles de humedad ",y='humedad');
