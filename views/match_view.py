from models.match_model import Match

class MatchView:
    @staticmethod
    def display_match_header(match: Match) -> None:
        if match.player_2 is None:
            # bye/repos
            p = match.player_1
            print(f"\n{match.name} : repos pour {p.first_name} {p.last_name}")
        else:
            print(
                f"\nMatch entre {match.get_player_info(match.player_1)} "
                f"et {match.get_player_info(match.player_2)}"
            )

    @staticmethod
    def ask_match_result(match: Match) -> int:
        """Demande à l’utilisateur qui a gagné."""
        print("Qui gagne ?")
        print(f"1 – {match.get_player_info(match.player_1)}")
        print(f"2 – {match.get_player_info(match.player_2)}")
        print("3 – Égalité")
        choix = input("> ")
        while choix not in ("1", "2", "3"):
            print("Entrée invalide, 1, 2 ou 3 seulement.")
            choix = input("> ")
        return int(choix)

    @staticmethod
    def show_match_result(match: Match) -> None:
        """Affiche le résultat final du match."""
        print(match.get_result())
