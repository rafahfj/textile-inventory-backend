import mysql.connector
from fastapi import Depends
import os

def get_db_connection():
    conn = mysql.connector.connect(
    host="ballast.proxy.rlwy.net",
    user="root",
    password="TxGoxWtQXRPwyaUNaiOHkixClkQUhPpo",
    database="railway",
    port=48991
)
    
    try:
        yield conn
    finally:
        conn.close()
