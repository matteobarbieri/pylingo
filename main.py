from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import random

from colors import bcolors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = 'Basics!A2:E'

SHEETS = ['Verbs - present']


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    """
    sheet_metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    properties = sheet_metadata.get('sheets')
    for item in properties:

        # Decomment to print full list of sheets
        # print(item.get("properties").get('title'))

        if item.get("properties").get('title') in SHEETS:
            print(item.get("properties").get('title'))
            print(type(item))
            print(dir(item))
            print(item.values())
            # sheet_id = (item.get("properties").get('sheetId'))

        # print (sheet_id)
    """

    sheet_metadata_range = SHEETS[0] + "!A1:B1"

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=sheet_metadata_range).execute()
    values = result.get('values', [])
    values = [int(item) for sublist in values for item in sublist]
    n_fields, n_rows = values

    # random.randint(

    sheet_data_range = SHEETS[0] + f"!A3:{chr(ord('A')+n_fields)}{n_rows+2}"

    # print(sheet_data_range)

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=sheet_data_range).execute()
    data = result.get('values', [])

    # print(data)
    # print(len(data))

    row_idx = random.randint(0, n_rows)
    data_row = data[row_idx]
    # print(data_row)

    prompt = data_row[0]
    right_answer = data_row[1].strip()

    print(SHEETS[0])
    print(f"What's the translation of {prompt}?")

    answer = input().strip()
    # print(answer)
    if answer == right_answer:
        print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}Wrong, correct answer was {right_answer}{bcolors.ENDC}")

    return

    cell_range = SHEETS[0] + "!A1:B4"

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=cell_range).execute()
    values = result.get('values', [])

    print(values)

    return

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    main()
