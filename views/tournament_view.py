import os
from rich.console import Console
from rich.table import Table
from rich import box

from config import PLAYERS_FOLDER, PLAYERS_FILENAME, ENTER_FOR_CONTINUE, DEFAULT_NUMBER_OF_ROUND
from controllers.player_controller import PlayerController
from models.tournament_model import Tournament
from utils.console import wait_for_enter
from utils.console import clear_screen
from utils.input_manager import get_valid_input
from views.player_view import PlayerView
from utils.input_formatters import (format_tournament_name,
                                    format_date,
                                    format_location_name,
                                    format_number_of_rounds,
                                    format_description,
                                    format_id_national_chess,)
from utils.error_messages import (invalid_tournament_name,
                                  invalid_tournament_start_date,
                                  invalid_tournament_end_date,
                                  invalid_location_name,
                                  invalid_number_of_rounds,
                                  invalid_description,
                                  invalid_id_national_chess,)
from utils.info_messages import (tournament_incomplete_text,
                                 tournament_info_text,
                                 player_already_in_tournament_text)
from utils.input_validators import (is_valid_tournament_name,
                                    is_valid_start_date,
                                    is_valid_end_date,
                                    is_valid_location_name,
                                    is_valid_number_of_rounds,
                                    make_description_validator,
                                    is_valid_id_national_chess)
from utils.ui_helpers import (
    show_tournament_name,
    show_location,
    show_start_date,
    show_end_date,
    show_number_of_rounds,
    show_description,
    show_players_inscription,
    show_players_list
)


