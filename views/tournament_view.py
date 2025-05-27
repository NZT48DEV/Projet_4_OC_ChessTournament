from utils.input_formatters import (
    format_tournament_name, 
    format_date, 
    format_location_name,
    format_number_of_rounds,
    format_description)
from utils.input_validators import (
    is_valid_tournament_name, 
    is_valid_start_date, 
    is_valid_end_date, 
    is_valid_location_name,
    is_valid_number_of_rounds,
    is_valid_description)
from utils.error_messages import (
    invalid_tournament_name, 
    invalid_date,
    invalid_location_name,
    invalid_number_of_rounds,
    invalid_description)
from utils.input_manager import get_valid_input


class CreateTournament:
    def display_create_tournament_menu(self):
        print("\n" + "=" * 40)
        print("🏆    CRÉATION D'UN TOURNOI    🏆")
        print("=" * 40)

        tournament_name = get_valid_input(
            prompt="Nom du tournoi : ",
            formatter=format_tournament_name,
            validator=is_valid_tournament_name,
            message_error=invalid_tournament_name
            )

        location = get_valid_input(
            prompt="Lieu : ",
            formatter=format_location_name,
            validator=is_valid_location_name,
            message_error=invalid_location_name
            )

        start_date = get_valid_input(
            prompt="Date de début (JJMMAAA) : ",
            formatter=format_date,
            validator=is_valid_start_date,
            message_error=invalid_date
            )
        
        end_date = get_valid_input(
            prompt="Date de fin (JJMMAAAA) : ",
            formatter=format_date,
            validator=lambda end_date_input: is_valid_end_date(end_date_input, start_date),
            message_error=invalid_date
            )
        
        number_of_rounds = get_valid_input(
            prompt="Nombre de rounds (par défaut 4): ",
            formatter=format_number_of_rounds,
            validator=is_valid_number_of_rounds,
            message_error=invalid_number_of_rounds
            )
        
        description = get_valid_input(
            prompt="Description/Remarques : ",
            formatter=format_description,
            validator=is_valid_description,
            message_error=invalid_description
            )

        return {
            "tournament_name": tournament_name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_rounds": number_of_rounds,
            "description": description
        }