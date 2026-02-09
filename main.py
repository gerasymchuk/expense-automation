from src.config import Config
from src import csv_processor
from src import helpers
from src.sheets_manager import SheetsManager

def main():
    config = Config()
    config.validate()
    sheets_manager = SheetsManager(config.SHEET_ID, config.CREDENTIALS_PATH)

    last_year, last_month = sheets_manager.get_last_processed_month()
    target_year, target_month = helpers.calc_next_month(last_year, last_month)


    rows = csv_processor.process_expenses(config.CSV_PATH, target_month, target_year)


    sheets_manager.insert_expense_rows(rows)
    sheets_manager.update_last_processed_month(f'{target_year} {target_month}') # year month

if __name__ == '__main__':
    main()