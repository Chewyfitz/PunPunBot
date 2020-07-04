from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheet():
    def __init__ (self, GSID:str, year:int =2020, month:int =7):
        self.dayMap = {
            1  : 'B', 2  : 'C', 3  : 'D', 4  : 'E', 5  : 'F', 6  : 'G', 7  : 'H',
            8  : 'I', 9  : 'J', 10 : 'K', 11 : 'L', 12 : 'M', 13 : 'N', 14 : 'O',
            15 : 'P', 16 : 'Q', 17 : 'R', 18 : 'S', 19 : 'T', 20 : 'U', 21 : 'V',
            22 : 'W', 23 : 'X', 24 : 'Y', 25 : 'Z', 26 : 'AA', 27 : 'AB', 28 : 'AC',
            29 : 'AD', 30 : 'AE', 31 : 'AF'
        }
        self.year = year
        self.month = month
        self.spreadsheet = GSID

    
    def startService(self):
        creds = None
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
        
        self.service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        self.sheet = self.service.spreadsheets()
        request = self.sheet.values().get(spreadsheetId=self.spreadsheet, range='{}-{:02d}!A1:A'.format(self.year, self.month))
        response = request.execute()

        # Get the list of user names and their corresponding row numbers
        # (this is a spreadsheet so it can be manually updated, but I'd recommend against that)
        self.users = {}
        self.max = 0
        for row in response['values']:
            self.max = self.max+1
            if(self.max < 2):
                continue
            self.users[row[0]] = self.max
        # print("self.users: {}".format(self.users))
        # print("self.max: {}".format(self.max))
        
    def addUser(self, name: str):
        self.max = self.max +1
        self.users[name] = self.max
        cell = "{}-{:02d}!{}{}".format(self.year, self.month, 'A', self.users[name])
        body = {"values": [[ name ]]}

        req = self.sheet.values().update(spreadsheetId=self.spreadsheet, range=cell, valueInputOption='USER_ENTERED', body=body)
        req.execute()

    
    def sleepTime(self, name: str, time: str, year:int, month: int, day: int):
        self.year = year
        self.month = month
        if name not in self.users:
            self.addUser(name)
        cell = "{}-{:02d}!{}{}".format(self.year, self.month, self.dayMap[day], self.users[name])

        body = {"values": [[ "{}:{}".format(time.hour, time.minute) ]]}

        req = self.sheet.values().update(spreadsheetId=self.spreadsheet, range=cell, valueInputOption='USER_ENTERED', body=body)
        req.execute()
        print("Set sleep time for {} to {}".format(name, "{}:{}".format(time.hour, time.minute)))