from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED, SIMPLE

from config import DRAW_POINT, BYE_POINT, WIN_POINT
from models.match_model import Match


class MatchView:
    console = Console()

    @staticmethod
    def ask_match_result(match: Match) -> int:
        """
        Affiche le panneau “MATCH” et la table des choix,
        puis lit et renvoie 1, 2 ou 3 (3 pour égalité).
        """
        MatchView.console.print(MatchView._build_match_panel(match))
        MatchView.console.print()
        MatchView.console.print(Text("Qui gagne ?", style="bold white", justify="center"))
        MatchView.console.print()
        MatchView.console.print(MatchView._build_choice_table(match))
        MatchView.console.print()

        while True:
            choice = MatchView.console.input("[bold cyan]> [/bold cyan]").strip()
            if choice in ("1", "2", "3"):
                return int(choice)
            MatchView.console.print("[bold red]Entrée invalide, tapez 1, 2 ou 3.[/bold red]")
            MatchView.console.print()

    @staticmethod
    def _build_match_panel(match: Match) -> Panel:
        """
        Construit et renvoie le panneau d’en-tête du match avec les noms, couleurs, etc.
        """
        p1, p2 = match.player_1, match.player_2
        titre = Text()
        titre.append(f"{p1.first_name} {p1.last_name} ({p1.id_national_chess})", style="bold yellow")
        titre.append(f" ({match.color_player_1}) ", style="white")
        titre.append("⚔️   ")
        titre.append(f"{p2.first_name} {p2.last_name} ({p2.id_national_chess})", style="bold yellow")
        titre.append(f" ({match.color_player_2})", style="white")
        return Panel(
            titre,
            title="[bold magenta]MATCH[/bold magenta]",
            border_style="magenta",
            box=ROUNDED,
            expand=False,
            padding=(0, 1)
        )

    @staticmethod
    def _build_choice_table(match: Match) -> Table:
        """
        Construit et renvoie la table de choix pour les résultats du match.
        """
        p1, p2 = match.player_1, match.player_2
        table = Table(show_header=False, box=SIMPLE, expand=False, padding=(0, 1))
        table.add_column("C", justify="center", no_wrap=True, width=3)
        table.add_column("Candidat", justify="left")
        table.add_row(
            "[bold green]1[/bold green]",
            f"{p1.first_name} {p1.last_name} ({p1.id_national_chess}) ({match.color_player_1})"
            )
        table.add_row(
            "[bold red]2[/bold red]",
            f"{p2.first_name} {p2.last_name} ({p2.id_national_chess}) ({match.color_player_2})"
            )
        table.add_row("[bold yellow]3[/bold yellow]", "Égalité")
        return table

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
            return Text.assemble(
                ("Match nul ", "b yellow"),
                (f"-> + {DRAW_POINT} point(s)", "i green"),
                (" pour chaque joueur")
            )
        # Victoire
        winner = match.get_winner()
        name = f"{winner.first_name} {winner.last_name} ({winner.id_national_chess})"
        return Text.assemble(
            ("Gagnant ", "yellow"),
            (name, "bold"),
            (f" -> + {WIN_POINT} point(s).", "i green")
        )

    @staticmethod
    def show_match_results(matches: Match | List[Match]) -> None:
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
