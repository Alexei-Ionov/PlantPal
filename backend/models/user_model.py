from psycopg2.errors import UniqueViolation
from backend.Exceptions import *
from backend.models.perform_query import perform_query
import uuid
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
    sql = """ SELECT nickname, current_moisture, desired_soil_moisture, last_update, esp32_ip, common_name, token_id FROM user_plants WHERE user_id = %s """
    params = (user_id,)
    try: 
        plants = perform_query(sql, params)
        result = []
        for nickname, current_moisture, desired_soil_moisture, last_update, esp32_ip, common_name, token_id in plants:
            result.append({"nickname": nickname, "current_moisture": current_moisture, "desired_soil_moisture": desired_soil_moisture, "last_update": last_update, "esp32_ip": esp32_ip, "common_name": common_name, "token": token_id})
        return result
    except Exception as e:
        raise e

def get_tokens(user_id):
    sql = """ SELECT token_id, esp32_ip FROM user_plants WHERE user_id = %s"""
    params = (user_id,)
    try:
        tokens = perform_query(sql, params)
        result = []
        for token_id, esp32_ip in tokens:
            result.append({"token_id": token_id, "esp32_ip": esp32_ip})
        return result
    except Exception as e:
        raise e

def add_plant(user_id, plant_name, nickname, desired_soil_moisture):
    #query for adding plant to user_plants table -> return the plant_id to be used for creating the token
    try: 
        token = str(uuid.uuid4())
        sql = """ INSERT INTO user_plants (common_name, token_id, nickname, desired_soil_moisture, user_id) VALUES (%s, %s, %s, %s, %s) """
        params = (plant_name, token, nickname, desired_soil_moisture, user_id)
        perform_query(sql, params)
        return token 
    except Exception as e:
        print(e)
        raise e
def add_esp_to_user_plant(user_id, token, esp32_ip):
    try: 
        sql = """ UPDATE user_plants SET esp32_ip = %s WHERE token_id = %s AND user_id = %s """
        params = (esp32_ip, token, user_id)
        perform_query(sql, params)
    except Exception as e:
        raise e

    

   




