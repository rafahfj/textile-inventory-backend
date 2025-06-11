import mysql.connector
import os
import time
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("MYSQLHOST")
user = os.getenv("MYSQLUSER", "root")
password = os.getenv("MYSQLPASSWORD")
database = os.getenv("MYSQLDATABASE", "railway")
port = int(os.getenv("MYSQLPORT", "3306"))

def get_db_connection():
    retries = 5
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            yield conn
            break
        except mysql.connector.Error as e:
            print(f"Koneksi ke database gagal: {e}")
            time.sleep(3)  # tunggu 3 detik sebelum mencoba lagi
    else:
        raise Exception("Gagal terkoneksi ke database setelah beberapa kali percobaan.")
