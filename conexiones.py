from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "AGREGA AQUI TU URL"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['shopping_list']


def insertar_datos(articulo, usuario):

    # Create the database for our example (we will use the same database throughout the tutorial
    db = get_database()

    # Create the collection for this example (we will use the same collection throughout the tutorial
    collection = db['articulos']

    # Insert a new record into the collection
    collection.insert_one({"nombre": articulo.get_nombre(), "cantidad": articulo.get_cantidad(
    ), "unidad": articulo.get_unidad(), "usuario": usuario})


def get_lista(usuario):

    # Create the database for our example (we will use the same database throughout the tutorial
    db = get_database()

    # Create the collection for this example (we will use the same collection throughout the tutorial
    collection = db['articulos']

    # Insert a new record into the collection
    return collection.find({"usuario": usuario})


def eliminar_articulo(usuario):
    # Create the database for our example (we will use the same database throughout the tutorial
    db = get_database()

    # Create the collection for this example (we will use the same collection throughout the tutorial
    collection = db['articulos']

    # Insert a new record into the collection
    collection.delete_one({"usuario": usuario})


def contador_articulos(usuario):
    # Create the database for our example (we will use the same database throughout the tutorial
    db = get_database()

    # Create the collection for this example (we will use the same collection throughout the tutorial
    collection = db['articulos']

    # Insert a new record into the collection
    return collection.count_documents({"usuario": usuario})


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    dbname = get_database()
