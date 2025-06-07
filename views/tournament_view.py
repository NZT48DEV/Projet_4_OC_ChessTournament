import os

from utils.input_formatters import (
    format_tournament_name,
    format_date,
    format_location_name,
    format_number_of_rounds,
    format_description,
    format_id_national_chess,
)
from utils.input_validators import (
    is_valid_tournament_name,
    is_valid_start_date,
    is_valid_end_date,
    is_valid_location_name,
    is_valid_number_of_rounds,
    is_valid_description,
    is_valid_id_national_chess,
)
from utils.error_messages import (
    invalid_tournament_name,
    invalid_tournament_date,
    invalid_location_name,
    invalid_number_of_rounds,
    invalid_description,
    invalid_id_national_chess,
    player_already_in_tournament_text
)

from utils.info_messages import (
    tournament_incomplete_text,
    tournament_info_text
)

from utils.input_manager            import get_valid_input
from utils.console                  import clear_screen
from controllers.player_controller  import PlayerController
from config                         import PLAYERS_FOLDER, PLAYERS_FILENAME
from views.player_view              import PlayerView
from models.tournament_model        import Tournament
from utils.console                  import wait_for_enter_continue
from rich.console                   import Console
from models.player_model            import Player
from rich.console                   import Console
from rich.table                     import Table
from rich                           import box 
from models.tournament_model        import Tournament
from utils.console                  import clear_screen


