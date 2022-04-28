import serial
import mysql.connector

# Conexión con la bd de mysql
dbConn = mysql.connector.connect(user="root", password="1234",
                                 host="localhost",
                                 database="weatherdata")

# Se abre el cursor para la bd
cursor = dbConn.cursor()
# Puerto utilizado
arduino = serial.Serial('COM3', 9600, timeout=3)

while True:
    # Lee los datos y elimina los dos ultimos caracteres con el salto de linea
    # Convierte los datos a utf-8
    data = arduino.readline().decode('utf-8')[:-2]
    # Datos mostrados obtenidos del puerto que  se agregaran a la bd
    print(data)
    pieces = data.split(" ")  #Split de los datos
    # Insersión de los datos
    query = "INSERT INTO tempHumDB (humedad, temperatura) VALUES (%s, %s)"
    # Ejecución del query
    cursor.execute(query,((pieces[0],pieces[1]),))
    dbConn.commit()
# Se cierra la conexión
cursor.close()

