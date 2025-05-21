import time
from utils.formatters import format_first_name, format_last_name, format_date, format_id_national_chess
from utils.validators import is_valid_name, is_valid_date, is_valid_id_national_chess
from utils.messages import invalide_name_message, invalid_date_message, invalide_id_national_chess
from utils.input_handlers import get_valid_input


class CreatePlayer():

    def display_menu(self):
        print("\n" + "=" * 40)
        print("👤    CRÉATION D'UN NOUVEAU JOUEUR    👤")
        print("=" * 40)

        first_name = get_valid_input(
            prompt="Quel est votre prénom : ",
            formatter=format_first_name,
            validator=is_valid_name,
            message_error=invalide_name_message
        )
        print(f"Le prénom du joueur est : {first_name}")

        last_name = get_valid_input(
            prompt="Quel est votre nom : ",
            formatter=format_last_name,
            validator=is_valid_name,
            message_error=invalide_name_message
        )
        print(f"Le nom du joueur est : {last_name}")

        date_of_birth = get_valid_input(
            prompt="Quelle est votre date de naissance (JJAAMMMM) : ",
            formatter=format_date,
            validator=is_valid_date,
            message_error=invalid_date_message
        )
        print(f"La date de naissance du joueur est le : {date_of_birth}")

        id_national_chess = get_valid_input(
            prompt="Quel est votre identifiant national d'échecs (XX00000) : ",
            formatter=format_id_national_chess,
            validator=is_valid_id_national_chess,
            message_error=invalide_id_national_chess
        )

        time.sleep(1)
        print(f"Joueur {first_name} {last_name} créé.")
        print(f"Retour au menu principal")
        time.sleep(2)
    
        return {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "id_national_chess": id_national_chess
        }
    
