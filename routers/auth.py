from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, UserLogin
from utils.auth import hash_password, verify_password, create_access_token
from database import get_db_connection
from utils.auth import require_role
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

# route login
@router.post("/login")
def login_user(user: UserLogin, conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)): # menerima dict login dan mysql connection
    cursor = conn.cursor(dictionary=True)  # variabel method cursor
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))  # execute syntax mysql mencari row user menggunakan email
    db_user = cursor.fetchone()  # melakukan fetch satu row setelah pencarian email
    cursor.close()  # menutup jaringan ke maysql

    if not db_user or not verify_password(user.password, db_user["password"]):  # jika db_user tidak ada hasil atau password pada database dengan password yang dimasukan tidak cocok
        raise HTTPException(status_code=401, detail="Invalid email or password")  # kembalikan pemberitahuan bahwa password salah atau user tidak ditemukan

    token = create_access_token({"email": db_user["email"], "role": db_user["role"],"fullname": db_user["fullname"], "username": db_user["username"], "id": db_user["id"] })
    return {"access_token": token, "token_type": "bearer"} # membuat token dengan body keseluruhan detail user dan mengembalikan tokennya

@router.get("/req-all", response_model=list)
def request_all_user( user = Depends(require_role(['admin'])), conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    cursor.close()

    return all_users