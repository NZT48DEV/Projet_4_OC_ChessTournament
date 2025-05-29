from utils.input_formatters import (
    format_tournament_name,
    format_date,
    format_location_name,
    format_number_of_rounds,
    format_description,
)
from utils.input_validators import (
    is_valid_tournament_name,
    is_valid_start_date,
    is_valid_end_date,
    is_valid_location_name,
    is_valid_number_of_rounds,
    is_valid_description,
)
from utils.error_messages import (
    invalid_tournament_name,
    invalid_date,
    invalid_location_name,
    invalid_number_of_rounds,
    invalid_description,
)
from utils.input_manager import get_valid_input


class TournamentView:
    """
    Vues CLI pour la création pas à pas d'un tournoi.
    """

    @staticmethod
    def ask_tournament_name() -> str:
        print("\n" + "="*40)
        print("🏆    NOM DU TOURNOI    🏆")
        print("="*40)
        return get_valid_input(
            prompt="Nom du tournoi : ",
            formatter=format_tournament_name,
            validator=is_valid_tournament_name,
            message_error=invalid_tournament_name,
        )

    @staticmethod
    def ask_location() -> str:
        print("\n" + "="*40)
        print("📍    LIEU DU TOURNOI    📍")
        print("="*40)
        return get_valid_input(
            prompt="Lieu : ",
            formatter=format_location_name,
            validator=is_valid_location_name,
            message_error=invalid_location_name,
        )

    @staticmethod
    def ask_start_date() -> str:
        print("\n" + "="*40)
        print("📅    DATE DE DÉBUT     📅")
        print("="*40)
        return get_valid_input(
            prompt="Date de début (JJMMAAAA) : ",
            formatter=format_date,
            validator=is_valid_start_date,
            message_error=invalid_date,
        )

    @staticmethod
    def ask_end_date(start_date: str) -> str:
        print("\n" + "="*40)
        print("📅    DATE DE FIN       📅")
        print("="*40)
        return get_valid_input(
            prompt="Date de fin (JJMMAAAA) : ",
            formatter=format_date,
            validator=lambda d: is_valid_end_date(d, start_date),
            message_error=invalid_date,
        )

    @staticmethod
    def ask_number_of_rounds() -> int:
        print("\n" + "="*40)
        print("🔢    NOMBRE DE ROUNDS   🔢")
        print("="*40)
        return get_valid_input(
            prompt="Nombre de rounds (par défaut 4) : ",
            formatter=format_number_of_rounds,
            validator=is_valid_number_of_rounds,
            message_error=invalid_number_of_rounds,
        )

    @staticmethod
    def ask_description() -> str:
        print("\n" + "="*40)
        print("📝    DESCRIPTION         📝")
        print("="*40)
        return get_valid_input(
            prompt="Description/Remarques : ",
            formatter=format_description,
            validator=is_valid_description,
            message_error=invalid_description,
        )
