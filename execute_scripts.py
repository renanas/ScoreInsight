from config.db_connection import get_connection
from scripts.create_tables_setup import create_tables

if __name__ == "__main__":

    connection = get_connection()
    create_tables(connection)