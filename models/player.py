class Player:
    def __init__(self, first_name, last_name, date_of_birth, id_national_chess) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.id_national_chess = id_national_chess
    
    def __str__(self):
        return(
            f"Prénom : {self.first_name}"
            f"Nom : {self.last_name}"
            f"Date de naissance : {self.date_of_birth}"
            f"ID national d'échecs : {self.id_national_chess}"
        )
    
    def get_serialized_player(self):
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "id_national_chess": self.id_national_chess
        }
        return serialized_player