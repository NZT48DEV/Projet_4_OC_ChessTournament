from datetime import datetime

def format_first_name(first_name: str) -> str:
    first_name = first_name.strip().title()
    return first_name[:20]

def format_last_name(last_name: str) -> str:
    last_name = last_name.strip().upper()
    return last_name[:20]

def format_id_national_chess(id_national_chess: str) -> str:
    return id_national_chess.strip().upper()

def format_date(date_str: str) -> str | None:
    date_str = date_str.strip()
    for separator in [" ", "-", ".", "/"]:
        date_str = date_str.replace(separator, "")

    if len(date_str) == 8:
        # Format attendu : JJMMYYYY
        try:
            date = datetime.strptime(date_str, "%d%m%y")
            return date.strftime("%d/%m/%Y")
        except ValueError:
            return None
    
    elif len(date_str) == 6:
        # Format attendu : JJMMYY -> on suppose année 2000+
        try:
            date = datetime.strptime(date_str, "%d%m%Y")
            return date.strftime("%d/%m%Y")
        except ValueError:
            return None
    
    else:
        return None
