import json
import os


def save_tournament_to_json(tournament_data, folder, filename):
    """
    Écrit (ou réécrit) systématiquement le JSON du tournoi.
    """
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(tournament_data, file, ensure_ascii=False, indent=4)

    return True


def load_tournament_from_json(filepath: str) -> dict:
    """
    Lit et retourne le contenu d'un fichier JSON de tournoi.
    
    - `filepath` doit être le chemin complet vers un fichier .json existant.
    - Si le fichier n'existe pas, on lève FileNotFoundError.
    - Si le contenu n'est pas un JSON valide, on lève json.JSONDecodeError.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Aucun fichier trouvé à l’emplacement : {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data