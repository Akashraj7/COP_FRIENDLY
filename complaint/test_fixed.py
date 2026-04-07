#!/usr/bin/env python
"""Test track and dashboard queries"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor(dictionary=True)

print("✅ Testing Track Query (Fixed)\n")
query = "SELECT complaint_id, title, description, location, type as category, status FROM complaints WHERE complaint_id=%s"
cursor.execute(query, (6,))  # Test with complaint ID 6
result = cursor.fetchone()

if result:
    print(f"Complaint ID: {result['complaint_id']}")
    print(f"  Title: {result['title']}")
    print(f"  Location: {result['location']}")
    print(f"  Category: {result['category']}")
    print(f"  Status: {result['status']}\n")
else:
    print("❌ Query failed\n")

print("="*50)
print("✅ Testing User Dashboard Query (User ID 1000)\n")
user_id = 1000
query = "SELECT complaint_id, title, description, location, status, type as category FROM complaints WHERE user_id=%s ORDER BY complaint_id DESC"
cursor.execute(query, (user_id,))
complaints = cursor.fetchall()

print(f"Found {len(complaints)} complaints:\n")
for c in complaints:
    print(f"  ID: {c['complaint_id']}, Title: {c['title']}, Status: {c['status']}")

db.close()
