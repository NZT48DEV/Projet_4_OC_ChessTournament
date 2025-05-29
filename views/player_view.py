from typing                 import Dict
from models.player_model    import Player
from utils.input_formatters import format_first_name, format_last_name, format_date, format_id_national_chess
from utils.input_validators import is_valid_name, is_valid_player_birthdate, is_valid_id_national_chess
from utils.error_messages   import invalide_name, invalid_date, invalide_id_national_chess
from utils.input_manager    import get_valid_input


class PlayerView():

    @staticmethod
    def display_create_player_menu() -> Dict[str, str]:
        print("\n" + "=" * 40)
        print("👤    CRÉATION D'UN NOUVEAU JOUEUR    👤")
        print("=" * 40)

        first_name = get_valid_input(
            prompt="Quel est votre prénom : ",
            formatter=format_first_name,
            validator=is_valid_name,
            message_error=invalide_name
        )

        last_name = get_valid_input(
            prompt="Quel est votre nom : ",
            formatter=format_last_name,
            validator=is_valid_name,
            message_error=invalide_name
        )

        date_of_birth = get_valid_input(
            prompt="Quelle est votre date de naissance (JJAAMMMM) : ",
            formatter=format_date,
            validator=is_valid_player_birthdate,
            message_error=invalid_date
        )

        id_national_chess = get_valid_input(
            prompt="Quel est votre identifiant national d'échecs (XX00000) : ",
            formatter=format_id_national_chess,
            validator=is_valid_id_national_chess,
            message_error=invalide_id_national_chess
        )
    
        return {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "id_national_chess": id_national_chess
        }
    
    @staticmethod
    def list_players(players: list[Player]) -> None:
        """Affiche une liste numérotée de tous les joueurs, triée par ordre alphabétique."""
        # On crée une nouvelle liste triée par nom puis prénom (insensible à la casse)
        sorted_players = sorted(
            players,
            key=lambda player: (player.last_name.lower(), player.first_name.lower())
        )
        print("\nListe des joueurs (ordre alphabétique) :")
        for idx, player in enumerate(sorted_players, start=1):
            print(f"{idx}. {player.last_name} {player.first_name} (ID : {player.id_national_chess})")

    
