import mysql.connector
import os

config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_SCHEMA'),
    'port': os.getenv('DB_PORT'),
    'raise_on_warnings': True
}

class DBClient:

    __connection = None

    @classmethod
    def connect(cls):
        if not cls.__connection:
            cls.__connection = mysql.connector.connect(**config)
        return cls.__connection
