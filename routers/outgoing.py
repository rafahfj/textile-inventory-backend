from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.outgoing import OutgoingCreate, OutgoingRead
from crud.outgoing import (
    create_outgoing_db,
    get_all_outgoing_db,
    get_outgoing_by_id_db,
    delete_outgoing_db
)

router = APIRouter(
    prefix="/outgoing",
    tags=["Outgoing Transactions"]
)

@router.post("/", response_model=OutgoingRead)
def create_outgoing(data: OutgoingCreate, conn: MySQLConnection = Depends(get_db_connection)):
    return create_outgoing_db(data, conn)

@router.get("/", response_model=list[OutgoingRead])
def get_all_outgoing(conn: MySQLConnection = Depends(get_db_connection)):
    return get_all_outgoing_db(conn)

@router.get("/{id}", response_model=OutgoingRead)
def get_outgoing(id: int, conn: MySQLConnection = Depends(get_db_connection)):
    return get_outgoing_by_id_db(id, conn)

@router.delete("/{id}")
def delete_outgoing(id: int, conn: MySQLConnection = Depends(get_db_connection)):
    return delete_outgoing_db(id, conn)
