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
  token_file = f"token_{user_id}.json"
  if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_file, "w") as token:
      token.write(creds.to_json())
  return creds

def create_event(user_id, user_email, plant_nickname, amount, recurrence):
  #recurrence is a string of DAILY, WEEKLY, MONTHLY, YEARLY
  try:
    creds = get_user_creds(user_id)
    service = build("calendar", "v3", credentials=creds)
    # Call the Calendar API
    # Get the current UTC time
        
    # Get the current UTC time and 5 minutes from now in ISO format
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"


    timezone = service.settings().get(setting='timezone').execute()
    event = {
      "summary": f"Water {plant_nickname}",
      "location": "Home",
      "Description": "NONE FOR NOW, maybe about info.",
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
      "attendees": [
        {"email": user_email}
      ]
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print("event created")
    return 

    

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  create_event("1", "alexei.ionov@berkeley.edu", "cock", "DAILY")
