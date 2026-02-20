from pathlib import Path
from datetime import datetime
import json
import pandas as pd
from src.sheets_manager import SheetsManager

class CacheManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.metadata_path = self.cache_dir / 'metadata.json'
        self.cache_dir.mkdir(exist_ok=True)

    def is_valid(self, sheet_name: str) -> bool:
        file_path = self.cache_dir / f'{sheet_name}.parquet'
        if not file_path.exists():
            return False

        metadata = self._get_metadata()

        if sheet_name not in metadata:
            return False

        last_updated = datetime.fromisoformat(metadata[sheet_name])
        today = datetime.now()

        return last_updated.year == today.year and last_updated.month == today.month

    def _get_metadata(self) -> dict:
        if not self.metadata_path.exists():
            return {}

        try:
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file: {self.metadata_path}")
            return {}

    def _save_metadata(self, metadata: dict) -> None:
        if not metadata:
            return

        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

    def load_dataframe(self, sheet_name: str) -> pd.DataFrame:
        return pd.read_parquet(self.cache_dir / f'{sheet_name}.parquet')

    def save_dataframe(self, sheet_name: str, df: pd.DataFrame) -> None:
        df.to_parquet(self.cache_dir / f'{sheet_name}.parquet')
        metadata = self._get_metadata()
        metadata[sheet_name] = datetime.now().isoformat()
        self._save_metadata(metadata)

class DataLoader:
    def __init__(self, sheets_manager: SheetsManager, cache: CacheManager):
        self.sheets_manager = sheets_manager
        self.cache = cache

    def _load_sheet(self, sheet_name: str, numeric_cols: list[str]) -> pd.DataFrame:
        if self.cache.is_valid(sheet_name):
            return self.cache.load_dataframe(sheet_name)
        else:
            data = self.sheets_manager.get_all_data(sheet_name)
            df = pd.DataFrame(data[1:], columns=data[0])
            df = self._normalize_columns(df)
            df = df.loc[:, df.columns != '']
            # df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

            self.cache.save_dataframe(sheet_name, df)
            return df

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = (df.columns
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
            .str.replace('(', '')
            .str.replace(')', '')
            .str.strip()
        )
        return df

    def get_expenses(self) -> pd.DataFrame:
        return self._load_sheet('Expenses', ['amount'])

    def get_income(self) -> pd.DataFrame:
        return self._load_sheet('Income', ['amount'])

    def get_savings(self) -> pd.DataFrame:
        return self._load_sheet('Savings', ['starting_balance', 'inflow', 'withdrawal', 'running_balance'])

    def get_currency_vault(self) -> pd.DataFrame:
        return self._load_sheet('Currency Vault', ['opening_balance', 'salary_gross', 'converted', 'closing_balance'])

    def get_budget(self) -> pd.DataFrame:
        return self._load_sheet('Budget', ['opening_balance', 'total_income', 'total_expenses', 'transfer_to_savings', 'inflow_from_savings', 'net_cash_flow', 'closing_balance'])

    def get_summary(self) -> pd.DataFrame:
        return self._load_sheet('Summary', ['net_income', 'estimated_total_income_usd', 'total_lifestyle_expenses', 'avg_monthly_expenses', 'transfer_to_savings', 'inflow_from_savings', 'annual_cash_balance'])