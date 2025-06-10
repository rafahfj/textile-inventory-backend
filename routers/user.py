from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.user import UserCreate, UserRead
from crud.user import create_user_db, get_all_users_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, conn: MySQLConnection = Depends(get_db_connection)):
    return create_user_db(user, conn)

@router.get("/", response_model=list[UserRead])
def get_users(conn: MySQLConnection = Depends(get_db_connection)):
    return get_all_users_db(conn)
