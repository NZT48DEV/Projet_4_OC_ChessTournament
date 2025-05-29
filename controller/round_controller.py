from storage.tournament_data        import save_tournament_to_json
from config                         import TOURNAMENTS_FOLDER
from models.round_model             import Round
from views.round_view               import RoundView
from controller.match_controller    import MatchController
from models.tournament_model        import Tournament
from models.player_model            import Player

class RoundController:
    """
    Contrôleur pour gérer l'enchaînement des rounds d'un tournoi,
    et sauvegarder l'état du tournoi après chaque match.
    """
    def __init__(self,
                tournament: Tournament,
                filename: str):
        
        self.tournament: Tournament   = tournament
        self.filename: str            = filename
        self.num_rounds: int          = tournament.number_of_rounds
        self.players: list[Player]    = tournament.list_of_players
        self.rounds: list[Round]      = []

    def make_round(self, index: int) -> Round:
        """Crée et initialise un Round (démarrage + appariements)."""
        rnd = Round(f"Round {index}")
        rnd.start_round()
        rnd.generate_pairings(self.players)
        return rnd

    def run(self) -> None:
        if len(self.players) < 2:
            RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
            return

        for round_number in range(1, self.num_rounds + 1):
            # Réinitialiser match_score pour tous avant chaque round
            for player in self.players:
                player.match_score = 0.0

            # Création et démarrage du round
            rnd = self.make_round(round_number)
            self.rounds.append(rnd)
            RoundView.show_round_start(rnd)

            # Exécution des matchs en mettant à jour les rangs et snapshots
            for match in rnd.matches:
                # a) Recalculer les rangs avant le match (live)
                self._update_ranks()
                self._refresh_match_snapshots()

                # b) Lancer le match
                mc = MatchController(match)
                mc.run()

                # c) Recalculer les rangs après le match (live)
                self._update_ranks()
                self._refresh_match_snapshots()

                # d) Figer l'instantané du match courant dans son propre objet
                match.snapshot()

                # e) Sauvegarder l'état du tournoi
                self._save_progress(round_number)

            # Rapport et affichage du classement intermédiaire
            RoundView.show_round_report(rnd)
            RoundView.show_intermediate_ranking(self.players)

            # Fin du round
            rnd.end_round()
            RoundView.show_round_end(rnd)

        # Sauvegarde finale de l'ensemble des rounds
        self._save_progress(self.num_rounds)

    def _update_ranks(self) -> None:
        """
        Classement dense sur tournament_score :
        - Palier 1 (score max) -> rank=1
        - Palier 2 -> rank=2, etc.
        """
        # Tri décroissant par score
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
        # Parcourt tous les matchs joués pour ajuster dynamiquement leurs ranks
        for match in current_round.matches:
           # uniquement si les snapshots existent
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
        """Met à jour le tournoi et écrit le JSON."""
        self.tournament.actual_round   = round_number
        self.tournament.list_of_rounds = self.rounds
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename
        )