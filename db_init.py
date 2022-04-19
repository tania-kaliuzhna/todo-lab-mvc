import sqlite3

from config import DB_NAME, TASK_LIST_TABLE, TASK_TABLE

conn = sqlite3.connect(DB_NAME)

conn.execute(f"""
    CREATE TABLE {TASK_LIST_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE
    );
""")

conn.execute(f"""
    CREATE TABLE {TASK_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    done BOOLEAN NOT NULL,
    {TASK_LIST_TABLE}_id INTEGER NOT NULL,
    FOREIGN KEY ({TASK_LIST_TABLE}_id) REFERENCES {TASK_LIST_TABLE}(id)
    );
""")
