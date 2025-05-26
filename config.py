import os

# Dossier des données
BASE_DATA_FOLDER = "data"

PLAYERS_FOLDER = os.path.join(BASE_DATA_FOLDER, "players")
PLAYERS_FILENAME = "players.json"

TOURNAMENTS_FOLDER = os.path.join(BASE_DATA_FOLDER, "tournaments")

# Formats
DATE_INPUT_FORMAT = "%d%m%Y"
DATE_STORAGE_FORMAT = "%d/%m/%Y"

# Autres constantes
MIN_PLAYER_AGE = 5
MIN_ROUND = 1

MAX_NAME_LENGTH = 40
MAX_ROUND = 20
MAX_DESCRIPTION_LENGTH = 500
