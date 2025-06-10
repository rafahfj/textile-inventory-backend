from fastapi import Depends, HTTPException
from mysql.connector import Error, MySQLConnection
from database import get_db_connection
from models.product import ProductCreate

def create_product_db(
    product: ProductCreate, 
    conn: MySQLConnection 
):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO products (name, type, color, unit, price, min_stock, current_stock, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product.name,
            product.type,
            product.color,
            product.unit,
            product.price,
            product.min_stock,
            product.current_stock,
            product.supplier_id
        ))
        conn.commit()
        product_id = cursor.lastrowid

        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return cursor.fetchone()

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_all_products_db(
    conn: MySQLConnection 
):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_product_by_id_db(
    product_id: int,
    conn: MySQLConnection 
):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    finally:
        cursor.close()

def delete_product_db(
    product_id: int,
    conn: MySQLConnection 
):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        return {"message": "Product deleted successfully"}
    finally:
        cursor.close()
