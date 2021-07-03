//Diego Hiriart y Luis Corales
#include<DHT.h>//Para utilizar DHT22
#include<SoftwareSerial.h>//Para puertos seriaes del HC-05

SoftwareSerial HC05_HiriartCorales(10, 11);

#define PinDHT22 7
#define tipoDHT DHT22
String datos;//Para guardar los datos de temperatura y humedad
DHT DHT22HC(PinDHT22, tipoDHT);

void setup() {
  Serial.begin(9600);//Debug
  HC05_HiriartCorales.begin(9600);//Comunicacion por BT
  DHT22HC.begin();//Iniciliza el DHT
}

void loop() {
  datos="";//Resetear cadena de datos
  
  datos=String(DHT22HC.readTemperature())+",";//Leer datos del sensor y guardarlos en la cadena
  datos+=String(DHT22HC.readHumidity());

  datos.concat("\n");//Salto de linea a los datos, permite lectura con python linea a linea

  HC05_HiriartCorales.write(datos.c_str());//Envia los datos por bluetooth converidos a una cadena tipo C para que pueda usarla el HC05
  Serial.write(datos.c_str());//Debug

  delay(1200000);//Tomar mediciones cada 20 mins (1200000 ms)
}
