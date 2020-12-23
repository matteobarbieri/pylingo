from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from wd import check_solution

import random

import argparse

from colors import bcolors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = 'Basics!A2:E'

SHEETS = [
    'Nouns',
    'Verbs - present',
    'Verbs - past',
    'Adjectives',
]

# def parse_args():

    # parser = argparse.ArgumentParser()

    # parser.add_argument('--simple', default=False)

    # args = parser.parse_args()

def fetch_data(sheet_name, sheets_handle):

    sheet_metadata_range = SHEETS[0] + "!A1:B1"

    result = sheets_handle.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=sheet_metadata_range).execute()

    values = result.get('values', [])
    values = [int(item) for sublist in values for item in sublist]
    n_fields, n_rows = values

    sheet_data_range = SHEETS[0] + f"!A3:{chr(ord('A')+n_fields)}{n_rows+2}"

    # print(sheet_data_range)

    result = sheets_handle.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=sheet_data_range).execute()
    data = result.get('values', [])

    return data

    pass

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
    sheets_handle = service.spreadsheets()

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

    data = fetch_data(SHEETS[0], sheets_handle)
    n_fields = len(data[0])

    # all_idx = list(range(n_rows))
    all_idx = list(range(len(data)))
    random.shuffle(all_idx)

    # Pick a limited number of questions
    idx = all_idx[:3]



    ask_questions(data, idx, n_fields)

    return

    # cell_range = SHEETS[0] + "!A1:B4"

    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                # range=cell_range).execute()
    # values = result.get('values', [])

    # print(values)

    # return

    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                # range=SAMPLE_RANGE_NAME).execute()
    # values = result.get('values', [])

    # if not values:
        # print('No data found.')
    # else:
        # print('Name, Major:')
        # for row in values:
            # # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s, %s' % (row[0], row[4]))

def ask_questions(data, idx, n_fields):

    for row_idx in idx:
        data_row = data[row_idx]
        # print(data_row)

        prompt = data_row[0]
        # right_answer = data_row[1].strip()
        right_answer = " ".join([x.strip() for x in data_row[1:n_fields+1]]).lower()

        print(f"What's the translation of {prompt}?")

        answer = input().strip().lower()

        print(50*"=")
        if answer == right_answer:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Wrong!{bcolors.ENDC}")
            check_solution(answer, right_answer)

if __name__ == '__main__':
    main()
