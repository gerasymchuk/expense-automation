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


    def insert_rows(self, worksheet_name: str, rows: list[TransactionRow]) -> None:
        if not rows:
            return

        ws = self.sheet.worksheet(worksheet_name)
        rows = [row.to_list() for row in rows]
        ws.insert_rows(rows, row=2, value_input_option='USER_ENTERED')

    def get_last_processed_month(self) -> tuple[str, str]:
        ws = self.sheet.worksheet('metadata')
        year_month = ws.get('B1')[0][0]
        last_processed_month = tuple[str, str](year_month.split(' ')) # ('2026', 'January')
        return last_processed_month

    def update_last_processed_month(self, year: str, month: str) -> None:
        ws = self.sheet.worksheet('metadata')
        ws.update_acell('B1', f"{year} {month}")

    def _find_month_rows(self, worksheet_name: str, year: str, month: str) -> list[int]:
        ws = self.sheet.worksheet(worksheet_name)
        all_rows = ws.get_all_values()
        list_of_indexes = []
        for row_number, row in enumerate[list[int]](all_rows[1:]):
            if row[0] == year and row[1] == month:
                list_of_indexes.append(row_number + 2)
        return list_of_indexes

    def insert_or_update_month(self, worksheet_name, rows: list[TransactionRow]):
        if not rows:
            return

        year = rows[0].year
        month = rows[0].month

        existing = self._find_month_rows(worksheet_name, year, month)

        if existing:
            first = existing[0]
            last = existing[-1]
            ws = self.sheet.worksheet(worksheet_name)
            ws.delete_rows(first, last)


        self.insert_rows(worksheet_name, rows)