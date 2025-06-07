from models.match_model         import Match
from views.match_view           import MatchView
from views.round_view           import RoundView
from utils.console              import clear_screen, wait_for_enter_continue
from storage.tournament_data    import save_tournament_to_json
from config                     import TOURNAMENTS_FOLDER


class MatchController:
    """
    Contrôleur pour exécuter et gérer un match au sein d'un tournoi d'échecs.

    Fonctionnalités :
    1. Traitement des matches de repos (bye).
    2. Traitement des matches classiques (deux joueurs).
    3. Clôture automatique de la ronde lorsque tous les matchs sont terminés.
    4. Persistance de l'état du tournoi dans un fichier JSON.
    """

    def __init__(self, match: Match, tournament=None, filename: str = None) -> None:
        """
        Args:
            match (Match): L'objet Match à exécuter.
            tournament: Objet Tournament pour mettre à jour la ronde (optionnel).
            filename (str): Nom du fichier JSON du tournoi pour la persistance (optionnel).
        """
        self.match = match
        self.tournament = tournament
        self.filename = filename

    def run(self) -> None:
        """
        Point d'entrée pour lancer le traitement d'un match.
        """
        clear_screen()

        if self._is_bye():
            self._handle_bye_match()
        else:
            self._handle_classic_match()

    def _is_bye(self) -> bool:
        """
        Détermine si le match est un match de repos ('bye')
        en recherchant 'repos' dans le nom du match.
        """
        return 'repos' in self.match.name.lower()

    def _handle_bye_match(self) -> None:
        """
        Traitement spécifique aux matches de repos :
          1. Attribution d'un demi-point si non encore appliqué.
          2. Snapshot du match.
          3. Clôture de la ronde si toutes les rencontres sont terminées.
          4. Affichage du début de ronde puis du résultat.
          5. Persistance finale et attente de saisie.
        """
        # Vérifier le joueur de repos
        if self.match.player_1 is None:
            RoundView.show_error("Impossible d'identifier le joueur de repos pour ce match.")
            return

        # Appliquer le score si non initialisé
        if self.match.match_score_1 is None:
            self.match.apply_result(0)

        self.match.snapshot()
        self._close_round_if_finished()

        # Afficher le bandeau de la ronde en cours
        self._show_round_banner()

        # Afficher le résultat du match de repos
        MatchView.show_match_results(self.match)

        self._save_tournament()
        wait_for_enter_continue()

    def _handle_classic_match(self) -> None:
        """
        Traitement des matches entre deux joueurs :
          1. Demande du résultat via la vue.
          2. Application du résultat et snapshot.
          3. Clôture de la ronde si nécessaire.
          4. Affichage du résultat.
          5. Persistance et attente de saisie.
        """
        choice = MatchView.ask_match_result(self.match)
        self.match.apply_result(choice)
        self.match.snapshot()
        self._close_round_if_finished()

        MatchView.show_match_results(self.match)
        self._save_tournament()
        wait_for_enter_continue()

    def _close_round_if_finished(self) -> None:
        """
        Vérifie si la ronde contenant ce match est terminée.
        Si tous les matchs de la ronde ont un score, clôture et sauvegarde.
        """
        if not self.tournament or not self.filename:
            return

        for rnd in self.tournament.list_of_rounds:
            if self.match not in rnd.matches:
                continue

            all_played = all(
                m.match_score_1 is not None and (m.player_2 is None or m.match_score_2 is not None)
                for m in rnd.matches
            )

            if all_played and rnd.end_time is None:
                rnd.end_round()
                save_tournament_to_json(
                    self.tournament.get_serialized_tournament(),
                    TOURNAMENTS_FOLDER,
                    self.filename
                )
            break

    def _show_round_banner(self) -> None:
        """
        Affiche la bannière de la ronde en cours avant le résultat du match.
        """
        if not self.tournament:
            return

        for rnd in self.tournament.list_of_rounds:
            if self.match in rnd.matches:
                RoundView.show_start_round(rnd)
                break

    def _save_tournament(self) -> None:
        """
        Sauvegarde l'état du tournoi si un fichier est fourni.
        """
        if self.tournament and self.filename:
            save_tournament_to_json(
                self.tournament.get_serialized_tournament(),
                TOURNAMENTS_FOLDER,
                self.filename
            )
