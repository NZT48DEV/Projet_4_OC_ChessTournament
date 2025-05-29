from typing                 import List
from models.match_model     import Match
from models.round_model     import Round
from models.player_model    import Player


class RoundView:
    @staticmethod
    def show_error(message: str) -> None:
        print(f"Erreur: {message}")

    @staticmethod
    def show_round_start(rnd: Round) -> None:
        print(f"\n{rnd.round_number} - Début")

    @staticmethod
    def ask_match_result(match: Match) -> int:
        print(f"\n{match.get_player_info(match.player_1)} vs {match.get_player_info(match.player_2)}")
        print("1: jouer joue 1, 2: joueur 2 gagne, 3: égalité")
        while True:
            choice = input("> ")
            if choice in ("1", "2", "3"):
                return int(choice)
            print("Entrée invalide")

    @staticmethod
    def show_match_results(matches: List[Match]) -> None:
        for match in matches:
            print(match.get_result())

    @staticmethod
    def show_intermediate_ranking(players: List[Player]) -> None:
        """
        Affiche le classement intermédiaire en montrant
        le rang, le nom et le score de tournoi.
        """
        print("\nClassement intermédiaire :\n")
        # On trie par rank croissant
        for player in sorted(players, key=lambda p: p.rank):
            print(f"{player.rank} – {player.first_name} {player.last_name} : {player.tournament_score}")

    @staticmethod
    def show_round_report(rnd: Round) -> None:
        print(rnd.get_round_report())

    @staticmethod
    def show_round_end(rnd: Round) -> None:
        print(f"\n{rnd.round_number} terminé à {rnd.get_formatted_end_time()}")
