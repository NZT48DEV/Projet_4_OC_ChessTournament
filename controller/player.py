from models.player import Player
from utils.formatters import format_first_name, format_last_name, format_date, format_id_national_chess
from utils.validators import is_valid_name, is_valid_date, is_valid_id_national_chess
from utils.messages import invalide_name_message

def create_player():
    print("\n" + "=" * 40)
    print("👤    CRÉATION D'UN NOUVEAU JOUEUR    👤")
    print("=" * 40)

    while True:
        first_name = format_first_name(input("Prénom : "))
        if is_valid_name(first_name):
            print(f"Le prénom du joueur est : {first_name}")
            # break
        else:
            print(invalide_name_message())


    last_name = input("Nom : ")


    date_of_birth = input("Date de naissance : ")


    id_national_chess = input("Identifiant National d'Echecs : ")

    player = Player(first_name, last_name, date_of_birth, id_national_chess)
    print(f"Joueur {player.first_name} {player.last_name} créé.")


