import serial
import mysql.connector
from datetime import datetime
# Conexión con la bd de mysql
dbConn = mysql.connector.connect(user="root", password="ElCochaLoquis300",
                                 host="localhost", database="weatherdata")

# Se abre el cursor para la bd
cursor = dbConn.cursor()
# Puerto utilizado
arduino = serial.Serial('COM3', 9600, timeout=3)

while True:
    # Lee los datos y elimina los dos ultimos caracteres con el salto de linea
    # Convierte los datos a utf-8
    data = arduino.readline().decode('utf-8')[:-2]
    #Recupera la actual hora, minuto y segundo del reloj
    fecha= datetime.now().strftime('%H:%M:%S')
    # Datos mostrados obtenidos del puerto que  se agregaran a la bd
    pieces = data.split(" ")  #Split de los datos
    print(pieces[0])
    print(pieces[1])
    print(fecha)
    print()
    # Insersión de los datos
    query = "INSERT INTO tempHumDB (humedad, temperatura, tiempoRegistro) VALUES (%s, %s, %s)"
    # Ejecución del query
    cursor.execute(query,(pieces[0],pieces[1],fecha))
    dbConn.commit()
# Se cierra la conexión
cursor.close()

# Puedes llevarlo el martes ya jalando? Que registre en la base de datos todo pls
# Y también ponle un atributo para la hora['25.70']
