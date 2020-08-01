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
        # request = self.sheet.values().get(spreadsheetId=self.spreadsheet, range='{}-{:02d}!A1:A'.format(self.year, self.month))
        request = self.sheet.values().get(spreadsheetId=self.spreadsheet, range='usermap!A1:B'.format(self.year, self.month))
        response = request.execute()

        # Get the list of user names and their corresponding row numbers
        # (this is a spreadsheet so it can be manually updated, but I'd recommend against that)
        self.users = {}
        self.uids = {}
        self.max = 0
        for row in response['values']:
            self.max = self.max+1
            if(self.max < 2):
                continue
            self.uids[row[0]] = self.max
            self.users[row[1]] = self.max
        # print("self.users: {}".format(self.users))
        # print("self.max: {}".format(self.max))
    

    # Add a new row to the spreadsheet
    def addUser(self, uid: str, userName: str):
        # Keep track of the number of users, and add the current user to the row map
        self.max = self.max +1
        self.uids[uid] = self.max
        self.users[userName] = self.max

        # Set the cell reference, and cell value
        cell = "{}-{:02d}!{}{}".format(self.year, self.month, 'A', self.users[uid])
        body = {"values": [[ uid ]]}

        # Create the update action
        req = self.sheet.values().update(spreadsheetId=self.spreadsheet, range=cell, valueInputOption='USER_ENTERED', body=body)

        # Commit the action
        req.execute()

        # Set cell reference and cell values for usermap
        cell2 = "usermap!A{}:B{}".format(self.users[uid], self.users[uid])
        body2 = {"values": [[ uid, userName ]]}

        # Add user to usermap
        req2 = self.sheet.values().update(spreadsheetId=self.spreadsheet, range=cell2, valueInputOption='USER_ENTERED', body=body2)
        req2.execute()

    
    def sleepTime(self, author: str, userName: str, time: str, year:int, month: int, day: int):
        # Update the year and month
        self.year = year
        self.month = month

        # Add user if not already participating
        if author.id not in self.uids:
            self.addUser(author.id, userName)

        # Set cell reference
        cell = "{}-{:02d}!{}{}".format(self.year, self.month, self.dayMap[day], self.uids[author.id])
        # Set cell value
        body = {"values": [[ "{}:{:02d}".format(time.hour, time.minute) ]]}
        # Create update action
        req = self.sheet.values().update(spreadsheetId=self.spreadsheet, range=cell, valueInputOption='USER_ENTERED', body=body)
        # Commit the action
        req.execute()

        # Log sleep time to STDOUT
        print("Set sleep time for {} to {}".format(author.id, "{}:{}".format(time.hour, time.minute)))