#!/usr/bin/env python
"""Check police user details"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor(dictionary=True)

print("🔍 Checking Users with 'police' role:\n")
cursor.execute("SELECT * FROM users WHERE role='police'")
police_users = cursor.fetchall()

if police_users:
    print(f"Found {len(police_users)} police user(s):")
    for user in police_users:
        print(f"  ID: {user.get('id')}, Email: {user.get('email')}, Name: {user.get('name')}")
else:
    print("❌ NO POLICE USERS FOUND!")
    print("\n💡 Please create a police user by registering with role='police'")

print("\n📊 All users in database:")
cursor.execute("SELECT id, name, email, role FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  {user['id']}: {user['email']} ({user['role']})")

db.close()
