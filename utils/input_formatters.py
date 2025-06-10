from config import (
    DATE_STORAGE_FORMAT,
    DEFAULT_NUMBER_OF_ROUND,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
    MAX_TOURNAMENT_NAME_LENGTH
)
from utils.date_helpers import parse_raw_date
from utils.error_messages import invalid_number_of_rounds


def format_name(last_name: str) -> str:
    """
    Formate le nom du joueur
    - Supprime les espaces en début et en fin de chaîne
    - Convertit tous les caractères en majuscules
    - Vérifie que la longueur du last_name soit inférieur ou = a MAX_NAME_LENGTH (40 caractères maximum)

    Args:
        last_name(str): Le nom du joueur à formater

    Returns:
        None
        ou
        str: Le nom formaté
    """
    last_name = last_name.strip().upper()
    if len(last_name) > MAX_LAST_NAME_LENGTH:
        return None
    return last_name


def format_first_name(first_name: str) -> str:

    first_name = first_name.strip().capitalize()
    if len(first_name) > MAX_FIRST_NAME_LENGTH:
        return None
    return first_name


def format_tournament_name(tournament_name: str) -> str:
    """
    Formate le nom du tournoi :
    - Si le nom est uniquement numérique, ajoute 'TOURNOI' devant
    - Transforme tout en majuscules
    - Coupe à MAX_NAME_LENGTH (40 caractères maximum)

    Args:
        tournament_name(str): Le nom du tournoi à formatter
    """
    tournament_name = tournament_name.strip().upper()[:MAX_TOURNAMENT_NAME_LENGTH]

    if tournament_name.isdigit():
        return f"TOURNOI {tournament_name[:MAX_TOURNAMENT_NAME_LENGTH]}"
    return tournament_name


def format_id_national_chess(id_national_chess: str) -> str:
    """
    Formate l'ID national d'échecs :
    - Supprime les espaces en début et en fin de chaîne
    - Transforme tout en majuscules

    Args:
        id_national_chess(str): l'ID national d'échecs à formatter
    """
    return id_national_chess.strip().upper()


def format_date(date_str: str) -> str | None:
    """
    Formate une date d'entrée utilisateur vers le format de stockage standard.

    Args:
        date_str (str): Une date brute (JJ/MM/AAAA, JJ-MM-AAAA, etc.)

    Returns:
        str | None: La date formatée (AAAA-MM-JJ) ou None si invalide.
    """
    date = parse_raw_date(date_str)
    if date is None:
        return None
    return date.strftime(DATE_STORAGE_FORMAT)


def format_location_name(location: str) -> str:
    """
    Formate le nom du lieu :
    - Supprime les espaces en début et en fin de chaîne
    - Transforme tout en majuscules

    Args:
        location(str): Le nom du lieu à formater

    Returns:
        str: Le nom du lieu formaté
    """
    return location.strip().upper()


def format_number_of_rounds(number_of_rounds: str) -> int:
    number_of_rounds = number_of_rounds.strip()

    if number_of_rounds == "":
        return DEFAULT_NUMBER_OF_ROUND

    try:
        return int(number_of_rounds)
    except ValueError:
        return invalid_number_of_rounds()


def format_description(description: str) -> str:
    """
    Nettoie la description :
    - Supprime les espaces en début/fin
    """
    return description.strip()


def format_yes_no(value: str) -> str:
    """
    Formatte une saisie en supprimant les espaces
    et en passant tout en majuscules.

    Exemple :
        " y "  → "Y"
        " n"   → "N"
    """
    return value.strip().upper()
