import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetsManager:
    def __init__(self, sheet_id: str, credentials_path: str):
        self.sheet_id = sheet_id
        self.credentials_path = credentials_path
        self.client = None
        self.sheet = None
        self.connect()

    def _connect(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
    ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(self.sheet_id)


    def get_sheet(self):
        return self.sheet

    def get_sheet_by_name(self, sheet_name: str):
        return self.sheet.worksheet(sheet_name)