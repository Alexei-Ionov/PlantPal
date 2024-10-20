from backend.external_api.gpt_api import get_plant_info_api
from backend.models.plant_species_model import get_cached_soil_moisture
from backend.models.user_model import add_plant
# import asynio
def filter_api_response(response):
    """
    Gets the float representing the soil moisture form the api response 
    """
    initial_digit_index = None
    for i in range(len(response)):
        char = response[i]
        if ord('0') <= ord(char) <= ord('9'):
            if initial_digit_index is None:
                initial_digit_index = i
        elif initial_digit_index is not None:
            return float(response[initial_digit_index:i])
    return None
def add_plant_service(plant, nickname, user_id):
    """
    - first we check to see if this plant species is already in our db 
    - if not, perform api request to gpt to find desired soil moisture 
    - next, we need to perform an api request to trefle to get species info
    - then we need to update our db 
    """
    try: 
        desired_soil_moisture = get_cached_soil_moisture(plant)
        if desired_soil_moisture is None:
            api_response = get_plant_info_api(plant)
            print(api_response)
            # desired_soil_moisture = filter_api_response(api_response)
            # if desired_soil_moisture is None:
            #     raise Exception(f"Failed to find soil moisture for {plant}")
            #now we need to update our db so that it contains this new species of plant
        return desired_soil_moisture 

    except Exception as e:
        print(e)
        raise e

