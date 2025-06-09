from rich.console               import Console

from models.player_model        import Player
from utils.input_formatters     import (
                                        format_first_name,
                                        format_name,
                                        format_date,
                                        format_id_national_chess,
                                    )
from utils.input_validators     import (
                                        is_valid_name,
                                        is_valid_player_birthdate,
                                        is_valid_id_national_chess,
                                    )
from utils.error_messages       import (
                                        invalid_name,
                                        invalid_date_of_birth,
                                        invalid_id_national_chess,
                                    )
from utils.info_messages        import (
                                        player_added_text,
                                        player_updated_text,
                                        player_already_exist_text,
                                        player_incomplete_text,
                                        player_info_text,
                                        player_nonexistent_text,
                                        player_added_to_chesstournament_text,
                                        player_already_in_tournament_text
                                    )
from utils.console              import clear_screen
from utils.input_manager        import get_valid_input



console = Console()


class PlayerView:
    """
    Vues CLI pour la création incrémentale d'un joueur.
    """

    @staticmethod
    def ask_id_national_chess() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("🆔        IDENTIFIANT NATIONAL        🆔")
        print("="*40)
        return get_valid_input(
            prompt="Votre IDN d'échecs (XX00000) : ",
            formatter=format_id_national_chess,
            validator=is_valid_id_national_chess,
            message_error=invalid_id_national_chess,
        )

    @staticmethod
    def ask_first_name() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("👤          PRÉNOM DU JOUEUR          👤")
        print("="*40)
        return get_valid_input(
            prompt="Prénom : ",
            formatter=format_first_name,
            validator=is_valid_name,
            message_error=invalid_name,
        )

    @staticmethod
    def ask_last_name() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("👤            NOM DU JOUEUR           👤")
        print("="*40)
        return get_valid_input(
            prompt="Nom : ",
            formatter=format_name,
            validator=is_valid_name,
            message_error=invalid_name,
        )

    @staticmethod
    def ask_date_of_birth() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("🎂          DATE DE NAISSANCE         🎂")
        print("="*40)
        return get_valid_input(
            prompt="Date de naissance (JJMMAAAA) : ",
            formatter=format_date,
            validator=is_valid_player_birthdate,
            message_error=invalid_date_of_birth,
        )
    
    @staticmethod
    def list_players(players: list[Player]) -> None:
        """
        Tri la liste des joueurs par nom (MAJ) puis prénom (Capitalisé).
        """
        # Tri par nom (MAJ) puis prénom (Capitalisé)
        sorted_list = sorted(
            players,
            key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )
        for idx, player in enumerate(sorted_list, start=1):
            print(f"{idx}. {player.last_name.upper()} {player.first_name.capitalize()} (IDN : {player.id_national_chess})")

    @staticmethod
    def display_player_added(player: Player) -> None:
        """
        Efface l'écran et affiche le message de succès pour la création d'un joueur.
        """
        clear_screen()
        console.print(player_added_text())
        console.print(player_info_text(player))

    @staticmethod
    def display_player_updated(player: Player) -> None:
        """
        Efface l'écran et affiche le message pour confirmer la modification du profil utilisateur.
        """
        clear_screen()
        console.print(player_updated_text())
        console.print(player_info_text(player))
    
    @staticmethod
    def display_player_already_exist(player: Player) -> None:
        """
        Efface l'écran et affiche le message pour informer que le joueur est déjà existant.
        """
        clear_screen()
        console.print(player_already_exist_text())
        console.print(player_info_text(player))
        

    @staticmethod
    def display_player_incomplete(player: Player) -> None:
        """
        Efface l'écran et affiche le message pour informer que le profil du joueur est incomplet.
        """
        clear_screen()
        console.print(player_incomplete_text())
        console.print(player_info_text(player))
    
    @staticmethod
    def display_player_info(player: Player) -> None:
        console.print(player_info_text(player))

    @staticmethod
    def display_nonexistent_player(player: Player) -> None:
        clear_screen()
        console.print(player_nonexistent_text(player))

    @staticmethod
    def display_player_added_to_chesstournament_text(player: Player) -> None:
        console.print(player_added_to_chesstournament_text(player))
    
    @staticmethod
    def display_duplicate_player(id_national: str) -> None:
        """
        Affiche “le joueur est déjà inscrit dans ce tournoi”.
        """
        console.print(player_already_in_tournament_text(id_national))