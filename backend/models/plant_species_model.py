from backend.models.perform_query import perform_query
from backend.Exceptions import *

def get_cached_soil_moisture(plant):
    sql = """ SELECT soil_moisture FROM plant_species WHERE common_name = %s """
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



