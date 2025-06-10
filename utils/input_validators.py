import re

from config import MIN_PLAYER_AGE, MIN_ROUND, MAX_ROUND, MAX_DESCRIPTION_LENGTH
from utils.date_helpers import get_today
from utils.input_formatters import parse_raw_date


def is_valid_name(name: str) -> bool:
    """
    Vérifie qu'un nom est valide pour un joueur.

    Le nom après suppression des espaces et des tirets doit :
      - ne contenir que des lettres (A–Z, a–z)
      - mesurer au moins 2 caractères

    Args:
        name (str): La chaîne entrée par l'utilisateur.

    Returns:
        bool: True si le nom est valide, False sinon.
    """
    if name is not None:
        cleaned_name = name.replace(" ", "").replace("-", "")
        return cleaned_name.isalpha() and len(cleaned_name) >= 2
    return False


def is_valid_player_birthdate(date_str: str | None) -> bool:
    """
    Vérifie si une date de naissance est valide et respecte l'âge minimum.

    Critères :
      - Format JJMMAAAA (avec ou sans séparateurs : /, -, ., espace)
      - Date réelle (ex. 31/02/2000 est invalide)
      - Non future
      - Année ≥ 1900
      - Âge ≥ MIN_PLAYER_AGE (si inférieur, affiche un message d'erreur)

    Args:
        date_str (str | None): Chaîne représentant la date de naissance.

    Returns:
        bool: True si la date est valide et l'âge suffisant, False sinon.
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
        return False

    return True


def is_valid_id_national_chess(id_national_chess: str) -> bool:
    """
    Vérifie la validité de l'identifiant national d'échecs.

    Format attendu : deux lettres majuscules suivies de cinq chiffres (ex. "AB12345").

    Args:
        id_national_chess (str): Chaîne à vérifier.

    Returns:
        bool: True si elle correspond au format, False sinon.
    """
    return re.fullmatch(r"[A-Z]{2}\d{5}", id_national_chess) is not None


def is_valid_tournament_name(tournament_name: str) -> bool:
    """
    Vérifie qu'un nom de tournoi est valide.

    Autorise lettres (A–Z, a–z), chiffres, espaces, tirets et apostrophes.

    Args:
        tournament_name (str): Nom saisi par l'utilisateur.

    Returns:
        bool: True si le nom est conforme, False sinon.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9\-' ]+", tournament_name))


def is_valid_start_date(date_str: str | None) -> bool:
    """
    Vérifie qu'une date de début de tournoi est valide.

    Critères :
      - Format JJMMAAAA correct (avec ou sans séparateurs)
      - Date ≥ aujourd'hui

    Args:
        date_str (str | None): Chaîne de date saisie.

    Returns:
        bool: True si la date est valide et pas dans le passé, False sinon.
    """
    if not isinstance(date_str, str):
        return False

    start_date = parse_raw_date(date_str)
    if start_date is None:
        return False

    return start_date.date() >= get_today().date()


def is_valid_end_date(date_str: str | None, start_date_str: str) -> bool:
    """
    Vérifie qu'une date de fin de tournoi est valide et après la date de début.

    Args:
        date_str (str | None): Chaîne de date de fin saisie.
        start_date_str (str): Chaîne de date de début déjà validée.

    Returns:
        bool: True si la date de fin est valide et ≥ date de début, False sinon.
    """
    if not isinstance(date_str, str) or not isinstance(start_date_str, str):
        return False

    end_date = parse_raw_date(date_str)
    start_date = parse_raw_date(start_date_str)
    if end_date is None or start_date is None:
        return False

    return end_date >= start_date


def is_valid_location_name(location: str) -> str | None:
    """
    Valide un nom de lieu selon les règles :
      - Au moins 2 caractères alphanumériques
      - Contient uniquement lettres, chiffres, espaces, tirets, apostrophes
      - Pas plus de 2 caractères spéciaux consécutifs
      - Ne commence ni ne finit par un caractère spécial

    Args:
        location (str): Chaîne entrée par l'utilisateur.

    Returns:
        str | None: La chaîne nettoyée si valide, None sinon.
    """
    if not isinstance(location, str):
        return None

    location = location.strip()
    only_alphanum = re.sub(r"[^a-zA-Z0-9]", "", location)
    if len(only_alphanum) < 2:
        return None

    if not re.fullmatch(r"[a-zA-Z0-9\s\-']+", location):
        return None

    if re.search(r"[\-'\s]{3,}", location):
        return None

    if re.match(r"^[\-\s']", location) or re.search(r"[\-\s']$", location):
        return None

    return location


def is_valid_number_of_rounds(number: int) -> bool:
    """
    Vérifie si le nombre de rounds est dans les bornes autorisées.

    Args:
        number (int): Nombre de rounds saisi.

    Returns:
        bool: True si MIN_ROUND ≤ number ≤ MAX_ROUND, False sinon.
    """
    return MIN_ROUND <= number <= MAX_ROUND


def is_valid_description(description: str) -> bool:
    """
    Valide la description d'un tournoi.

    Critères :
      - Chaîne optionnelle (vide autorisé)
      - Longueur ≤ MAX_DESCRIPTION_LENGTH

    Args:
        description (str): Texte de description saisi.

    Returns:
        bool: True si la description est vide ou de longueur acceptable, False sinon.
    """
    if not isinstance(description, str):
        return False

    cleaned_description = description.strip()
    return len(cleaned_description) == 0 or len(cleaned_description) <= MAX_DESCRIPTION_LENGTH


def is_valid_yes_no(value: str) -> bool:
    """
    Vérifie qu'une réponse formatée est soit "Y", soit "N".

    À utiliser après avoir normalisé la saisie via format_yes_no().

    Args:
        value (str): Chaîne attendue ("Y" ou "N").

    Returns:
        bool: True si value == "Y" ou "N", False sinon.
    """
    return value in ("Y", "N")
