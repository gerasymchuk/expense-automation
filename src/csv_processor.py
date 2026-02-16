import pandas as pd
from src.model import TransactionRow
from datetime import datetime

def _parse_date_column(df: pd.DataFrame, col: str = 'date') -> pd.DataFrame:
    df[col] = pd.to_datetime(df[col])
    return df

def _extract_year_month(df: pd.DataFrame, col: str = 'date') -> pd.DataFrame:
    df['year'] = df[col].dt.year.astype(str)
    df['month'] = df[col].dt.month_name()
    return df

def filter_by_month_year(df: pd.DataFrame, month: str, year: str) -> pd.DataFrame:
    return df[(df['year'] == year) & (df['month'] == month)]

def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    categories_to_exclude = ['Transfer'] # temp
    df = df[~df['category'].isin(categories_to_exclude)]
    df = df[df['outcome'] < 0].groupby(['year', 'month', 'category'])['outcome'].sum().abs().reset_index()
    return df

def to_expense_rows(df: pd.DataFrame) -> list[TransactionRow]:
    return [TransactionRow(year=row.year, month=row.month, category=row.category, amount=row.outcome) for row in df.itertuples()]

def process_expenses(csv_path:str, month: str, year: str) -> list[TransactionRow]:
    df = pd.read_csv(csv_path)
    df = _parse_date_column(df)

    today = datetime.now()
    future_transactions = df[df['date'] > today]

    if len(future_transactions) > 0:
        future_dates = future_transactions['date'].tolist()
        raise ValueError(f"Found transactions with future dates: {future_dates}")

    df = _extract_year_month(df)
    df = filter_by_month_year(df, month, year)
    df = aggregate_by_category(df)

    return to_expense_rows(df)