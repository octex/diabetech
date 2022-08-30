# Diabetech
Pequeña cartilla para turnos, controles, insumos y demás datos que requiere mantener al día una persona con diabetes.


## Instalacion y configuracion

Este proyecto funciona con Python 3.X

Es necesario tener instalado Python y pip para poder configurar correctamente el proyecto.

A continuacion se muestra como configurar el entorno y, adicionalmente, como crear un servicio que ejecute de manera automatica diabetech.

### Instancia local

1. Crear un virtual environment:

```
python3 -m venv ./venv
```


2. Activarlo:

```
source venv/bin/activate
```


3. Instalar las dependencias:

```
pip install -r requirements.txt
```
4. Ejecutar `run.sh`
```
./run.sh
```
La instancia local de Diabetech ya esta lista!

### Diabetech como servicio

1. Realizar los pasos anteriores hasta el numero 3.


2. Modificar el archivo `diabetech.service` en las siguientes lineas:

```
WorkingDirectory=/absolute/path/to/diabetech/folder/
ExecStart=bash /absolute/path/to/diabetech/folder/run.sh
```
Por defecto, el archivo tiene el directorio absoluto de una 
Raspberry Pi pero es necesario que se modifique de acuerdo a donde se este levantando el proyecto.


3. Una vez modificado el archivo, ejecutar la siguiente linea:

```
sudo cp diabetech.service /etc/systemd/system/
```

Al hacer esto vamos a poder levantar el servicio y poder administrarlo desde ahi


4. Iniciamos el servicio:

```
sudo systemctl start diabetech.service
```
Procedemos a confirmar que este funcionando de manera correcta ingresando al navegador: `<ip maquina host>:5000/`
> Para saber la ip en la que se esta ejecutando introducimos ifconfig o ipconfig
>


5. Si vemos que responde bien y el sistema funciona, habilitamos el servicio:

```
sudo systemctl enable diabetech.service
```
A partir de este momento, cada vez que se reinicie la maquina, el servicio iniciara automaticamente.


6. Por ultimo si deseamos revisar logs o ver el estado del servicio, ingresamos:

```
sudo systemctl status diabetech.service
```

## Acceso a la base de datos

Por defecto, la aplicacion crea una base de datos por archivo con el motor SQLite3. Dentro de la base habra solo una tabla llamada `controles`

Para acceder a la tabla basta con solo tener un cliente SQLite3 por consola:


1. Instalamos el cliente (si es que ya no lo tenemos):

```
sudo apt-get install sqlite3
```


2. Nos paramos en el directorio donde este el proyecto


3. Ejecutamos el cliente y abrimos el archivo de la base:

```
sqlite3
.open diabetech.db
```
>Recomiento ejecutar `.headers on` y `.mode column` para una mejor visualizacion de las queries
>

A partir de aqui, es posible ejecutar cualquier query SQL soportada por el motor.


## Actualizaciones y uso de la app

Con el paso del tiempo, la idea es ir agregando mas features y mejoras al proyecto.
El uso via web es sencillo y practico (dependiendo a quien le preguntes) La idea detras de este proyecto tambien es que quien quiera y lo desee pueda modificarlo a gusto en caso de no gustarle la experiencia por defecto.
Por ese mismo motivo, lo que trae de base la aplicacion esta abierto a cualquier modificacion y agregado que se desee.

