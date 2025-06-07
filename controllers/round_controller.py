from storage.tournament_data import save_tournament_to_json
from config import TOURNAMENTS_FOLDER
from models.round_model import Round
from views.round_view import RoundView
from controllers.match_controller import MatchController
from models.tournament_model import Tournament
from models.player_model import Player
from utils.console import clear_screen, wait_for_enter_continue
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
        # Charger les rounds déjà existants (peuvent être vides)
        self.rounds: list[Round] = tournament.list_of_rounds or []

    def make_round(self, index: int) -> Round:
        """Crée et initialise un Round (démarrage + appariements)."""
        rnd = Round(f"Round {index}")
        rnd.start_round()
        rnd.generate_pairings(self.players)
        # Dès création, initialiser les champs des matchs à None et préparer snapshots à null
        for match in rnd.matches:
            match.assign_color()
            if match.player_2 is not None:
                # pour les matchs « classiques », on remet bien à None
                match.match_score_1 = None
                match.match_score_2 = None
                match.winner = None
            else: 
                # Cas du bye : on veut un match_scire_1 à None
                match.match_score_1 = None
                match.winner = None
            # mais si match.player_2 est None → bye, on laisse match_score_1 = 0.5

            # Préparer le snapshot "à blanc" pour player_1 et player_2
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
        """
        Exécute tous les rounds du tournoi depuis le début.
        """
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return

        # On commence au round 1
        self.start_from_round(1)

    def start_from_round(self, starting_round: int) -> None:

        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return

        for rnd_num in range(starting_round, self.num_rounds + 1):
            # Réinitialiser le score de match pour tous les joueurs avant chaque round
            for player in self.players:
                player.match_score = None

            # a) Récupérer ou créer le round
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

            # b) Parcours des matchs du round, en sautant ceux déjà joués
            for match in rnd.matches:
                # 1) Si c'est un match "bye" (repos) et qu'il a déjà match_score_1 → on skip
                if match.player_2 is None and match.match_score_1 is not None:
                    continue

                # 2) Sinon, si c'est un match classique à deux joueurs, on skip s'il a déjà ses deux scores
                if match.player_2 is not None:
                    # (on n'a plus besoin de _snap1, on se fie directement à match_score_1/2)
                    if match.match_score_1 is not None and match.match_score_2 is not None:
                        continue

                # i. Recalculer les rangs avant le match
                self._update_ranks()
                self._refresh_match_snapshots()

                # Affichage du début du round
                RoundView.show_start_round(rnd)

                # ii. Lancer le match (via MatchController)
                mc = MatchController(match, self.tournament, self.filename)
                mc.run()

                # iii. Recalculer les rangs après le match
                self._update_ranks()
                self._refresh_match_snapshots()

                # iv. Prendre un instantané du match fraîchement joué
                match.snapshot()
                
                # v. Sauvegarder l’état du tournoi après ce match
                self._save_progress(rnd_num)

             # c) Ici, tous les matchs du round sont joués. On peut donc REELLEMENT terminer le round.
            rnd.end_round()

            # d) Sauvegarder une dernière fois ce round, avec end_time renseigné
            self._save_progress(rnd_num)

            # e) Affichage du récapitulatif complet du round
            RoundView.show_round_report(rnd)

            # f) Afficher le classement intermédiaire pour que l’utilisateur lise
            RoundView.show_intermediate_ranking(self.players)
            print()

            # g) Attendre la touche Entrée avant de passer au round suivant
            wait_for_enter_continue()

        # 2) Une fois tous les rounds joués, on affiche le résumé final du tournoi
        clear_screen()
        print("Tournoi terminé. Voici le résumé final :\n")
        TournamentView.show_tournament_summary(self.tournament)

    def _update_ranks(self) -> None:
        """
        Classement dense sur tournament_score :
        - Palier 1 (score max) -> rank=1
        - Palier 2 -> rank=2, etc.
        """
        sorted_players = sorted(self.players, key=lambda p: -p.tournament_score)

        prev_score = None
        prev_rank = 0
        dense_rank = 1

        for p in sorted_players:
            if prev_score is None or p.tournament_score != prev_score:
                p.rank = dense_rank
                prev_score = p.tournament_score
                prev_rank = dense_rank
                dense_rank += 1
            else:
                p.rank = prev_rank

    def _refresh_match_snapshots(self) -> None:
        """
        Met à jour les champs 'rank' des snapshots des matchs
        déjà joués dans le round en cours pour refléter
        le classement live.
        """
        if not self.rounds:
            return
        current_round = self.rounds[-1]
        for match in current_round.matches:
            if hasattr(match, '_snap1') and match._snap1:
                pid1 = match._snap1['id_national_chess']
                new_rank1 = next((p.rank for p in self.players if p.id_national_chess == pid1), None)
                if new_rank1 is not None:
                    match._snap1['rank'] = new_rank1
            if hasattr(match, '_snap2') and match._snap2:
                pid2 = match._snap2['id_national_chess']
                new_rank2 = next((p.rank for p in self.players if p.id_national_chess == pid2), None)
                if new_rank2 is not None:
                    match._snap2['rank'] = new_rank2

    def _save_progress(self, round_number: int) -> None:
        """Met à jour le tournoi et écrit le JSON après chaque match."""
        self.tournament.actual_round = round_number
        self.tournament.list_of_rounds = self.rounds
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename
        )
