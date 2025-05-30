import os

from utils.input_formatters import (
    format_tournament_name,
    format_date,
    format_location_name,
    format_number_of_rounds,
    format_description,
    format_id_national_chess
)
from utils.input_validators import (
    is_valid_tournament_name,
    is_valid_start_date,
    is_valid_end_date,
    is_valid_location_name,
    is_valid_number_of_rounds,
    is_valid_description,
    is_valid_id_national_chess
)
from utils.error_messages import (
    invalid_tournament_name,
    invalid_date,
    invalid_location_name,
    invalid_number_of_rounds,
    invalid_description,
    invalide_id_national_chess
)
from utils.input_manager            import get_valid_input
from utils.console                  import clear_screen
from utils.info_messages            import show_player_registration
from storage.player_data            import load_player_from_json
from controller.player_controller   import PlayerController
from config                         import MIN_PLAYERS, PLAYERS_FOLDER, PLAYERS_FILENAME


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
        Demande automatique pour les MIN_PLAYERS premiers, puis optionnelle pour les suivants.
        Retourne la liste des objets Player.
        """
        players = []
        clear_screen()
        print("\n" + "="*40)
        print("♟️➕     INSCRIPTION DES JOUEURS     ➕♟️")
        print("="*40)
        show_player_registration(MIN_PLAYERS, max_players)

        def register_and_add(idx: int):
            prompt = (
                f"\nInscription du joueur {idx}\n"
                "IDN (XX00000) du joueur : "
            )
            id_input = get_valid_input(
                prompt=prompt,
                formatter=lambda x: x.strip().upper(),
                validator=is_valid_id_national_chess,
                message_error=invalide_id_national_chess,
            )
            filepath = os.path.join(
                PLAYERS_FOLDER,
                PLAYERS_FILENAME.format(id_input=id_input)
            )
            if os.path.exists(filepath):
                player = load_player_from_json(PLAYERS_FOLDER, id_input)
                print(f"[INFO] Joueur ajouté : {player.first_name} {player.last_name}")
            else:
                player = PlayerController.create_player_with_id(id_input)
                print(f"[INFO] Nouveau joueur créé et ajouté : {player.first_name} {player.last_name}")
            players.append(player)

        # Inscrire automatiquement les MIN_PLAYERS premiers
        for idx in range(1, MIN_PLAYERS + 1):
            register_and_add(idx)

        # Option : ajouter jusqu'à max_players
        idx = MIN_PLAYERS + 1
        while idx <= max_players:
            add_more = get_valid_input(
                prompt="\nVoulez-vous ajouter un autre joueur ? (Y/N) : ",
                formatter=lambda x: x.strip().upper(),
                validator=lambda x: x in ['Y', 'N'],
                message_error="Réponse invalide, Y ou N attendu.",
            )
            if add_more == 'N':
                break
            register_and_add(idx)
            idx += 1

        return players
