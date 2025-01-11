import mysql.connector

# hosted at : aiven

db_config = {
    
    'user': 'avnadmin',
    'password': 'AVNS_tnJimgAkaMP36guFO_1',
    'host': 'filtermanager-mysql-filtermanager.e.aivencloud.com',
    'database': 'defaultdb',
    'port': '25607'
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
