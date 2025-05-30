import os
from storage.tournament_data        import save_tournament_to_json
from config                         import TOURNAMENTS_FOLDER, TODAY
from views.tournament_view          import TournamentView
from controller.round_controller    import RoundController
from models.tournament_model        import Tournament
from views.round_view               import RoundView

class TournamentController:
    def __init__(self, filename: str = None):
        self.tournament: Tournament = None
        self.filename: str = filename

    def _save_progress(self) -> None:
        """
        Sauvegarde l'état courant du tournoi dans un fichier JSON.
        - Lors de la première sauvegarde (self.filename None), crée un nouveau fichier unique si besoin.
        - Ensuite, écrase simplement ce même fichier.
        """
        # Préparation du dossier
        os.makedirs(TOURNAMENTS_FOLDER, exist_ok=True)

        # Si aucun fichier n'est encore défini, on crée un nom unique
        if self.filename is None:
            base = self.tournament.tournament_name.replace(' ', '_').lower()
            date_str = TODAY
            existing = [
                f for f in os.listdir(TOURNAMENTS_FOLDER)
                if f.startswith(f"{base}_{date_str}") and f.endswith('.json')
            ]
            # Détermine suffixe
            if existing:
                count = len(existing) + 1
                self.filename = f"{base}_{date_str}_{count}.json"
            else:
                self.filename = f"{base}_{date_str}.json"

        # Écriture dans le même fichier à chaque appel
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename
        )

    def run(self) -> None:
        # Initialisation basique du tournoi
        name = TournamentView.ask_tournament_name()
        self.tournament = Tournament(
            tournament_name=name,
            location="",
            start_date="",
            end_date="",
            number_of_rounds=0,
            description=""
        )
        self._save_progress()
        
        self.tournament.location = TournamentView.ask_location()
        self._save_progress()
        self.tournament.start_date = TournamentView.ask_start_date()
        self._save_progress()
        self.tournament.end_date = TournamentView.ask_end_date(self.tournament.start_date)
        self._save_progress()
        self.tournament.number_of_rounds = TournamentView.ask_number_of_rounds()
        self._save_progress()
        self.tournament.description = TournamentView.ask_description()
        self._save_progress()

        # Inscription des joueurs via la vue
        max_players = 2 ** self.tournament.number_of_rounds
        participants = TournamentView.ask_players(max_players)
        self.tournament.list_of_players = participants
        self._save_progress()

        if len(participants) < 2:
            RoundView.show_error("Un tournoi nécessite au moins 2 joueurs.")
            return

        # Exécution des rounds
        round_controller = RoundController(self.tournament, self.filename)
        round_controller.run()

        # Sauvegarde finale
        self.tournament.actual_round = self.tournament.number_of_rounds
        self.tournament.list_of_rounds = round_controller.rounds
        self._save_progress()
        print("\nTournoi terminé !")
