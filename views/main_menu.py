import os
from rich.console import Console

from config import TOURNAMENTS_FOLDER, ENTER_FOR_MAIN_MENU
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from storage.tournament_data import load_tournament_from_json
from utils.console import clear_screen, wait_for_enter
from utils.info_messages import prompt_file_to_load
from views.reports_view import ReportsView


class MenuView:
    """
    Vue principale pour afficher le menu et naviguer
    entre la création de joueurs, la gestion de tournois
    et l’affichage des rapports.
    """
    console = Console()

    @classmethod
    def display_main_menu(cls) -> None:
        """Affiche le menu principal."""
        print("\n" + "=" * 40)
        print("♟️       TOURNOI D'ÉCHECS - MENU       ♟️")
        print("=" * 40)
        print("1. ♟️  Créer un joueur")
        print("2. 🏆 Créer un tournoi")
        print("3. 📂 Charger un tournoi")
        print("4. 📊 Afficher des rapports")
        print("0. ❌ Quitter")
        print("-" * 40)

    @classmethod
    def menu(cls) -> None:
        """
        Boucle principale du menu :
        affiche le menu, lit le choix et appelle la méthode associée.
        """
        while True:
            clear_screen()
            cls.display_main_menu()
            choix = input("Votre Choix → ").strip()

            if choix == "1":
                clear_screen()
                PlayerController.create_player()

            elif choix == "2":
                clear_screen()
                tournoi = TournamentController()
                tournoi.run()

            elif choix == "3":
                clear_screen()
                cls._load_tournament_flow()

            elif choix == "4":
                clear_screen()
                cls._show_reports_menu()

            elif choix == "0":
                clear_screen()
                print("👋 Fin du programme, au revoir")
                break

            else:
                clear_screen()
                print("Choix invalide, veuillez réessayer.")

    @staticmethod
    def _show_reports_menu() -> None:
        """
        Affiche le sous-menu des rapports et exécute
        l’action correspondant au choix de l’utilisateur.
        """
        while True:
            print("\n" + "=" * 40)
            print("📊        AFFICHER DES RAPPORTS       📊")
            print("=" * 40)
            print("1. Liste des joueurs (ordre alphabétique)")
            print("2. Liste des tournois enregistrés")
            print("3. Infos d’un tournoi (nom, dates)")
            print("4. Liste des joueurs d’un tournoi (ordre alphabétique)")
            print("5. Liste des rounds et matches d’un tournoi")
            print("0. Retour au menu principal")
            report_choice = input("Votre Choix → ").strip()

            if report_choice == "1":
                ReportsView.list_all_players()
            elif report_choice == "2":
                ReportsView.list_all_tournaments()
            elif report_choice == "3":
                ReportsView.show_tournament_basic_info()
            elif report_choice == "4":
                ReportsView.list_players_for_tournament()
            elif report_choice == "5":
                ReportsView.list_rounds_and_matches_for_tournament()
            elif report_choice == "0":
                clear_screen()
                break
            else:
                clear_screen()
                print("Choix invalide, veuillez réessayer.")

    @classmethod
    def _load_tournament_flow(cls) -> None:
        """
        Gère l'expérience utilisateur de chargement de tournoi :
        liste les fichiers disponibles, demande un choix, puis charge ou redirige.
        """
        if not os.path.isdir(TOURNAMENTS_FOLDER):
            print(f"Aucun dossier '{TOURNAMENTS_FOLDER}' trouvé.")
            print("Créez d’abord un tournoi (option 2).")
            wait_for_enter(ENTER_FOR_MAIN_MENU)
            return

        files = cls._list_json_files()
        if not files:
            print(f"Aucun tournoi enregistré dans {TOURNAMENTS_FOLDER}.")
            print("Créez d’abord un tournoi (option 2).")
            wait_for_enter(ENTER_FOR_MAIN_MENU)
            return

        file_choice = cls._prompt_for_file(files)
        if file_choice:
            cls._handle_file_choice(file_choice, files)

    @classmethod
    def _list_json_files(cls) -> list[str]:
        """
        Liste et affiche tous les fichiers .json du dossier TOURNAMENTS_FOLDER.

        Returns:
            Liste des fichiers .json trouvés.
        """
        files = [f for f in os.listdir(TOURNAMENTS_FOLDER) if f.endswith(".json")]
        clear_screen()
        print("\nFichiers de tournois disponibles :\n")
        for filename in files:
            print(f"  • {filename}")
        cls.console.print(prompt_file_to_load())
        return files

    @staticmethod
    def _prompt_for_file(files: list[str]) -> str | None:
        """
        Demande à l'utilisateur de saisir un nom de fichier.

        Returns:
            Le nom choisi ou None si annulation.
        """
        file_choice = input("Nom du fichier à charger → ").strip()
        return file_choice if file_choice else None

    @staticmethod
    def _handle_file_choice(file_choice: str, files: list[str]) -> None:
        """
        Traite le fichier choisi par l'utilisateur : charge le tournoi ou propose d'en créer un.

        Args:
            file_choice: Nom du fichier choisi.
            files: Liste des fichiers disponibles.
        """
        if file_choice not in files:
            clear_screen()
            print(f"❌ Le fichier « {file_choice} » n'existe pas.")
            rep = input("Souhaitez-vous créer un nouveau tournoi ? (O/N) → ").strip().upper()
            if rep == "O":
                clear_screen()
                tournoi = TournamentController()
                tournoi.run()
            else:
                clear_screen()
            return

        chemin = os.path.join(TOURNAMENTS_FOLDER, file_choice)
        tournoi_data = load_tournament_from_json(chemin)
        tournoi = TournamentController.load_existing_tournament(tournoi_data, file_choice)
        tournoi.resume()
