import psycopg2

# Establish a connection to the PostgreSQL database
try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="pyVeRefine",
        user="postgres",
        password="Football61!"
    )
    print("Connection established successfully!")

    # Perform database operations here

except psycopg2.Error as error:
    print("Error connecting to PostgreSQL database:", error)

finally:
    # Close the database connection when done
    if connection:
        connection.close()
        print("Connection closed.")
