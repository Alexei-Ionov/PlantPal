from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_user_creds(user_id):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  try: 
    token_file = f"token_{user_id}.json"
    if os.path.exists(token_file):
      creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     "credentials.json", SCOPES
        # )
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "credentials.json")):
          print("can't find credentials.json")
          raise FileNotFoundError("The credentials.json file is required to run this application.")
        flow = InstalledAppFlow.from_client_secrets_file(
          os.path.join(os.path.dirname(__file__), "credentials.json"), SCOPES
        )
        creds = flow.run_local_server(port=5555)
      # Save the credentials for the next run
      with open(token_file, "w") as token:
        token.write(creds.to_json())
    return creds
  except Exception as e:
    print("ERROR")
    raise e

def create_event(user_id, user_email, plant_nickname, amount, recurrence):
  #recurrence is a string of DAILY, WEEKLY, MONTHLY, YEARLY
  #amount is how much we should be watering the plant (light, medium, heavy)
  try:
    creds = get_user_creds(f"{user_id}")
    service = build("calendar", "v3", credentials=creds)
    # Call the Calendar API
    # Get the current UTC time
        
    # Get the current UTC time and 5 minutes from now in ISO format
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"


    timezone = service.settings().get(setting='timezone').execute()
    # Define the event details, ensuring the recurrence rule is formatted correctly
    event = {
        "summary": f"Water {plant_nickname}",
        "location": "Home",
        "description": f"{plant_nickname} requires {amount} watering {recurrence}",
        "colorId": 1,
        "start": {
            "dateTime": now,
            "timeZone": timezone["value"]
        },
        "end": {
            "dateTime": end,
            "timeZone": timezone["value"]
        },
        "recurrence": [f"RRULE:FREQ={recurrence}"],
        "attendees": [{"email": user_email}]
    }
    # Serialize to JSON to check format (optional, for debugging)
    
    # event = service.events().insert(calendarId="primary", body=event).execute()
    created_event = service.events().insert(calendarId="primary", body=event).execute()

    print("event created")
    return 
  except HttpError as error:
    print(f"An error occurred: {error}")
    raise error
  except Exception as e:
    print(e)
    raise e

# if __name__ == "__main__":
#   create_event("1", "alexei.ionov@berkeley.edu", "big green", "LIGHT", "DAILY")