from storage.tournament_data import save_tournament_to_json
from config import TOURNAMENTS_FOLDER
from models.round_model import Round
from views.round_view import RoundView
from controllers.match_controller import MatchController
from models.tournament_model import Tournament
from models.player_model import Player
from utils.console import clear_screen, wait_for_enter_continue
from utils.update_ranks import update_ranks
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

    def make_round(self, index: int) -> Round:
        rnd = Round(f"Round {index}")
        rnd.start_round()
        rnd.generate_pairings(self.players)
        for match in rnd.matches:
            match.assign_color()
            if match.player_2 is not None:
                match.match_score_1 = None
                match.match_score_2 = None
                match.winner = None
            else:
                match.match_score_1 = None
                match.winner = None
            p1 = getattr(match, 'player_1', None)
            p2 = getattr(match, 'player_2', None)
            if p1 and p2:
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

    def run(self) -> None:
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return
        self.start_from_round(1)

    def start_from_round(self, starting_round: int) -> None:
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return

        for rnd_num in range(starting_round, self.num_rounds + 1):
            for player in self.players:
                player.match_score = None

            if rnd_num <= len(self.rounds):
                rnd = self.rounds[rnd_num - 1]
            else:
                rnd = self.make_round(rnd_num)
                self.rounds.append(rnd)
                self.tournament.list_of_rounds = self.rounds
                self.tournament.actual_round = rnd_num
                save_tournament_to_json(
                    self.tournament.get_serialized_tournament(),
                    TOURNAMENTS_FOLDER,
                    self.filename
                )

            for match in rnd.matches:
                if match.player_2 is None and match.match_score_1 is not None:
                    continue
                if (match.player_2 is not None
                        and match.match_score_1 is not None
                        and match.match_score_2 is not None):
                    continue

                # classement live avant le match
                update_ranks(self.tournament)
                self._refresh_match_snapshots()
                RoundView.show_start_round(rnd)

                mc = MatchController(match, self.tournament, self.filename)
                try:
                    mc.run()
                finally:
                    # quoi qu'il arrive, on garantit : 
                    # snapshot, mise à jour des ranks, save, et clôture si nécessaire
                    match.snapshot()
                    update_ranks(self.tournament)
                    self._refresh_match_snapshots()
                    self._save_progress(rnd_num)

                    all_played = all(
                        (m.match_score_1 is not None
                         and (m.player_2 is None or m.match_score_2 is not None))
                        for m in rnd.matches
                    )
                    if all_played and rnd.end_time is None:
                        rnd.end_round()
                        self._save_progress(rnd_num)

            # une fois tous les matchs parcourus, round déjà close si terminé
            RoundView.show_round_report(rnd)
            RoundView.show_intermediate_ranking(self.players)
            print()
            wait_for_enter_continue()

        clear_screen()
        print("Tournoi terminé. Voici le résumé final :\n")
        TournamentView.show_tournament_summary(self.tournament)

    def _refresh_match_snapshots(self) -> None:
        if not self.rounds:
            return
        current_round = self.rounds[-1]
        for match in current_round.matches:
            if hasattr(match, '_snap1') and match._snap1:
                pid1 = match._snap1['id_national_chess']
                new_rank1 = next(
                    (p.rank for p in self.players if p.id_national_chess == pid1),
                    None
                )
                if new_rank1 is not None:
                    match._snap1['rank'] = new_rank1
            if hasattr(match, '_snap2') and match._snap2:
                pid2 = match._snap2['id_national_chess']
                new_rank2 = next(
                    (p.rank for p in self.players if p.id_national_chess == pid2),
                    None
                )
                if new_rank2 is not None:
                    match._snap2['rank'] = new_rank2

    def _save_progress(self, round_number: int) -> None:
        self.tournament.actual_round = round_number
        self.tournament.list_of_rounds = self.rounds
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename
        )
