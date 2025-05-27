import random
from typing import Tuple

class Match:
    def __init__(self,
        name: str, 
        players_pair: Tuple[str, str]
        ) -> None:

        self.name: str = name
        self.player_1 = players_pair[0]
        self.player_2 = players_pair[1]

        self.score_player_1: float = 0.0
        self.score_player_2: float = 0.0

        self.color_player_1: str = ""
        self.color_player_2: str = ""
        
        self.winner: str = ""

    def __repr__(self) -> str:
        return (
            f"{self.player_1} ({self.color_player_1}) : {self.score_player_1} | " \
            f"{self.player_2} ({self.color_player_2}) : {self.score_player_2}"
        )
        
    
    def assign_color(self):
        """Tire aléatoirement qui joue 'Blanc' et qui joue 'Noir'"""
        color = random.choice(["Blanc", "Noir"])
        if color == "Blanc":
            self.color_player_1 = "Blanc"
            self.color_player_2 = "Noir"
        else:
            self.color_player_1 = "Noir"
            self.color_player_2 = "Blanc" 

    def play_match(self) -> None:
        self.assign_color()

        print()
        print(f"Match entre {self.player_1} ({self.color_player_1}) et {self.player_2} ({self.color_player_2})")
        result = input(
            f"Gagnant ?\n"
            f"1 - {self.player_1} ({self.color_player_1})\n"
            f"2 - {self.player_2} ({self.color_player_2})\n"
            f"3 - Égalité\n> "
            )
        
        if result == "1":
            self.score_player_1 += 1
            self.winner = self.player_1
        elif result == "2":
            self.score_player_2 += 1
            self.winner = self.player_2
        elif result == "3":
            self.score_player_1 += 0.5
            self.score_player_2 += 0.5
            self.winner = "Égalité"
        else:
            print("Entrée invalide, veuillez entrer 1, 2 ou 3")
            self.play_match()

    def get_result(self):
        if self.winner == "Égalité":
            return f"\nLe match est un match nul.\n"
        return f"\nLe gagnant est {self.winner}\n"
    
    def get_scores(self):
        return f"{self.player_1}: {self.score_player_1}\n" \
               f"{self.player_2}: {self.score_player_2}"
    

if __name__ == "__main__":
    # Création d'un match avec deux joueurs
    match = Match("Match 1", ("Alice", "Bob"))
    
    # Lancer le match et assigner les couleurs
    match.assign_color()
    
    # Lancer le match (demander le résultat à l'utilisateur)
    match.play_match()

    # Affichage du résultat
    print(match.get_result())

    # Affichage des scores
    print(match.get_scores())    

