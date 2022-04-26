#include <SPI.h>
#include <LiquidCrystal_I2C.h> 
#include<Wire.h>

/*
  Este codigo toma datos recolectados de un sensor de humedad conectado a la entrada analogica A0.
  El LED es un auxiliar que muestra cuando se estan recolectado los datos.
*/

LiquidCrystal_I2C lcd(0x27 ,16,2); //Creación el objeto lcd  dirección  0x27 y 16 columnas x 2 filas
int sensorPin = A0;   // Entrada analogica del sensor
int ledPin = 13;      // Salida del LED
int sensorValue = 0;  // Valor inicial del sensor
String humedad = "Humedad: "; //Texto en pantalla

void setup() {
  lcd.init(); // Inicializar el LCD
  lcd.backlight(); //Encender la luz de fondo
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  lcd.setCursor(0,0); //Ubicación de las lineas del mensaje de humedad
  lcd.print(humedad);
  sensorValue = analogRead(sensorPin);
  lcd.setCursor(10,0);
  lcd.print(sensorValue,1);//1 decimal
  Serial.println(sensorValue); //Imprime en consola el valor recolectado por el sensor
  //El LED parpadea y da 1 segundo de delay en los que se toma la proxima muestra
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);
}
