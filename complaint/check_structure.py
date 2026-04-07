#!/usr/bin/env python
"""Check table structure"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor()

print("📊 Users Table Structure:")
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col}")

print("\n\n📊 Complaints Table Structure:")
cursor.execute("DESCRIBE complaints")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col}")

print("\n\n👤 Sample from users table:")
cursor.execute("SELECT * FROM users LIMIT 1")
result = cursor.fetchone()
if result:
    print(f"  {result}")

db.close()
