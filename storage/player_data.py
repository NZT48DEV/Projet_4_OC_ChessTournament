import json
import os
from models.player_model import Player


def save_player_to_json(player_data: dict, folder: str, filename: str) -> bool:
    """
    Sauvegarde les données d'un joueur dans un fichier JSON nommé selon son identifiant unique.
    Le fichier est (ré)écrit à chaque appel pour permettre les mises à jour incrémentales.

    Args:
        player_data (dict): Les données du joueur à enregistrer.
        folder (str): Le dossier dans lequel enregistrer le fichier.
        filename (str): Le nom du fichier (ex : 'AB12345.json').

    Returns:
        bool: True si l’écriture a réussi.
    """
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(player_data, file, ensure_ascii=False, indent=4)

    return True


def load_players_from_json(folder: str) -> list[Player]:
    """
    Charge tous les joueurs depuis le dossier `data/players` en lisant
    les fichiers JSON. Supporte les fichiers JSON contenant un seul dict.
    """
    players: list[Player] = []

    if not os.path.exists(folder):
        print(f"Le dossier {folder} n'existe pas.")
        return players

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if not filename.endswith(".json") or not os.path.isfile(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                players.append(_player_from_dict(data))
            else:
                # Juste au cas où, on ignore les autres formats
                print(f"Ignoré : {filename} n'est pas un objet JSON.")

    return players

def load_player_from_json(folder: str, id_national: str) -> Player:
    """
    Tente de charger le joueur dont l’ID national vaut `id_national`.
    Lève FileNotFoundError si le fichier JSON n'existe pas.
    Utilise os.path au lieu de pathlib.
    """
    # Construction du chemin vers le fichier JSON
    filename = f"{id_national}.json"
    path = os.path.join(folder, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Pas de joueur avec ID {id_national}")

    # Lecture et désérialisation
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Création de l'objet Player à partir du dict
    return Player.from_dict(data)

def _player_from_dict(d: dict) -> Player:
    """Convertit un dict JSON en instance Player."""
    return Player(
        first_name        = d["first_name"],
        last_name         = d["last_name"],
        date_of_birth     = d["date_of_birth"],
        id_national_chess = d["id_national_chess"],
        tournament_score  = d.get("tournament_score", 0.0),
        rank              = d.get("rank", 0),
        played_with       = d.get("played_with", []),
    )