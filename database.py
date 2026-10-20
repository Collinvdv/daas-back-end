import sqlite3
from pathlib import Path

# -----------
# DB CORE FUNCTIONS
# -----------
def get_connection():
    # path naar de sql lite db
    DB_FILE = Path(__file__).parent / "pulsetrack.db"

    # Effectief connectie met sqllite en maak reference naar conn
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # rows behave like dictionaries
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def get_query(query: str, params: tuple = ()):
    # for reads: always close the connection, even when the query fails
    conn = get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    formattedRows = []
    for row in rows:
        formattedRows.append(dict(row))

    return formattedRows

def execute_query(query: str, params: tuple = ()):
    # for writes (insert/update/delete): commit and return affected row count
    conn = get_connection()
    try:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()   # release the write lock when the statement fails
        raise
    finally:
        conn.close()

def insert_query(query: str, params: tuple = ()):
    # for inserts: commit and return the id of the new row
    conn = get_connection()
    try:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()   # release the write lock when the statement fails
        raise
    finally:
        conn.close()

# -----------
# DATA FUNCTIONS: GET
# -----------
def get_activities():
    return get_query("select * from activities");

def get_activity(activity_id: int):
    # returns one activity as dict, or None when not found
    rows = get_query("select * from activities where id = ?", (activity_id,))
    return rows[0] if rows else None

def get_users():
    return get_query("select * from users");

# -----------
# DATA FUNCTIONS: INSERT
# -----------
def create_activity(user_id: int, sport: str, title: str, started_at: str, duration_s: int, distance_m: float):
    # returns id of the newly created activity
    return insert_query(
        "insert into activities (user_id, sport, title, started_at, duration_s, distance_m) values (?, ?, ?, ?, ?, ?)",
        (user_id, sport, title, started_at, duration_s, distance_m),
    )

# -----------
# DATA FUNCTIONS: DELETE
# -----------
def delete_user(user_id: int):
    # returns number of deleted rows (0 = not found, 1 = deleted)
    return execute_query("delete from users where id = ?", (user_id,))