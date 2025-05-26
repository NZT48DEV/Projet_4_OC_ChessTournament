import json
import os


def save_tournament_to_json(tournament_data, folder, filename):

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        return False

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(tournament_data, file, ensure_ascii=False, indent=4)