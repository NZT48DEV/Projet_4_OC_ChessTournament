import os
from rich.console import Console

console = Console()

def clear_screen():
    """
    Efface le contenu de la console en fonction du système d'exploitation :
    - Sur Windows, exécute la commande 'cls'
    - Sur Unix/Linux/MacOS, exécute la commande 'clear'
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_for_enter_continue() -> None:
    """
    Affiche un message et met en pause jusqu’à ce que l’utilisateur appuie sur Entrée.
    """
    console.input("\nAppuyez sur [b yellow][i]Entrée[/i][/b yellow] pour continuer…")

def wait_for_enter_menu() -> None:
    """
    Affiche un message et met en pause jusqu’à ce que l’utilisateur appuie sur Entrée.
    """
    console.input("\nAppuyez sur [b yellow][i]Entrée[/i][/b yellow] pour revenir au menu principal.")

def wait_for_enter_rapports() -> None:
    """
    Affiche un message et met en pause jusqu’à ce que l’utilisateur appuie sur Entrée.
    """
    console.input("\nAppuyez sur [b yellow][i]Entrée[/i][/b yellow] pour revenir au menu des rapports.")