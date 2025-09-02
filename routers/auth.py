from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from models.user import UserCreate, UserLogin
from utils.auth import hash_password, verify_password, create_access_token
from database import get_db_connection
from utils.auth import require_role
import json
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
def login_user(user: UserLogin, response: Response, conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or email does not registered")
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"email": db_user["email"], "role": db_user["role"],"fullname": db_user["fullname"], "username": db_user["username"], "id": db_user["id"] })
    
    # --- Perubahan di sini ---
    # Durasi 1 hari dalam detik
    max_age_seconds = 60 * 60 * 24 

    # Tentukan apakah ini lingkungan pengembangan (HTTP) atau produksi (HTTPS)
    # Anda bisa membuat variabel lingkungan atau konfigurasi untuk ini
    # Contoh sederhana untuk localhost:
    is_secure_env = True # Biasanya False untuk http://localhost

    response.set_cookie(
        key="access_token",
        value=token,
        max_age=max_age_seconds,
        path="/", # PENTING: Membuat cookie tersedia di seluruh path aplikasi
        domain=None, # Biarkan None atau hapus jika di localhost agar browser menanganinya
                      # Jika di produksi, setel ke domain Anda, misal "example.com"
        secure=is_secure_env, # PENTING: True jika HTTPS, False jika HTTP
        httponly=True, # PENTING: Mencegah akses dari JavaScript (keamanan)
        samesite="None" # PENTING: Atau "None" jika Anda butuh cookie untuk cross-site (dan set secure=True)
    )
    response.set_cookie(
        key="user_info",
        value=json.dumps({"email": db_user["email"], "role": db_user["role"],"fullname": db_user["fullname"], "username": db_user["username"]}),
        max_age=max_age_seconds,
    )
    # --- Akhir Perubahan ---

    return "Login Succesfull"
 # membuat token dengan body keseluruhan detail user dan mengembalikan tokennya

@router.get("/req-all", response_model=list)
def request_all_user( user = Depends(require_role('admin')), conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    cursor.close()

    return all_users