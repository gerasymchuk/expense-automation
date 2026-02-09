from datetime import date, datetime

def calc_next_month(year: str, month: str) -> tuple[str, str]:
    if month == 'December':
        return (str(int(year) + 1), 'January')
    else:
        month_number = datetime.strptime(month, '%B').month
        return (year, datetime.strftime(date(int(year), month_number + 1, 1), '%B'))

def to_date(year: str, month_name: str) -> datetime:
    # "2026" + "January" → datetime(2026, 1, 1)
    return datetime.strptime(f"{year} {month_name}", "%Y %B")

def current_month_date() -> datetime:
    now = datetime.now()
    return datetime(now.year, now.month, 1)
