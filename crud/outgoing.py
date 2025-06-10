from fastapi import HTTPException
from mysql.connector import Error, MySQLConnection
from models.outgoing import OutgoingCreate

def create_outgoing_db(data: OutgoingCreate, conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO stock_out (product_id, qty, date, purpose, user_id, note)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.product_id,
            data.qty,
            data.date,
            data.purpose,
            data.user_id,
            data.note
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM stock_out WHERE id = %s", (new_id,))
        return cursor.fetchone()
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_all_outgoing_db(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM stock_out")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_outgoing_by_id_db(id: int, conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM stock_out WHERE id = %s", (id,))
        record = cursor.fetchone()
        if not record:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return record
    finally:
        cursor.close()

def delete_outgoing_db(id: int, conn: MySQLConnection):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stock_out WHERE id = %s", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")
        conn.commit()
        return {"message": "Transaction deleted"}
    finally:
        cursor.close()
