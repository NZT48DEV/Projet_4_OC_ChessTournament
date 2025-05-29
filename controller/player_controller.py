from models.player_model    import Player
from views.player_view      import PlayerView
from storage.player_data    import save_player_to_json, load_player_from_json
from config                 import PLAYERS_FOLDER

class PlayerController:
    """
    Contrôleur pour gérer la création incrémentale et l'enregistrement des joueurs.
    """
    @staticmethod
    def create_player() -> Player:
        """
        Flux pas à pas : demande chaque donnée et sauvegarde après chaque étape.
        Commence par l'ID, puis prénom, nom, date de naissance.
        """
        # 1. Identifiant national
        id_nat = PlayerView.ask_id_national_chess()
        try:
            # si déjà existant, on le charge et on termine
            player = load_player_from_json(PLAYERS_FOLDER, id_nat)
            print(f"Joueur existant chargé : {player.first_name} {player.last_name}")
            return player
        except FileNotFoundError:
            # création d'un nouvel objet minimal
            player = Player(
                id_national_chess=id_nat,
                first_name='',
                last_name='',
                date_of_birth=''
            )
            # première sauvegarde avec ID seulement
            save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

        # 2. Prénom
        first = PlayerView.ask_first_name()
        player.first_name = first
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

        # 3. Nom
        last = PlayerView.ask_last_name()
        player.last_name = last
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

        # 4. Date de naissance
        dob = PlayerView.ask_date_of_birth()
        player.date_of_birth = dob
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

        # 5. Feedback final
        PlayerView.player_added_message(player)
        return player

    @staticmethod
    def create_player_with_id(id_national: str) -> Player:
        """
        Charge un joueur existant par ID ou crée un nouvel en utilisant l'ID fourni.
        Ne redemande pas l'ID, poursuit directement le flux pour prénom, nom, dob.
        """
        try:
            player = load_player_from_json(PLAYERS_FOLDER, id_national)
            print(f"Joueur existant chargé : {player.first_name} {player.last_name}")
            return player
        except FileNotFoundError:
            # on crée un objet minimal avec l'ID
            print(f"Joueur avec ID {id_national} non trouvé. Création d’un nouveau profil.")
            player = Player(
                id_national_chess=id_national,
                first_name='',
                last_name='',
                date_of_birth=''
            )
            save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_national}.json")

        # Continuer le flux : prénom
        first = PlayerView.ask_first_name()
        player.first_name = first
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_national}.json")

        # Nom
        last = PlayerView.ask_last_name()
        player.last_name = last
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_national}.json")

        # Date de naissance
        dob = PlayerView.ask_date_of_birth()
        player.date_of_birth = dob
        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_national}.json")

        PlayerView.player_added_message(player)
        return player
