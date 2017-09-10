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
* correr el comando **python api/app.py** para levantar la app con el servidor de pruebas de Flask

## Reporte de cobertura
El reporte de cobertura de código se generará en .coverage luego de correr el comando **nosetests --with-coverage**

## Linter
Para correr el linter de la aplicacion, correr el comando **pylint --rcfile=.pylintrc api test model > linterReport** y el reporte se generara en linterReport

## Tests
Para correr los tests de la aplicación, correr el comando **pytest test/**
