from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.incoming import IncomingCreate, IncomingRead
from utils.auth import require_role
from crud.incoming import (
    create_incoming_db,
    get_all_incoming_db,
    get_incoming_by_id_db,
    delete_incoming_db
)

router = APIRouter(
    prefix="/incoming",
    tags=["Incoming Transactions"]
)

@router.post("/", response_model=IncomingRead)
def create_incoming(data: IncomingCreate, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin'))):
    return create_incoming_db(data, conn)

@router.get("/", response_model=list[IncomingRead])
def get_all_incoming( conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin', 'viewer'))):
    return get_all_incoming_db(conn)

@router.get("/{id}", response_model=IncomingRead)
def get_incoming(id: int, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin', 'viewer'))):
    return get_incoming_by_id_db(id, conn)

@router.delete("/{id}")
def delete_incoming(id: int, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin'))):
    return delete_incoming_db(id, conn)
