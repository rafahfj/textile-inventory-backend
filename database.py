import mysql.connector
from fastapi import Depends
import os

def get_db_connection():
    conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE", "railway"),
    port=int(os.getenv("MYSQLPORT", 48991))
)
    
    try:
        yield conn
    finally:
        conn.close()
