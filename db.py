import sqlite3

DB_NAME = "farmer_data.db"

def create_table():
    """Create records table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_type TEXT NOT NULL,
            detail TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_record(record_type, detail, date):
    """Add a new record to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO records (record_type, detail, date)
        VALUES (?, ?, ?)
    """, (record_type, detail, date))
    conn.commit()
    conn.close()

def get_records():
    """Fetch all records from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

# Initialize database
create_table()

