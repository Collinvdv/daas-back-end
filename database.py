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

def get_query(query: str):
    conn = get_connection()
    rows = conn.execute(query).fetchall()

    formattedRows = []
    for row in rows:
        formattedRows.append(dict(row))

    return formattedRows

def execute_query(query: str, params: tuple = ()):
    # for writes (insert/update/delete): commit and return affected row count
    conn = get_connection()
    cursor = conn.execute(query, params)
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()

    return rowcount

# -----------
# DATA FUNCTIONS: GET
# -----------
def get_activities():
    return get_query("select * from activities");

def get_users():
    return get_query("select * from users");

# -----------
# DATA FUNCTIONS: DELETE
# -----------
def delete_user(user_id: int):
    # returns number of deleted rows (0 = not found, 1 = deleted)
    return execute_query("delete from users where id = ?", (user_id,))