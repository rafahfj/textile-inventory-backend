import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()

host = os.getenv("MYSQLHOST")
user = os.getenv("MYSQLUSER", "root")
password = os.getenv("MYSQLPASSWORD")
database = os.getenv("MYSQLDATABASE", "railway")
port = int(os.getenv("MYSQLPORT", "3306"))

def get_db_connection():
     # Mengambil URL koneksi dari variabel lingkungan
    db_url = os.environ.get("DATABASE_URL") # Sesuai dengan nama variabel yang Anda buat di Railway

    if not db_url:
        raise Exception("DATABASE_URL environment variable is not set!")

    # Parsing URL koneksi (karena MYSQL_URL akan dalam format URL)
    parsed_url = urlparse(db_url)

    # Mendapatkan komponen koneksi
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 3306
    user = parsed_url.username
    password = parsed_url.password
    database = parsed_url.path.strip('/') # Menghilangkan '/' di awal nama database

    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        if not connection.is_connected():
            raise Exception("Failed to establish database connection")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        raise Exception(f"Failed to connect to database: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during database connection: {e}")
        raise