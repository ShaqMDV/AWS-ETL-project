# This file exists to separate the direct use of psycopg2 in 'connect_to_db.py'
# from functions here that only care about the Connection and Cursor - this makes these easier to unit test.


import uuid
import logging


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    try:
        # Create branches table
        LOGGER.info('create_db_tables: creating branches table')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS branches (
                branch_id INT IDENTITY(1, 1) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL
            );
        ''')


        # Create transactions table
        LOGGER.info('create_db_tables: creating transactions table')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                payment_id INT IDENTITY(1, 1) PRIMARY KEY,
                branch_id INT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                total_amount NUMERIC(10, 2) NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
            );
        ''')


        # Create products table
        LOGGER.info('create_db_tables: creating products table')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INT IDENTITY(1, 1) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                variant VARCHAR(255),
                size VARCHAR(50),
                price NUMERIC(10, 2) NOT NULL
            );
        ''')


        # Create product_transactions table
        LOGGER.info('create_db_tables: creating product_transactions table')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_transactions (
                product_transactions_id INT IDENTITY(1, 1) PRIMARY KEY,
                payment_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                FOREIGN KEY (payment_id) REFERENCES transactions(payment_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        ''')


        LOGGER.info('create_db_tables: committing changes')
        connection.commit()
        LOGGER.info('create_db_tables: done')
    except Exception as ex:
        LOGGER.error(f'create_db_tables: failed to create tables: {ex}')
        raise ex


def create_guid():
    """
    Generate a GUID for unique identifiers (if required).
    """
    return str(uuid.uuid4())


def save_data_in_db(connection, cursor, table_name, data):
    
    LOGGER.info(f'save_data_in_db: inserting into table {table_name}')
    if not data:
        LOGGER.info(f'save_data_in_db: no data to insert into {table_name}')
        return


    try:
        # Get column names excluding identity columns
        if table_name == "branches":
            excluded_columns = ["branch_id"]
        elif table_name == "transactions":
            excluded_columns = ["payment_id"]
        elif table_name == "products":
            excluded_columns = ["product_id"]
        elif table_name == "product_transactions":
            excluded_columns = ["product_transactions_id"]
        else:
            excluded_columns = []


        # Exclude identity columns from data
        filtered_data = [
            {key: value for key, value in row.items() if key not in excluded_columns}
            for row in data
        ]


        # Generate column names and placeholders dynamically
        columns = ', '.join(filtered_data[0].keys())
        placeholders = ', '.join(['%s'] * len(filtered_data[0]))
        insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'


        # Batch insert rows for better performance
        rows = [tuple(row.values()) for row in filtered_data]
        cursor.executemany(insert_query, rows)
        connection.commit()
        LOGGER.info(f'save_data_in_db: successfully inserted {len(filtered_data)} rows into {table_name}')
    except Exception as ex:
        LOGGER.error(f'save_data_in_db: failed to insert data into {table_name}: {ex}')
        connection.rollback()
        raise ex