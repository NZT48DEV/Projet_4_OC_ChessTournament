import os
from storage.player_data         import load_players_from_json
from storage.tournament_data     import save_tournament_to_json
from config                      import PLAYERS_FOLDER, TOURNAMENTS_FOLDER, TODAY
from views.tournament_view       import TournamentView
from models.tournament_model     import Tournament
from controller.round_controller import RoundController
from views.round_view            import RoundView

def create_tournament():
    # 1. Formulaire de création
    entries = TournamentView().display_create_tournament_menu()
    tournament = Tournament(
        tournament_name  = entries["tournament_name"],
        location         = entries["location"],
        start_date       = entries["start_date"],
        end_date         = entries["end_date"],
        number_of_rounds = entries.get("number_of_rounds", 4),
        description      = entries.get("description", "")
    )

    # 2. Charger et inscrire les joueurs
    players = load_players_from_json(PLAYERS_FOLDER)
    if len(players) < 2:
        RoundView.show_error("Pas assez de joueurs pour démarrer le tournoi.")
        return
    tournament.list_of_players = players

    # 3. Générer un nom de fichier unique tourné vers la date du jour
    base     = tournament.tournament_name.replace(' ', '_').lower()
    counter  = 0
    filename = f"{base}_{TODAY}.json"
    filepath = os.path.join(TOURNAMENTS_FOLDER, filename)

    # 3.1. Tant que ce fichier existe, on ajoute un suffixe _1, _2, etc.
    while os.path.exists(filepath):
        counter += 1
        filename = f"{base}_{TODAY}_{counter}.json"
        filepath = os.path.join(TOURNAMENTS_FOLDER, filename)

    # 4. Sauvegarde initiale (métadonnées + joueurs)
    save_tournament_to_json(
        tournament.get_serialized_tournament(),
        TOURNAMENTS_FOLDER,
        filename
    )

    # 5. Lancement des rounds via RoundController
    controller = RoundController(tournament, filename)
    controller.run()                # orchestrer tous les rounds

    # 6. Récupération des rounds joués et mise à jour du tournoi
    tournament.actual_round   = tournament.number_of_rounds
    tournament.list_of_rounds = controller.rounds

    # 7. Sauvegarde finale (ajout des rounds et round_score mis à jour)
    save_tournament_to_json(
        tournament.get_serialized_tournament(),
        TOURNAMENTS_FOLDER,
        filename
    )

    print("\n Tournoi terminé !")
