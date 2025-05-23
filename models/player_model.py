class Player:
    def __init__(self,
        first_name: str, 
        last_name: str, 
        date_of_birth: str, 
        id_national_chess: str,
        total_score: float = 0.0,
        tournament_score: float = 0.0,
        rank: int = 0,
        played_with: list = None
        ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.id_national_chess = id_national_chess
        self.total_score = total_score
        self.tournament_score = tournament_score
        self.rank = rank
        self.played_with = played_with if played_with is not None else []

    
    def __str__(self):
        return(
            f"Prénom : {self.first_name}"
            f"Nom : {self.last_name}"
            f"Date de naissance : {self.date_of_birth}"
            f"ID national d'échecs : {self.id_national_chess}"
            f"Score Total : {self.total_score}"
            f"Score Tournoi : {self.tournament_score}"
            f"Classement : {self.rank}"
            f"A déjà joué avec : {self.played_with}"
        )
    
    def get_serialized_player(self):
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "id_national_chess": self.id_national_chess,
            "total_score": self.total_score,
            "tournament_score": self.tournament_score,
            "rank": self.rank,
            "played_with": self.played_with
        }
        return serialized_player