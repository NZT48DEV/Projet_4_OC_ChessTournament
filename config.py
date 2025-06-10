import os
import datetime

BASE_DATA_FOLDER = "data"

PLAYERS_FOLDER = os.path.join(BASE_DATA_FOLDER, "players")
PLAYERS_FILENAME = "{id_input}.json"
TOURNAMENTS_FOLDER = os.path.join(BASE_DATA_FOLDER, "tournaments")

DATE_INPUT_FORMAT = "%d%m%Y"
DATE_STORAGE_FORMAT = "%d/%m/%Y"

MIN_PLAYER_AGE = 5
MIN_ROUND = 1
MIN_PLAYERS = 2

MAX_NAME_LENGTH = 40
MAX_ROUND = 20
MAX_DESCRIPTION_LENGTH = 500

BYE_POINT = 0.5
DRAW_POINT = 0.5
WIN_POINT = 1.0
LOSE_POINT = 0.0
DEFAULT_NUMBER_OF_ROUND = 4
SWISS_MAX_PLAYERS_BASE = 2

ENTER_FOR_CONTINUE = "continuer…"
ENTER_FOR_MAIN_MENU = "revenir au menu principal."
ENTER_FOR_RAPPORT = "revenir au menu des rapports."

TODAY = datetime.datetime.now().strftime("%Y%m%d")
