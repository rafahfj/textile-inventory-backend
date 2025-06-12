from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector import MySQLConnection
from models.product import ProductCreate, ProductRead
from utils.auth import require_role
from crud.product import (
    create_product_db,
    get_all_products_db,
    get_product_by_id_db,
    delete_product_db
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role(['staff', 'admin']))):
    return create_product_db(product,conn)

@router.get("/", response_model=list[ProductRead] )
def get_products( conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role(['staff', 'admin', 'viewer'])) ):
    return get_all_products_db(conn)

@router.get("/{product_id}/", response_model=ProductRead)
def get_product(product_id: int, conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role(['staff', 'admin', 'viewer']))):
    return get_product_by_id_db(product_id,conn)

@router.delete("/{product_id}/")
def delete_product(product_id: int,  conn: MySQLConnection = Depends(get_db_connection), user = Depends(require_role(['staff', 'admin']))):
    return delete_product_db(product_id,conn)
