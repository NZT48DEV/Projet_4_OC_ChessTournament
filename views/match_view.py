from typing                 import List, Union
from models.match_model     import Match
from rich.console           import Console
from rich.table             import Table
from rich.panel             import Panel
from rich.text              import Text
from rich.box               import ROUNDED, SIMPLE
from config                 import DRAW_POINT, BYE_POINT


class MatchView:
    console = Console()

    @staticmethod
    def ask_match_result(match: Match) -> int:
        """
        Affiche le panneau “MATCH” et la table des choix,
        puis lit et renvoie 1, 2 ou 3 (3 pour égalité).
        """
        p1, p2 = match.player_1, match.player_2

        # Titre DUEL
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
            expand=False,
            padding=(0,1)
        )

        # Table de choix
        choix_table = Table(show_header=False, box=SIMPLE, expand=False, padding=(0,1))
        choix_table.add_column("C", justify="center", no_wrap=True, width=3)
        choix_table.add_column("Candidat", justify="left")
        choix_table.add_row("[bold green]1[/bold green]", f"{p1.first_name} {p1.last_name} ({p1.id_national_chess}) (Blanc)")
        choix_table.add_row("[bold red]2[/bold red]",   f"{p2.first_name} {p2.last_name} ({p2.id_national_chess}) (Noir)")
        choix_table.add_row("[bold yellow]3[/bold yellow]", "Égalité")

        MatchView.console.print(panel_title)
        MatchView.console.print() 
        MatchView.console.print(Text("Qui gagne ?", style="bold white", justify="center"))
        MatchView.console.print()
        MatchView.console.print(choix_table)
        MatchView.console.print()

        while True:
            choice = MatchView.console.input("[bold cyan]> [/bold cyan]").strip()
            if choice in ("1", "2", "3"):
                return int(choice)
            MatchView.console.print("[bold red]Entrée invalide, tapez 1, 2 ou 3.[/bold red]")
            MatchView.console.print()

    @staticmethod
    def format_result(match: Match) -> Text:
        """
        Construit et renvoie un Text Rich du résultat, 
        selon match.result_type() et match.get_winner().
        """
        t = match.result_type()
        # Bye
        if t == "bye":
            return Text.assemble(
                ("Match de Repos pour le joueur : ", "b yellow"),
                (f"{match.player_1.first_name} {match.player_1.last_name}", "b"),
                (f" ({match.player_1.id_national_chess})", "b"),
                (f" -> + {BYE_POINT} point(s)", "i green")
            )
        # Non joué
        if t == "unplayed":
            return Text("Match non joué.", style="bold red")
        # Nul
        if t == "draw":
            return Text(f"Match nul -> {DRAW_POINT} point(s) pour chaque joueur", style="yellow bold")
        # Victoire
        winner = match.get_winner()
        name = f"{winner.first_name} {winner.last_name} ({winner.id_national_chess})"
        return Text.assemble(
            ("Gagnant : ", "yellow"),
            (name, "bold")
        )

    @staticmethod
    def show_match_results(matches: Union[Match, List[Match]]) -> None:
        """
        Affiche un ou plusieurs résultats : 
        utilise format_result() au lieu de match.get_result().
        """
        if isinstance(matches, Match):
            matches = [matches]

        for match in matches:
            print()
            MatchView.console.print(MatchView.format_result(match))
            print()
