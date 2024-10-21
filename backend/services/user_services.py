from backend.external_api.gpt_api import get_plant_info_api
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
        print(e)
        raise e

