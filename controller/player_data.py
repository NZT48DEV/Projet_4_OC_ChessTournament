import json
import os

from config import PLAYERS_FOLDER, PLAYERS_FILENAME


def save_player_to_json(player_data, filename=PLAYERS_FILENAME, folder=PLAYERS_FOLDER):
    """Ajoute un joueur au fichier JSON commun contenant tous les joueurs"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    data.append(player_data)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)