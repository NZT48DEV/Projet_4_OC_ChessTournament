import time
from models.player import Player
from views.player import CreatePlayer

def create_player():

    users_entries = CreatePlayer().display_menu()

    player = Player(
        users_entries['first_name'],
        users_entries['last_name'],
        users_entries['date_of_birth'],
        users_entries['id_national_chess']
    )

    serialized_player = player.get_serialized_player()
    print(serialized_player)
    time.sleep(2)
    
    