# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, UserLogin
from utils.auth import hash_password, verify_password, create_access_token
from database import get_db_connection
import mysql.connector

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register_user(user: UserCreate, conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    cursor.execute("""
        INSERT INTO users (username, fullname, email, password, role)
        VALUES (%s, %s, %s, %s, %s)
    """, (user.username, user.fullname, user.email, hashed_pw, user.role))
    conn.commit()
    cursor.close()

    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin, conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}
