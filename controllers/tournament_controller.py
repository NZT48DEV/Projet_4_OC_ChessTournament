# controllers/tournament_controller.py

import os
import datetime

from storage.tournament_data import save_tournament_to_json, load_tournament_from_json
from storage.player_data     import load_player_from_json

from config                      import TOURNAMENTS_FOLDER, MIN_PLAYERS, TODAY, PLAYERS_FOLDER
from views.tournament_view       import TournamentView
from views.player_view           import PlayerView
from views.round_view            import RoundView
from controllers.round_controller import RoundController

from models.tournament_model import Tournament
from models.player_model     import Player
from models.round_model      import Round
from models.match_model      import Match

from utils.input_manager    import get_valid_input
from utils.console          import clear_screen, wait_for_enter_continue
from utils.input_formatters import format_yes_no
from utils.input_validators import is_valid_yes_no
from utils.error_messages   import invalid_yes_no


class TournamentController:
    def __init__(self, filename: str = None):
        self.tournament = None
        self.filename = filename

    def _save_progress(self) -> None:
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename,
        )

    def run(self) -> None:
        """
        Création complète d’un nouveau tournoi :
        1. Saisie du nom (génération du filename).
        2. Saisie des infos de base (lieu, dates, rounds, description) + sauvegarde à chaque étape.
        3. Détermination du nombre maximal de joueurs (= number_of_rounds^2).
        - Phase 1 : tant que #joueurs < MIN_PLAYERS, on force l’ajout (sans afficher la liste vide).
        - Phase 2 : une fois au moins MIN_PLAYERS atteint, on affiche la liste et on propose Y/N jusqu’au maximum.
        - Sauvegarde immédiate après chaque ajout.
        4. Lancer tous les rounds (via RoundController.run()).
        """
        # 1. Saisie du nom et génération du filename
        name = TournamentView.ask_tournament_name()
        safe_name = name.strip().replace(" ", "_")
        self.filename = f"{safe_name}_{TODAY}.json"

        # 2. Création du modèle avec description=None
        self.tournament = Tournament(
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
        # Sauvegarde initiale
        self._save_progress()

        # 3. Compléter les champs obligatoires
        self.tournament.location = TournamentView.ask_location()
        self._save_progress()

        self.tournament.start_date = TournamentView.ask_start_date()
        self._save_progress()

        self.tournament.end_date = TournamentView.ask_end_date(self.tournament.start_date)
        self._save_progress()

        self.tournament.number_of_rounds = TournamentView.ask_number_of_rounds()
        self._save_progress()

        # Autoriser la description vide
        self.tournament.description = TournamentView.ask_description(allow_empty=True)
        self._save_progress()

        # 4. Calculer le nombre maximal de joueurs
        max_players_limit = self.tournament.number_of_rounds ** 2

        players = []
        count = 0

        # --- Phase 1 : forcer l’ajout jusqu’à MIN_PLAYERS sans liste vide ni message « Il manque… » ---
        while count < MIN_PLAYERS:
            # Formulaire d'inscription + vérification d'unicité
            while True:
                clear_screen()
                TournamentView.show_player_list_header(players)
                new_player = TournamentView.register_one_player(count + 1, max_players_limit)
                idn = new_player.id_national_chess
                existing_ids = {p.id_national_chess for p in players}
                if idn in existing_ids:
                    TournamentView.display_player_already_in_tournament_text(idn)
                    wait_for_enter_continue()
                    continue
                break

            players.append(new_player)
            count += 1
            self.tournament.list_of_players = players
            self._save_progress()

        # --- Phase 2 : on a maintenant au moins MIN_PLAYERS. Boucle « montrons la liste + Y/N » ---
        while True:
            clear_screen()
            TournamentView.show_player_list_header(players)
            count = len(players)

            # 4.b – Si on a déjà atteint le maximum autorisé
            if count >= max_players_limit:
                clear_screen()
                TournamentView.show_player_list_header(players)
                print(f"\nNombre maximal de joueurs atteint ({max_players_limit}).")
                wait_for_enter_continue()
                break

            # 4.c – Entre MIN_PLAYERS et max_players_limit, on propose Y/N
            choix = get_valid_input(
                prompt=f"\nVoulez-vous ajouter un joueur ({count} / {max_players_limit}) ? (Y/N) : ",
                formatter=format_yes_no,
                validator=is_valid_yes_no,
                message_error=invalid_yes_no
            )
            if choix == "Y":
                # Afficher la liste + [INFO], déjà fait juste au-dessus
                # Formulaire d'inscription + vérification d'unicité
                while True:
                    clear_screen()
                    TournamentView.show_player_list_header(players)
                    new_player = TournamentView.register_one_player(count + 1, max_players_limit)
                    idn = new_player.id_national_chess
                    existing_ids = {p.id_national_chess for p in players}
                    if idn in existing_ids:
                        TournamentView.display_player_already_in_tournament_text(idn)
                        wait_for_enter_continue()
                        continue
                    break

                players.append(new_player)
                count += 1
                self.tournament.list_of_players = players
                self._save_progress()
                continue
            else:
                # L’utilisateur refuse d’ajouter plus de joueurs → on sort de la boucle
                break

        # 5. Lancer tous les rounds si on a au moins MIN_PLAYERS
        if len(self.tournament.list_of_players) >= MIN_PLAYERS:
            RoundController(self.tournament, self.filename).run()
        else:
            clear_screen()
            print("Le tournoi est interrompu, pas assez de joueurs inscrits.")




    @staticmethod
    def load_existing_tournament(data: dict, filename: str) -> "TournamentController":
        """
        Charge un tournoi depuis son JSON (data) et retourne un TournamentController prêt à reprendre.
        1. Reconstruit l’instance Tournament (avec tous ses champs).
        1bis. Complète les champs manquants (location, dates, number_of_rounds, description) avant toute autre logique.
        2. Si actual_round >= 1, on ne demande pas d’ajout de joueur (tournoi en cours).
           Sinon (actual_round == 0), on parcourt la liste existante et on demande d’ajouter
           pour atteindre au moins MIN_PLAYERS et jusqu’à number_of_rounds^2.
        3. Reconstruit les rounds et les matchs.
        4. Renvoie le controller prêt pour resume().
        """
        tc = TournamentController(filename=filename)
        miss_info = ["Info manquante"]

        # 1) Reconstruire les champs simples depuis le JSON
        t = Tournament(
            tournament_name=data["tournament_name"],
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            actual_round=data.get("actual_round", 0),
            list_of_players=[],
            list_of_rounds=[],
            number_of_rounds=data.get("number_of_rounds"),
            description=data.get("description")  # None ou chaîne vide possible
        )
        tc.tournament = t

        # 1bis) Compléter les champs manquants avant toute autre logique
        missing_fields = []
        if not t.location:
            missing_fields.append("location")
        if not t.start_date:
            missing_fields.append("start_date")
        if not t.end_date:
            missing_fields.append("end_date")
        if t.number_of_rounds is None:
            missing_fields.append("number_of_rounds")
        # description peut être chaîne vide, mais s’il est None, c’est manquant
        if t.description is None:
            missing_fields.append("description")

        if missing_fields:
            clear_screen()
            TournamentView.display_tournament_incomplete(t)
            print()
            wait_for_enter_continue()

            if "location" in missing_fields:
                t.location = TournamentView.ask_location()
                save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

            if "start_date" in missing_fields:
                t.start_date = TournamentView.ask_start_date()
                save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

            if "end_date" in missing_fields:
                t.end_date = TournamentView.ask_end_date(t.start_date)
                save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

            if "number_of_rounds" in missing_fields:
                t.number_of_rounds = TournamentView.ask_number_of_rounds()
                save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

            if "description" in missing_fields:
                t.description = TournamentView.ask_description(allow_empty=True)
                save_tournament_to_json(t.get_serialized_tournament(), TOURNAMENTS_FOLDER, filename)

        # 2) Si un round a déjà commencé, on ne touche pas à la liste des joueurs
        if t.actual_round >= 1:
            players_map = {}
            for p_data in data.get("list_of_players", []):
                idn = p_data["id_national_chess"]
                try:
                    player_full = load_player_from_json(PLAYERS_FOLDER, idn)
                except FileNotFoundError:
                    player_full = Player(
                        id_national_chess=idn,
                        first_name="",
                        last_name="",
                        date_of_birth=p_data.get("date_of_birth", ""),
                        tournament_score=p_data.get("tournament_score", 0.0),
                        rank=p_data.get("rank", 0),
                        played_with=p_data.get("played_with", []),
                    )
                else:
                    player_full.tournament_score = p_data.get("tournament_score", 0.0)
                    player_full.rank = p_data.get("rank", 0)
                    player_full.played_with = p_data.get("played_with", [])
                players_map[idn] = player_full
                t.list_of_players.append(player_full)

            for r_data in data.get("list_of_rounds", []):
                rnd = Round(r_data.get("round_number", ""))
                if r_data.get("start_time"):
                    rnd.start_time = datetime.datetime.strptime(
                        r_data["start_time"], "%d/%m/%Y %H:%M:%S"
                    )
                if r_data.get("end_time"):
                    rnd.end_time = datetime.datetime.strptime(
                        r_data["end_time"], "%d/%m/%Y %H:%M:%S"
                    )

                for m_data in r_data.get("matches", []):
                    name = m_data.get("name", "")
                    name_lower = name.lower()

                    # “bye” ou match normal
                    if "repos" in name_lower:
                        bye_id = m_data.get("player_1", {}).get("id_national_chess")
                        bye_player = players_map.get(bye_id)
                        if bye_player is None:
                            rnd.matches.append(Match(name, (None, None)))
                            continue
                        match = Match(name, (bye_player, None))
                        snap1 = m_data.get("player_1", {})
                        match._snap1 = {
                            "id_national_chess": snap1.get("id_national_chess"),
                            "match_score": snap1.get("match_score", 0.5),
                            "tournament_score": snap1.get("tournament_score", bye_player.tournament_score),
                            "rank": snap1.get("rank", bye_player.rank),
                            "color": snap1.get("color", None),
                            "played_with": snap1.get("played_with", list(bye_player.played_with))
                        }
                        match.match_score_1 = match._snap1["match_score"]
                        match.color_player_1 = match._snap1["color"]
                        match._snap2 = None
                        rnd.matches.append(match)
                    else:
                        p1_data = m_data.get("player_1", {})
                        p2_data = m_data.get("player_2", {})
                        pid1 = p1_data.get("id_national_chess")
                        pid2 = p2_data.get("id_national_chess")
                        player1 = players_map.get(pid1)
                        player2 = players_map.get(pid2)
                        match = Match(name, (player1, player2))
                        match.color_player_1 = p1_data.get("color")
                        match.color_player_2 = p2_data.get("color")
                        match.match_score_1 = p1_data.get("match_score", None)
                        match.match_score_2 = p2_data.get("match_score", None)
                        match._snap1 = p1_data.copy()
                        match._snap2 = p2_data.copy()
                        rnd.matches.append(match)

                t.list_of_rounds.append(rnd)

            return tc

        # 3) Compléter la liste des joueurs si actual_round == 0
        players_map = {}
        for p_data in data.get("list_of_players", []):
            idn = p_data["id_national_chess"]
            try:
                player_full = load_player_from_json(PLAYERS_FOLDER, idn)
            except FileNotFoundError:
                player_full = Player(
                    id_national_chess=idn,
                    first_name="",
                    last_name="",
                    date_of_birth=p_data.get("date_of_birth", ""),
                    tournament_score=p_data.get("tournament_score", 0.0),
                    rank=p_data.get("rank", 0),
                    played_with=p_data.get("played_with", []),
                )
            else:
                player_full.tournament_score = p_data.get("tournament_score", 0.0)
                player_full.rank = p_data.get("rank", 0)
                player_full.played_with = p_data.get("played_with", [])
            players_map[idn] = player_full
            t.list_of_players.append(player_full)

        # 3bis) Maintenant que number_of_rounds est fixé, on peut calculer max_players_limit
        max_players_limit = t.number_of_rounds ** 2

        while True:
            clear_screen()
            TournamentView.show_player_list_header(t.list_of_players)
            count = len(t.list_of_players)

            # 3.a – Moins que le minimum, on force l'ajout
            if count < MIN_PLAYERS:
                needed = MIN_PLAYERS - count
                print(f"\nIl manque {needed} joueur(s) pour atteindre le minimum de ({MIN_PLAYERS}) joueur(s) requis.")
                print()
                wait_for_enter_continue()

                # On n’appelle plus show_player_list_header ici,
                # car on l’affiche directement dans la boucle suivante à chaque ajout.
                for i in range(needed):
                    while True:
                        # 1) Affiche la liste des joueurs + bloc [INFO]
                        TournamentView.show_player_list_header(t.list_of_players)

                        # 2) Lancer ensuite le formulaire d'inscription
                        new_player = TournamentView.register_one_player(
                            count + 1,
                            max_players_limit
                        )
                        idn = new_player.id_national_chess
                        existing_ids = {p.id_national_chess for p in t.list_of_players}
                        if idn in existing_ids:
                            TournamentView.display_player_already_in_tournament_text(idn)
                            wait_for_enter_continue()
                            continue
                        break
                    t.list_of_players.append(new_player)
                    count += 1
                    save_tournament_to_json(
                        t.get_serialized_tournament(),
                        TOURNAMENTS_FOLDER,
                        filename
                    )
                continue

            # 3.b – Si on a déjà atteint le maximum autorisé
            if count >= max_players_limit:
                print(f"\nNombre maximal de joueurs atteint ({max_players_limit}).")
                wait_for_enter_continue()
                break

            # 3.c – Entre MIN_PLAYERS et max_players_limit, on propose Y/N
            choix = get_valid_input(
                prompt=f"\nVoulez-vous ajouter un joueur ({count} / {max_players_limit} (max)) ? (Y/N) : ",
                formatter=format_yes_no,
                validator=is_valid_yes_no,
                message_error=invalid_yes_no
            )
            if choix == "Y":
                while True:
                    # Afficher d'abord la liste des joueurs + bloc [INFO]
                    TournamentView.show_player_list_header(t.list_of_players)

                    # Puis lancer le formulaire d'inscription
                    new_player = TournamentView.register_one_player(
                        count + 1,
                        max_players_limit
                    )
                    idn = new_player.id_national_chess
                    existing_ids = {p.id_national_chess for p in t.list_of_players}
                    if idn in existing_ids:
                        TournamentView.display_player_already_in_tournament_text(idn)
                        wait_for_enter_continue()
                        continue
                    break
                t.list_of_players.append(new_player)
                save_tournament_to_json(
                t.get_serialized_tournament(),
                TOURNAMENTS_FOLDER,
                filename
                )
                continue
            else:
                break

        # 4) Reconstruire les rounds et les matchs
        for r_data in data.get("list_of_rounds", []):
            rnd = Round(r_data.get("round_number", ""))
            if r_data.get("start_time"):
                rnd.start_time = datetime.datetime.strptime(
                    r_data["start_time"], "%d/%m/%Y %H:%M:%S"
                )
            if r_data.get("end_time"):
                rnd.end_time = datetime.datetime.strptime(
                    r_data["end_time"], "%d/%m/%Y %H:%M:%S"
                )

            for m_data in r_data.get("matches", []):
                name = m_data.get("name", "")
                name_lower = name.lower()

                # “bye” ou match normal
                if "repos" in name_lower:
                    bye_id = m_data.get("player_1", {}).get("id_national_chess")
                    bye_player = players_map.get(bye_id)
                    if bye_player is None:
                        rnd.matches.append(Match(name, (None, None)))
                        continue
                    match = Match(name, (bye_player, None))
                    snap1 = m_data.get("player_1", {})
                    match._snap1 = {
                        "id_national_chess": snap1.get("id_national_chess"),
                        "match_score": snap1.get("match_score", 0.5),
                        "tournament_score": snap1.get("tournament_score", bye_player.tournament_score),
                        "rank": snap1.get("rank", bye_player.rank),
                        "color": snap1.get("color", None),
                        "played_with": snap1.get("played_with", list(bye_player.played_with))
                    }
                    match.match_score_1 = match._snap1["match_score"]
                    match.color_player_1 = match._snap1["color"]
                    match._snap2 = None
                    rnd.matches.append(match)
                else:
                    p1_data = m_data.get("player_1", {})
                    p2_data = m_data.get("player_2", {})
                    pid1 = p1_data.get("id_national_chess")
                    pid2 = p2_data.get("id_national_chess")
                    player1 = players_map.get(pid1)
                    player2 = players_map.get(pid2)
                    match = Match(name, (player1, player2))
                    match.color_player_1 = p1_data.get("color")
                    match.color_player_2 = p2_data.get("color")
                    match.match_score_1 = p1_data.get("match_score", None)
                    match.match_score_2 = p2_data.get("match_score", None)
                    match._snap1 = p1_data.copy()
                    match._snap2 = p2_data.copy()
                    rnd.matches.append(match)

                t.list_of_rounds.append(rnd)

        return tc


    def resume(self) -> None:
        """
        Poursuit le tournoi :
        1) Si actual_round == 0, on lance tous les rounds via RoundController.run().
        2) Si 1 <= actual_round < number_of_rounds, on vérifie :
           - Si le round courant est déjà terminé (end_time non None), on passe au round suivant.
           - Sinon, on relance le round courant pour terminer la saisie des matchs.
        3) Si actual_round == number_of_rounds :
           - Si le dernier round (number_of_rounds) a end_time renseigné, on affiche le classement final.
           - Sinon, on relance ce dernier round pour terminer la saisie.
        4) Si actual_round > number_of_rounds (cas imprévu), on affiche le résumé final.
        """
        t = self.tournament

        # 1) Aucun round démarré (actual_round == 0) → on lance tout le tournoi depuis le début
        if t.actual_round == 0:
            RoundController(t, self.filename).run()
            return

        # 2) En plein milieu du tournoi (round 1, 2, …, number_of_rounds - 1)
        if 1 <= t.actual_round < t.number_of_rounds:
            # Récupérer l’objet Round correspondant à actual_round
            current_round = t.list_of_rounds[t.actual_round - 1]

            # 2.a) Si le round courant est déjà terminé (end_time non None),
            #      on incrémente actual_round pour passer au round suivant.
            if current_round.end_time is not None:
                t.actual_round += 1
                # On enregistre immédiatement cette mise à jour dans le JSON
                self._save_progress()

            # Toujours relancer start_from_round pour la (nouvelle) valeur de actual_round
            RoundController(t, self.filename).start_from_round(t.actual_round)
            return

        # 3) Nous sommes au dernier round (actual_round == number_of_rounds)
        if t.actual_round == t.number_of_rounds:
            last_round = t.list_of_rounds[-1]

            # 3.a) Si ce dernier round est terminé (end_time renseigné) → affichage du classement final
            if last_round.end_time is not None:
                clear_screen()
                print("Ce tournoi est déjà terminé. Voici le récapitulatif final :\n")
                TournamentView.show_tournament_summary(t)
                return

            # 3.b) Sinon, on relance ce dernier round pour terminer la saisie des résultats
            RoundController(t, self.filename).start_from_round(t.actual_round)
            return

        # 4) (Cas imprévu : actual_round > number_of_rounds) → on affiche quand même le résumé final
        clear_screen()
        print("Ce tournoi est déjà terminé. Voici le récapitulatif final :\n")
        TournamentView.show_tournament_summary(t)
