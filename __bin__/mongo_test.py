""" Ejemplo de insert en mongo """
# Para correrlo:
# 1. Levantar base de datos en mongo
# 2. Ejecutar python __bin__/mongo_test.py

import datetime
from pymongo import MongoClient

# Esto se va a usar cuando tengamos la base de datos en Heroku
# import os
# dbUrl= os.environ.get('DATABASE_URL')

DB_URL = 'mongodb://localhost:27017/'

CLIENT = MongoClient(DB_URL)

# Obtengo una referencia a la BBDD 'test'
DB = CLIENT.test

# Obtengo una referencia a la collection/tabla 'posts'
POSTS = DB.posts

POST = {"author": "Mike", "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# Inserto un post y obtengo su id
POST_ID = POSTS.insert_one(POST).inserted_id

print(POST_ID)
# En la base hacer: db.posts.find({}) y va a mostrar nuestro registro