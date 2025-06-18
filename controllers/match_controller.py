from typing import Optional

from config import DRAW_POINT, TOURNAMENTS_FOLDER, ENTER_FOR_CONTINUE
from models.match_model import Match
from models.round_model import Round
from models.tournament_model import Tournament
from storage.tournament_data import save_tournament_to_json
from utils.console import wait_for_enter
from utils.update_ranks import update_ranks
from views.match_view import MatchView
from views.round_view import RoundView


class MatchController:
    @staticmethod
    def run(
        match: Match,
        current_round: Round,
        tournament: Optional[Tournament] = None,
        filename: str = None
    ) -> None:
        """
        Orchestrates a single match within a round:
        1) Updates live rankings and displays round banner
        2) Applies result (auto-assigns a draw for byes or prompts user)
        3) Finalizes match: shows result, updates snapshots/rankings, persists state,
           and waits for user confirmation.

        Args:
            match:      The Match instance to play.
            current_round: The Round containing the match.
            tournament: Optional Tournament for ranking and persistence.
            filename:   Optional JSON filename for saving tournament.
        """
        # 1) Pre-match setup
        MatchController._before_match(current_round, tournament)

        name_lower = match.name.lower()
        is_bye = "repos" in name_lower

        # 2) Determine and apply result
        if is_bye:
            if not match.player_1:
                RoundView.show_error("Impossible d'identifier le joueur de repos pour ce match.")
                return
            if match.match_score_1 is None:
                MatchController._apply_and_rank(match, DRAW_POINT, tournament)
            else:
                MatchController._rank_and_snapshot(match, tournament)
        else:
            choice = MatchView.ask_match_result(match)
            MatchController._apply_and_rank(match, choice, tournament)

        # Intermediate snapshot
        match.snapshot()

        # 3) Post-match finalization
        MatchController._finalize_match(match, current_round, tournament, filename)

    @staticmethod
    def _before_match(
        current_round: Round,
        tournament: Optional[Tournament] = None
    ) -> None:
        """
        Updates player rankings, refreshes existing snapshots, and displays
        the start-of-round banner before playing the provided match.

        Args:
            current_round: The Round before which to display the banner.
            tournament:    Optional Tournament for live ranking updates.
        """
        if tournament:
            update_ranks(tournament)
        MatchController._refresh_match_snapshots(current_round, tournament)
        RoundView.show_start_round(current_round)

    @staticmethod
    def _refresh_match_snapshots(
        current_round: Round,
        tournament: Optional[Tournament] = None
    ) -> None:
        """
        Updates the 'rank' fields of any existing snapshots for matches
        already played in the current round.

        Args:
            current_round: The Round whose matches to refresh.
            tournament:    Optional Tournament providing updated ranks.
        """
        if not tournament:
            return
        for m in current_round.matches:
            if hasattr(m, "_snap1") and m._snap1:
                pid1 = m._snap1["id_national_chess"]
                new_rank1 = next(
                    (p.rank for p in tournament.list_of_players
                     if p.id_national_chess == pid1),
                    None
                )
                if new_rank1 is not None:
                    m._snap1["rank"] = new_rank1
            if hasattr(m, "_snap2") and m._snap2:
                pid2 = m._snap2["id_national_chess"]
                new_rank2 = next(
                    (p.rank for p in tournament.list_of_players
                     if p.id_national_chess == pid2),
                    None
                )
                if new_rank2 is not None:
                    m._snap2["rank"] = new_rank2

    @staticmethod
    def _apply_and_rank(
        match: Match,
        score: float,
        tournament: Optional[Tournament] = None
    ) -> None:
        """
        Applies the given score to the match, updates rankings,
        and takes a fresh snapshot.

        Args:
            match:      The Match to update.
            score:      Score to assign to player 1 (mirror applies).
            tournament: Optional Tournament for live rank updates.
        """
        match.apply_result(score)
        MatchController._rank_and_snapshot(match, tournament)

    @staticmethod
    def _rank_and_snapshot(
        match: Match,
        tournament: Optional[Tournament] = None
    ) -> None:
        """
        Updates player rankings (if a tournament is provided) and captures
        a snapshot of the match state.

        Args:
            match:      The Match to snapshot.
            tournament: Optional Tournament for ranking update.
        """
        if tournament:
            update_ranks(tournament)
        match.snapshot()

    @staticmethod
    def _show_and_save_results(
        match: Match,
        tournament: Optional[Tournament] = None,
        filename: str = None
    ) -> None:
        """
        Displays the final result of the match and saves the tournament state.

        Args:
            match:      The Match whose results to display.
            tournament: Optional Tournament to persist.
            filename:   JSON filename for saving.
        """
        MatchView.show_match_results(match)
        if tournament and filename:
            save_tournament_to_json(
                tournament.get_serialized_tournament(),
                TOURNAMENTS_FOLDER,
                filename
            )

    @staticmethod
    def _finalize_match(
        match: Match,
        current_round: Round,
        tournament: Optional[Tournament] = None,
        filename: str = None
    ) -> None:
        """
        After a match completes (or a bye):
         1) Show results and save tournament once
         2) Recompute live rankings
         3) Refresh all snapshots for the current round
         4) Save tournament again to include updated ranks
         5) Wait for user to press Enter

        Args:
            match:        The Match just played.
            current_round: The Round containing the match.
            tournament:   Optional Tournament for rank updates and persistence.
            filename:     JSON filename for saving.
        """
        MatchController._show_and_save_results(match, tournament, filename)
        if tournament:
            update_ranks(tournament)
            MatchController._refresh_match_snapshots(current_round, tournament)
            if filename:
                save_tournament_to_json(
                    tournament.get_serialized_tournament(),
                    TOURNAMENTS_FOLDER,
                    filename
                )
        wait_for_enter(ENTER_FOR_CONTINUE)
