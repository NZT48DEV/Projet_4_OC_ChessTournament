from config import TOURNAMENTS_FOLDER, ENTER_FOR_MAIN_MENU, ENTER_FOR_CONTINUE
from controllers.match_controller import MatchController
from storage.tournament_data import save_tournament_to_json
from models.match_model import Match
from models.player_model import Player
from models.round_model import Round
from models.tournament_model import Tournament
from utils.console import wait_for_enter
from views.round_view import RoundView
from views.tournament_view import TournamentView


class RoundController:
    """
    Contrôleur pour gérer l'enchaînement des rounds d'un tournoi,
    et sauvegarder l'état du tournoi après chaque match.
    """

    def __init__(self,
                 tournament: Tournament,
                 filename: str):
        self.tournament: Tournament = tournament
        self.filename: str = filename
        self.num_rounds: int = tournament.number_of_rounds
        self.players: list[Player] = tournament.list_of_players
        self.rounds: list[Round] = tournament.list_of_rounds or []

    def run(self) -> None:
        """
        Démarre la séquence de rounds depuis le premier.
        """
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return
        self.start_from_round(1)

    def start_from_round(self, starting_round: int) -> None:
        """
        Exécute tous les rounds du tournoi à partir du numéro indiqué.
        """
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return

        for rnd_num in range(starting_round, self.num_rounds + 1):
            rnd = self._get_or_create_round(rnd_num)

            for match in rnd.matches:
                if self._is_match_completed(match):
                    continue
                self._execute_match(match, rnd, rnd_num)

            self._finalize_round(rnd)
            print()
            wait_for_enter(ENTER_FOR_CONTINUE)

        TournamentView.show_tournament_summary(self.tournament)
        wait_for_enter(ENTER_FOR_MAIN_MENU)

    def _get_or_create_round(self, rnd_num: int) -> Round:
        """Récupère un Round existant ou en crée un nouveau."""
        if rnd_num <= len(self.rounds):
            return self.rounds[rnd_num - 1]
        rnd = self.make_round(rnd_num)
        self.rounds.append(rnd)
        self.tournament.list_of_rounds = self.rounds
        self.tournament.actual_round = rnd_num
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER, self.filename
        )
        return rnd

    def make_round(self, index: int) -> Round:
        """
        Crée un Round, démarre l'horodatage et génère les appariements.
        Initialise les scores et snapshots des matchs.
        """
        rnd = Round(f"Round {index}")
        rnd.start_round()
        rnd.generate_pairings(self.players)
        for match in rnd.matches:
            match.assign_color()
            # initialisation des scores
            match.match_score_1 = None
            if match.player_2:
                match.match_score_2 = None
                match.winner = None
            else:
                match.winner = None
            # snapshot initial
            if match.player_2:
                p1, p2 = match.player_1, match.player_2
                match._snap1 = {
                    "id_national_chess": p1.id_national_chess,
                    "match_score": None,
                    "tournament_score": None,
                    "rank": None,
                    "color": match.color_player_1,
                    "played_with": [p2.id_national_chess]
                }
                match._snap2 = {
                    "id_national_chess": p2.id_national_chess,
                    "match_score": None,
                    "tournament_score": None,
                    "rank": None,
                    "color": match.color_player_2,
                    "played_with": [p1.id_national_chess]
                }
        return rnd

    def _execute_match(self, match: Match, rnd: Round, rnd_num: int) -> None:
        """
        Lance un match et garantit persistance, snapshot et clôture de round si nécessaire.
        """
        mc = MatchController(
            match=match,
            current_round=rnd,
            tournament=self.tournament,
            filename=self.filename)
        try:
            mc.run()
        finally:
            if self._is_round_finished(rnd):
                rnd.end_round()
                self._save_progress(rnd_num)

    def _is_match_completed(self, match: Match) -> bool:
        """Retourne True si le match a déjà ses scores renseignés."""
        if match.player_2 is None:
            return match.match_score_1 is not None
        return (match.match_score_1 is not None
                and match.match_score_2 is not None)

    def _finalize_round(self, rnd: Round) -> None:
        """Affiche le rapport et le classement intermédiaire pour le round achevé."""
        RoundView.show_round_report(rnd)
        RoundView.show_intermediate_ranking(self.players)

    def _is_round_finished(self, rnd: Round) -> bool:
        """Teste si tous les matchs du round ont leurs scores renseignés."""
        return all(
            (m.match_score_1 is not None
             and (m.player_2 is None or m.match_score_2 is not None))
            for m in rnd.matches
        )

    def _save_progress(self, round_number: int) -> None:
        """Sauvegarde l'état actuel du tournoi dans le fichier JSON."""
        self.tournament.actual_round = round_number
        self.tournament.list_of_rounds = self.rounds
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER, self.filename
        )
