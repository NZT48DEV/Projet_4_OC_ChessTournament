from typing                     import List
from rich.console               import Console
from rich.panel                 import Panel
from rich.text                  import Text

from models.round_model         import Round
from models.player_model        import Player
from utils.console              import clear_screen

class RoundView:
    console = Console()

    @staticmethod
    def show_error(message: str) -> None:
        RoundView.console.print(f"[bold red]Erreur:[/bold red] {message}")

    @staticmethod
    def show_intermediate_ranking(players: List[Player]) -> None:
        """
        Affiche le classement intermédiaire en montrant
        le rang, le nom et le score de tournoi,
        avec alignement des IDN et des scores.
        """
        RoundView.console.print("\n[b yellow]Classement intermédiaire[/b yellow]\n")

        # Préparer deux listes : 
        # - left_parts contiendra "1. Prénom NOM"
        # - id_parts contiendra "(IDN)"
        # - score_parts contiendra "1.5"
        entries = []
        for player in sorted(players, key=lambda p: p.rank):
            left = f"{player.rank}. {player.first_name} {player.last_name}"
            idn = f"({player.id_national_chess})"
            score_str = f"{player.tournament_score:.1f}"
            entries.append((left, idn, score_str))

        # Calculer la largeur max pour le texte de nom (left) et pour l'IDN (idn)
        max_left_width = max(len(left) for left, _, _ in entries)
        max_idn_width = max(len(idn) for _, idn, _ in entries)

        # Afficher chaque ligne en alignant d'abord la partie "nom", puis "IDN", puis ": score"
        for left, idn, score_str in entries:
            # Espaces pour aligner les IDN
            pad_left = " " * (max_left_width - len(left))
            # Espaces pour aligner les deux-points après l'IDN
            pad_idn = " " * (max_idn_width - len(idn))
            RoundView.console.print(f"{left}{pad_left} {idn}{pad_idn} : [b]{score_str}[/b]")

    @staticmethod
    def show_round_report(rnd: Round) -> None:
        clear_screen()
        header = Text(f"{rnd.round_number}  ", style="bold white on blue")
        header.append("– Récap", style="bold white on blue")
        RoundView.console.print(Panel(header, expand=False, border_style="blue"))
        RoundView.console.print(rnd.get_round_report())

    @staticmethod
    def show_start_round(rnd: Round) -> None:
        clear_screen()
        header = Text(f"{rnd.round_number}  ", style="bold white on blue")
        header.append("– En cours", style="bold white on blue")
        RoundView.console.print(Panel(header, expand=False, border_style="blue"))
    