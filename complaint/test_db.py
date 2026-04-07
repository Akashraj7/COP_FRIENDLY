#!/usr/bin/env python
"""Database diagnostic script"""

import mysql.connector

print("🔍 Testing MySQL Connection...\n")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akash@007",
        database="complaint"
    )
    print("✅ MySQL Connection: SUCCESS")
    
    cursor = db.cursor(dictionary=True)
    
    # Check if tables exist
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📊 Tables in 'complaint' database:")
    for table in tables:
        print(f"  - {list(table.values())[0]}")
    
    # Check complaints table
    try:
        cursor.execute("SELECT COUNT(*) as count FROM complaints")
        result = cursor.fetchone()
        print(f"\n📋 Complaints Table: EXISTS (Contains {result['count']} records)")
    except Exception as e:
        print(f"❌ Complaints Table: NOT FOUND - {e}")
    
    # Check users table
    try:
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        print(f"👥 Users Table: EXISTS (Contains {result['count']} records)")
    except Exception as e:
        print(f"❌ Users Table: NOT FOUND - {e}")
    
    db.close()
    
except mysql.connector.Error as err:
    print(f"❌ MySQL Connection FAILED:")
    print(f"   Error: {err}")
    print(f"\n💡 Troubleshooting:")
    print(f"   1. Make sure MySQL server is running")
    print(f"   2. Check if database 'complaint' exists")
    print(f"   3. Verify username 'root' and password 'Akash@007'")
