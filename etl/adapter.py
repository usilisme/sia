import os
import sqlite3
from sqlite3 import Error

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database = os.path.join(root, 'db.sqlite3')


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
