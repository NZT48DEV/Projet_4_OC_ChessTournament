from typing                     import Optional

from config                     import DRAW_POINT, TOURNAMENTS_FOLDER, ENTER_FOR_CONTINUE 
from models.match_model         import Match
from models.round_model         import Round
from models.tournament_model    import Tournament
from storage.tournament_data    import save_tournament_to_json
from utils.console              import wait_for_enter
from utils.update_ranks         import update_ranks
from views.match_view           import MatchView
from views.round_view           import RoundView


class MatchController:
    tournament: Optional[Tournament]

    def __init__(
        self,
        match: Match,
        current_round: Round,
        tournament: Optional[Tournament] = None,
        filename: str = None
    ) -> None:
        """
        - match        : l'objet Match à exécuter
        - current_round: l'objet Round contenant ce match (pour rafraîchir les snapshots)
        - tournament   : l'objet Tournament (nécessaire pour update_ranks)
        - filename     : nom du fichier JSON du tournoi (pour save_tournament_to_json)
        """
        self.match = match
        self.current_round = current_round
        self.tournament = tournament
        self.filename = filename

    def run(self) -> None:
        """
        Orchestration d'un match :
        1) Classement live & bandeau
        2) Application du score (bye = DRAW_POINT ou choix utilisateur)
        3) Finalisation (affichage, rangs, snapshots, sauvegardes, attente)
        """
        # 1) Avant le match : mise à jour des rangs et bandeau
        self._before_match()

        name_lower = self.match.name.lower()
        is_bye = "repos" in name_lower

        # 2) Détermination et application du résultat
        if is_bye:
            if not self.match.player_1:
                RoundView.show_error("Impossible d'identifier le joueur de repos pour ce match.")
                return
            if self.match.match_score_1 is None:
                self._apply_and_rank(DRAW_POINT)
            else:
                self._rank_and_snapshot()
        else:
            choice = MatchView.ask_match_result(self.match)
            self._apply_and_rank(choice)

        # 3) Finalisation
        self._finalize_match()

    def _before_match(self) -> None:
        """
        Met à jour le classement, rafraîchit les snapshots
        et affiche le bandeau du round avant d'exécuter CE match.
        """
        if self.tournament:
            update_ranks(self.tournament)
        self._refresh_match_snapshots()
        RoundView.show_start_round(self.current_round)

    def _refresh_match_snapshots(self) -> None:
        """
        Met à jour les champs 'rank' des snapshots des
        matchs déjà joués dans self.current_round.
        """
        if not self.tournament:
            return
        for m in self.current_round.matches:
            if hasattr(m, "_snap1") and m._snap1:
                pid1 = m._snap1["id_national_chess"]
                new_rank1 = next(
                    (p.rank for p in self.tournament.list_of_players
                     if p.id_national_chess == pid1),
                    None
                )
                if new_rank1 is not None:
                    m._snap1["rank"] = new_rank1
            if hasattr(m, "_snap2") and m._snap2:
                pid2 = m._snap2["id_national_chess"]
                new_rank2 = next(
                    (p.rank for p in self.tournament.list_of_players
                     if p.id_national_chess == pid2),
                    None
                )
                if new_rank2 is not None:
                    m._snap2["rank"] = new_rank2

    def _apply_and_rank(self, score: float) -> None:
        """
        Applique le résultat sur le match, met à jour les rangs
        et prend un snapshot.
        """
        self.match.apply_result(score)
        self._rank_and_snapshot()

    def _rank_and_snapshot(self) -> None:
        """
        Met à jour les rangs de tous les joueurs puis prend le snapshot du match.
        """
        if self.tournament:
            update_ranks(self.tournament)
        self.match.snapshot()

    def _show_and_save_results(self) -> None:
        """
        Affiche le résultat du match et sauvegarde l'état actuel du tournoi.
        """
        MatchView.show_match_results(self.match)
        if self.tournament and self.filename:
            save_tournament_to_json(
                self.tournament.get_serialized_tournament(),
                TOURNAMENTS_FOLDER,
                self.filename
            )

    def _finalize_match(self) -> None:
        """
        Après un match (ou un bye) :
         1) Affiche et sauve le tournoi
         2) Recalcule les rangs live
         3) Rafraîchit tous les snapshots de la ronde
         4) Sauve à nouveau pour inclure les rangs à jour
         5) Attend que l'utilisateur appuie sur Entrée
        """
        # Affichage + première sauvegarde
        self._show_and_save_results()

        if self.tournament:
            # Recalcul des rangs pour tous les joueurs
            update_ranks(self.tournament)

            # Rafraîchissement des snapshots sur toute la ronde
            self._refresh_match_snapshots()

            # Sauvegarde finale pour inclure les nouveaux rangs
            if self.filename:
                save_tournament_to_json(
                    self.tournament.get_serialized_tournament(),
                    TOURNAMENTS_FOLDER,
                    self.filename
                )

        wait_for_enter(ENTER_FOR_CONTINUE)
