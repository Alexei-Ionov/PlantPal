import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize the connection pool to None initially
db_pool = None

def init_connection_pool(minconn=1, maxconn=10):
    """Initialize the connection pool if it hasn't been created."""
    global db_pool
    if db_pool is None:
        try:
            db_pool = pool.SimpleConnectionPool(
                minconn,  # Minimum number of connections
                maxconn,  # Maximum number of connections
                DATABASE_URL
            )
            print("Connection pool created successfully.")
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            raise

def get_connection():
    """Get a connection from the pool."""
    if db_pool is None:
        raise Exception("Connection pool is not initialized.")
    try:
        connection = db_pool.getconn()
        print("Connection obtained from pool.")
        return connection
    except Exception as e:
        print(f"Error obtaining connection: {e}")
        return None

def release_connection(connection):
    """Release a connection back to the pool."""
    if connection:
        db_pool.putconn(connection)
        print("Connection returned to pool.")

def close_pool():
    """Close all connections in the pool."""
    if db_pool:
        db_pool.closeall()
        print("Connection pool closed.")

# if __name__ == "__main__":
#     init_connection_pool()
