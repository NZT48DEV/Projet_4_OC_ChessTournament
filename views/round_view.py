from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from models.round_model import Round
from models.player_model import Player
from utils.console import clear_screen


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
        report = RoundView.format_round_report(rnd)
        RoundView.console.print(report)

    @staticmethod
    def show_start_round(rnd: Round) -> None:
        clear_screen()
        header = Text(f"{rnd.round_number}  ", style="bold white on blue")
        header.append("– En cours", style="bold white on blue")
        RoundView.console.print(Panel(header, expand=False, border_style="blue"))

    @staticmethod
    def format_round_report(rnd: Round) -> str:
        """
        Retourne un rapport textuel aligné des matchs de ce round,
        plaçant les byes en premier et espaçant par des lignes vides.
        """
        # tri : byes d'abord
        ordered = sorted(rnd.matches, key=lambda m: m.player_2 is not None)
        groups: List[List[tuple]] = []
        for m in ordered:
            if m.player_2 is None:
                p = m.player_1
                groups.append([(f"{p.first_name} {p.last_name}", f"[{p.id_national_chess}]",
                              "(Repos)", f"{m.match_score_1:.1f}")])
            else:
                p1, p2 = m.player_1, m.player_2
                groups.append([
                    (f"{p1.first_name} {p1.last_name}", f"[{p1.id_national_chess}]",
                     f"({m.color_player_1})", f"{(m.match_score_1 or 0.0):.1f}"),
                    (f"{p2.first_name} {p2.last_name}", f"[{p2.id_national_chess}]",
                     f"({m.color_player_2})", f"{(m.match_score_2 or 0.0):.1f}")
                ])
        # calcul des largeurs
        all_entries = [e for grp in groups for e in grp]
        max_name = max((len(name) for name, *_ in all_entries), default=0)
        max_id = max((len(idn) for _, idn, *_ in all_entries), default=0)
        max_color = max((len(color) for *_, color, _ in all_entries), default=0)

        # construction des lignes
        lines = [f"\n{rnd.round_number} – Matchs :\n\n"]
        for i, grp in enumerate(groups):
            for name, idn, color, score in grp:
                lines.append(f"{name:<{max_name}} {idn:<{max_id}} {color:<{max_color}} : {score}\n")
            if i < len(groups) - 1:
                lines.append("\n")
        return "".join(lines)
