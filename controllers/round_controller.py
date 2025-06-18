from typing import List

from config import (
    TOURNAMENTS_FOLDER,
    ENTER_FOR_MAIN_MENU,
    ENTER_FOR_CONTINUE,
    MIN_PLAYERS
)
from controllers.match_controller import MatchController
from storage.tournament_data import save_tournament_to_json
from models.match_model import Match
from models.player_model import Player
from models.round_model import Round
from models.tournament_model import Tournament
from utils.console import wait_for_enter, clear_screen
from views.round_view import RoundView
from views.tournament_view import TournamentView


class RoundController:
    @staticmethod
    def run(
        tournament: Tournament,
        filename: str
    ) -> None:
        """
        Démarre la séquence de tous les rounds d'un tournoi.

        Vérifie d'abord qu'il y a suffisamment de joueurs, affiche une erreur le cas échéant,
        puis délègue à start_from_round pour enchaîner les rounds depuis le premier.

        Args:
            tournament: L'objet Tournament en cours.
            filename: Nom du fichier JSON pour la persistance.
        """
        players: List[Player] = tournament.list_of_players
        if len(players) < MIN_PLAYERS:
            clear_screen()
            RoundView.show_error(
                f"Pas assez de joueurs pour démarrer le tournoi (minimum : {MIN_PLAYERS} joueur(s))."
            )
            print()
            wait_for_enter(ENTER_FOR_MAIN_MENU)
            return

        rounds: List[Round] = tournament.list_of_rounds or []
        num_rounds: int = tournament.number_of_rounds
        RoundController.start_from_round(
            starting_round=1,
            tournament=tournament,
            filename=filename,
            players=players,
            rounds=rounds,
            num_rounds=num_rounds
        )

    @staticmethod
    def start_from_round(
        starting_round: int,
        tournament: Tournament,
        filename: str,
        players: List[Player],
        rounds: List[Round],
        num_rounds: int
    ) -> None:
        """
        Exécute chaque round à partir d'un numéro donné.

        Parcourt les rounds existants ou les crée, exécute chaque match non encore joué,
        affiche le rapport intermédiaire et attend la validation de l'utilisateur.

        Args:
            starting_round: Numéro du round de début.
            tournament: L'objet Tournament en cours.
            filename: Nom du fichier JSON pour la sauvegarde.
            players: Liste des joueurs du tournoi.
            rounds: Liste des rounds déjà créés.
            num_rounds: Nombre total de rounds à jouer.
        """
        for rnd_num in range(starting_round, num_rounds + 1):
            rnd = RoundController._get_or_create_round(
                rnd_num, tournament, filename, players, rounds
            )

            for match in rnd.matches:
                if RoundController._is_match_completed(match):
                    continue
                RoundController._execute_match(
                    match, rnd, rnd_num, tournament, filename, rounds
                )

            RoundController._finalize_round(rnd, players)
            print()
            wait_for_enter(ENTER_FOR_CONTINUE)

        TournamentView.show_tournament_summary(tournament)
        wait_for_enter(ENTER_FOR_MAIN_MENU)

    @staticmethod
    def _get_or_create_round(
        rnd_num: int,
        tournament: Tournament,
        filename: str,
        players: List[Player],
        rounds: List[Round]
    ) -> Round:
        """
        Récupère un round existant ou en crée un nouveau.

        Si le round existe déjà dans la liste, le retourne. Sinon, génère
        un nouveau round, le sauvegarde et l'ajoute à tournament.list_of_rounds.

        Args:
            rnd_num: Numéro du round.
            tournament: L'objet Tournament en cours.
            filename: Nom du fichier JSON pour la persistance.
            players: Liste des joueurs pour la génération d'appariements.
            rounds: Liste mutable des rounds.

        Returns:
            L'objet Round correspondant au numéro.
        """
        if rnd_num <= len(rounds):
            return rounds[rnd_num - 1]

        rnd = RoundController.make_round(rnd_num, players)
        rounds.append(rnd)
        tournament.list_of_rounds = rounds
        tournament.actual_round = rnd_num
        save_tournament_to_json(
            tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            filename
        )
        return rnd

    @staticmethod
    def make_round(
        index: int,
        players: List[Player]
    ) -> Round:
        """
        Crée un nouveau round et initialise les matchs.

        - Initialise l'horodatage.
        - Génère les appariements selon la liste de joueurs.
        - Initialise les scores et snapshots des matchs créés.

        Args:
            index: Numéro du round.
            players: Liste des joueurs à apparier.

        Returns:
            Le nouvel objet Round initialisé.
        """
        rnd = Round(f"Round {index}")
        rnd.start_round()
        rnd.generate_pairings(players)

        for match in rnd.matches:
            match.assign_color()
            RoundController._initialize_match_scores(match)
            if match.player_2:
                RoundController._initialize_match_snapshots(match)
        return rnd

    @staticmethod
    def _initialize_match_scores(match: Match) -> None:
        """
        Initialise les scores et le gagnant d'un match à None.

        Args:
            match: Objet Match à initialiser.
        """
        match.match_score_1 = None
        if match.player_2:
            match.match_score_2 = None
        match.winner = None

    @staticmethod
    def _initialize_match_snapshots(match: Match) -> None:
        """
        Initialise les snapshots pour suivre l'état d'avant et d'après.

        Crée _snap1 et _snap2 contenant : id, scores, rank, couleur et history.

        Args:
            match: Objet Match à préparer.
        """
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

    @staticmethod
    def _execute_match(
        match: Match,
        rnd: Round,
        rnd_num: int,
        tournament: Tournament,
        filename: str,
        rounds: List[Round]
    ) -> None:
        """
        Lance l'orchestration d'un match et sauvegarde après.

        Utilise MatchController.run, puis vérifie si le round est terminé
        pour clôturer et persister l'état du round.

        Args:
            match: L'objet Match à jouer.
            rnd: Le Round courant.
            rnd_num: Numéro du round.
            tournament: L'objet Tournament en cours.
            filename: Nom du fichier JSON pour sauvegarde.
            rounds: Liste des rounds pour persistance.
        """
        try:
            MatchController.run(
                match, rnd, tournament, filename
            )
        finally:
            if RoundController._is_round_finished(rnd):
                rnd.end_round()
                RoundController._save_progress(
                    rnd_num, tournament, filename, rounds
                )

    @staticmethod
    def run_match(
        match: Match,
        current_round: Round,
        tournament: Tournament,
        filename: str
    ) -> None:
        """
        Wrapper simple pour appeler MatchController.run.

        Args:
            match: Objet Match à exécuter.
            current_round: Round courant.
            tournament: Objet Tournament en cours.
            filename: Nom du fichier JSON.
        """
        MatchController.run(
            match=match,
            current_round=current_round,
            tournament=tournament,
            filename=filename
        )

    @staticmethod
    def _is_match_completed(match: Match) -> bool:
        """
        Indique si un match a déjà ses scores assignés.

        Args:
            match: Objet Match à vérifier.

        Returns:
            True si match_score_1 (et 2 si présent) est non None.
        """
        if match.player_2 is None:
            return match.match_score_1 is not None
        return (
            match.match_score_1 is not None and
            match.match_score_2 is not None
        )

    @staticmethod
    def _finalize_round(rnd: Round, players: List[Player]) -> None:
        """
        Affiche le rapport du round achevé et le classement intermédiaire.

        Args:
            rnd: Round qui vient de se terminer.
            players: Liste des joueurs pour le classement.
        """
        RoundView.show_round_report(rnd)
        RoundView.show_intermediate_ranking(players)

    @staticmethod
    def _is_round_finished(rnd: Round) -> bool:
        """
        Vérifie si tous les matchs d'un round ont leurs scores renseignés.

        Args:
            rnd: Round à évaluer.

        Returns:
            True si chaque match a ses scores complétés.
        """
        return all(
            (m.match_score_1 is not None
             and (m.player_2 is None or m.match_score_2 is not None))
            for m in rnd.matches
        )

    @staticmethod
    def _save_progress(
        round_number: int,
        tournament: Tournament,
        filename: str,
        rounds: List[Round]
    ) -> None:
        """
        Sauvegarde l'état actuel du tournoi après la fin d'un round.

        Met à jour tournament.actual_round et list_of_rounds,
        puis écrit le JSON.

        Args:
            round_number: Numéro du round désormais terminé.
            tournament: Objet Tournament mis à jour.
            filename: Nom du fichier JSON pour la persistance.
            rounds: Liste des rounds à sauvegarder.
        """
        tournament.actual_round = round_number
        tournament.list_of_rounds = rounds
        save_tournament_to_json(
            tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            filename
        )
