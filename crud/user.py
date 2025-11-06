from fastapi import HTTPException
from mysql.connector import Error
from mysql.connector import MySQLConnection
from models.user import UserCreate
from utils.auth import hash_password

def create_user_db(user: UserCreate, conn:MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (user["email"],))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email or Username already registered")

        hashed = hash_password(user["password"])

        cursor.execute(
            "INSERT INTO users (username, fullname, email, password, role) VALUES (%s, %s, %s, %s, %s)",
            (user["username"], user["fullname"],user["email"],hashed, user["role"])
        )
        conn.commit()
        cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
        return cursor.fetchall()
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

