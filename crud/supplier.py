from fastapi import HTTPException, Depends
from mysql.connector import Error,MySQLConnection
from database import get_db_connection
from models.supplier import SupplierCreate

def create_supplier_db(supplier: SupplierCreate, conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO suppliers (name, contact, address)
            VALUES (%s, %s, %s)
        """, (
            supplier.name,
            supplier.contact,
            supplier.address
        ))
        conn.commit()
        supplier_id = cursor.lastrowid

        cursor.execute("SELECT * FROM suppliers WHERE id = %s", (supplier_id,))
        return cursor.fetchone()

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_all_suppliers_db(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM suppliers")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_supplier_by_id_db(supplier_id: int, conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM suppliers WHERE id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    finally:
        cursor.close()

def delete_supplier_db(supplier_id: int, conn: MySQLConnection):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM suppliers WHERE id = %s", (supplier_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Supplier not found")
        conn.commit()
        return {"message": "Supplier deleted successfully"}
    finally:
        cursor.close()
