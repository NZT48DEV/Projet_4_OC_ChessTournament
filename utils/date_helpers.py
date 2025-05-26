from datetime import datetime
from config import DATE_STORAGE_FORMAT, DATE_INPUT_FORMAT


def get_today() -> datetime:
    """Retourne la date/heure actuelle."""
    return datetime.today()


def parse_date_str(date_str: str) -> datetime | None:
    """
    Essaie de parser une date au format DATE_STORAGE_FORMAT (AAAA-MM-JJ).
    
    Args:
        date_str (str): La date en chaîne.

    Returns:
        datetime | None: L’objet datetime si valide, sinon None.
    """
    try:
        return datetime.strptime(date_str, DATE_STORAGE_FORMAT)
    except (ValueError, TypeError):
        return None
    

def parse_raw_date(date_str: str) -> datetime | None:
    """
    Nettoie une date brute (avec ou sans séparateurs) et tente de la parser
    en format JJMMYYYY (ex: '01/01/2025', '01-01-2025', etc.).

    Returns:
        datetime | None: Objet datetime si succès, sinon None.
    """
    if not isinstance(date_str, str):
        return None
    
    cleaned = date_str.strip()
    for sep in [" ", "-", ".", "/"]:
        cleaned = cleaned.replace(sep, "")

    if len(cleaned) != 8:
        return None

    try:
        return datetime.strptime(cleaned, DATE_INPUT_FORMAT)
    except ValueError:
        return None