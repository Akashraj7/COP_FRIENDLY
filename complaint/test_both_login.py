#!/usr/bin/env python
"""Test both user and police login"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@007",
    database="complaint"
)

cursor = db.cursor(dictionary=True)

print("✅ Testing Citizen (User) Login\n")
email = "akashraj.28it@licet.ac.in"
password = "Akash2527."
role = "citizen"

query = "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s"
cursor.execute(query, (email, password, role))
citizen_user = cursor.fetchone()

if citizen_user:
    print(f"✅ CITIZEN LOGIN SUCCESS!")
    print(f"   Name: {citizen_user['name']}")
    print(f"   Email: {citizen_user['email']}")
    print(f"   User ID: {citizen_user['user_id']}")
    print(f"   Role: {citizen_user['role']}")
else:
    print("❌ CITIZEN LOGIN FAILED")

print("\n" + "="*50)
print("✅ Testing Police Login\n")
email = "akashvip2007@gmail.com"
password = "Akash2527."
role = "police"

query = "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s"
cursor.execute(query, (email, password, role))
police_user = cursor.fetchone()

if police_user:
    print(f"✅ POLICE LOGIN SUCCESS!")
    print(f"   Name: {police_user['name']}")
    print(f"   Email: {police_user['email']}")
    print(f"   User ID: {police_user['user_id']}")
    print(f"   Role: {police_user['role']}")
else:
    print("❌ POLICE LOGIN FAILED")

db.close()
