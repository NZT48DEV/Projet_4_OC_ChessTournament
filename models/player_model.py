from typing import List, Dict, Any

class Player:
    """
    Modèle pour un joueur.
    """
    def __init__(
        self,
        id_national_chess: str,
        first_name: str = None,
        last_name: str = None,
        date_of_birth: str = None,
        tournament_score: float = 0.0,
        rank: int = 0,
        played_with: List[str] = None
    ) -> None:
        self.id_national_chess = id_national_chess
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.tournament_score = tournament_score
        self.rank = rank
        self.played_with = played_with if played_with is not None else []

    def get_serialized_player(self) -> Dict[str, Any]:
        """
        Sérialise le joueur pour JSON.
        """
        return {
            "id_national_chess": self.id_national_chess,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "tournament_score": self.tournament_score,
            "rank": self.rank,
            "played_with": list(self.played_with)
        }
    
    def get_tournament_data(self) -> dict:
        """
        Sérialisation “light” pour intégrer le joueur dans un tournoi :
        - on exclut volontairement first_name et last_name pour rester concis.
        """
        return {
            "id_national_chess": self.id_national_chess,
            "tournament_score":  self.tournament_score,
            "rank":              self.rank,
            "played_with":       self.played_with,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """
        Reconstruit une instance Player à partir d'un dict désérialisé.
        """
        return cls(
            id_national_chess=data.get("id_national_chess"),
            first_name=data.get("first_name", None),
            last_name=data.get("last_name", None),
            date_of_birth=data.get("date_of_birth", None),
            tournament_score=data.get("tournament_score", 0.0),
            rank=data.get("rank", 0),
            played_with=data.get("played_with", [])
        )
