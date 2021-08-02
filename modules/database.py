import sqlite3 as sql
import time
import hashlib


db = sql.connect(r'database.sqlite', check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS downloads(process_id, file_name, status, ip_addr)")


def create_process_id() -> str:
    id = hashlib.md5(str(time.time()).encode()).hexdigest()
    return id


def add_data(file_name: str, ip_addr: str) -> str:

    process_id = create_process_id()
    cursor.execute(
        f"INSERT INTO downloads VALUES ('{process_id}', '{file_name}', 'False', '{ip_addr}')"
        )
    db.commit()

    return process_id


def change_status(process_id: str) -> None:
    cursor.execute(
        f"UPDATE downloads SET status = 'True' WHERE process_id = '{process_id}'"
        )
    db.commit()


def check_status(process_id: str) -> str:
    cursor.execute(
        f"SELECT status FROM downloads WHERE process_id = '{process_id}'"
        )
    z = cursor.fetchone()

    return z


def download(process_id: str) -> str:
    cursor.execute(
        f"SELECT file_name FROM downloads WHERE process_id = '{process_id}'"
        )
    z = cursor.fetchone()

    return z
