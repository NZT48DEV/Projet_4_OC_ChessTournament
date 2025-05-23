import json
import os


def save_tournament_to_json(tournament_data, folder, filename):
    """Ajoute un tournoi au fichier JSON commun contenant tous les tournois"""
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
    
    data.append(tournament_data)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)