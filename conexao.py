import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3307,        # sua porta do XAMPP
        user='root',
        password='',
        database='db_clinica'
    )
    return conn


# import sqlite3

# def get_connection():
#     # Cria o arquivo db_clinica.db automaticamente se não existir
#     conn = sqlite3.connect("db_clinica.db", check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

