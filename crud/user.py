from fastapi import HTTPException
from mysql.connector import Error, MySQLConnection
from models.user import UserCreate
import hashlib

def create_user_db(user: UserCreate, conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """, (user.username, hashed_password, user.role))
        conn.commit()
        user_id = cursor.lastrowid

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()


def get_all_users_db(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
