import sqlite3
import os

DB_NAME = "ticket_system.db"
# Ensure the DB is saved in the backend directory
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            reg_no TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Tickets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            reg_no TEXT NOT NULL,
            query TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            resolved_by TEXT,
            reply TEXT
        )
    ''')

    # Ticket departments (for routing to multiple/single departments and rerouting)
    c.execute('''
        CREATE TABLE IF NOT EXISTS ticket_departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            department_name TEXT NOT NULL,
            is_current BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY(ticket_id) REFERENCES tickets(id)
        )
    ''')

    # Ticket logs (timeline history of ticket)
    c.execute('''
        CREATE TABLE IF NOT EXISTS ticket_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            event TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            detail TEXT NOT NULL,
            FOREIGN KEY(ticket_id) REFERENCES tickets(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