class TournamentView:
    console = Console()

    @staticmethod
    def ask_tournament_name() -> str:
        show_tournament_name()
        return get_valid_input(
            prompt="Nom du tournoi : ",
            formatter=format_tournament_name,
            validator=is_valid_tournament_name,
            message_error=invalid_tournament_name,
        )

    @staticmethod
    def ask_location() -> str:
        show_location()
        return get_valid_input(
            prompt="Lieu : ",
            formatter=format_location_name,
            validator=is_valid_location_name,
            message_error=invalid_location_name,
        )

    @staticmethod
    def ask_start_date() -> str:
        show_start_date()
        return get_valid_input(
            prompt="Date de début (JJMMAAAA) : ",
            formatter=format_date,
            validator=is_valid_start_date,
            message_error=invalid_tournament_start_date,
        )

    @staticmethod
    def ask_end_date(start_date: str) -> str:
        show_end_date()
        return get_valid_input(
            prompt="Date de fin (JJMMAAAA) : ",
            formatter=format_date,
            validator=lambda end_date: is_valid_end_date(end_date, start_date),
            message_error=invalid_tournament_end_date,
        )

    @staticmethod
    def ask_number_of_rounds() -> int:
        show_number_of_rounds()
        return get_valid_input(
            prompt=f"Nombre de rounds (par défaut {DEFAULT_NUMBER_OF_ROUND}) : ",
            formatter=format_number_of_rounds,
            validator=is_valid_number_of_rounds,
            message_error=invalid_number_of_rounds,
        )

    @staticmethod
    def ask_description(allow_empty: bool = False) -> str:
        show_description()

        return get_valid_input(
            prompt="Description/Remarques : ",
            formatter=format_description,
            validator=make_description_validator(allow_empty),
            message_error=invalid_description,
        )

    @staticmethod
    def show_player_list_header(list_of_players: list):
        """
        Affiche uniquement la liste des joueurs inscrits :
          • Titre “👥  LISTE DES JOUEURS  👥”
          • Puis chaque joueur (via PlayerView.list_players).
        """
        show_players_list()

        if list_of_players:
            PlayerView.list_players(list_of_players)
            print()  # Ligne vide pour aérer
        else:
            print("[Aucun joueur inscrit]\n")

    @staticmethod
    def show_registration_header(current_count: int, max_players: int):
        """
        Affiche uniquement le bloc d’en-tête d’inscription :
        “♟️➕ INSCRIPTION DES JOUEURS ➕♟️”
        """
        show_players_inscription()
        print(f"Nombre de joueurs inscrits : {current_count} / {max_players}\n")

    @staticmethod
    def register_one_player(idx: int, max_players: int):
        """
        Inscrit un seul joueur (joueur #idx sur max_players) et le retourne.
        1. Affiche l’en-tête d’inscription (sans retomber sur la liste).
        2. Appelle display_player_registration_text(idx, max_players).
        3. Demande l’IDN via get_valid_input.
        4. Appelle PlayerController.create_player_with_id pour charger/créer/compléter le profil.
        5. Renvoie l’objet Player complet.
        """
        # 1. Afficher uniquement l’en-tête d’inscription (juste le compteur, sans la liste)
        TournamentView.show_registration_header(idx - 1, max_players)

        # 2. Lecture de l’IDN
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

        # 3. Si le fichier n'existe pas, afficher le message “Aucun profil trouvé…”, attendre Entrée
        if not os.path.exists(filepath):
            PlayerView.display_nonexistent_player(id_input)
            print()
            wait_for_enter(ENTER_FOR_CONTINUE)

        # 4. Charger/créer/completer le profil via le controller
        player = PlayerController.create_player_with_id(id_input)

        # 5. Retourner le Player complet
        return player

    @staticmethod
    def display_player_already_in_tournament_text(id_national: str):
        TournamentView.console.print(player_already_in_tournament_text(id_national))

    @staticmethod
    def display_tournament_incomplete(tournament: Tournament) -> None:
        """
        Efface l'écran et affiche le message pour informer que le profil du joueur est incomplet.
        """
        TournamentView.console.print(tournament_incomplete_text())
        TournamentView.console.print(tournament_info_text(tournament))

    @staticmethod
    def show_tournament_summary(tournament: Tournament) -> None:
        """
        Affiche un résumé complet d’un tournoi terminé ou en cours :
        1. En-tête général
        2. Classement final
        3. Détail des rounds et matchs
        4. Indication si le tournoi est toujours en cours
        """
        clear_screen()
        console = TournamentView.console

        players_map = TournamentView._build_players_map(tournament)

        if tournament.actual_round == 0:
            console.print(
                "[italic yellow]Le tournoi n’a pas encore démarré. Aucun round n’a été joué.[/italic yellow]\n"
            )
        else:
            print("Tournoi terminé. Récapitulatif final :\n")
            TournamentView._print_tournament_header(tournament)
            TournamentView._print_final_ranking(tournament)
            TournamentView._print_rounds_summary(tournament, players_map)

            if tournament.actual_round < tournament.number_of_rounds:
                last_round = tournament.list_of_rounds[-1]
                if last_round.end_time is None:
                    console.print(
                        f"[italic yellow]\nLe tournoi est en cours : "
                        f"{tournament.actual_round - 1} / {tournament.number_of_rounds} round(s) joué(s).\n"
                        f"Le round {tournament.actual_round} est en cours...[/italic yellow]"
                    )

    console.print()
    console.print("[bold green]»» Résumé du tournoi affiché.[/bold green]\n")

    @staticmethod
    def _build_players_map(tournament: Tournament) -> dict:
        """
        Crée un dictionnaire d’accès rapide entre IDN et Player.

        Args:
            tournament (Tournament): Le tournoi contenant la liste des joueurs.

        Returns:
            dict: Clé = IDN, Valeur = Player instance
        """
        return {p.id_national_chess: p for p in tournament.list_of_players}

    @staticmethod
    def _print_tournament_header(tournament: Tournament) -> None:
        """
        Affiche l’en-tête général d’un tournoi : nom, lieu et dates.

        Args:
            tournament (Tournament): Tournoi à résumer.
        """
        console = TournamentView.console
        console.print()
        console.print(f"[b underline]🏆 Résumé du tournoi : {tournament.tournament_name}[/b underline]\n")
        console.print(f"📍  Lieu       : {tournament.location}")
        console.print(f"📅  Période    : {tournament.start_date}  →  {tournament.end_date}\n\n")

    @staticmethod
    def _print_final_ranking(tournament: Tournament) -> None:
        """
        Affiche le classement final ou provisoire des joueurs.

        Args:
            tournament (Tournament): Le tournoi avec les scores à afficher.
        """
        console = TournamentView.console
        console.print("[b]Classement final[/b]\n")
        table = Table(
            title="Classement des joueurs",
            box=box.SIMPLE_HEAVY,
            show_edge=True,
            header_style="bold magenta"
        )
        table.add_column("Rang", justify="center")
        table.add_column("IDN", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Score", justify="center")

        for player in sorted(tournament.list_of_players, key=lambda p: p.rank):
            table.add_row(
                str(player.rank),
                player.id_national_chess,
                player.last_name,
                player.first_name,
                f"{player.tournament_score:.1f}"
            )

        console.print(table)
        console.print()

    @staticmethod
    def _print_rounds_summary(tournament: Tournament, players_map: dict) -> None:
        """
        Affiche le détail des rounds du tournoi et de leurs matchs.

        Args:
            tournament (Tournament): Tournoi à afficher.
            players_map (dict): Dictionnaire IDN → Player.
        """
        console = TournamentView.console

        def fmt_score(score):
            return f"{score:.1f}" if score is not None else "[Match non commencé]"

        for rnd in tournament.list_of_rounds:
            console.print(f"→ {rnd.round_number}")
            start = rnd.get_formatted_start_time() if rnd.start_time else "[Pas commencé]"
            end = rnd.get_formatted_end_time() if rnd.end_time else "[En cours]"
            console.print(f"   • Début : {start} | Fin : {end}")

            table = Table(box=box.MINIMAL, show_edge=False)
            table.add_column("Match", justify="left")
            table.add_column("Joueur 1 (IDN)", justify="center")
            table.add_column("Nom 1", justify="center")
            table.add_column("Prénom 1", justify="center")
            table.add_column("Score 1", justify="center")
            table.add_column("VS", justify="center")
            table.add_column("Joueur 2 (IDN)", justify="center")
            table.add_column("Nom 2", justify="center")
            table.add_column("Prénom 2", justify="center")
            table.add_column("Score 2", justify="center")

            for match in rnd.matches:
                if match.player_2 is None:
                    p1 = players_map.get(match._snap1.get("id_national_chess"), None)
                    table.add_row(
                        match.name,
                        match._snap1.get("id_national_chess", ""),
                        p1.last_name if p1 else "[?]",
                        p1.first_name if p1 else "[?]",
                        fmt_score(match._snap1.get("match_score")),
                        "⚔️", "-", "-", "-", "-"
                    )
                else:
                    id1 = match._snap1.get("id_national_chess", "")
                    id2 = match._snap2.get("id_national_chess", "")
                    p1 = players_map.get(id1, None)
                    p2 = players_map.get(id2, None)

                    table.add_row(
                        match.name,
                        id1, p1.last_name if p1 else "[?]",
                        p1.first_name if p1 else "[?]",
                        fmt_score(match._snap1.get("match_score")),
                        "⚔️",
                        id2, p2.last_name if p2 else "[?]",
                        p2.first_name if p2 else "[?]",
                        fmt_score(match._snap2.get("match_score"))
                    )
            console.print(table)
            console.print()

    @staticmethod
    def show_error(message: str) -> None:
        TournamentView.console.print(f"[bold red]Erreur:[/bold red] {message}")
