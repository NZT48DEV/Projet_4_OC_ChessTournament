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

        if self.player_2 is None:
            # Cas du bye : on donne 0.5 point(s)
            self.match_score_1 = 0.5
            self.player_1.tournament_score += 0.5
            self.winner = self.player_1
        elif choice == 1:
            # Victoire du joueur 1
            self.match_score_1, self.match_score_2 = 1.0, 0.0
            self.player_1.tournament_score += 1.0
            self.winner = self.player_1
        elif choice == 2:
            # Victoire du joueur 2
            self.match_score_1, self.match_score_2 = 0.0, 1.0
            self.player_2.tournament_score += 1.0
            self.winner = self.player_2
        else:
            # Match nul
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
                "id_national_chess": player.id_national_chess,
                "match_score": score,
                "tournament_score": player.tournament_score,
                "rank": player.rank,
                "color": color,
                "played_with": list(player.played_with)
            }

        # Snapshot du premier joueur
        self._snap1 = make_snap(self.player_1, self.match_score_1, self.color_player_1)

        # Pour le second joueur : s'il existe, snapshot normal, sinon None
        if self.player_2:
            self._snap2 = make_snap(self.player_2, self.match_score_2, self.color_player_2)
        else:
            self._snap2 = None
    
    def get_result(self) -> str:
        """
        Renvoie une chaîne décrivant le résultat du match pour l'affichage,
        avec les styles Rich. On ne se base plus sur self.winner pour le bye,
        mais directement sur self.player_1, qui est toujours un Player.
        """

        # 1) Cas du bye (repos) :
        if self.player_2 is None:
            # Toujours afficher le nom de player_1 (le joueur qui reçoit le bye).
            # On suppose que player_1 existe et est bien une instance Player.
            return (
                f"[b yellow]Match de Repos (0.5 point(s)) : [/b yellow]"
                f"[b]{self.player_1.first_name} {self.player_1.last_name} "
                f"({self.player_1.id_national_chess})[/b]"
            )

        # 2) Cas d'un match normal à deux joueurs :
        #    Si aucun des deux scores n'a été saisi, on considère que le match n'est pas encore joué.
        if self.match_score_1 is None or self.match_score_2 is None:
            return "Match non joué."

        # 3) Si les deux scores sont égaux → match nul
        if self.match_score_1 == self.match_score_2:
            return "[b yellow]Match nul (0.5 point(s)) pour chaque joueur[/b yellow]"

        # 4) Sinon, il y a un vrai gagnant :
        #    On se repose sur self.winner pour le nom, mais on peut aussi
        #    vérifier par match_score_1 vs match_score_2. Ici, on suppose
        #    self.winner est bien une instance Player (recréée par le loader).
        if self.winner is not None:
            return (
                f"[b yellow]Gagnant[/b yellow] : "
                f"[b]{self.winner.first_name} {self.winner.last_name} "
                f"({self.winner.id_national_chess})[/b]"
            )

        # Cas de sécurité (ne devrait pas arriver si `apply_result` a été appelé correctement) :
        return "Résultat inconnu"



        

    def get_player_info(self, player: Player) -> str:
        color = self.color_player_1 if player is self.player_1 else self.color_player_2
        return f"{player.first_name} {player.last_name} [{player.id_national_chess}] ({color})"

    def get_serialized_match(self) -> Dict[str, Any]:
        # 1) Si c'est un match de repos
        if self.player_2 is None:
            if self._snap1:
                snap1 = self._snap1
            else:
                snap1 = {
                    "id_national_chess": self.player_1.id_national_chess,
                    "match_score": self.match_score_1,            # ce doit être 0.5
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

        # 2) Cas match classique
        if (
            self._snap1 is None or
            self._snap2 is None or
            self._snap1.get("match_score") is None or
            self._snap2.get("match_score") is None
        ):
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

        # 3) Match effectivement joué
        if self.winner is None:
            winner_field = "draw"
        else:
            winner_field = { "id_national_chess": self.winner.id_national_chess }

        return {
            "name": self.name,
            "player_1": self._snap1,
            "player_2": self._snap2,
            "winner": winner_field
        }
