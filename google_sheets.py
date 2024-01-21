import os
import json
import glob

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.api_core.exceptions import AlreadyExists

# https://developers.google.com/sheets/api/scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def authorize():
  credentials = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      credentials = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(credentials.to_json())
  return credentials

def upload_to_google_sheets(credentials, csv_file_paths, spreadsheet_id):
  service = build("sheets", "v4", credentials=credentials)
  sheet_names = [os.path.basename(csv_file_path)[:-4] for csv_file_path in csv_file_paths]
  create_sheets(service, spreadsheet_id, sheet_names)
  write_values(service, csv_file_paths, spreadsheet_id)

# Tries to create new sheets corresponding to the csv file names. If a sheet
# with the name already exists, user input is requested asking if they would
# like to override the values in the sheet
def create_sheets(service, spreadsheet_id, sheet_names):
  print("Creating sheets...")

  requests = []
  for sheet_name in sheet_names:
    requests.append({
      "addSheet": {
        "properties": {
          "title":sheet_name
        }
      }
    })

  result = (
    service.spreadsheets()
    .batchUpdate(
      spreadsheetId=spreadsheet_id, 
      body={"requests": requests},
    )
    .execute()
  )
  for response in result["replies"]:
    print(f"Created sheet with title {response['addSheet']['properties']['title']}")

def write_values(service, csv_file_paths, spreadsheet_id):
  print("Updating cells...")

  data = []
  for csv_file_path in csv_file_paths:
    sheet_name = os.path.basename(csv_file_path)[:-4]
    with open(csv_file_path, 'r') as csv_file:
        rows = csv_file.read().splitlines()
    data.append({"range": sheet_name, "values": [row.split(',') for row in rows]})
    
  result = (
      service.spreadsheets()
      .values()
      .batchUpdate(
          spreadsheetId=spreadsheet_id,
          body={"valueInputOption": "USER_ENTERED", "data": data},
      )
      .execute()
  )
  
  for response in result["responses"]:
    print(f"{response.get('updatedCells')} cells in {response['updatedRange']} updated.")

      
if __name__ == "__main__":
  with open("config.json", "r") as config_file:
    config = json.load(config_file)

  credentials = authorize()
  try:
    upload_to_google_sheets(credentials, glob.glob("data/csv/*.csv"), config["google sheets id"])
  except HttpError as error:
    print(error)