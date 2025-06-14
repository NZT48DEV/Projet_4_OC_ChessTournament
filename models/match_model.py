import random
from typing import Tuple, Optional, Dict, Any

from config import DRAW_POINT, WIN_POINT, LOSE_POINT, BYE_POINT
from models.player_model import Player


class Match:
    """
    Modèle d'un match entre deux joueurs.
    Logique métier :
      - attribution des couleurs
      - application du résultat (mise à jour des scores)
      - préparation de snapshots pour la persistance
      - sérialisation JSON
    """

    def __init__(
        self,
        name: str,
        players_pair: Tuple[Player, Optional[Player]]
    ) -> None:
        """
        Initialise un match avec un nom et un tuple de joueurs (player_1, player_2).

        Args:
            name: Nom du match, typiquement "Round X - Match Y" ou "Round X - Repos".
            players_pair: Tuple contenant le joueur 1 et, ou none si bye.
        """
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
        """
        Représentation textuelle concise du match pour le débogage et les logs.
        Affiche "Repos" et score pour un bye, ou deux lignes pour un match classique.
        """
        if self.player_2 is None:
            return (
                f"{self.player_1.first_name} {self.player_1.last_name} – "
                f"Repos : {self.match_score_1} point(s)"
            )

        return (
            f"{self.player_1.first_name} {self.player_1.last_name} "
            f"[{self.color_player_1}] : {self.match_score_1} point(s)\n"
            f"{self.player_2.first_name} {self.player_2.last_name} "
            f"[{self.color_player_2}] : {self.match_score_2} point(s)"
        )

    def assign_color(self) -> None:
        """
        Assigne aléatoirement une couleur ("Blanc" ou "Noir")
        à player_1, et l’inverse à player_2.
        Pour un bye, aucune couleur n'est assignée.
        """
        if self.player_2 is None:
            self.color_player_1 = None
            return
        if random.choice([True, False]):
            self.color_player_1, self.color_player_2 = "Blanc", "Noir"
        else:
            self.color_player_1, self.color_player_2 = "Noir", "Blanc"

    def apply_result(self, choice: int) -> None:
        """
        Applique le résultat du match:
          - pour un bye, attribue BYE_POINT à player_1.
          - choice == 1 : victoire player_1 (WIN_POINT).
          - choice == 2 : victoire player_2 (WIN_POINT).
          - autre      : match nul (DRAW_POINT).
        Met également à jour player.tournament_score et self.winner.

        Args:
            choice: Code du résultat (1, 2, autre).
        """
        if self.player_2 is None:
            self.match_score_1 = BYE_POINT
            self.player_1.tournament_score += BYE_POINT
            self.winner = self.player_1
        elif choice == 1:
            self.match_score_1, self.match_score_2 = WIN_POINT, LOSE_POINT
            self.player_1.tournament_score += WIN_POINT
            self.winner = self.player_1
        elif choice == 2:
            self.match_score_1, self.match_score_2 = LOSE_POINT, WIN_POINT
            self.player_2.tournament_score += WIN_POINT
            self.winner = self.player_2
        else:
            self.match_score_1 = self.match_score_2 = DRAW_POINT
            self.player_1.tournament_score += DRAW_POINT
            if self.player_2:
                self.player_2.tournament_score += DRAW_POINT
            self.winner = None

    def snapshot(self) -> None:
        """
        Construit et stocke un snapshot interne des deux joueurs
        (score, tournament_score, rank, couleur, historique de parties).
        Utile pour la sérialisation ultérieure.
        """
        def make_snap(player: Player, score: float, color: Optional[str]) -> Dict[str, Any]:
            return {
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

    def result_type(self) -> str:
        """
        Renvoie un code indiquant l'état du match :
        - 'bye'      : match de repos
        - 'unplayed' : pas encore joué
        - 'draw'     : match nul
        - 'win'      : victoire d’un des joueurs
        """
        if self.player_2 is None:
            return "bye"
        if self.match_score_1 is None or self.match_score_2 is None:
            return "unplayed"
        if self.match_score_1 == self.match_score_2:
            return "draw"
        return "win"

    def get_winner(self) -> Optional[Player]:
        """
        Retourne le Player gagnant, ou None si nul.
        """
        return self.winner

    def get_serialized_match(self) -> Dict[str, Any]:
        """
        Sérialise l'objet Match en dictionnaire prêt pour JSON.
        Différencie les cas : match avec repos, non joué, ou joué.
        """
        if self.player_2 is None:
            return self._serialize_bye_match()
        if (
            self._snap1 is None or
            self._snap2 is None or
            self._snap1.get("match_score") is None or
            self._snap2.get("match_score") is None
        ):
            return self._serialize_unplayed_match()
        return self._serialize_played_match()

    def _serialize_bye_match(self) -> Dict[str, Any]:
        """
        Sérialise un match de repos (bye), uniquement le joueur 1 est concerné.
        """
        snap1 = self._snap1 or {
            "id_national_chess": self.player_1.id_national_chess,
            "match_score": self.match_score_1,
            "tournament_score": self.player_1.tournament_score,
            "rank": self.player_1.rank,
            "color": None,
            "played_with": list(self.player_1.played_with)
        }
        return {
            "name": self.name,
            "player_1": snap1,
            "player_2": None,
            "winner": {"id_national_chess": snap1["id_national_chess"]}
        }

    def _serialize_unplayed_match(self) -> Dict[str, Any]:
        """
        Sérialise un match classique non encore joué (snapshots ou scores manquants).
        """
        return {
            "name": self.name,
            "player_1": {
                "id_national_chess": self.player_1.id_national_chess,
                "match_score": None,
                "tournament_score": self.player_1.tournament_score,
                "rank": self.player_1.rank,
                "color": self.color_player_1,
                "played_with": list(self.player_1.played_with)
            },
            "player_2": {
                "id_national_chess": self.player_2.id_national_chess,
                "match_score": None,
                "tournament_score": self.player_2.tournament_score,
                "rank": self.player_2.rank,
                "color": self.color_player_2,
                "played_with": list(self.player_2.played_with)
            },
            "winner": None
        }

    def _serialize_played_match(self) -> Dict[str, Any]:
        """
        Sérialise un match classique terminé, avec snapshots complets et vainqueur.
        """
        winner_field = "draw" if self.winner is None else {
            "id_national_chess": self.winner.id_national_chess
        }
        return {
            "name": self.name,
            "player_1": self._snap1,
            "player_2": self._snap2,
            "winner": winner_field
        }
