from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.supplier import SupplierCreate, SupplierRead
from utils.auth import require_role
from crud.supplier import (
    create_supplier_db,
    get_all_suppliers_db,
    get_supplier_by_id_db,
    delete_supplier_db
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)

@router.post("/", response_model=SupplierRead)
def create_supplier(supplier: SupplierCreate,conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin'))):
    return create_supplier_db(supplier, conn)

@router.get("/", response_model=list[SupplierRead])
def get_suppliers( conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin', 'viewer'))):
    return get_all_suppliers_db(conn)

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin', 'viewer'))):
    return get_supplier_by_id_db(supplier_id, conn)

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int,conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role('staff', 'admin'))):
    return delete_supplier_db(supplier_id, conn)
