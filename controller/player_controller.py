import time
from models.player_model import Player
from views.player_view import CreatePlayer
from controller.player_data import save_player_to_json

def create_player():

    users_entries = CreatePlayer().display_create_player_menu()

    player = Player(
        users_entries['first_name'],
        users_entries['last_name'],
        users_entries['date_of_birth'],
        users_entries['id_national_chess']
    )

    serialized_player = player.get_serialized_player()
    save_player_to_json(serialized_player)
    
    print(f"Joueur {player.first_name} {player.last_name} ajouté au fichier 'players.json'.")
    time.sleep(2)
    
    