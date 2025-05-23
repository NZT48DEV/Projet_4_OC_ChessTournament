import time
from models.player_model import Player
from views.player_view import CreatePlayer
from storage.player_data import save_player_to_json
from config import PLAYERS_FOLDER
from utils.info_messages import player_added_message, player_already_exists_message

def create_player():

    users_entries = CreatePlayer().display_create_player_menu()

    player = Player(
        users_entries['first_name'],
        users_entries['last_name'],
        users_entries['date_of_birth'],
        users_entries['id_national_chess']
    )

    serialized_player = player.get_serialized_player()

    save_succes = save_player_to_json(
        player_data=serialized_player,
        folder=PLAYERS_FOLDER,
        filename=f"{player.id_national_chess}.json"
        )
    
    if save_succes:
        print(player_added_message(player))
    else:
        print(player_already_exists_message(player))
    
    time.sleep(2)
    
    