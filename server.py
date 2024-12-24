import mysql.connector

# hosted at : freemysqlhosting.net 
db_config = {
    
    'user': 'sql3753434',
    'password': 'jW8Lj1AvuT',
    'host': 'sql3.freemysqlhosting.net',
    'database': 'sql3753434',
    'port': '3306'
}

connection = None

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():print("Successfully connected to the database")
    cursor = connection.cursor()

    # Execute a sample query
    cursor.execute("SELECT * FROM filters;")

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Don't forget to close the cursor
    cursor.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed")
