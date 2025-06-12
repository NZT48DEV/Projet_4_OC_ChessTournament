from rich.console import Console

from models.player_model import Player
from utils.input_formatters import (
    format_first_name,
    format_name,
    format_date,
    format_id_national_chess,
)
from utils.input_validators import (
    is_valid_name,
    is_valid_player_birthdate,
    is_valid_id_national_chess,
)
from utils.error_messages import (
    invalid_first_name,
    invalid_last_name,
    invalid_date_of_birth,
    invalid_id_national_chess,
)
from utils.info_messages import (
    player_added_text,
    player_updated_text,
    player_already_exist_text,
    player_incomplete_text,
    player_info_text,
    player_nonexistent_text,
    player_added_to_chesstournament_text,
    player_already_in_tournament_text
)
from utils.ui_helpers import (
    show_id_national_chess,
    show_first_name,
    show_last_name,
    show_date_of_birth
)
from utils.console import clear_screen
from utils.input_manager import get_valid_input


class PlayerView:
    """
    Vues CLI pour la création incrémentale d'un joueur.
    """
    console = Console()

    @staticmethod
    def ask_id_national_chess() -> str:
        show_id_national_chess()
        return get_valid_input(
            prompt="Votre IDN d'échecs (XX00000) : ",
            formatter=format_id_national_chess,
            validator=is_valid_id_national_chess,
            message_error=invalid_id_national_chess,
        )

    @staticmethod
    def ask_first_name() -> str:
        show_first_name()
        return get_valid_input(
            prompt="Prénom : ",
            formatter=format_first_name,
            validator=is_valid_name,
            message_error=invalid_first_name,
        )

    @staticmethod
    def ask_last_name() -> str:
        show_last_name()
        return get_valid_input(
            prompt="Nom : ",
            formatter=format_name,
            validator=is_valid_name,
            message_error=invalid_last_name,
        )

    @staticmethod
    def ask_date_of_birth() -> str:
        show_date_of_birth()
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
            print(
                f"{idx}. {
                    player.last_name.upper()} {
                    player.first_name.capitalize()} (IDN : {
                    player.id_national_chess})")

    @staticmethod
    def display_player_added(player: Player) -> None:
        """
        Efface l'écran et affiche le message de succès pour la création d'un joueur.

        Args:
            player (Player): L'instance du joueur qui a été créé.
        """
        clear_screen()
        PlayerView.console.print(player_added_text())
        PlayerView.console.print(player_info_text(player))

    @staticmethod
    def display_player_updated(player: Player) -> None:
        """
        Efface l'écran et affiche le message confirmant la modification du profil utilisateur.

        Args:
            player (Player): L'instance du joueur dont le profil a été mis à jour.
        """
        clear_screen()
        PlayerView.console.print(player_updated_text())
        PlayerView.console.print(player_info_text(player))

    @staticmethod
    def display_player_already_exist(player: Player) -> None:
        """
        Efface l'écran et affiche le message pour informer que le joueur existe déjà.

        Args:
            player (Player): L'instance du joueur déjà existant.
        """
        clear_screen()
        PlayerView.console.print(player_already_exist_text())
        PlayerView.console.print(player_info_text(player))

    @staticmethod
    def display_player_incomplete(player: Player) -> None:
        """
        Efface l'écran et affiche le message pour informer que le profil du joueur est incomplet.

        Args:
            player (Player): L'instance du joueur dont le profil est incomplet.
        """
        clear_screen()
        PlayerView.console.print(player_incomplete_text())
        PlayerView.console.print(player_info_text(player))

    @staticmethod
    def display_player_info(player: Player) -> None:
        """
        Affiche les informations complètes d'un joueur.

        Args:
            player (Player): L'instance du joueur dont on veut afficher les détails.
        """
        PlayerView.console.print(player_info_text(player))

    @staticmethod
    def display_nonexistent_player(player: Player) -> None:
        """
        Avertit que le joueur spécifié n'existe pas.

        Args:
            player (Player): L'instance du joueur recherché (inexistante).
        """
        clear_screen()
        PlayerView.console.print(player_nonexistent_text(player))

    @staticmethod
    def display_player_added_to_chesstournament_text(player: Player) -> None:
        """
        Informe qu'un joueur a été ajouté au tournoi d'échecs.

        Args:
            player (Player): L'instance du joueur ajouté au tournoi.
        """
        PlayerView.console.print(player_added_to_chesstournament_text(player))

    @staticmethod
    def display_duplicate_player(id_national: str) -> None:
        """
        Informe que le joueur avec l'ID national spécifié est déjà inscrit dans ce tournoi.

        Args:
            id_national (str): Identifiant national du joueur dupliqué.
        """
        PlayerView.console.print(player_already_in_tournament_text(id_national))
