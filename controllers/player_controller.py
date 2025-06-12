from config import PLAYERS_FOLDER, ENTER_FOR_CONTINUE
from models.player_model import Player
from storage.player_data import load_player_from_json, save_player_to_json
from utils.input_manager import get_valid_input
from utils.input_formatters import format_yes_no
from utils.input_validators import is_valid_yes_no
from utils.error_messages import invalid_yes_no
from utils.console import wait_for_enter
from views.player_view import PlayerView


class PlayerController:
    """
    Contrôleur pour gérer la création, le chargement et la mise à jour des profils de joueurs.

    Méthodes statiques pour :
    - Détecter les champs manquants d'un joueur.
    - Compléter ces champs via l'interface utilisateur.
    - Charger ou créer un profil joueur avec persistance JSON.
    """

    @staticmethod
    def _load_or_create(id_national: str, prompt_modify: bool) -> Player:
        """
        Charge un profil joueur depuis le JSON ou en crée un nouveau.

        Si le fichier existe :
          - Complète les champs manquants.
          - Si prompt_modify=True et le profil est complet, propose une modification.
        Sinon :
          - Crée un profil minimal, persiste l'ID puis invite à saisir tous les champs.

        Args:
            id_national (str): Identifiant national unique du joueur.
            prompt_modify (bool): Si True, invite à modifier un profil déjà complet.

        Returns:
            Player: L'objet Player chargé ou créé et mis à jour.
        """
        try:
            # Tentative de chargement depuis JSON
            player = load_player_from_json(PLAYERS_FOLDER, id_national)
            missing = PlayerController._get_missing_fields(player)

            if missing:
                PlayerView.display_player_incomplete(player)
                wait_for_enter(ENTER_FOR_CONTINUE)
                PlayerController._complete_fields(player, missing)
                PlayerView.display_player_updated(player)
                wait_for_enter(ENTER_FOR_CONTINUE)

            elif prompt_modify:
                PlayerView.display_player_already_exist(player)
                wait_for_enter(ENTER_FOR_CONTINUE)
                choice = get_valid_input(
                    prompt="Voulez-vous modifier ce joueur (Y/N) ? ",
                    formatter=format_yes_no,
                    validator=is_valid_yes_no,
                    message_error=invalid_yes_no,
                )
                if choice == "Y":
                    # Complète tous les champs pour une modification complète
                    PlayerController._complete_fields(
                        player, ["first_name", "last_name", "date_of_birth"]
                    )
                    PlayerView.display_player_updated(player)
                    wait_for_enter(ENTER_FOR_CONTINUE)

            return player

        except FileNotFoundError:
            # Création d'un nouveau profil minimal
            player = Player(
                id_national_chess=id_national,
                first_name=None,
                last_name=None,
                date_of_birth=None,
            )
            # Première persistance de l'ID seul
            save_player_to_json(
                player.get_serialized_player(),
                PLAYERS_FOLDER,
                f"{id_national}.json"
            )
            # Saisie de tous les champs puis feedback
            PlayerController._complete_fields(
                player, ["first_name", "last_name", "date_of_birth"]
            )
            PlayerView.display_player_added(player)
            wait_for_enter(ENTER_FOR_CONTINUE)
            return player

    @staticmethod
    def _get_missing_fields(player: Player) -> list[str]:
        """
        Identifie les attributs d'un joueur qui sont vides ou non définis.

        Args:
            player (Player): Instance du modèle Player à vérifier.

        Returns:
            list[str]: Liste des noms de champs manquants ("first_name", "last_name", "date_of_birth").
        """
        return [
            field
            for field in ("first_name", "last_name", "date_of_birth")
            if not getattr(player, field)
        ]

    @staticmethod
    def _complete_fields(player: Player, fields: list[str]) -> None:
        """
        Demande à l'utilisateur de saisir et sauvegarde chaque champ spécifié.

        Pour chaque nom de champ fourni :
        1. Appelle la méthode PlayerView correspondante.
        2. Assigne la valeur retournée sur l'attribut du joueur.
        3. Persiste immédiatement le joueur en JSON.

        Args:
            player (Player): Instance du modèle Player à mettre à jour.
            fields (list[str]): Liste des noms de champs à compléter.
        """
        field_map = {
            "first_name": PlayerView.ask_first_name,
            "last_name": PlayerView.ask_last_name,
            "date_of_birth": PlayerView.ask_date_of_birth,
        }
        for field in fields:
            # Appel dynamique de la fonction de saisie
            value = field_map[field]()
            # Mise à jour de l'attribut
            setattr(player, field, value)
            # Persistance JSON immédiate
            save_player_to_json(
                player.get_serialized_player(),
                PLAYERS_FOLDER,
                f"{player.id_national_chess}.json"
            )

    @staticmethod
    def create_player() -> Player:
        """
        Point d'entrée pour créer ou charger un joueur via l'interaction utilisateur.

        1. Demande l'ID national au joueur.
        2. Appelle _load_or_create avec prompt_modify=True afin de proposer
           une modification même si le profil est complet.

        Returns:
            Player: Joueur chargé ou nouvellement créé.
        """
        id_national = PlayerView.ask_id_national_chess()
        return PlayerController._load_or_create(id_national, prompt_modify=True)

    @staticmethod
    def create_player_with_id(id_national: str) -> Player:
        """
        Charge ou crée un profil joueur à partir d'un ID fourni par le code.

        Contrairement à create_player, prompt_modify=False par défaut,
        on ne propose pas la modification si le profil est déjà complet,
        uniquement la complétion des champs manquants.

        Args:
            id_national (str): Identifiant national du joueur.

        Returns:
            Player: Joueur chargé ou nouvellement créé.
        """
        return PlayerController._load_or_create(id_national, prompt_modify=False)
