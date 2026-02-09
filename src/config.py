from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SHEET_ID = os.getenv('SHEET_ID')
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')
    CSV_PATH = os.getenv('CSV_PATH')

    @classmethod
    def validate(cls):
        if not cls.SHEET_ID:
            raise ValueError('SHEET_ID is not set')
        if not cls.CREDENTIALS_PATH:
            raise ValueError('CREDENTIALS_PATH is not set')
        if not os.path.exists(cls.CREDENTIALS_PATH):
            raise FileNotFoundError(f'Credentials file not found: {cls.CREDENTIALS_PATH}')
        if not os.path.exists(cls.CSV_PATH):
            raise FileNotFoundError(f'CSV file not found: {cls.CSV_PATH}')
        if not cls.CSV_PATH.endswith('.csv'):
            raise ValueError('CSV file must have a .csv extension')
