import re
from config                     import MIN_PLAYER_AGE, MIN_ROUND, MAX_ROUND, MAX_DESCRIPTION_LENGTH
from utils.date_helpers         import get_today
from utils.error_messages       import invalid_min_player_age
from utils.input_formatters     import parse_raw_date




def is_valid_name(name: str) -> str:
    if name is not None:
        cleaned_name = name.replace(" ", "").replace("-", "")
        return cleaned_name.isalpha() and len(cleaned_name) >= 2


def is_valid_player_birthdate(date_str: str | None) -> bool:
    """
    Vérifie si une date de naissance saisie par l'utilisateur est valide.

    La date doit :
    - Être au format JJMMAAAA (avec ou sans séparateurs : /, -, ., espace)
    - Être une date réelle (ex. 31022000 est invalide)
    - Ne pas être dans le futur
    - Être postérieure à l'année 1900
    - Correspondre à un âge supérieur ou égal à MIN_PLAYER_AGE

    Args:
        birth_date (str | None): La date de naissance saisie par l'utilisateur.

    Returns:
        bool: True si la date est valide, False sinon.
    """
    if not isinstance(date_str, str):
        return False

    birth_date = parse_raw_date(date_str)
    if birth_date is None:
        return False

    today = get_today()

    if birth_date > today or birth_date.year < 1900:
        return False

    age = (today - birth_date).days // 365
    if age < MIN_PLAYER_AGE:
        invalid_min_player_age()
        return False

    return True


def is_valid_id_national_chess(id_national_chess: str) -> bool:
    return re.fullmatch(r"[A-Z]{2}\d{5}", id_national_chess) is not None


def is_valid_tournament_name(tournament_name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9\-' ]+", tournament_name))


def is_valid_start_date(date_str: str | None) -> bool:
    """
    Vérifie que la date de début est :
    - une date valide au format JJMMAAAA (libre)
    - supérieure ou égale à la date d'aujourd'hui
    """
    if not isinstance(date_str, str):
        return False
    
    start_date = parse_raw_date(date_str)
    if start_date is None:
        return False
    return start_date.date() >= get_today().date()


def is_valid_end_date(date_str: str | None, start_date_str: str) -> bool:
    """
    Vérifie que la date de fin est :
    - une date valide au format JJMMAAAA (libre)
    - supérieure ou égale à la date de début
    """
    if not isinstance(date_str, str) or not isinstance(start_date_str, str):
        return False
    
    end_date = parse_raw_date(date_str)
    start_date = parse_raw_date(start_date_str)
    
    if not end_date or not start_date:
        return False
    
    return end_date >= start_date


def is_valid_location_name(location: str) -> str | None:
    """
    Valide un nom de lieu selon les règles suivantes :
    - Contient au moins 2 caractères alphanumériques
    - N'utilise que lettres, chiffres, espaces, tirets et apostrophes
    - Ne contient pas plus de 2 caractères spéciaux consécutifs
    - Ne commence ni ne finit par un caractère spécial

    Returns:
        str | None: Le nom en majuscules si valide, sinon None
    """
    if not isinstance(location, str):
        return None

    location = location.strip()

    # On conserve uniquement lettres et chiffres pour vérifier la quantité minimale
    only_alphanum = re.sub(r"[^a-zA-Z0-9]", "", location)
    if len(only_alphanum) < 2:
        return None

    # Autoriser : lettres, chiffres, espaces, tirets, apostrophes
    if not re.fullmatch(r"[a-zA-Z0-9\s\-']+", location):
        return None

    # Pas plus de 2 caractères spéciaux consécutifs
    if re.search(r"[\-'\s]{3,}", location):
        return None

    # Ne commence ni ne termine par un caractère spécial
    if re.match(r"^[\-\s']", location) or re.search(r"[\-\s']$", location):
        return None

    return location


def is_valid_number_of_rounds(number: int) -> bool:
    return MIN_ROUND <= number <= MAX_ROUND

def is_valid_description(description: str) -> bool:
    """
    Valide une description :
    - optionnelle (vide autorisé)
    - < ou = 500 caractères
    """
    if not isinstance(description, str):
        return False

    cleaned_description = description.strip()

    return len(cleaned_description) == 0 or len(cleaned_description) <= MAX_DESCRIPTION_LENGTH


def is_valid_yes_no(value: str) -> bool:
    """
    Vérifie que la chaîne formatée est exactement "Y" ou "N".

    À utiliser après avoir appelé `format_yes_no()`.

    Exemple :
        is_valid_yes_no("Y")  → True
        is_valid_yes_no("N")  → True
        is_valid_yes_no("X")  → False
        is_valid_yes_no("")   → False
    """
    return value in ("Y", "N")
