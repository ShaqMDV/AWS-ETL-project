import psycopg2
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection setup
def connect_to_database():
    """
    Connect to the PostgreSQL database.
    :return: psycopg2 connection object
    """
    try:
        connection = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432",
            database=os.getenv("POSTGRES_DB")
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to load JSON data
def load_json(file_path):
    """
    Loads JSON data from a file.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None

# Insert data into tables
def insert_data(connection, table_name, data):
    """
    Inserts data into the specified table.
    :param connection: psycopg2 connection object.
    :param table_name: Name of the table to insert data into.
    :param data: List of dictionaries representing the data.
    """
    try:
        with connection.cursor() as cursor:
            # Dynamically create INSERT statement based on data keys
            for row in data:
                columns = ", ".join(row.keys())
                values = ", ".join([f"%({key})s" for key in row.keys()])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(insert_query, row)
            connection.commit()
            print(f"Data successfully inserted into {table_name}")
    except Exception as e:
        connection.rollback()
        print(f"Error inserting data into {table_name}: {e}")

# Main execution block
if __name__ == "__main__":
    # File paths for normalized data
    data_files = {
        "branches": "../data/branches.json",
        "transactions": "../data/transactions.json",
        "products": "../data/products.json",
        "product_transactions": "../data/product_transactions.json",
    }

    # Connect to the database
    connection = connect_to_database()
    if not connection:
        print("Database connection failed. Exiting.")
        exit(1)

    # Load and insert data
    for table_name, file_path in data_files.items():
        print(f"Processing table: {table_name}")
        data = load_json(file_path)
        if data:
            insert_data(connection, table_name, data)

    # Close the connection
    connection.close()
