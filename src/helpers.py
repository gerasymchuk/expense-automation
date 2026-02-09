from datetime import date, datetime

def calc_next_month(year: str, month: str) -> tuple[str, str]:
    if month == 'December':
        return (str(int(year) + 1), 'January')
    else:
        month_number = datetime.strptime(month, '%B').month
        return (year, datetime.strftime(date(int(year), month_number + 1, 1), '%B'))