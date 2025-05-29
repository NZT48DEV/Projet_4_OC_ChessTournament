from models.match_model     import Match
from views.match_view       import MatchView

class MatchController:
    def __init__(self, match: Match):
        self.match = match

    def run(self):
        player_1 = self.match.player_1
        player_2 = self.match.player_2
        # Cas du bye (joueur 2 est None)
        if player_2 is None:
            self.match.match_score_1 = 0.5
            player_1.tournament_score += 0.5
            print(f"\n{self.match.name} : repos pour {player_1.first_name} {player_1.last_name} (+0.5 point(s))")
            # fige et retourne
            self.match.assign_color()
            self.match.snapshot()
            return

        # Attribution des couleurs
        self.match.assign_color()

        # Affichage du match
        MatchView.display_match_header(self.match)

        # Saisie du résultat
        choice = MatchView.ask_match_result(self.match)

        # Application et fige du résultat
        self.match.apply_result(choice)
        self.match.snapshot()

        # Affichage du résultat final
        MatchView.show_match_result(self.match)
