""" Facilita la operacion con la base de datos de mongo """
import os
from pymongo import MongoClient

# Url de base de datos de prueba
DEF_DB_URL = 'mongodb://localhost:27017/test'

MONGODB_URI = os.getenv('MONGODB_URI', '')
DATABASE_URL = os.getenv('DATABASE_URL', '')

DB_URL = None

if MONGODB_URI:
    print('Variable de entorno MONGODB_URI detectada')
    DB_URL = MONGODB_URI
if DATABASE_URL:
    print('Variable de entorno DATABASE_URL detectada')
    DB_URL = DATABASE_URL

if not DB_URL:
    print("""Variables de entorno DATABASE_URL o MONGODB_URI no definidas,
    usando url de BBDD por defecto: """, DEF_DB_URL)
    DB_URL = 'mongodb://localhost:27017/'

CLIENT = MongoClient(DB_URL, maxPoolSize=5)

def get_client():
    """ Obtiene un cliente de mongo para operar """
    return CLIENT

def get_database(db_name='test'):
    """ Obtiene una base de datos de mongo con la cual operar. El nombre por defecto es test """
    client = get_client()
    return client[db_name]

def get_table(table_name, db_name='test'):
    """ Obtiene una tabla/coleccion con la cual operar. """
    database = get_database(db_name)
    return database[table_name]

def get_locations_by_type(type):
    return []

def main():
    """ Modulo principal para pruebas """
    posts = get_table('posts')
    post = {"author": "Mike", "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]}

    # Inserto un post y obtengo su id
    post_id = posts.insert_one(post).inserted_id
    print(post_id.__str__())

if __name__ == '__main__':
    main()
