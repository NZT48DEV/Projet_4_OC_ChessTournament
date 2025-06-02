from controllers.player_controller       import PlayerController
from controllers.tournament_controller   import TournamentController
from storage.player_data                import load_players_from_json   
from config                             import PLAYERS_FOLDER           
from views.player_view                  import PlayerView               
from utils.console                      import clear_screen, wait_for_enter_menu, wait_for_enter_rapports


class MenuView:
    def display_main_menu(self):
        print("\n" + "=" * 40)
        print("♟️       TOURNOI D'ÉCHECS - MENU       ♟️")
        print("=" * 40)
        print("1. 🧑 Créer un joueur")
        print("2. 🏆 Créer un tournoi")
        print("3. 📊 Afficher des rapports")
        print("0. ❌ Quitter")
        print("-" * 40)

    def menu(self):
        while True:
            clear_screen()
            self.display_main_menu()
            choix = input("Votre Choix → ")

            if choix == '1':
                clear_screen()
                PlayerController.create_player()                   
                wait_for_enter_menu()

            elif choix == '2':
                clear_screen()
                tournoi = TournamentController()
                tournoi.run()         
                wait_for_enter_menu()

            elif choix == '3':
                clear_screen()
                self._show_reports_menu()

            elif choix == '0':
                clear_screen()
                print("👋 Fin du programme, au revoir")
                break

            else:
                clear_screen()
                print("Choix invalide, veuillez réessayer.")

    def _show_reports_menu(self):
        """Sous-menu pour les différents rapports."""
        while True:
            print("\n" + "=" * 40)
            print("📊        AFFICHER DES RAPPORTS       📊")
            print("=" * 40)
            print("1. Liste des joueurs (ordre alphabétique)")
            print("0. Retour au menu principal")
            report_choice = input("Votre Choix → ")

            if report_choice == '1':
                clear_screen()
                # 1) Charger tous les joueurs
                players = load_players_from_json(PLAYERS_FOLDER)  
                # 2) Afficher la liste triée via PlayerView (clé : nom, puis prénom)
                PlayerView.list_players(players)
                wait_for_enter_rapports()
                clear_screen()

            elif report_choice == '0':
                clear_screen()
                break

            else:
                clear_screen()
                print("Choix invalide, veuillez réessayer.")
