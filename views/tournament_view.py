import os

from utils.input_formatters import (
    format_tournament_name,
    format_date,
    format_location_name,
    format_number_of_rounds,
    format_description,
    format_id_national_chess,
    format_yes_no
)
from utils.input_validators import (
    is_valid_tournament_name,
    is_valid_start_date,
    is_valid_end_date,
    is_valid_location_name,
    is_valid_number_of_rounds,
    is_valid_description,
    is_valid_id_national_chess,
    is_valid_yes_no
)
from utils.error_messages import (
    invalid_tournament_name,
    invalid_date,
    invalid_location_name,
    invalid_number_of_rounds,
    invalid_description,
    invalid_id_national_chess,
    invalid_yes_no
)
from utils.info_messages import (
    show_player_registration, 
    player_added_to_chesstournament_text
)

from utils.input_manager            import get_valid_input
from utils.console                  import clear_screen

from storage.player_data            import load_player_from_json
from controllers.player_controller  import PlayerController
from config                         import MIN_PLAYERS, PLAYERS_FOLDER, PLAYERS_FILENAME
from views.player_view              import PlayerView
from utils.console                  import wait_for_enter_continue


class TournamentView:
    @staticmethod
    def ask_tournament_name() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("🏆           NOM DU TOURNOI           🏆")
        print("="*40)
        return get_valid_input(
            prompt="Nom du tournoi : ",
            formatter=format_tournament_name,
            validator=is_valid_tournament_name,
            message_error=invalid_tournament_name,
        )

    @staticmethod
    def ask_location() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("📍          LIEU DU TOURNOI           📍")
        print("="*40)
        return get_valid_input(
            prompt="Lieu : ",
            formatter=format_location_name,
            validator=is_valid_location_name,
            message_error=invalid_location_name,
        )

    @staticmethod
    def ask_start_date() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("📅            DATE DE DÉBUT           📅")
        print("="*40)
        return get_valid_input(
            prompt="Date de début (JJMMAAAA) : ",
            formatter=format_date,
            validator=is_valid_start_date,
            message_error=invalid_date,
        )

    @staticmethod
    def ask_end_date(start_date: str) -> str:
        clear_screen()
        print("\n" + "="*40)
        print("📅            DATE DE FIN             📅")
        print("="*40)
        return get_valid_input(
            prompt="Date de fin (JJMMAAAA) : ",
            formatter=format_date,
            validator=lambda end_date: is_valid_end_date(end_date, start_date),
            message_error=invalid_date,
        )

    @staticmethod
    def ask_number_of_rounds() -> int:
        clear_screen()
        print("\n" + "="*40)
        print("🔢           NOMBRE DE ROUNDS         🔢")
        print("="*40)
        return get_valid_input(
            prompt="Nombre de rounds (par défaut 4) : ",
            formatter=format_number_of_rounds,
            validator=is_valid_number_of_rounds,
            message_error=invalid_number_of_rounds,
        )

    @staticmethod
    def ask_description() -> str:
        clear_screen()
        print("\n" + "="*40)
        print("📝             DESCRIPTION            📝")
        print("="*40)
        return get_valid_input(
            prompt="Description/Remarques : ",
            formatter=format_description,
            validator=is_valid_description,
            message_error=invalid_description,
        )

    @staticmethod
    def ask_players(max_players: int):
        """
        Inscription séquentielle des joueurs jusqu'à max_players.
        Si un joueur existant a des infos manquantes, on force la complétion
        comme dans la création standard du player.
        Retourne la liste des objets Player complets.
        """
        players = []

        def show_registration_header(current_count: int):
            clear_screen()
            print("\n" + "=" * 40)
            print(f"♟️➕     INSCRIPTION DES JOUEURS     ➕♟️")
            print("=" * 40 + "\n")
            print(f"Nombre de joueurs inscrits : {current_count}\n")

        def register_and_add(idx: int):
            show_registration_header(len(players))
            show_player_registration(MIN_PLAYERS, max_players)
            print(f"\nInscription du joueur {idx} / {max_players}\n")

            id_input = get_valid_input(
                prompt="IDN (XX00000) du joueur : ",
                formatter=format_id_national_chess,
                validator=is_valid_id_national_chess,
                message_error=invalid_id_national_chess,
            )
            filepath = os.path.join(
                PLAYERS_FOLDER,
                PLAYERS_FILENAME.format(id_input=id_input)
            )

            if os.path.exists(filepath):
                # La méthode create_player_with_id se charge elle-même,
                # une fois seulement, de détecter “incomplet” et de forcer la saisie.
                player = PlayerController.create_player_with_id(id_input)

            else:
                # Le profil n’existe pas -> on affiche “profil inexistant”
                PlayerView.display_nonexistent_player(id_input)
                wait_for_enter_continue()

                # Puis, on appelle la même méthode pour créer et compléter le joueur
                player = PlayerController.create_player_with_id(id_input)

            # À ce stade, `player` est forcement complet. On peut donc l’ajouter au tournoi :
            clear_screen()
            PlayerView.display_player_added_to_chesstournament_text(id_input)
            PlayerView.display_player_info(player)
            wait_for_enter_continue()

            players.append(player)
        # --- Inscrire automatiquement les MIN_PLAYERS premiers ---
        for idx in range(1, MIN_PLAYERS + 1):
            register_and_add(idx)

        # --- Option : ajouter jusqu'à max_players ---
        idx = MIN_PLAYERS + 1
        while idx <= max_players:
            show_registration_header(len(players))
            add_more = get_valid_input(
                prompt="\nVoulez-vous ajouter un autre joueur ? (Y/N) : ",
                formatter=format_yes_no,
                validator=is_valid_yes_no,
                message_error=invalid_yes_no,
            )
            if add_more == 'N':
                break

            register_and_add(idx)
            idx += 1

        return players