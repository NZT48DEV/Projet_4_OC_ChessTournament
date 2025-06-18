from __future__ import annotations
import os
import datetime
from typing import Any, Dict, List, Tuple

from config import (
    TODAY,
    MIN_PLAYERS,
    TOURNAMENTS_FOLDER,
    PLAYERS_FOLDER,
    ENTER_FOR_CONTINUE,
    SWISS_MAX_PLAYERS_BASE
)
from controllers.round_controller import RoundController
from models.match_model import Match
from models.player_model import Player
from models.round_model import Round
from models.tournament_model import Tournament
from storage.player_data import load_player_from_json
from storage.tournament_data import save_tournament_to_json
from utils.input_manager import get_valid_input
from utils.console import clear_screen, wait_for_enter
from utils.error_messages import invalid_yes_no
from utils.input_formatters import format_yes_no
from utils.input_validators import is_valid_yes_no
from views.tournament_view import TournamentView


class TournamentController:
    @staticmethod
    def run() -> None:
        """
        Point d'entrée unique pour la création d'un tournoi.
        """
        TournamentController.start_new()

    @staticmethod
    def start_new() -> None:
        """
        Crée un nouveau tournoi, collecte les informations, inscrit les joueurs,
        confirme le démarrage et lance la séquence de rounds.
        """
        t, filename = TournamentController._create_and_save_new()
        TournamentController._collect_basic_info(t, filename)
        TournamentController._register_players(t, filename)
        if not TournamentController._confirm_start():
            return
        RoundController.run(t, filename)

    @staticmethod
    def _create_and_save_new() -> Tuple[Tournament, str]:
        """
        Demande le nom du tournoi, génère un nom de fichier unique,
        initialise l'objet Tournament et sauvegarde l'état initial.

        Returns:
            Tuple contenant l'objet Tournament et le nom du fichier JSON.
        """
        name = TournamentView.ask_tournament_name()
        safe = name.strip().replace(' ', '_')
        filename = f"{safe}_{TODAY}.json"
        counter = 2
        while os.path.exists(os.path.join(TOURNAMENTS_FOLDER, filename)):
            filename = f"{safe}_{TODAY}_{counter}.json"
            counter += 1
        t = Tournament(
            tournament_name=name,
            location=None,
            start_date=None,
            end_date=None,
            number_of_rounds=None,
            description=None,
            list_of_players=[],
            list_of_rounds=[],
            actual_round=0
        )
        save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)
        return t, filename

    @staticmethod
    def _collect_basic_info(t: Tournament, filename: str) -> None:
        """
        Demande successivement les champs : lieu, dates, nombre de rounds,
        description, et sauvegarde après chaque saisie.

        Args:
            t: Objet Tournament à compléter.
            filename: Nom du fichier pour la sauvegarde JSON.
        """
        for attr, view_fn in [
            ('location', TournamentView.ask_location),
            ('start_date', TournamentView.ask_start_date),
            ('end_date', lambda: TournamentView.ask_end_date(t.start_date)),
            ('number_of_rounds', TournamentView.ask_number_of_rounds),
            ('description', lambda: TournamentView.ask_description(allow_empty=True))
        ]:
            clear_screen()
            setattr(t, attr, view_fn())
            save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

    @staticmethod
    def _confirm_start() -> bool:
        """
        Demande confirmation à l'utilisateur pour démarrer le tournoi.

        Returns:
            True si l'utilisateur répond "Y", False sinon.
        """
        clear_screen()
        choix = get_valid_input(
            prompt="\nVoulez-vous démarrer le tournoi maintenant ? (Y/N) : ",
            formatter=format_yes_no,
            validator=is_valid_yes_no,
            message_error=invalid_yes_no
        )
        return choix == 'Y'

    @staticmethod
    def _register_players(t: Tournament, filename: str) -> None:
        """
        Inscrit les joueurs en deux phases :
        Phase 1 jusqu'au nombre minimum, Phase 2 optionnelle jusqu'au maximum.
        Conserve les joueurs déjà présents.

        Args:
            t: Objet Tournament contenant la liste des joueurs.
            filename: Nom du fichier JSON pour la sauvegarde.
        """
        limit = SWISS_MAX_PLAYERS_BASE ** t.number_of_rounds
        players: List[Player] = list(t.list_of_players)
        # Phase 1: atteindre au moins MIN_PLAYERS
        while len(players) < MIN_PLAYERS:
            clear_screen()
            TournamentView.show_player_list_header(players)
            p = TournamentController._ask_unique(players, len(players) + 1, limit)
            players.append(p)
            t.list_of_players = players
            save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)
        # Phase 2: ajout optionnel
        while True:
            clear_screen()
            TournamentView.show_player_list_header(players)
            if len(players) >= limit:
                TournamentView.show_error(f"Nombre maximal atteint ({limit}).")
                wait_for_enter(ENTER_FOR_CONTINUE)
                break
            choix = get_valid_input(
                prompt=f"\nAjouter joueur ({len(players)}/{limit}) ? (Y/N): ",
                formatter=format_yes_no,
                validator=is_valid_yes_no,
                message_error=invalid_yes_no
            )
            if choix != 'Y':
                break
            p = TournamentController._ask_unique(players, len(players) + 1, limit)
            players.append(p)
            t.list_of_players = players
            save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

    @staticmethod
    def _ask_unique(existing: List[Player], idx: int, limit: int) -> Player:
        """
        Lance la saisie d'un joueur et garantit l'unicité de son ID.

        Args:
            existing: Liste des joueurs déjà inscrits.
            idx: Position d'affichage pour la saisie.
            limit: Nombre maximum de joueurs autorisés.

        Returns:
            Le nouvel objet Player valide.
        """
        while True:
            p = TournamentView.register_one_player(idx, limit)
            if p.id_national_chess in {e.id_national_chess for e in existing}:
                TournamentView.display_player_already_in_tournament_text(p.id_national_chess)
                wait_for_enter(ENTER_FOR_CONTINUE)
                clear_screen()
                TournamentView.show_player_list_header(existing)
                continue
            return p

    @staticmethod
    def load_existing_tournament(data: Dict[str, Any], filename: str) -> Any:
        """
        Prépare un Loader pour reprendre un tournoi existant au lieu de créer un nouveau.

        Args:
            data: Contenu JSON du tournoi.
            filename: Nom du fichier JSON.

        Returns:
            Un objet Loader exposant une méthode resume().
        """
        class Loader:
            @staticmethod
            def resume() -> None:
                TournamentController._resume_existing(data, filename)
        return Loader

    @staticmethod
    def _resume_existing(data: Dict[str, Any], filename: str) -> None:
        """
        Reprend un tournoi existant :
         1) Reconstruction du modèle
         2) Complétion des champs manquants
         3) Proposition d'ajout de joueurs avant le premier round
         4) Lancement ou reprise des rounds

        Args:
            data: Dictionnaire des données JSON.
            filename: Nom du fichier JSON.
        """
        t = TournamentController._build_from_data(data)
        TournamentController._complete_missing_fields(t, filename)
        if t.actual_round == 0:
            if not TournamentController._before_first_round(t, filename):
                return
        RoundController.run(t, filename)

    @staticmethod
    def _build_from_data(data: Dict[str, Any]) -> Tournament:
        """
        Reconstruit un objet Tournament complet depuis les données JSON.

        Args:
            data: Dictionnaire du JSON chargé.

        Returns:
            Instance de Tournament.
        """
        t = Tournament(
            tournament_name=data['tournament_name'],
            location=data.get('location'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            number_of_rounds=data.get('number_of_rounds'),
            description=data.get('description'),
            list_of_players=[],
            list_of_rounds=[],
            actual_round=data.get('actual_round', 0)
        )
        for p_data in data.get('list_of_players', []):
            try:
                player = load_player_from_json(PLAYERS_FOLDER, p_data['id_national_chess'])
            except FileNotFoundError:
                player = Player(
                    id_national_chess=p_data['id_national_chess'],
                    first_name=None,
                    last_name=None,
                    date_of_birth=p_data.get('date_of_birth'),
                    tournament_score=p_data.get('tournament_score', 0.0),
                    rank=p_data.get('rank', 0),
                    played_with=p_data.get('played_with', [])
                )
            else:
                player.tournament_score = p_data.get('tournament_score', 0.0)
                player.rank = p_data.get('rank', 0)
                player.played_with = p_data.get('played_with', [])
            t.list_of_players.append(player)
        for r_data in data.get('list_of_rounds', []):
            rnd = Round(r_data['round_number'])
            if r_data.get('start_time'):
                rnd.start_time = datetime.datetime.strptime(r_data['start_time'], '%d/%m/%Y %H:%M:%S')
            if r_data.get('end_time'):
                rnd.end_time = datetime.datetime.strptime(r_data['end_time'], '%d/%m/%Y %H:%M:%S')
            for m_data in r_data.get('matches', []):
                name = m_data['name']
                if 'repos' in name.lower():
                    pid = m_data['player_1']['id_national_chess']
                    p = next(x for x in t.list_of_players if x.id_national_chess == pid)
                    match = Match(name, (p, None))
                    match._snap1 = m_data['player_1'].copy()
                    match.match_score_1 = match._snap1['match_score']
                    match.color_player_1 = match._snap1.get('color')
                    match._snap2 = None
                else:
                    p1 = next(
                        x for x in t.list_of_players if
                        x.id_national_chess == m_data['player_1']['id_national_chess'])
                    p2 = next(
                        x for x in t.list_of_players if
                        x.id_national_chess == m_data['player_2']['id_national_chess'])
                    match = Match(name, (p1, p2))
                    match._snap1 = m_data['player_1'].copy()
                    match._snap2 = m_data['player_2'].copy()
                    match.match_score_1 = m_data['player_1']['match_score']
                    match.match_score_2 = m_data['player_2']['match_score']
                    match.color_player_1 = m_data['player_1'].get('color')
                    match.color_player_2 = m_data['player_2'].get('color')
                rnd.matches.append(match)
            t.list_of_rounds.append(rnd)
        return t

    @staticmethod
    def _complete_missing_fields(t: Tournament, filename: str) -> None:
        """
        Complète les champs manquants du tournoi rechargé et sauvegarde.

        Args:
            t: Objet Tournament à compléter.
            filename: Nom du fichier JSON pour la sauvegarde.
        """
        missing = []
        if not t.location:
            missing.append('location')
        if not t.start_date:
            missing.append('start_date')
        if not t.end_date:
            missing.append('end_date')
        if t.number_of_rounds is None:
            missing.append('number_of_rounds')
        if t.description is None:
            missing.append('description')
        if not missing:
            return
        clear_screen()
        TournamentView.display_tournament_incomplete(t)
        wait_for_enter(ENTER_FOR_CONTINUE)
        for f in missing:
            if f == 'location':
                t.location = TournamentView.ask_location()
            elif f == 'start_date':
                t.start_date = TournamentView.ask_start_date()
            elif f == 'end_date':
                t.end_date = TournamentView.ask_end_date(t.start_date)
            elif f == 'number_of_rounds':
                t.number_of_rounds = TournamentView.ask_number_of_rounds()
            elif f == 'description':
                t.description = TournamentView.ask_description(allow_empty=True)
            save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

    @staticmethod
    def _before_first_round(t: Tournament, filename: str) -> None:
        """
        Avant le premier round, propose d'ajouter des joueurs si nécessaire,
        puis confirme le lancement.

        Args:
            t: Objet Tournament à préparer.
            filename: Nom du fichier JSON pour la sauvegarde.
        """
        clear_screen()
        TournamentView.show_player_list_header(t.list_of_players)
        if len(t.list_of_players) < MIN_PLAYERS:
            TournamentController._register_players(t, filename)
        else:
            TournamentController._register_players(t, filename)
        clear_screen()
        start = get_valid_input(
            prompt="\nVoulez-vous démarrer le tournoi maintenant ? (Y/N) : ",
            formatter=format_yes_no,
            validator=is_valid_yes_no,
            message_error=invalid_yes_no
        )
        if start != 'Y':
            return False
        return True
