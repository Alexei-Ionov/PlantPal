from psycopg2.errors import UniqueViolation
from backend.Exceptions import *
from backend.models.perform_query import perform_query
from backend.database.db import get_connection
from backend.database.db import release_connection
def check_token_and_process_update(soil_moisture, token):
    """
    this function single handedly performs the following 2 operations: 
    1.) checks to see if token is associated with any user plant, and if it is, update the current sensor reading
    2.) insert new sensor record into the sensor_readings table
    """
   
    cursor = None
    connection = None
    try: 
        connection = get_connection()
        if not connection:
            raise Exception("Failed to get a connection to the db - pool might be max'd out")
        cursor = connection.cursor()
        if not cursor:
            raise Exception("Failed to get cursor for connection to db")


        # UPDATE user_plants w/ current soil_moisture level
        query1 = """ UPDATE user_plants SET current_moisture = %s WHERE token_id = %s RETURNING user_id, id; """
        params1 = (soil_moisture, token)
        cursor.execute(query1, params1)

        if not cursor.rowcount:
            raise Exception("Token doesn't exist!")
        result = cursor.fetchall()
        user_id, plant_id = result[0]
        #INSERT NEW RECORD INTO sensor_readings table

        query2 = """ INSERT INTO sensor_readings (moisture_level, user_id, plant_id) VALUES (%s, %s, %s) """
        params2 = (soil_moisture, user_id, plant_id)
        cursor.execute(query2, params2)

        connection.commit()
        print("sensor reading update succesfull!")
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            release_connection(connection)


