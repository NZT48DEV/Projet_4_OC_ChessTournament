from models.player_model import Player
from models.round_model import Round


class Tournament:
    def __init__(
        self,
        tournament_name: str,
        location: str = None,
        start_date: str = None,
        end_date: str = None,
        actual_round: int = 0,
        list_of_players: list[Player] = None,
        list_of_rounds: list[Round] = None,
        number_of_rounds: int = None,
        description: str = None
    ) -> None:

        self.tournament_name = tournament_name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.actual_round = actual_round
        self.list_of_rounds = list_of_rounds if list_of_rounds is not None else []
        self.list_of_players = list_of_players if list_of_players is not None else []
        self.number_of_rounds = number_of_rounds
        self.description = description

    def get_serialized_tournament(self) -> dict:
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "actual_round": self.actual_round,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "list_of_players": [p.get_tournament_data() for p in self.list_of_players],
            "list_of_rounds": [r.get_serialized_round() for r in self.list_of_rounds]
        }
