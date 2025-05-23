class Tournament:
    def __init__(
        self, 
        name: str, 
        location: str, 
        start_date: str, 
        end_date: str, 
        actual_round: int = 0,
        list_of_players: list = None,
        list_of_rounds: list = None, 
        number_of_rounds: int = 4, 
        description: str = ""
        ) -> None:

        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.actual_round = actual_round
        self.list_of_rounds = list_of_rounds if list_of_rounds is not None else []
        self.list_of_players = list_of_players if list_of_players is not None else []
        self.number_of_rounds = number_of_rounds
        self.description = description
    
    def get_serialized_tournament(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "actual_round": self.actual_round,
            "list_of_rounds": self.list_of_rounds,
            "list_of_players": self.list_of_players,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description
        }