console = Console()

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
            message_error=invalid_tournament_date,
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
            message_error=invalid_tournament_date,
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
    def ask_description(allow_empty: bool = False) -> str:
        clear_screen()
        print("\n" + "=" * 40)
        print("📝             DESCRIPTION            📝")
        print("=" * 40)

        if allow_empty:
            # Simple prompt, on récupère la saisie brute et on la retourne (peut être chaîne vide)
            desc = input("Description/Remarques (optionnel) : ").strip()
            return desc

        # Si allow_empty == False, on réutilise get_valid_input pour forcer une saisie valide
        return get_valid_input(
            prompt="Description/Remarques : ",
            formatter=format_description,
            validator=is_valid_description,
            message_error=invalid_description,
        )

    @staticmethod
    def show_player_list_header(list_of_players: list):
        """
        Affiche uniquement la liste des joueurs inscrits :
          • Titre “👥  LISTE DES JOUEURS  👥”
          • Puis chaque joueur (via PlayerView.list_players).
        """
        clear_screen()
        print("\n" + "=" * 40)
        print("👥         LISTE DES JOUEURS         👥")
        print("=" * 40 + "\n")

        if list_of_players:
            PlayerView.list_players(list_of_players)
            print()  # Ligne vide pour aérer
        else:
            print("[Aucun joueur inscrit pour l’instant]\n")


    @staticmethod
    def show_registration_header(current_count: int, max_players: int):
        """
        Affiche uniquement le bloc d’en-tête d’inscription :
        “♟️➕ INSCRIPTION DES JOUEURS ➕♟️” + “Nombre de joueurs inscrits : current_count / max_players”
        """
        print("\n" + "=" * 40)
        print(f"♟️➕     INSCRIPTION DES JOUEURS     ➕♟️")
        print("=" * 40 + "\n")
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
            wait_for_enter_continue()

        # 4. Charger/créer/completer le profil via le controller
        player = PlayerController.create_player_with_id(id_input)

        # 5. Retourner le Player complet
        return player
    
    @staticmethod
    def display_player_already_in_tournament_text(id_national: str):
        console.print(player_already_in_tournament_text(id_national))

    @staticmethod
    def display_tournament_incomplete(tournament: Tournament) -> None:
        """
        Efface l'écran et affiche le message pour informer que le profil du joueur est incomplet.
        """
        console.print(tournament_incomplete_text())
        console.print(tournament_info_text(tournament))

    @staticmethod
    def show_tournament_summary(tournament: Tournament) -> None:
        """
        Affiche un résumé complet d’un tournoi déjà terminé ou en cours :
        1. En-tête général (nom, lieu, dates)
        2. Classement final (ou provisoire) des joueurs
        3. Pour chaque round : numéro, horaire et tableau des matchs.

        - `tournament`: instance de Tournament ayant les listes list_of_players et list_of_rounds complètes.
        """
        console = Console()

        # 0) Construire un mapping IDN → Player
        players_map: dict[str, Player] = {
            p.id_national_chess: p for p in tournament.list_of_players
        }

        # 1) En-tête général
        console.print()
        console.print(f"[b underline]🏆 Résumé du tournoi : {tournament.tournament_name}[/b underline]\n")
        console.print(f"📍  Lieu       : {tournament.location}")
        console.print(f"📅  Période    : {tournament.start_date}  →  {tournament.end_date}\n\n")

        # 2) Classement final (ou provisoire)
        console.print("[b]Classement final[/b]\n")
        classement = Table(
            title="Classement des joueurs",
            box=box.SIMPLE_HEAVY,
            show_edge=True,
            header_style="bold magenta"
        )
        classement.add_column("Rang", justify="center")
        classement.add_column("IDN", justify="center")
        classement.add_column("Nom", justify="center")
        classement.add_column("Prénom", justify="center")
        classement.add_column("Score", justify="center")

        # On trie par rang croissant
        for player in sorted(tournament.list_of_players, key=lambda p: p.rank):
            score = player.tournament_score
            s_str = f"{score:.1f}"
            classement.add_row(
                str(player.rank),
                player.id_national_chess,
                player.last_name,
                player.first_name,
                s_str
            )

        console.print(classement)
        console.print()

        # 3) Pour chaque round, afficher son tableau de matchs
        for rnd in tournament.list_of_rounds:
            console.print(f"→ {rnd.round_number}")
            # Date de début ou “[Pas commencé]” si start_time est None
            start = rnd.get_formatted_start_time() if rnd.start_time else "[Pas commencé]"
            # Date de fin ou “[En cours]” si end_time est None
            end   = rnd.get_formatted_end_time()   if rnd.end_time   else "[En cours]"
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
                # Cas « match de repos » : player_2 est None
                if match.player_2 is None:
                    p1_snap = match._snap1
                    id1     = p1_snap.get("id_national_chess", "")
                    # Récupérer le Player complet depuis players_map
                    if id1 in players_map:
                        p1_full: Player = players_map[id1]
                        nom1    = p1_full.last_name
                        prenom1 = p1_full.first_name
                    else:
                        nom1    = "[?]"
                        prenom1 = "[?]"

                    sc1 = p1_snap.get("match_score", None)
                    sc1_str = f"{sc1:.1f}" if sc1 is not None else "[Match non commencé]"

                    # On affiche le match de repos : pas de joueur 2
                    table.add_row(
                        match.name,
                        id1,
                        nom1,
                        prenom1,
                        sc1_str,
                        "⚔️",
                        "-", "-", "-", "-"
                    )

                else:
                    # Cas « match classique »
                    p1_snap = match._snap1 or {}
                    p2_snap = match._snap2 or {}

                    id1     = p1_snap.get("id_national_chess", "")
                    id2     = p2_snap.get("id_national_chess", "")

                    # Nom/prénom réel pour le joueur 1
                    if id1 in players_map:
                        p1_full: Player = players_map[id1]
                        nom1    = p1_full.last_name
                        prenom1 = p1_full.first_name
                    else:
                        nom1    = "[?]"
                        prenom1 = "[?]"

                    # Nom/prénom réel pour le joueur 2
                    if id2 in players_map:
                        p2_full: Player = players_map[id2]
                        nom2    = p2_full.last_name
                        prenom2 = p2_full.first_name
                    else:
                        nom2    = "[?]"
                        prenom2 = "[?]"

                    sc1 = p1_snap.get("match_score", None)
                    sc2 = p2_snap.get("match_score", None)

                    # Afficher toujours la décimale (0.0, 0.5, 1.0) ou “[En cours]”
                    def fmt_score(x):
                        return f"{x:.1f}" if x is not None else "[Match non commencé]"

                    sc1_str = fmt_score(sc1)
                    sc2_str = fmt_score(sc2)

                    table.add_row(
                        match.name,
                        id1, nom1, prenom1, sc1_str,
                        "⚔️",
                        id2, nom2, prenom2, sc2_str
                    )

            console.print(table)
            console.print()  # Ligne vide après chaque round

        # Si le tournoi n’est pas terminé, on l’indique
        if tournament.actual_round < tournament.number_of_rounds:
            if end == "[En cours]":
                console.print(
                    f"[italic yellow]\nLe tournoi est en cours : "
                    f"{tournament.actual_round - 1} / {tournament.number_of_rounds} rounds joués.\n"
                    f"Le round {tournament.actual_round} est en cours...[/italic yellow]"
                )

        console.print()
        console.print("[bold green]»» Résumé du tournoi affiché.[/bold green]\n")