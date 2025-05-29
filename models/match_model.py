import random
from typing                 import Tuple, Optional, Dict, Any
from models.player_model    import Player


class Match:
    """
    Modèle d'un match entre deux joueurs.
    Logique métier : attribution des couleurs, application du résultat
    et sérialisation pour JSON.
    """
    def __init__(self,
        name: str,
        players_pair: Tuple[Player, Optional[Player]]
        ) -> None:

        self.name = name
        self.player_1, self.player_2 = players_pair

        # score et couleurs sur CE match
        self.match_score_1: float = 0.0
        self.match_score_2: float = 0.0
        self.color_player_1: Optional[str] = None
        self.color_player_2: Optional[str] = None

        # winner sera None en cas de nul, ou Player gagnant
        self.winner: Optional[Player] = None

        # snapshots figés sur les états de CE match
        self._snap1: Optional[Dict[str, Any]] = None
        self._snap2: Optional[Dict[str, Any]] = None

    def __repr__(self) -> str:
        if self.player_2 is None:
            return f"{self.player_1.first_name} {self.player_1.last_name} – Repos : {self.match_score_1} point(s)"
        return (
            f"{self.get_player_info(self.player_1)} : {self.match_score_1} point(s)\n"
            f"{self.get_player_info(self.player_2)} : {self.match_score_2} point(s)"
        )

    def assign_color(self) -> None:
        if self.player_2 is None:
            self.color_player_1 = None
            return
        if random.choice([True, False]):
            self.color_player_1, self.color_player_2 = "Blanc", "Noir"
        else:
            self.color_player_1, self.color_player_2 = "Noir", "Blanc"

    def apply_result(self, choice: int) -> None:
        """
        Applique le résultat sur les joueurs et met à jour leurs tournament_score.
        """
        self.assign_color()

        if self.player_2 is None:
            self.match_score_1 = 0.5
            self.player_1.tournament_score += 0.5
            self.winner = self.player_1
        elif choice == 1:
            self.match_score_1, self.match_score_2 = 1.0, 0.0
            self.player_1.tournament_score += 1.0
            self.winner = self.player_1
        elif choice == 2:
            self.match_score_1, self.match_score_2 = 0.0, 1.0
            self.player_2.tournament_score += 1.0
            self.winner = self.player_2
        else:
            self.match_score_1 = self.match_score_2 = 0.5
            self.player_1.tournament_score += 0.5
            if self.player_2:
                self.player_2.tournament_score += 0.5
            self.winner = None

    def snapshot(self) -> None:
        """
        Fige l'état courant du match (score, rank, tournament_score, couleurs, played_with)
        pour la sérialisation ultérieure.
        """
        def make_snap(player: Player, score: float, color: Optional[str]) -> Dict[str, Any]:
            return {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "id_national_chess": player.id_national_chess,
                "match_score": score,
                "tournament_score": player.tournament_score,
                "rank": player.rank,
                "color": color,
                "played_with": list(player.played_with)
            }

        self._snap1 = make_snap(self.player_1, self.match_score_1, self.color_player_1)
        if self.player_2:
            self._snap2 = make_snap(self.player_2, self.match_score_2, self.color_player_2)
        else:
            self._snap2 = None
    
    def get_result(self) -> str:
        """
        Renvoie une chaîne décrivant le résultat du match pour l'affichage.
        """
        if self.player_2 is None:
            return "Repos (0.5 point(s))"
        if self.winner is None:
            return "Match nul."
        return f"Gagnant : {self.winner.first_name} {self.winner.last_name}"

    def get_player_info(self, player: Player) -> str:
        color = self.color_player_1 if player is self.player_1 else self.color_player_2
        return f"{player.first_name} {player.last_name} ({color})"

    def get_serialized_match(self) -> Dict[str, Any]:
        """
        Retourne les données JSON figées au moment du snapshot.
        """
        if self._snap1 is None:
            return {"name": self.name, "matches": []}

        if self._snap2 is None:
            return {"name": self.name, "player": self._snap1, "type": "repos"}

        return {
            "name": self.name,
            "player_1": self._snap1,
            "player_2": self._snap2,
            "winner": None if self.winner is None else {
                "first_name": self.winner.first_name,
                "last_name":  self.winner.last_name,
                "id_national_chess": self.winner.id_national_chess
            }
        }