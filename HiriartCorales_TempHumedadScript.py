
"""
Diego Hiriart, Luis Corales
ISW2401-01 COmputación ubicua
2021-Julio-01

@author: DiegoH
@author: LuisC
"""

from serial import Serial
from datetime import datetime#Para el campo de fecha y hora
import pyodbc#Para la base de datos
import numpy as np#Librerias para los graficos
import matplotlib.pyplot as plt
from os import environ
import sys#Librerias para salir del programa
import signal
import time#Para el sleep que permite esperar a borrar el buffer serial

def salir(signal, frame):#Se llama esta funcion si en algún momento se presiona el keyboard interrupt
    print("Programa terminado")
    sys.exit(0)
    
def conectarDB():
    server = "localhost\MSSQLSERVERDEV"
    base = "TempHumedad-HiriartCorales"
    conexion = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER="+server+";DATABASE="+base+";Trusted_Connection=yes;")
    return conexion

def ignorarADvertencias():#Hace que no aparexcan las advertencias al crear el grafico
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"
    
def main(arg):
    if(len(arg)>1 or len(arg)==0):
        print("No ha ingresado el número correcto de argumentos")
    else:
        if(arg[0]=="registro"):
            try:
                BTHiriartCorales = Serial(port = 'COM18', baudrate = 9600, timeout = None)
                #Serial.flushInput(BTHiriartCorales)#Limpia el buffer, pues estarian todos los datos que envio el Arduino antes de la ejecucion del script
                #time.sleep(1)#Delay para que se borre el buffer antes de continuar
                while(True):
                    datos=""#Vaciar string de datos
                    signal.signal(signal.SIGINT, salir)#Si se presiona el comando para keyboard interrupt, se llama esta funcion
                    while(BTHiriartCorales.inWaiting() == 0):
                        pass
                    lecturaCOM = (BTHiriartCorales.readline().decode('utf-8'))
                    datos = lecturaCOM.split(',')
                    if(len(datos)==2):#Solo continuar si se leyo bien
                        #Guardar datos en la base
                        temp = float(datos[0])
                        humedad = float(datos[1])
                        fechaHora = datetime.now()
                        print(fechaHora.strftime("%Y/%m/%d"),", ",fechaHora.strftime("%H:%M:%S"),", ",temp,", ",humedad)       
                        consola=conectarDB().cursor()#Consola para ejecutar comandos
                        #Insercion de datos en la tabla de la base de datos
                        consola.execute("INSERT INTO FechaTempHumedad (FechaHora, Temperatura, Humedad) values(?, ?, ?)",
                                        (fechaHora, temp, humedad))
                        consola.commit()#Para guardar la insercion
                
            except Exception as error:
                print("Se desconectó el sensor, reconecte y ejecute de nuevo")
                print(error)#Para debug
            finally:
                BTHiriartCorales.close()#Cierra el puerto
        elif(arg[0]=="graficar"):
            fechaHora = np.array([])
            temp = np.array([])
            humedad = np.array([])
            consola=conectarDB().cursor()#Consola para ejecutar comandos
            lecturas = consola.execute("SELECT * FROM FechaTempHumedad")#Leer datos
            for i in lecturas:
                fechaHora = np.append(fechaHora, str(i[1].strftime("%Y/%m/%d\n%H:%M:%S")))
                temp = np.append(temp, i[2])
                humedad = np.append(humedad, i[3])
                
            #Graficos
            print("\nCreando grafico de temperatura y humedad")
            ignorarADvertencias()
            figura = plt.figure(figsize=(30,20))
            plt.subplot(311)
            plt.title("Análisis de datos de temperatura y humedad en el tiempo")            
            plt.xlabel("Tiempo (fechas)")
            plt.ylabel("Valores")
            plt.plot(fechaHora, temp, 'r', label="Temperatura C°")
            plt.plot(fechaHora, humedad, 'b', label="Humedad %")
            plt.legend()
            plt.grid(True)            
            plt.show()
            
            print("\nPrograma terminado")
            
            
            
        else:
            print("No ingresó un parámetro válido. \nIngrese 'registro' para guardar datos y 'graficar' para ver el análisis de datos")
    
if __name__=="__main__":
    main(sys.argv[1:])#Llamar a main
