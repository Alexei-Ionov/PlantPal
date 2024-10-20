from psycopg2.errors import UniqueViolation
from backend.Exceptions import *
from backend.models.perform_query import perform_query
def create_user(username, hashed_password, email):
    sql = """INSERT INTO users (username, hashed_password, email, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP) """
    params = (username, hashed_password, email)
    try: 
        perform_query(sql, params)
        return {"success": "true", "message": "User created successfully"}
    except UniqueViolation:
        raise JsonException({"status": "error", "message": "User with this email or username already exists."})
    except Exception as e:
        raise e

    
def login_user(email, plain_text_password):
    sql = """SELECT username, id, hashed_password FROM users WHERE email = %s """
    params = (email,)
    try: 
        result = perform_query(sql, params)
        if not result:
            return None
        return result[0]
    except Exception as e:
        print("ERROR IN LOGIN_USER")
        raise e

def get_plants(user_id):
    sql = """ SELECT nickname, current_moisture, desired_soil_moisture, last_update FROM user_plants WHERE user_id = %s """
    params = (user_id,)
    try: 
        plants = perform_query(sql, params)
        result = []
        for nickname, current_moisture, desired_soil_moisture, last_update in plants:
            result.append({"nickname": nickname, "current_moisture": current_moisture, "desired_soil_moisture": desired_soil_moisture, "last_update": last_update})
        return result
    except Exception as e:
        raise Exception

def add_plant(user_id, plant_name, nickname):
    sql = """ INSERT INTO user_plants (common_name, nickname, current_moisture)
     id SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    current_moisture FLOAT NOT NULL,
    desired_soil_moisture FLOAT NOT NULL,
    last_update TIMESTAMP, 
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    ); 
    """


   




