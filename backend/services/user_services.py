from backend.external_api.gpt_api import *
from backend.external_api.google_calendar.google_calendar_api import *
from backend.models.plant_species_model import *
from backend.models.user_model import add_plant
import json
def add_plant_service(plant, nickname, user_id):
    """
    - first we check to see if this plant species is already in our db 
    - if not, perform api request to gpt to find desired soil moisture 
    - next, we need to perform an api request to tresfle to get species info
    - then we need to update our db 
    """
    try: 
        desired_soil_moisture = get_cached_soil_moisture(plant) #checks whetehr this plant is alr in our db
        if desired_soil_moisture is None:
            api_response = get_plant_info_api(plant)
            plant_info = json.loads(api_response)
            print(plant_info)
            #add information regarding the plant species into our db
            desired_soil_moisture = add_plant_species(plant_info)
        #add the plant for the user and get the token for this (user_id, plant_id) combo
        token = add_plant(user_id, plant, nickname, desired_soil_moisture)
        return token
    except Exception as e:
        raise e

def add_event_service(user_id, user_email, plant, plant_nickname):
    try: 
        api_response = get_watering_schedule_api(plant)
        print(api_response)
        plant_info = json.loads(api_response)
        print(plant_info)
        if "recurrence" not in plant_info or "amount" not in plant_info:
            raise Exception("Failed api response")
        possible_recurrences = {'DAILY': "DAILY", 'WEEKLY': "WEEKLY", 'MONTHLY': "MONTHLY", 'YEARLY': "YEARLY"}
        if plant_info["recurrence"] not in possible_recurrences:
            raise Exception("Failed api response")
        possible_watering_amounts = {"LIGHT", "MEDIUM", "HEAVY"}
        if plant_info["amount"] not in possible_watering_amounts:
            raise Exception("Failed api response")
        # recurrence = str(plant_info["amount"])
        recurrence = possible_recurrences[plant_info["recurrence"]]
        create_event(user_id, user_email, plant_nickname, plant_info["amount"], recurrence)
    except Exception as e:
        raise e



