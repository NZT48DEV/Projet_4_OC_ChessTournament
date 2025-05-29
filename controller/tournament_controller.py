import os
from storage.player_data            import load_player_from_json
from storage.tournament_data        import save_tournament_to_json
from config                         import PLAYERS_FOLDER, TOURNAMENTS_FOLDER, TODAY
from views.tournament_view          import TournamentView
from controller.round_controller    import RoundController
from controller.player_controller   import PlayerController
from models.tournament_model        import Tournament
from views.round_view               import RoundView


class TournamentController:
    """
    Contrôleur pour gérer la création pas à pas,
    l'inscription des joueurs et l'exécution d'un tournoi.
    """
    def __init__(self, filename: str = None):
        self.tournament: Tournament = None
        self.filename: str = filename

    def _save_progress(self) -> None:
        """
        Sauvegarde l'état courant du tournoi dans le fichier JSON.
        """
        if not self.filename:
            # Générer un nom de fichier si pas encore défini
            base = self.tournament.tournament_name.replace(' ', '_').lower()
            self.filename = f"{base}_{TODAY}.json"
        save_tournament_to_json(
            self.tournament.get_serialized_tournament(),
            TOURNAMENTS_FOLDER,
            self.filename
        )

    def run(self) -> None:
        """Démarre la création pas à pas, l'inscription, puis l'exécution du tournoi."""
        # 1. Création incrémentale du modèle
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
        print(f"Tournoi '{name}' créé et sauvegardé.")

        loc = TournamentView.ask_location()
        self.tournament.location = loc
        self._save_progress()

        start = TournamentView.ask_start_date()
        self.tournament.start_date = start
        self._save_progress()

        end = TournamentView.ask_end_date(start)
        self.tournament.end_date = end
        self._save_progress()

        rounds = TournamentView.ask_number_of_rounds()
        self.tournament.number_of_rounds = rounds
        self._save_progress()

        desc = TournamentView.ask_description()
        self.tournament.description = desc
        self._save_progress()

        print(f"Tournoi '{self.tournament.tournament_name}' paramétré et sauvegardé étape par étape.")

        # 2. Inscription des joueurs
        max_players = 2 ** self.tournament.number_of_rounds
        participants = []
        print(f"\nInscription des joueurs (max {max_players}).")
        while len(participants) < max_players:
            ans = input("Ajouter un joueur (Y/N) ? ").strip().upper()
            if ans == 'N':
                break
            if ans != 'Y':
                print("Réponse invalide, Y ou N attendu.")
                continue
            id_input = input("ID national d'échecs (XX00000) : ").strip().upper()
            try:
                player = load_player_from_json(PLAYERS_FOLDER, id_input)
                print(f"Joueur trouvé : {player.first_name} {player.last_name}")
            except FileNotFoundError:
                player = PlayerController.create_player_with_id(id_input)
                print(f"Nouveau joueur créé : {player.first_name} {player.last_name}")
            if any(p.id_national_chess == player.id_national_chess for p in participants):
                print("Ce joueur est déjà inscrit.")
            else:
                participants.append(player)
                self.tournament.list_of_players = participants
                self._save_progress()

        if len(participants) < 2:
            RoundView.show_error("Un tournoi nécessite au moins 2 joueurs.")
            return

        # 3. Exécution des rounds
        round_controller = RoundController(self.tournament, self.filename)
        round_controller.run()

        # 4. Sauvegarde finale
        self.tournament.actual_round = self.tournament.number_of_rounds
        self.tournament.list_of_rounds = round_controller.rounds
        self._save_progress()
        print("\nTournoi terminé !")
