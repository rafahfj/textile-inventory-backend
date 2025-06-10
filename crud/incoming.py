from fastapi import HTTPException, Depends
from mysql.connector import Error, MySQLConnection
from database import get_db_connection
from models.incoming import IncomingCreate

def create_incoming_db(data: IncomingCreate, conn: MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO stock_in (product_id, qty, date, user_id, note)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.product_id,
            data.qty,
            data.date,
            data.user_id,
            data.note
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM stock_in WHERE id = %s", (new_id,))
        return cursor.fetchone()
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_all_incoming_db(conn: MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM stock_in")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_incoming_by_id_db(id: int, conn: MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM stock_in WHERE id = %s", (id,))
        record = cursor.fetchone()
        if not record:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return record
    finally:
        cursor.close()

def delete_incoming_db(id: int, conn: MySQLConnection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stock_in WHERE id = %s", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")
        conn.commit()
        return {"message": "Transaction deleted"}
    finally:
        cursor.close()
