from fastapi import APIRouter, Depends
from database import get_db_connection  # custom dependency to get MySQL connection
import mysql.connector

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def get_dashboard_summary(conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM products")
    total_products = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(qty) AS total FROM stock_in")
    total_stock_in = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT SUM(qty) AS total FROM stock_out")
    total_stock_out = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT COUNT(*) AS total FROM suppliers")
    total_suppliers = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT id, name, current_stock, min_stock
        FROM products
        WHERE current_stock < min_stock
    """)
    low_stock_products = cursor.fetchall()

    cursor.execute("SELECT price, current_stock FROM products")
    products = cursor.fetchall()
    total_inventory_value = sum([p["price"] * p["current_stock"] for p in products])

    cursor.close()

    return {
        "total_products": total_products,
        "total_stock_in": total_stock_in,
        "total_stock_out": total_stock_out,
        "total_suppliers": total_suppliers,
        "low_stock_products": low_stock_products,
        "total_inventory_value": total_inventory_value
    }
