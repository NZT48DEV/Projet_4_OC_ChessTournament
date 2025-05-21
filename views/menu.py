from controller.player import create_player
from utils.console import clear_screen

class Menu:
    def display_menu(self):
            print("\n" + "=" * 40)
            print("♟️       TOURNOI D'ÉCHECS - MENU       ♟️")
            print("=" * 40)
            print("1. 🧑 Créer un joueur")
            print("0. ❌ Quitter")
            print("-" * 40)

    def menu(self):
        while True:
            clear_screen()
            self.display_menu()
            choix = input("Votre Choix → ")

            if choix == '1':
                clear_screen()
                create_player()
                

            elif choix == '0': 
                clear_screen()
                print("👋 Fin du programme, aurevoir")
                break
