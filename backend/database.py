import os
import sqlite3

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("postgres"):
        import psycopg2
        import psycopg2.extras
        # Handle Render's postgres:// scheme
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.DictCursor)
        return PostgresConnWrapper(conn)
    else:
        # Fallback to local SQLite
        DB_NAME = "ticket_system.db"
        DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

class PostgresCursorWrapper:
    """Wraps psycopg2 cursor to act like sqlite3 cursor for ? parameter syntax"""
    def __init__(self, cursor):
        self.cursor = cursor
        
    def execute(self, query, args=None):
        # Replace sqlite '?' placeholders with postgres '%s'
        query = query.replace('?', '%s')
        if args is not None:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
            
    def fetchone(self): 
        return self.cursor.fetchone()
    
    def fetchall(self): 
        return self.cursor.fetchall()
        
    def close(self): 
        self.cursor.close()

class PostgresConnWrapper:
    def __init__(self, conn):
        self.conn = conn
    
    def cursor(self): 
        return PostgresCursorWrapper(self.conn.cursor())
        
    def commit(self): 
        self.conn.commit()
        
    def close(self): 
        self.conn.close()

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    is_pg = os.environ.get("DATABASE_URL", "").startswith("postgres")

    if is_pg:
        # PostgreSQL schema
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                reg_no TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
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
        c.execute('''
            CREATE TABLE IF NOT EXISTS ticket_departments (
                id SERIAL PRIMARY KEY,
                ticket_id TEXT NOT NULL,
                department_name TEXT NOT NULL,
                is_current BOOLEAN NOT NULL DEFAULT true,
                FOREIGN KEY(ticket_id) REFERENCES tickets(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS ticket_logs (
                id SERIAL PRIMARY KEY,
                ticket_id TEXT NOT NULL,
                event TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                detail TEXT NOT NULL,
                FOREIGN KEY(ticket_id) REFERENCES tickets(id)
            )
        ''')
    else:
        # SQLite schema
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_no TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
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
        c.execute('''
            CREATE TABLE IF NOT EXISTS ticket_departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                department_name TEXT NOT NULL,
                is_current BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY(ticket_id) REFERENCES tickets(id)
            )
        ''')
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
    print("Database fully initialized.")
