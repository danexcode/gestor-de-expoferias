import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

""" DB_CONFIG = {
    'host': 'localhost', 
    'database': 'gestor_expoferias',
    'user': 'root',
    'password': 'admin'       
} """

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print(f"Conexión exitosa a la base de datos '{DB_CONFIG['database']}'")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    return None

def close_connection(connection):
    """
    Cierra la conexión a la base de datos MySQL.

    Args:
        connection (mysql.connector.connection.MySQLConnection): Objeto de conexión a cerrar.
    """
    if connection and connection.is_connected():
        try:
            connection.close()
            print("Conexión a MySQL cerrada.")
        except Error as e:
            print(f"Error al cerrar la conexión a MySQL: {e}")



if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        # Aquí podrías realizar una operación simple para verificar, por ejemplo,
        # obtener la versión del servidor.
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()
            print(f"Versión del servidor MySQL: {db_version[0]}")
            cursor.close()
        except Error as e:
            print(f"Error al ejecutar una consulta de prueba: {e}")
        finally:
            close_connection(db_connection)