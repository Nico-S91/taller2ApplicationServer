# Application Server
[![Build Status](https://travis-ci.org/Nico-S91/taller2ApplicationServer.svg?branch=master)](https://travis-ci.org/Nico-S91/taller2ApplicationServer)
<a href='https://coveralls.io/github/Nico-S91/taller2ApplicationServer?branch=master'><img src='https://coveralls.io/repos/github/Nico-S91/taller2ApplicationServer/badge.svg?branch=master' alt='Coverage Status' /></a>

## Prerequisitos
Para poder correr la aplicación, es necesario contar con:
* Python v >= 3.5

## Instalación
Previo a iniciar el server, es necesario correr los siguientes comandos:
* pip install -r requirements.txt

## Inicio
Para iniciar el server, se debe:
* el puerto por defecto de la aplicacion va a ser 5000 (sin gunicorn)
* correr el comando **python main_app.py** para levantar la app con el servidor de pruebas de Flask

Para iniciar el servidor corriendo sobre Gunicorn:
* Ejecutar el comando "gunicorn main_app" (sin las comillas)
* La aplicacion sera levantada sobre localhost, puerto 8000 (http://localhost:8000 o 127.0.0.1:8000)

La aplicacion esta hosteada en Heroku, para acceder a ella:
* Ingesar a taller2-application-server.herokuapp.com
* poner luego una url correspondiente al listado de los servicios de endpoints disponibles

## Reporte de cobertura
El reporte de cobertura de código se generará en coverageReport luego de correr el comando **coverage report > coverageReport**

## Linter
Para correr el linter de la aplicacion, correr el comando **pylint --rcfile=.pylintrc api test model > linterReport** y el reporte se generara en linterReport

## Tests
Para correr los tests de la aplicación, correr el comando **pytest test/**

##Levantar MongoDB en UBUNTU
Para levantar la instancia de MongoDB correr el comando **sudo service mongod start**

#REPORTEEEES
correr **pydoc -w <url_de_archivo>**

#Coverage reports
i. correr **coverage run main_app.py**
ii. correr **coverage report**
iii. correr **coverage html**
iv. se va a haber creado la carpeta "htmlcov" con el reporte en formato html

##Nombre de google api Key
llevame-grupo6: AIzaSyC0Ro5dttq9RUlR78Lta4_exF8fIK1qgxM

##Docker
correr **docker-compose up** en el directorio del proyecto! (si tira error, probablemente es que la version en linux es '2' y hay un '3'!!)