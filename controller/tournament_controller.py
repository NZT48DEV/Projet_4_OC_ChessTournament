from models.tournament_model import Tournament
from views.tournament_view import CreateTournamentView
from storage.tournament_data import save_tournament_to_json
from config import TOURNAMENTS_FOLDER


def create_tournament():
    users_entries = CreateTournamentView().display_create_tournament_menu()

    tournament = Tournament(
        name=users_entries["name"],
        location=users_entries["location"],
        start_date=users_entries["start_date"],
        end_date=users_entries["end_date"],
        number_of_rounds=users_entries["number_of_rounds"],
        description=users_entries["description"]

    )

    serialized_tournament = tournament.get_serialized_tournament()

    save_tournament_to_json(
        tournament_data=serialized_tournament,
        folder=TOURNAMENTS_FOLDER,
        filename=f"{tournament.name.replace(" ", "_").lower()}.json"
    )


