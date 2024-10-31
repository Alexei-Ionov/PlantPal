import os
from openai import OpenAI
from dotenv import load_dotenv
import json
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
def convert_response(response):
    #converts a possible invalid api response to a valid one
    valid_response = {"recurrence": None, "amount": None}
    def dfs(response):
        for key in response:
            if key == "recurrence" or key == "amount":
                valid_response[key] = response[key].upper()
            elif type(response[key]) is dict:
                dfs(response[key])
    dfs(response)
    return valid_response
            
def get_watering_schedule_api(plant):
   
    json_example = {
        "recurrence": "[DAILY, WEEKLY, MONTHLY, or YEARLY]",
        "amount": "[LIGHT, MEDIUM, or HEAVY]"
    }

    prompt = f"""
        Given the plant's common name '{plant}', please determine a recommended watering schedule in the following JSON format exactly as shown below, with only "recurrence" and "amount" as the keys and acceptable values as specified.

        Return only valid JSON, formatted precisely like this:
            {{
                "recurrence": "<recurrence value>",
                "amount": "<amount value>"
            }}

        Notes:
            - Use one of these values for "recurrence": "DAILY", "WEEKLY", "MONTHLY", or "YEARLY".
            - Use one of these values for "amount": "LIGHT", "MEDIUM", or "HEAVY".
            - Ensure that all key, values are in double quotes.
            Please provide no additional information or commentary; only the JSON object itself in the exact format required.

    """

    try: 
        api_response = get_gpt_response(prompt)

        
        # valid_response = convert_response(api_response)
        # print("AFTER:", valid_response)
        return api_response
    except Exception as e:
        raise e