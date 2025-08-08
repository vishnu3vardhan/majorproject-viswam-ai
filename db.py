import sqlite3

DB_NAME = "farmer_data.db"

# === General Record Table ===
def create_table():
    """Create general records table if it doesn't exist."""
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
    """Add a new record to the records table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO records (record_type, detail, date)
        VALUES (?, ?, ?)
    """, (record_type, detail, date))
    conn.commit()
    conn.close()

def get_records():
    """Fetch all records from the records table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

# === Disease Image Table ===
def create_image_table():
    """Create disease_images table for storing crop/cattle disease images."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disease_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT CHECK(category IN ('crop', 'cattle')) NOT NULL,
            description TEXT,
            image BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_image(name, category, description, image_path):
    """Insert a new disease image into the database."""
    with open(image_path, 'rb') as file:
        image_data = file.read()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO disease_images (name, category, description, image)
        VALUES (?, ?, ?, ?)
    ''', (name, category, description, image_data))
    conn.commit()
    conn.close()

def get_image_by_id(image_id):
    """Retrieve a specific image entry by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, category, description, image FROM disease_images WHERE id=?', (image_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def list_all_images():
    """List metadata of all stored disease images."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, description FROM disease_images ORDER BY id DESC')
    results = cursor.fetchall()
    conn.close()
    return results

def delete_image(image_id):
    """Delete a disease image entry by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM disease_images WHERE id=?', (image_id,))
    conn.commit()
    conn.close()

# Initialize tables
create_table()
create_image_table()



'''
# pages/record_keeping.py
import streamlit as st
from db import add_record, get_records

def show():
    st.header("📒 Farm Record Keeping")

    record_type = st.selectbox("📂 Record Type", ["Dairy", "Poultry", "Crop"])
    detail = st.text_input("📝 Record Details")

    if st.button("💾 Save Record"):
        add_record(record_type, detail, "2025-07-17")  # You can replace with current date
        st.success("✅ Record saved successfully!")

    if st.checkbox("📜 Show All Records"):
        records = get_records()
        st.table(records)

This is the only file where db is imported
'''