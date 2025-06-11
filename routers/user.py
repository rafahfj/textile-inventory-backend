from fastapi import APIRouter, Depends, HTTPException, security
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.user import UserCreate, UserRead, UserLogin
from crud.user import create_user_db, get_all_users_db
from utils.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserRead)
def create_user(user: UserCreate, conn: MySQLConnection = Depends(get_db_connection)):
    return create_user_db(user, conn)

@router.post("/login", response_model=UserRead)
def login(login: UserLogin, conn: MySQLConnection = Depends(get_db_connection)):
    user = authenticate_user(login, conn)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}