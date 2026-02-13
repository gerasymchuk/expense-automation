from dotenv import load_dotenv
import os
import pandas as pd

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

    def validate_csv(csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        if not csv_path.endswith('.csv'):
            raise ValueError("File must be .csv")

        if os.path.getsize(csv_path) == 0:
            raise ValueError("CSV file is empty")

        try:
            df = pd.read_csv(csv_path)
            if len(df) == 0:
                raise ValueError("CSV has no data rows")

            # required columns
            required_cols = ['date', 'category', 'amount']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing columns: {missing}")

        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"CSV parsing error: {e}")