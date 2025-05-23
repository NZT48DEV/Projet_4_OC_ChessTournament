import os

# Dossier des données
BASE_DATA_FOLDER = "data"

PLAYERS_FOLDER = os.path.join(BASE_DATA_FOLDER, "players")
PLAYERS_FILENAME = "players.json"

TOURNAMENTS_FOLDER = os.path.join(BASE_DATA_FOLDER, "tournaments")


# Formats
DATE_INPUT_FORMAT = "%d%m%Y"
DATE_STORAGE_FORMAT = "%d/%m/%Y"

# Règles d’âge
MIN_PLAYER_AGE = 5

# Autres constantes
MAX_NAME_LENGTH = 20
