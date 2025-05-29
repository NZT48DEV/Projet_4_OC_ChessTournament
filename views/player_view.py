from utils.input_formatters     import (
                                        format_first_name,
                                        format_last_name,
                                        format_date,
                                        format_id_national_chess,
                                    )
from utils.input_validators     import (
                                        is_valid_name,
                                        is_valid_player_birthdate,
                                        is_valid_id_national_chess,
                                    )
from utils.error_messages       import (
                                        invalide_name,
                                        invalid_date,
                                        invalide_id_national_chess,
                                    )
from utils.input_manager        import get_valid_input
from utils.console              import clear_screen
from models.player_model        import Player
from rich.console               import Console


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
            message_error=invalide_id_national_chess,
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
            message_error=invalide_name,
        )

    @staticmethod
    def ask_last_name() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("👤            NOM DU JOUEUR           👤")
        print("="*40)
        return get_valid_input(
            prompt="Nom : ",
            formatter=format_last_name,
            validator=is_valid_name,
            message_error=invalide_name,
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
            message_error=invalid_date,
        )
    

    @staticmethod
    def display_player(player) -> None:
        print(f"\nJoueur : {player.first_name} {player.last_name} (ID {player.id_national_chess})")
        print(f"Date de naissance : {player.date_of_birth}")

    def player_added_message(player: Player) -> str:
        clear_screen()
        console.print(
            "\n[bold yellow][INFO][/bold yellow] [bold]Joueur créé avec succès.[/bold]\n"
            f"IDN : [bold]{player.id_national_chess}[/bold]\n"
            f"Prénom : [bold]{player.first_name}[/bold]\n"
            f"Nom : [bold]{player.last_name}[/bold]\n"
            f"Date de naissance : [bold]{player.date_of_birth}[/bold]"
        )