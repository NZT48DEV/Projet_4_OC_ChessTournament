from models.player_model    import Player
from views.player_view      import PlayerView
from storage.player_data    import save_player_to_json, load_player_from_json
from config                 import PLAYERS_FOLDER
from utils.input_manager    import get_valid_input
from utils.input_formatters import format_yes_no
from utils.input_validators import is_valid_yes_no
from utils.error_messages   import invalid_yes_no
from utils.console          import wait_for_enter_continue

class PlayerController:
    """
    Contrôleur pour gérer la création incrémentale et l'enregistrement des joueurs.
    """
    @staticmethod
    def create_player() -> Player:
        """
        Flux pas à pas pour créer ou mettre à jour un joueur :

        1. Demande l’identifiant national (IDN) via la vue.
        2. Tente de charger un joueur existant depuis le JSON.
        - Si le joueur existe mais a des champs manquants (prénom, nom ou date de naissance) :
            • Affiche un message d’incomplétude.
            • Invite à compléter chaque champ manquant, en sauvegardant après chaque saisie.
            • Affiche un message de confirmation de mise à jour.
            • Retourne l’objet Player mis à jour.
        - Si le joueur existe et que toutes ses informations sont présentes :
            • Affiche le récapitulatif du profil.
            • Demande si l’utilisateur souhaite modifier ses informations.
            - Si oui : invite à resaisir prénom, nom et date de naissance (sauvegarde à chaque étape)
                puis affiche un message de confirmation de mise à jour.
            - Sinon : affiche un message « joueur déjà existant ».
            • Retourne l’objet Player existant (éventuellement modifié).
        3. Si aucun joueur n’est trouvé (FileNotFoundError) :
        - Crée un objet Player minimal avec l’ID saisi.
        - Sauvegarde immédiatement dans le JSON le fichier du joueur avec ID seul.
        - Invite successivement à saisir prénom, nom et date de naissance, en enregistrant après chaque saisie.
        - Affiche un message de confirmation de création.
        - Retourne l’objet Player complet.
        """
        # 1. Identifiant national
        id_nat = PlayerView.ask_id_national_chess()
        try:
            # si déjà existant, on le charge et on termine
            player = load_player_from_json(PLAYERS_FOLDER, id_nat)

            missing_fields = []
            if not player.first_name:
                missing_fields.append("first_name")
            if not player.last_name:
                missing_fields.append("last_name")
            if not player.date_of_birth:
                missing_fields.append("date_of_birth")
            
            if missing_fields:
                # Informer qu'il manque des infos et forcer la saisie de chaque champ manquant
                PlayerView.display_player_incomplete(player)
                wait_for_enter_continue()

                if "first_name" in missing_fields:
                    first = PlayerView.ask_first_name()
                    player.first_name = first
                    save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")
                
                if "last_name" in missing_fields:
                    last = PlayerView.ask_last_name()
                    player.last_name = last
                    save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")
                
                if "date_of_birth" in missing_fields:
                    dob = PlayerView.ask_date_of_birth()
                    player.date_of_birth = dob
                    save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

                PlayerView.display_player_updated(player)
                return player
            
            else:

                if player:
                    PlayerView.display_player_already_exist(player)
                    
                    modify_choice = get_valid_input(
                        prompt="Voulez-vous modifier les informations associer au joueur (Y/N) ? ",
                        formatter=format_yes_no,
                        validator=is_valid_yes_no,
                        message_error=invalid_yes_no,
                        )
                    
                    if modify_choice == "Y":
                        new_first = PlayerView.ask_first_name()
                        player.first_name = new_first
                        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

                        new_last = PlayerView.ask_last_name()
                        player.last_name = new_last
                        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

                        new_dob = PlayerView.ask_date_of_birth()
                        player.date_of_birth = new_dob
                        save_player_to_json(player.get_serialized_player(), PLAYERS_FOLDER, f"{id_nat}.json")

                        PlayerView.display_player_updated(player)
                    
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
        PlayerView.display_player_added(player)
        wait_for_enter_continue()
        return player

    @staticmethod
    def create_player_with_id(id_national: str) -> Player:
        """
        Charge un joueur existant par ID ou crée un nouvel en utilisant l'ID fourni.
        Si le joueur existe mais a des champs manquants, on le renvoie vers la complétion.
        """
        try:
            player = load_player_from_json(PLAYERS_FOLDER, id_national)
            # 1) On a bien un fichier JSON, mais on vérifie s’il manque des champs
            missing_fields = []
            if not player.first_name:
                missing_fields.append("first_name")
            if not player.last_name:
                missing_fields.append("last_name")
            if not player.date_of_birth:
                missing_fields.append("date_of_birth")

            if missing_fields:
                # On affiche “profil incomplet” et on force la complétion
                PlayerView.display_player_incomplete(player)
                wait_for_enter_continue()

                # On repropose prénom / nom / date pour chaque champ manquant
                if "first_name" in missing_fields:
                    player.first_name = PlayerView.ask_first_name()
                    save_player_to_json(player.get_serialized_player(),
                                        PLAYERS_FOLDER,
                                        f"{id_national}.json")
                if "last_name" in missing_fields:
                    player.last_name = PlayerView.ask_last_name()
                    save_player_to_json(player.get_serialized_player(),
                                        PLAYERS_FOLDER,
                                        f"{id_national}.json")
                if "date_of_birth" in missing_fields:
                    player.date_of_birth = PlayerView.ask_date_of_birth()
                    save_player_to_json(player.get_serialized_player(),
                                        PLAYERS_FOLDER,
                                        f"{id_national}.json")

            return player

        except FileNotFoundError:
            # 3) Le JSON n'existe pas du tout => on crée un nouveau profil
            player = Player(
                id_national_chess=id_national,
                first_name='',
                last_name='',
                date_of_birth=''
            )
            save_player_to_json(player.get_serialized_player(),
                                PLAYERS_FOLDER,
                                f"{id_national}.json")

        # 4) Si on arrive ici, c’est parce que le fichier n’existait pas :
        #    on invite simplement à saisir les champs (comme dans create_player initial)
        player.first_name = PlayerView.ask_first_name()
        save_player_to_json(player.get_serialized_player(),
                            PLAYERS_FOLDER,
                            f"{id_national}.json")

        player.last_name = PlayerView.ask_last_name()
        save_player_to_json(player.get_serialized_player(),
                            PLAYERS_FOLDER,
                            f"{id_national}.json")

        player.date_of_birth = PlayerView.ask_date_of_birth()
        save_player_to_json(player.get_serialized_player(),
                            PLAYERS_FOLDER,
                            f"{id_national}.json")

        PlayerView.display_player_added(player)
        return player