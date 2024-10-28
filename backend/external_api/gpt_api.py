import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPEN_AI_API_KEY")
)
def get_gpt_response(prompt):
    try: 
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        ) 
        # Extract the response text from the 'choices' list
        response_text = chat_completion.choices[0].message.content
        return response_text
    except Exception as e:
        raise e
def get_plant_info_api(plant):
    json_ = {
        "plant_name": f"[{plant}]",
        "desired_soil_moisture": "[Single value from 0.0 to 10.0]",
        "genus": "[Genus Name]",
        "family": "[Family Name]",
        "edible": "[Yes/No]",
        "image_url": "[URL to an image of the plant]",
        "growth_rate": "[Slow/Medium/Fast]",
        "toxicity": "[None/Low/Medium/High]",
        "average_height": "[Float Value]",
        "Light": "[None/Low/Medium/High]"
    }
    prompt = f"Given the common name of the plant, {plant}, provide detailed information about it in the following json format: {json_}"
    try: 
        return get_gpt_response(prompt)
    except Exception as e:
        raise e
def get_watering_schedule_api(plant):
   
    json_ = {
        "recurrence": f"[DAILY/WEEKLY/MONTLY/YEARLY]",
        "amount": f"[LIGHT/MEDIUM/HEAVY]"
    }
    prompt = f"""
                Given the common name of the plant, {plant}, please determine a recommended watering schedule. Include: 1. Watering frequency as a recurrence value (e.g., DAILY, WEEKLY, MONTHLY, YEARLY) 2. The amount of water per watering session (e.g., LIGHT, MEDIUM, HEAVY) in the following json format: {json_}
                Please factor in general guidelines for the plant’s typical needs, assuming indoor placement with moderate light and average humidity. Example plants could be 'Aloe Vera,' 'Fiddle Leaf Fig,' or 'Peace Lily'.
            """
    try: 
        return get_gpt_response(prompt)
    except Exception as e:
        raise e