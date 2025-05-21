import re
from datetime import datetime


def is_valid_name(name: str) -> str:
    cleaned_name = name.replace(" ", "").replace("-", "")
    return cleaned_name.isalpha() and len(cleaned_name) >= 2


def is_valid_date(date_str: str | None) -> bool:
    # Si date_str = None, return False
    if not isinstance(date_str, str):
        return False
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")

        # Vérifie que la date n'est pas dans le futur
        if date > datetime.today():
            return False
        
        # Vérifie que ce soit une année réaliste
        if date.year < 1900:
            return False
        
        # Vérifie que l'âge est raisonnable
        # age = (datetime.today() - date).days // 365
        # if age < 5:
        #     print("Âge minimal pour s'inscrire : 5 ans")
        #     return False
        
        return True
    
    except ValueError:
        return False


def is_valid_id_national_chess(id_national_chess: str) -> bool:
    return re.fullmatch(r"[A-Z]{2}\d{5}", id_national_chess) is not None

