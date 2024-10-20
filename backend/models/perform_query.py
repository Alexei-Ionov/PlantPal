from backend.database.db import get_connection
from backend.database.db import release_connection

def perform_query(query, params=None):
    cursor = None
    connection = None
    try: 
        connection = get_connection()
        if not connection:
            raise Exception("Failed to get a connection to the db - pool might be max'd out")
        cursor = connection.cursor()
        if not cursor:
            raise Exception("Failed to get cursor for connection to db")
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            connection.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            release_connection(connection)