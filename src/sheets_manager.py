import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from src.model import TransactionRow


class SheetsManager:
    def __init__(self, sheet_id: str, credentials_path: str):
        self.sheet_id = sheet_id
        self.credentials_path = credentials_path
        self.client = None
        self.sheet = None
        self._connect()

    def _connect(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
    ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(self.sheet_id)


    def insert_expense_rows(self, rows: list[TransactionRow]) -> None:
        if not rows:
            return

        ws = self.sheet.worksheet('Витрати')
        rows = [row.to_list() for row in rows]
        ws.insert_rows(rows, row=2, value_input_option='USER_ENTERED')

    def insert_income_rows(self, rows: list[TransactionRow]) -> None:
        if not rows:
            return

        ws = self.sheet.worksheet('Доходи')
        rows = [row.to_list() for row in rows]
        ws.insert_rows(rows, row=2)

    def get_last_processed_month(self) -> tuple[str, str]:
        ws = self.sheet.worksheet('metadata')
        year_month = ws.get('B1')[0][0]
        last_processed_month = tuple[str, str](year_month.split(' ')) # ('2026', 'January')
        return last_processed_month

    def update_last_processed_month(self, year_month: str) -> None:
        ws = self.sheet.worksheet('metadata')
        ws.update_acell('B1', year_month)