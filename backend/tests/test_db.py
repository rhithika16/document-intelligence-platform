from database.connection import get_db_connection

try:
    connection = get_db_connection()

    if connection.is_connected():
        print("✅ Connected to MySQL successfully!")

    connection.close()

except Exception as e:
    print("❌ Connection Failed")
    print(e)