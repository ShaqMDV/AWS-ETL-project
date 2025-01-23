import psycopg2
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Load the SQL script from file
def load_sql_script(file_path):
    """
    Reads the SQL script from a file.
    :param file_path: Path to the SQL file.
    :return: The SQL script as a string.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        return None

# Execute the SQL script
def execute_sql_script(connection, script):
    """
    Executes the given SQL script using the provided connection.
    :param connection: psycopg2 connection object.
    :param script: SQL script to execute.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(script)
            connection.commit()
            print("Schema created successfully.")
    except Exception as e:
        print(f"Error executing SQL script: {e}")
        connection.rollback()

if __name__ == "__main__":
    # Define the path to your SQL file
    schema_table_path = "../database/create_schema.sql"

    # Load the SQL script
    schema_script = load_sql_script(schema_table_path)
    if not schema_script:
        print("Failed to load the SQL script.")
        exit(1)

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432",
            database=os.getenv("POSTGRES_DB")
        )

        # Execute the SQL script
        execute_sql_script(connection, schema_script)

    except Exception as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if connection:
            connection.close()
