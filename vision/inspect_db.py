import sqlite3
import os

# Connect to the local SQLite DB
db_path = "vector_store.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Data Stored in Local SQLite DB ---")
try:
    cursor.execute("SELECT doc_name, COUNT(*) FROM chunks GROUP BY doc_name")
    rows = cursor.fetchall()
    
    if not rows:
        print("Database is currently empty (or not yet indexed).")
    else:
        for row in rows:
            print(f"📄 Document: {row[0]:<20} | 🧩 Chunks: {row[1]}")
            
    cursor.execute("SELECT COUNT(*) FROM chunks")
    total = cursor.fetchone()[0]
    print("-" * 50)
    print(f"📊 Total vectors stored: {total}")

except Exception as e:
    print(f"Error reading DB: {e}")

conn.close()
