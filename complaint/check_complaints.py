#!/usr/bin/env python
"""Check complaints in database"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor(dictionary=True)

print("📋 All Complaints in Database:\n")
query = "SELECT complaint_id, user_id, title, location, status, type FROM complaints ORDER BY complaint_id DESC"
cursor.execute(query)
complaints = cursor.fetchall()

for c in complaints:
    print(f"ID: {c['complaint_id']}")
    print(f"  User ID: {c['user_id']}")
    print(f"  Title: {c['title']}")
    print(f"  Location: {c['location']}")
    print(f"  Status: {c['status']}")
    print(f"  Type: {c['type']}")
    print()

if not complaints:
    print("❌ No complaints found")

# Map user_id to names
print("\n" + "="*50)
print("👥 User-Complaint Mapping:\n")
cursor.execute("SELECT user_id, name, email FROM users WHERE user_id IN (SELECT DISTINCT user_id FROM complaints)")
users = cursor.fetchall()
for user in users:
    print(f"User {user['user_id']}: {user['name']} ({user['email']})")

db.close()
