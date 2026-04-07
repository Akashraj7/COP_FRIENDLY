#!/usr/bin/env python
"""Test user login"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor(dictionary=True)

print("👥 All users in database:\n")
cursor.execute("SELECT user_id, name, email, role, password FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}, Role: {user['role']}")
    print(f"    Password: {user['password']}\n")

# Test login query  
print("\n🔐 Testing Login Query:")
print("Attempting to login as user with role='citizen'\n")

email = "akashvip2007@gmail.com"
password = "test"  # Generic attempt
role = "citizen"

query = "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s"
cursor.execute(query, (email, password, role))
user = cursor.fetchone()

if user:
    print(f"✅ Login successful!")
    print(f"   User ID: {user.get('user_id')}")
else:
    print(f"❌ Login failed with role='citizen'")
    
# Try without role check
query2 = "SELECT * FROM users WHERE email=%s AND password=%s"
cursor.execute(query2, (email, password))
user2 = cursor.fetchone()

if user2:
    print(f"\n✅ Login works WITHOUT role check")
    print(f"   User role in DB: {user2.get('role')}")

db.close()
