import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
START_COL = "O"
END_COL = "V"

COLUMNS_TEMPLATE = 'NIK,DPT,NAMA PEMILIH,TPS,ALAMAT TPS,KABUPATEN,KECAMATAN,KELURAHAN'

class GoogleSheet(object):
    def __init__(self,spreadsheet_id, sheet_name, start_range, end_range):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.sheet_range = f'{START_COL}{start_range}:{END_COL}{end_range}'

        
    def createService(self):
        print("\nConecting to Spreadsheets...")
        self.creds = None
        if os.path.exists("token.json"):
            try:
                self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            except:
                print("Token Expired")
      
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Spreadsheet Token Request\n")
                self.creds.refresh(Request())
            else:
                try:
                    print("Read GSCredential\n")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "./GSCredential.json", SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                except:
                    print("ERROR!: GSCredential.json not found")
                    exit()

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        print("Connection Successfully\n")

    def read(self):
        print(f"Get Data From Sheet: {self.sheet_name} {self.sheet_range}")
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.spreadsheet_id, range=f'{self.sheet_name}!{self.sheet_range}')
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("ERROR!: No data found.")
                exit()
            
            columns = COLUMNS_TEMPLATE.split(',')
            rows = values
 
            print(f"Total data: {len(rows)} NIK")
            data = []
            for row in rows:
                dataObj = {}
                for idx, col in enumerate(columns):
                    if len(row) >= idx+1:
                        dataObj[col] = row[idx]
                    else:
                        dataObj[col] = None
                data.append(dataObj)

            df= pd.DataFrame.from_dict(data)
            return df
        except HttpError as err:
            raise Exception(err)
    def write(self,data):
        try:
            service = build("sheets", "v4", credentials=self.creds)
            values = data.T.reset_index().T.values.tolist()[1:]
            data = [
                {"range": f"{self.sheet_name}!{self.sheet_range}", "values": values},
            
            ]
            body = {"valueInputOption": 'USER_ENTERED', "data": data}
            result = (
                service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
                .execute()
            )

            print('Sheet successfully Updated')
        except HttpError as err:
            raise Exception(err)

    def writeRow(self,data_result,row):
        try:
            service = build("sheets", "v4", credentials=self.creds)
            values = data_result.T.reset_index().T.values.tolist()[1:]
            data = [
                {"range": f"{self.sheet_name}!{START_COL}{row}:{END_COL}{row}", "values": values}
            ]
            body = {"valueInputOption": 'USER_ENTERED', "data": data}
            result = (
                service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
                .execute()
            )
        except:
            try:
                service = build("sheets", "v4", credentials=self.creds)
                values = data_result.T.reset_index().T.values.tolist()[1:]
                data = [
                    {"range": f"{self.sheet_name}!{START_COL}{row}:{END_COL}{row}", "values": values}
                ]
                body = {"valueInputOption": 'USER_ENTERED', "data": data}
                result = (
                    service.spreadsheets()
                    .values()
                    .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
                    .execute()
                )
            except HttpError as err:
                print(err)
        