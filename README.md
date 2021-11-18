# HiriartCorales-DBTemperaturaHumedad
### [Diego Hiriart](https://github.com/Diego-Hiriart) & [Luis Corales](https://github.com/LuisCorales)

Proyecto de computación ubicua para recolección y análisis de datos de temperatura y humedad en el tiempo.

- El control de Arduino con su sensor de temperatura y humedad y módulo Bluetooth se logra mediante un sketch de Arduino. Con un script de Python se almacena la información recolectada por el Arduino y se la puede graficar.
- Con el sketch de Arduino se logra lo siguiente:
    - Recolectar datos de humedad y temperatura en intervaloes de tiempo predefinidos.
    - Enviar a un computador, mediante Bluetooth, la información recolectada.
- Un script de Python, que cuenta con dos posibles argumentos de ejecución, permite:
    - Guardar en una base de datos la información recibida por Bluetooth.
    - Recuperar información de la base de datos para graficar los valores de temperatura y humedad que se han recolectado.
