from src.config import Config
from src import csv_processor
from src import helpers
from src.sheets_manager import SheetsManager


def main():
    config = Config()
    config.validate()
    config.validate_csv(config.CSV_PATH)
    sheets_manager = SheetsManager(config.SHEET_ID, config.CREDENTIALS_PATH)

    last_year, last_month = sheets_manager.get_last_processed_month()
    target_year, target_month = helpers.calc_next_month(last_year, last_month)
    current_date = helpers.current_month_date()

    last_processed = None
    failed_months = []

    while helpers.to_date(target_year, target_month) < current_date:
        try:
            print(f'Processing {target_year} {target_month}')
            rows = csv_processor.process_expenses(config.CSV_PATH, target_month, target_year)

            if len(rows) == 0:
                print(f'No rows to process for {target_year} {target_month}')
            else:
                sheets_manager.insert_or_update_month('Expenses', rows)

            last_processed = (target_year, target_month)
        except Exception as e:
            print(f"Failed to process {target_year}-{target_month}: {e}")
            failed_months.append((target_year, target_month))

        finally:
            target_year, target_month = helpers.calc_next_month(target_year, target_month)

    if last_processed:
        sheets_manager.update_last_processed_month(*last_processed)

    if failed_months:
        print(f"Failed months (process manually): {', '.join([f"{y} {m}" for y, m in failed_months])}")

if __name__ == '__main__':
    main()