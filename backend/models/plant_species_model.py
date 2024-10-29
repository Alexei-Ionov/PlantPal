from backend.models.perform_query import perform_query
from backend.Exceptions import *

def get_cached_soil_moisture(plant):
    sql = """ SELECT desired_soil_moisture FROM plant_species WHERE common_name = %s """
    params = (plant,)
    try: 
        result = perform_query(sql, params)
        if not result:
            return None
        desired_soil_moisture = result[0]
        return desired_soil_moisture
    except Exception as e:
        print(e)
        raise e

def add_plant_species(plant_info):
    sql = """ INSERT INTO plant_species (common_name, genus, family, edible, image_url, growth_rate, toxicity, average_height, light, desired_soil_moisture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try: 
        common_name, desired_soil_moisture, genus, family, edible, image_url, growth_rate, toxicity, average_height, light = plant_info.get("plant_name"), plant_info.get("desired_soil_moisture"), plant_info.get("genus"), plant_info.get("family"), plant_info.get("edible"), plant_info.get("image_url"), plant_info.get("growth_rate"), plant_info.get("toxicity"), plant_info.get("average_height"), plant_info.get("Light")
        params = (common_name, genus, family, edible, image_url, growth_rate, toxicity, average_height, light, desired_soil_moisture)
        perform_query(sql, params)
        return desired_soil_moisture
    except Exception as e:
        print(e)
        raise e
    
def get_info(plant_name):
    sql = """ SELECT common_name, genus, family, edible, image_url, growth_rate, toxicity, average_height, light, desired_soil_moisture FROM plant_species WHERE common_name = %s """
    params = (plant_name,)
    try: 
        result = perform_query(sql, params)
        print(result)
        common_name, genus, family, edible, image_url, growth_rate, toxicity, average_height, light, desired_soil_moisture = result[0]
        response = {"common_name": common_name, "genus": genus, "family": family, "edible": edible, "image_url": image_url, "growth_rate": growth_rate, "toxicity": toxicity, "average_height": average_height, "light": light, "desired_soil_moisture": desired_soil_moisture}
        return response
    except Exception as e:
        raise e
