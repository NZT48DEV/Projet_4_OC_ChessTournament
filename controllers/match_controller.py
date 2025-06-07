from typing                     import Optional
from config                     import TOURNAMENTS_FOLDER, DRAW_POINT
from models.tournament_model    import Tournament
from models.match_model         import Match
from storage.tournament_data    import save_tournament_to_json
from utils.console              import wait_for_enter_continue
from utils.update_ranks         import update_ranks
from views.match_view           import MatchView
from views.round_view           import RoundView


class MatchController:
    tournament: Optional[Tournament]
    def __init__(self, match: Match, tournament=None, filename: str = None):
        """
        - match      : l'objet Match à exécuter
        - tournament : l'objet Tournament (nécessaire pour mettre à jour le end_time de la ronde)
        - filename   : nom du fichier JSON du tournoi (pour save_tournament_to_json)
        """
        self.match = match
        self.tournament = tournament
        self.filename = filename

    def run(self) -> None:
        """
        Orchestration d'un match :
        1) Détermination et application du score (bye = 0.5 ou choix utilisateur)
        2) Mise à jour des rangs, snapshot, fermeture de la ronde si terminé
        3) Affichage, sauvegarde et attente utilisateur
        """
        name_lower = self.match.name.lower()
        is_bye = "repos" in name_lower

        # 1) Déterminer et appliquer le score
        if is_bye:
            if not self.match.player_1:
                RoundView.show_error(
                    "Impossible d'identifier le joueur de repos pour ce match."
                )
                return
            if self.match.match_score_1 is None:
                self._apply_and_rank(DRAW_POINT)
            else:
                self._rank_and_snapshot()
        else:
            choice = MatchView.ask_match_result(self.match)
            self._apply_and_rank(choice)

        # 2) Affichage, sauvegarde, attente
        self._show_and_save_results()
        self._wait_for_user()

    def _apply_and_rank(self, score: float) -> None:
        """
        Applique le résultat, met à jour les rangs et prend un snapshot.
        """
        self.match.apply_result(score)
        self._rank_and_snapshot()

    def _rank_and_snapshot(self) -> None:
        """
        Met à jour les rangs de tous les joueurs et prend le snapshot du match.
        """
        if self.tournament:
            update_ranks(self.tournament)
        self.match.snapshot()

    def _show_and_save_results(self) -> None:
        """
        Affiche les résultats du match et sauvegarde le tournoi.
        """
        MatchView.show_match_results(self.match)
        if self.tournament and self.filename:
            save_tournament_to_json(
                self.tournament.get_serialized_tournament(),
                TOURNAMENTS_FOLDER, self.filename
            )

    def _wait_for_user(self) -> None:
        """
        Attend que l'utilisateur appuie sur Entrée pour continuer.
        """
        wait_for_enter_continue()
