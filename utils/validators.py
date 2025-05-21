import re
from datetime import datetime

def is_valid_name(name: str) -> str:
    cleaned_name = name.replace(" ", "").replace("-", "")
    return cleaned_name.isalpha() and len(cleaned_name) >= 2

def is_valid_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_valid_id_national_chess(id_national_chess: str) -> bool:
    return re.fullmatch(r"[A-Z]{2}\d{5}", id_national_chess) is not None

