import re

from datetime import datetime

from utils.error_messages import invalid_min_player_age_message
from config import DATE_STORAGE_FORMAT, MIN_PLAYER_AGE



def is_valid_name(name: str) -> str:
    cleaned_name = name.replace(" ", "").replace("-", "")
    return cleaned_name.isalpha() and len(cleaned_name) >= 2


def is_valid_date(date_str: str | None) -> bool:
    # Si date_str = None, return False
    if not isinstance(date_str, str):
        return False
    try:
        date = datetime.strptime(date_str, DATE_STORAGE_FORMAT)

        # Vérifie que la date n'est pas dans le futur
        if date > datetime.today():
            return False
        
        # Vérifie que ce soit une année réaliste
        if date.year < 1900:
            return False
        
        # Vérifie que l'âge est raisonnable
        age = (datetime.today() - date).days // 365
        if age < MIN_PLAYER_AGE:
            invalid_min_player_age_message()
            return False
        
        return True
    
    except ValueError:
        return False


def is_valid_id_national_chess(id_national_chess: str) -> bool:
    return re.fullmatch(r"[A-Z]{2}\d{5}", id_national_chess) is not None

