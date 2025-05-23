import json
import os


def save_player_to_json(player_data, folder, filename):
    """
    Sauvegarde les données d'un joueur dans un fichier JSON nommé selon son identifiant unique.

    Le fichier est créé uniquement s'il n'existe pas déjà.
    
    Args:
        player_data (dict): Les données du joueur à enregistrer.
        folder (str): Le dossier dans lequel enregistrer le fichier.
        filename (str): Le nom du fichier (ex : 'AB12345.json').

    Returns:
        bool: True si le fichier a été créé, False s'il existait déjà.
    """
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        return False
    
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(player_data, file, ensure_ascii=False, indent=4)
    
    return True