from typing                     import List, Union
from models.match_model         import Match
from models.match_model         import Match
from rich.console               import Console
from rich.table                 import Table
from rich.panel                 import Panel
from rich.text                  import Text
from rich.box                   import ROUNDED, SIMPLE
from utils.console              import clear_screen

class MatchView:
    console = Console()

    @staticmethod
    def ask_match_result(match: Match) -> None:
        """
        Affiche un petit panneau “DUEL” à gauche (pas plein écran),
        puis la question “Qui gagne ?” et enfin la table des choix.
        """
        # 1. Informations des deux joueurs
        p1 = match.player_1
        p2 = match.player_2

        # 2. Titre “DUEL” dans un Panel compact (expand=False)
        titre = Text()
        titre.append(f"{p1.first_name} {p1.last_name} ({p1.id_national_chess})", style="bold yellow")
        titre.append(" (Blanc) ", style="white")
        titre.append("⚔️   ")
        titre.append(f"{p2.first_name} {p2.last_name} ({p2.id_national_chess})", style="bold yellow")
        titre.append(" (Noir)", style="white")

        panel_title = Panel(
            titre,
            title="[bold magenta]MATCH[/bold magenta]",
            border_style="magenta",
            box=ROUNDED,
            expand=False,   # IMPORTANT : le panel reste juste de la largeur du texte
            padding=(0, 1)
        )

        # 3. Construction de la table des choix (expand=False aussi)
        choix_table = Table(
            show_header=False,
            box=SIMPLE,   # boîte simple
            expand=False,   # n'occupe pas tout l'espace horizontal
            padding=(0, 1),
        )
        # Colonne “numéro”  
        choix_table.add_column("C", justify="center", no_wrap=True, width=3)
        choix_table.add_column("Candidat", justify="left")

        choix_table.add_row(
            "[bold green]1[/bold green]",
            f"{p1.first_name} {p1.last_name} ({p1.id_national_chess}) (Blanc)"
        )
        choix_table.add_row(
            "[bold red]2[/bold red]",
            f"{p2.first_name} {p2.last_name} ({p2.id_national_chess}) (Noir)"
        )
        choix_table.add_row(
            "[bold yellow]3[/bold yellow]",
            "Égalité"
        )

        # 4. On enlève tout appel à Rule() ou Align.center pour ne pas forcer la largeur
        MatchView.console.print(panel_title)
        MatchView.console.print()  # ligne vide
        MatchView.console.print(Text("Qui gagne ?", style="bold white", justify="center"))
        MatchView.console.print()  # ligne vide
        MatchView.console.print(choix_table)
        MatchView.console.print()  # ligne vide

        # 5. Lecture de l’entrée utilisateur
        while True:
            choice = MatchView.console.input("[bold cyan]> [/bold cyan]").strip()
            if choice in ("1", "2", "3"):
                return int(choice)
            MatchView.console.print("[bold red]Entrée invalide, tapez 1, 2 ou 3.[/bold red]")
            MatchView.console.print()
    
    @staticmethod
    def show_match_results(matches: Union[Match, List[Match]]) -> None:
        """
        Affiche le(s) résultat(s) du/des match(es).
        Si on lui passe un unique Match, on le met en liste [match].
        """
        if isinstance(matches, Match):
            matches = [matches]

        for match in matches:
            print()
            MatchView.console.print(match.get_result())
            print()
            
            
            