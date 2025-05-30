import os
import datetime

# Dossier des données
BASE_DATA_FOLDER = "data"

PLAYERS_FOLDER = os.path.join(BASE_DATA_FOLDER, "players")
PLAYERS_FILENAME = "{id_input}.json"

TOURNAMENTS_FOLDER = os.path.join(BASE_DATA_FOLDER, "tournaments")

# Formats
DATE_INPUT_FORMAT = "%d%m%Y"
DATE_STORAGE_FORMAT = "%d/%m/%Y"

# Autres constantes
MIN_PLAYER_AGE = 5
MIN_ROUND = 1
MIN_PLAYERS = 2

MAX_NAME_LENGTH = 40
MAX_ROUND = 20
MAX_DESCRIPTION_LENGTH = 500

TODAY = datetime.datetime.now().strftime("%Y%m%d")
