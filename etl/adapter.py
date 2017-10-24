import sqlite3
from sqlite3 import Error

database = "C:\\Users\usilisme\OneDrive\Projects\sia\db.sqlite3"

def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return None