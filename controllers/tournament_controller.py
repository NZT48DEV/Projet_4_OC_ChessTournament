from __future__ import annotations
import os
import datetime

from config import (
    TODAY,
    MIN_PLAYERS,
    TOURNAMENTS_FOLDER,
    PLAYERS_FOLDER,
    ENTER_FOR_CONTINUE,
    ENTER_FOR_MAIN_MENU,
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
    """
    Contrôleur principal pour la gestion d'un tournoi :
      - Création et édition d'un nouveau tournoi
      - Chargement et reprise d'un tournoi existant
      - Inscription des joueurs
      - Lancement et reprise des rounds
    """

    def __init__(self, filename: str = None):
        """
        Initialise le controller.

        Args:
            filename: nom du fichier JSON si on recharge un tournoi existant.
        """
        self.tournament: Tournament | None = None
        self.filename: str | None = filename
        self._raw_data: dict | None = None

    def _save_progress(self) -> None:
        """
        Sauvegarde l'état courant du tournoi dans un fichier JSON.
        """
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename,
        )

    def run(self) -> None:
        """
        Lance le processus de création d’un nouveau tournoi :
          1) Création du tournoi et collecte des infos de base
          2) Inscription des joueurs (phase 1 puis phase 2)
          3) Confirmation de démarrage
          4) Démarrage des rounds
        """
        self._create_empty_tournament()
        self._collect_basic_info()
        self._register_players_phase1()
        self._register_players_phase2()

        if not self._ask_to_start():
            return

        self._start_rounds()

    def _create_empty_tournament(self) -> None:
        """
        Demande à l’utilisateur le nom du tournoi, génère un filename unique
        (ajoute _2, _3… s’il existe déjà), initialise l’objet Tournament et le sauvegarde.
        """
        name = TournamentView.ask_tournament_name()
        safe_name = name.strip().replace(" ", "_")
        base = f"{safe_name}_{TODAY}"
        filename = f"{base}.json"
        counter = 2
        while os.path.exists(os.path.join(TOURNAMENTS_FOLDER, filename)):
            filename = f"{base}_{counter}.json"
            counter += 1

        self.filename = filename
        self.tournament = Tournament(
            tournament_name=name,
            location=None,
            start_date=None,
            end_date=None,
            number_of_rounds=None,
            description=None,
            list_of_players=[],
            list_of_rounds=[],
            actual_round=0,
        )
        self._save_progress()

    def _collect_basic_info(self) -> None:
        """
        Demande successivement :
          - le lieu du tournoi
          - la date de début
          - la date de fin
          - le nombre de rounds
          - la description (optionnelle)
        Et sauvegarde après chaque saisie.
        """
        t = self.tournament
        t.location = TournamentView.ask_location()
        self._save_progress()
        t.start_date = TournamentView.ask_start_date()
        self._save_progress()
        t.end_date = TournamentView.ask_end_date(t.start_date)
        self._save_progress()
        t.number_of_rounds = TournamentView.ask_number_of_rounds()
        self._save_progress()
        t.description = TournamentView.ask_description(allow_empty=True)
        self._save_progress()

    def _register_players_phase1(self) -> None:
        """
        Inscription forcée des joueurs jusqu'au seuil MIN_PLAYERS,
        sans proposer de quitter.
        """
        t = self.tournament
        limit = SWISS_MAX_PLAYERS_BASE ** t.number_of_rounds
        players: list[Player] = []
        count = 0

        while count < MIN_PLAYERS:
            clear_screen()
            TournamentView.show_player_list_header(players)
            new_player = self._ask_unique_player(players, count + 1, limit)
            players.append(new_player)
            count += 1
            t.list_of_players = players
            self._save_progress()

    def _register_players_phase2(self) -> None:
        """
        Propose à l’utilisateur d’ajouter des joueurs jusqu’au maximum autorisé.
        Peut être quitté dès que l’on le souhaite.
        """
        t = self.tournament
        limit = SWISS_MAX_PLAYERS_BASE ** t.number_of_rounds
        players = t.list_of_players

        while True:
            clear_screen()
            TournamentView.show_player_list_header(players)
            count = len(players)
            if count >= limit:
                print()
                TournamentView.show_error(f"Nombre maximal de joueurs atteint ({limit}).")
                wait_for_enter(ENTER_FOR_CONTINUE)
                break

            choix = get_valid_input(
                prompt=f"\nVoulez-vous ajouter un joueur ({count} / {limit}) ? (Y/N) : ",
                formatter=format_yes_no,
                validator=is_valid_yes_no,
                message_error=invalid_yes_no,
            )

            if choix == "Y":
                clear_screen()
                TournamentView.show_player_list_header(players)
                new_player = self._ask_unique_player(players, count + 1, limit)
                players.append(new_player)
                t.list_of_players = players
                self._save_progress()
            elif count < 2:
                clear_screen()
                TournamentView.show_error(
                    f"Pas assez de joueurs pour démarrer le tournoi (minimum : {MIN_PLAYERS} joueur(s)).\n"
                    f"Veuillez ajouter au minimum {MIN_PLAYERS - count} joueur(s).")
                print()
                wait_for_enter(ENTER_FOR_CONTINUE)
            else:
                break

    def _ask_unique_player(self, existing: list[Player], idx: int, limit: int) -> Player:
        """
        Lance la saisie d’un joueur et vérifie l’unicité de son ID.

        Args:
            existing: liste des joueurs déjà inscrits.
            idx: numéro d’ordre pour l’affichage du formulaire.
            limit: nombre maximal de joueurs.
        Returns:
            L’objet Player créé.
        """
        while True:
            player = TournamentView.register_one_player(idx, limit)
            if player.id_national_chess in {p.id_national_chess for p in existing}:
                TournamentView.display_player_already_in_tournament_text(player.id_national_chess)
                wait_for_enter(ENTER_FOR_CONTINUE)
                clear_screen()
                TournamentView.show_player_list_header(existing)
                continue
            return player

    def _ask_to_start(self) -> bool:
        """
        Demande si l’on démarre le tournoi.

        Returns:
            True si l’utilisateur répond 'Y', False sinon.
        """
        clear_screen()
        choix = get_valid_input(
            prompt="\nVoulez-vous démarrer le tournoi maintenant ? (Y/N) : ",
            formatter=format_yes_no,
            validator=is_valid_yes_no,
            message_error=invalid_yes_no
        )
        return (choix == "Y")

    def _start_rounds(self) -> None:
        """
        Vérifie qu’il y a au moins MIN_PLAYERS et lance la boucle de rounds.
        """
        if len(self.tournament.list_of_players) >= MIN_PLAYERS:
            RoundController(self.tournament, self.filename).run()
        else:
            clear_screen()
            TournamentView.show_error(
                "Pas assez de joueurs pour démarrer le tournoi"
                f" (minimum : {MIN_PLAYERS} joueur(s)).")
            wait_for_enter(ENTER_FOR_MAIN_MENU)

    @staticmethod
    def load_existing_tournament(data: dict, filename: str) -> TournamentController:
        """
        Reconstruit un TournamentController à partir du JSON existant.

        Args:
            data: contenu chargé du JSON.
            filename: nom du fichier original.
        Returns:
            Un controller prêt à reprendre le tournoi.
        """
        tc = TournamentController(filename=filename)
        tc._raw_data = data
        t = Tournament(
            tournament_name=data["tournament_name"],
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            number_of_rounds=data.get("number_of_rounds"),
            description=data.get("description"),
            list_of_players=[],
            list_of_rounds=[],
            actual_round=data.get("actual_round", 0),
        )
        tc.tournament = t

        TournamentController._load_players_and_rounds(data, tc)
        return tc

    @staticmethod
    def _fill_missing_fields(data: dict, tc: TournamentController) -> None:
        """
        Pour un tournoi rechargé, demande les champs manquants parmi
        location, dates, nombre de rounds, description.
        """
        t = tc.tournament
        missing = []
        if not t.location:
            missing.append("location")
        if not t.start_date:
            missing.append("start_date")
        if not t.end_date:
            missing.append("end_date")
        if t.number_of_rounds is None:
            missing.append("number_of_rounds")
        if t.description is None:
            missing.append("description")
        if not missing:
            return

        clear_screen()
        TournamentView.display_tournament_incomplete(t)
        wait_for_enter(ENTER_FOR_CONTINUE)

        for field in missing:
            if field == "location":
                t.location = TournamentView.ask_location()
            elif field == "start_date":
                t.start_date = TournamentView.ask_start_date()
            elif field == "end_date":
                t.end_date = TournamentView.ask_end_date(t.start_date)
            elif field == "number_of_rounds":
                t.number_of_rounds = TournamentView.ask_number_of_rounds()
            elif field == "description":
                t.description = TournamentView.ask_description(allow_empty=True)
            save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, tc.filename)

    @staticmethod
    def _load_players_and_rounds(data: dict, tc: TournamentController) -> None:
        """
        Reconstruit les joueurs et les rounds à partir des données JSON.
        """
        t = tc.tournament
        players_map = TournamentController._load_players(data, t)
        rounds_data = data.get("list_of_rounds", [])
        for r_data in rounds_data:
            rnd = TournamentController._load_round(r_data, players_map)
            t.list_of_rounds.append(rnd)

    @staticmethod
    def _load_players(data: dict, tournament: Tournament) -> dict[str, Player]:
        """
        Reconstruit la liste des joueurs depuis le JSON et les ajoute au tournoi.

        Args:
            data: dictionnaire contenant les données JSON du tournoi.
            tournament: instance du tournoi à remplir.

        Returns:
            Un dictionnaire associant chaque ID national à un objet Player.
        """
        players_map = {}
        for p_data in data.get("list_of_players", []):
            idn = p_data["id_national_chess"]
            try:
                player = load_player_from_json(PLAYERS_FOLDER, idn)
            except FileNotFoundError:
                player = Player(
                    id_national_chess=idn,
                    first_name=None,
                    last_name=None,
                    date_of_birth=p_data.get("date_of_birth"),
                    tournament_score=p_data.get("tournament_score", 0.0),
                    rank=p_data.get("rank", 0),
                    played_with=p_data.get("played_with", []),
                )
            else:
                player.tournament_score = p_data.get("tournament_score", 0.0)
                player.rank = p_data.get("rank", 0)
                player.played_with = p_data.get("played_with", [])
            players_map[idn] = player
            tournament.list_of_players.append(player)
        return players_map

    @staticmethod
    def _load_round(r_data: dict, players_map: dict[str, Player]) -> Round:
        """
        Reconstruit un round et ses matchs depuis les données JSON.

        Args:
            r_data: dictionnaire contenant les données du round.
            players_map: dictionnaire des joueurs indexé par ID national.

        Returns:
            Un objet Round reconstruit avec ses matchs.
        """
        rnd = Round(r_data["round_number"])
        if r_data.get("start_time"):
            rnd.start_time = datetime.datetime.strptime(r_data["start_time"], "%d/%m/%Y %H:%M:%S")
        if r_data.get("end_time"):
            rnd.end_time = datetime.datetime.strptime(r_data["end_time"], "%d/%m/%Y %H:%M:%S")

        for m_data in r_data.get("matches", []):
            match = TournamentController._load_match(m_data, players_map)
            rnd.matches.append(match)

        return rnd

    @staticmethod
    def _load_match(m_data: dict, players_map: dict[str, Player]) -> Match:
        """
        Reconstruit un match depuis les données JSON.

        Args:
            m_data: dictionnaire contenant les données du match.
            players_map: dictionnaire des joueurs indexé par ID national.

        Returns:
            Un objet Match reconstruit.
        """
        name = m_data["name"]
        if "repos" in name.lower():
            bye_id = m_data["player_1"]["id_national_chess"]
            player = players_map.get(bye_id)
            match = Match(name, (player, None))
            match._snap1 = m_data["player_1"].copy()
            match.match_score_1 = match._snap1["match_score"]
            match.color_player_1 = match._snap1.get("color")
            match._snap2 = None
        else:
            p1 = players_map[m_data["player_1"]["id_national_chess"]]
            p2 = players_map[m_data["player_2"]["id_national_chess"]]
            match = Match(name, (p1, p2))
            match._snap1 = m_data["player_1"].copy()
            match._snap2 = m_data["player_2"].copy()
            match.match_score_1 = m_data["player_1"]["match_score"]
            match.match_score_2 = m_data["player_2"]["match_score"]
            match.color_player_1 = m_data["player_1"].get("color")
            match.color_player_2 = m_data["player_2"].get("color")
        return match

    def resume(self) -> None:
        """
        Reprend un tournoi existant en fonction de son état :
        - Si aucun round n’a commencé : collecte ou complète les infos, puis démarre.
        - Si un round est en cours : reprend à partir du bon round.
        - Si le tournoi est terminé : affiche le récapitulatif.
        """
        t = self.tournament
        if t.actual_round == 0:
            self._resume_before_first_round()
        elif 1 <= t.actual_round < t.number_of_rounds:
            self._resume_ongoing_round()
        elif t.actual_round == t.number_of_rounds:
            self._resume_after_last_round()

    def _resume_before_first_round(self) -> None:
        """
        Reprend la configuration du tournoi si aucun round n’a encore démarré :
        vérifie les champs, permet d’inscrire les joueurs, puis propose de démarrer.
        """
        t = self.tournament
        if self._raw_data:
            TournamentController._fill_missing_fields(self._raw_data, self)

        if not t.list_of_players:
            self._register_players_phase1()
            self._register_players_phase2()
            if not self._ask_to_start():
                return
        else:
            clear_screen()
            self._register_players_phase2()
            if not self._ask_to_start():
                return

        RoundController(t, self.filename).run()

    def _resume_ongoing_round(self) -> None:
        """
        Reprend un tournoi en cours entre deux rounds.
        Incrémente si le round précédent est terminé, puis lance le round suivant.
        """
        t = self.tournament
        current = t.list_of_rounds[t.actual_round - 1]
        if current.end_time is not None:
            t.actual_round += 1
            self._save_progress()
        RoundController(t, self.filename).start_from_round(t.actual_round)

    def _resume_after_last_round(self) -> None:
        """
        Reprend un tournoi terminé (ou dont le dernier round est en cours).
        Si le dernier round est fini, affiche le récapitulatif.
        Sinon, propose de le compléter.
        """
        t = self.tournament
        last = t.list_of_rounds[-1]
        if last.end_time is not None:
            TournamentView.show_tournament_summary(t)
            wait_for_enter(ENTER_FOR_MAIN_MENU)
        else:
            RoundController(t, self.filename).start_from_round(t.actual_round)
