import os
from rich.console import Console

from config import PLAYERS_FOLDER, TOURNAMENTS_FOLDER, ENTER_FOR_RAPPORT
from controllers.tournament_controller import TournamentController
from models.player_model import Player
from storage.player_data import load_players_from_json, load_player_from_json
from storage.tournament_data import load_tournament_from_json
from utils.console import clear_screen, wait_for_enter
from utils.info_messages import prompt_file_to_load
from utils.ui_helpers import show_tournament_information
from views.tournament_view import TournamentView


console = Console()


class ReportsView:
    @staticmethod
    def list_all_players():
        clear_screen()
        players = load_players_from_json(PLAYERS_FOLDER)
        TournamentView.show_player_list_header(players)
        print()
        wait_for_enter(ENTER_FOR_RAPPORT)
        clear_screen()

    @staticmethod
    def list_all_tournaments():
        clear_screen()
        if not os.path.isdir(TOURNAMENTS_FOLDER):
            print(f"Aucun dossier '{TOURNAMENTS_FOLDER}' trouvé.")
        else:
            files = sorted(f for f in os.listdir(TOURNAMENTS_FOLDER) if f.endswith('.json'))
            if not files:
                print(f"Aucun tournoi enregistré dans {TOURNAMENTS_FOLDER}.")
            else:
                print("\n" + "=" * 40)
                print("🏆   LISTE DES TOURNOIS ENREGISTRÉS   🏆")
                print("=" * 40 + "\n")
                for idx, filename in enumerate(files, start=1):
                    print(f"{idx}. {filename}")
        print()
        wait_for_enter(ENTER_FOR_RAPPORT)
        clear_screen()

    @staticmethod
    def _choose_tournament_file() -> str:
        """
        Affiche la liste des fichiers JSON dans TOURNAMENTS_FOLDER et demande de choisir.
        Renvoie le chemin complet du fichier sélectionné, ou vide si l'utilisateur annule.
        """
        if not os.path.isdir(TOURNAMENTS_FOLDER):
            clear_screen()
            print(f"Aucun dossier '{TOURNAMENTS_FOLDER}' trouvé.")
            wait_for_enter(ENTER_FOR_RAPPORT)
            clear_screen()
            return ""

        files = sorted(f for f in os.listdir(TOURNAMENTS_FOLDER) if f.endswith('.json'))
        if not files:
            clear_screen()
            print(f"Aucun tournoi enregistré dans {TOURNAMENTS_FOLDER}.")
            wait_for_enter(ENTER_FOR_RAPPORT)
            clear_screen()
            return ""

        clear_screen()
        print("\nFichiers de tournois disponibles :\n")
        for filename in files:
            print(f"  • {filename}")
        console.print(prompt_file_to_load())
        choice = input("Nom du fichier à charger → ").strip()
        if not choice:
            clear_screen()
            return ""
        if choice not in files:
            clear_screen()
            print(f"❌ Le fichier « {choice} » n'existe pas.")
            wait_for_enter(ENTER_FOR_RAPPORT)
            clear_screen()
            return ""
        return os.path.join(TOURNAMENTS_FOLDER, choice)

    @staticmethod
    def show_tournament_basic_info():
        """
        Via le nom d’un tournoi (fichier), affiche :
         - Le nom du tournoi
         - Les dates (start_date → end_date)
         - Nombre de rounds
         - Description (différencie "" de None)
        """
        chemin = ReportsView._choose_tournament_file()
        if not chemin:
            return

        data = load_tournament_from_json(chemin)
        miss_info = "[Info manquante]"
        no_desc = "[Pas de description]"

        show_tournament_information()

        # Nom du tournoi (toujours présent dans le JSON)
        print(f"Nom du tournoi  : {data['tournament_name']}")

        # Lieu
        lieu = data.get("location", None)
        if lieu is None:
            print(f"Lieu            : {miss_info}")
        elif lieu == "":
            print("Lieu            : [Pas de lieu]")
        else:
            print(f"Lieu            : {lieu}")

        # Période
        start = data.get("start_date", None)
        end = data.get("end_date", None)
        start_str = miss_info if start is None else start
        end_str = miss_info if end is None else end
        print(f"Période         : {start_str} → {end_str}")

        # Nombre de rounds
        nbr = data.get("number_of_rounds", None)
        if nbr is None:
            print(f"Nombre de rounds: {miss_info}")
        else:
            print(f"Nombre de rounds: {nbr}")

        # Description
        desc = data.get("description", None)
        if desc is None:
            print(f"Description     : {miss_info}")
        elif desc == "":
            print(f"Description     : {no_desc}")
        else:
            print(f"Description     : {desc}")

        print()
        wait_for_enter(ENTER_FOR_RAPPORT)
        clear_screen()

    @staticmethod
    def list_players_for_tournament():
        """
        Via le nom d’un tournoi, affiche la liste des joueurs inscrits (ordre alphabétique).
        Si le fichier de profil d’un joueur est introuvable, on l’indique explicitement.
        """
        chemin = ReportsView._choose_tournament_file()
        if not chemin:
            return

        data = load_tournament_from_json(chemin)
        players_data = data.get("list_of_players", [])
        if not players_data:
            clear_screen()
            print("\nAucun joueur inscrit dans ce tournoi.")
            print()
            wait_for_enter(ENTER_FOR_RAPPORT)
            clear_screen()
            return

        # On préparera deux listes :
        #  - players_objs : instances Player valides à afficher
        #  - missing_ids  : liste des IDN pour lesquels aucun fichier n'a été trouvé
        players_objs: list[Player] = []
        missing_ids: list[str] = []

        for p in players_data:
            idn = p.get("id_national_chess", "")
            try:
                player_full = load_player_from_json(PLAYERS_FOLDER, idn)
            except FileNotFoundError:
                missing_ids.append(idn)
                continue
            else:
                # Mettre à jour les champs spécifiques au tournoi
                player_full.tournament_score = p.get("tournament_score", 0.0)
                player_full.rank = p.get("rank", 0)
                player_full.played_with = p.get("played_with", [])
                players_objs.append(player_full)

        clear_screen()
        # Afficher d’abord la liste des profils valides, si elle n'est pas vide
        if players_objs:
            TournamentView.show_player_list_header(players_objs)
        else:
            print("Aucun profil de joueur valide n'a été trouvé pour ce tournoi.")

        # Ensuite, pour chaque IDN manquant, afficher un message explicite
        if missing_ids:
            print("\n-----\n")
            for idn in missing_ids:
                print(f"Le joueur avec l’IDN {idn} n’existe pas.")
        print()
        wait_for_enter(ENTER_FOR_RAPPORT)
        clear_screen()

    @staticmethod
    def list_rounds_and_matches_for_tournament():
        """
        Via le nom d’un tournoi, affiche pour chaque round la liste de tous les matchs,
        en utilisant RoundView.show_tournament_summary().
        """
        chemin = ReportsView._choose_tournament_file()
        if not chemin:
            return

        # Récupérer le nom de fichier (ex. "mon_tournoi_20250605.json")
        filename = os.path.basename(chemin)

        # Charger les données JSON et reconstruire un TournamentController temporaire
        data = load_tournament_from_json(chemin)
        controller = TournamentController.load_existing_tournament(data, filename)
        tournoi = controller.tournament

        clear_screen()
        # show_tournament_summary affiche automatiquement tous les rounds et matchs
        TournamentView.show_tournament_summary(tournoi)

        print()
        wait_for_enter(ENTER_FOR_RAPPORT)
        clear_screen()
