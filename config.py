import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

BASE_DATA_FOLDER = "data"
PLAYERS_FOLDER = os.path.join(BASE_DATA_FOLDER, "players")
PLAYERS_FILENAME = "{id_input}.json"
TOURNAMENTS_FOLDER = os.path.join(BASE_DATA_FOLDER, "tournaments")

DATE_INPUT_FORMAT = "%d%m%Y"
DATE_STORAGE_FORMAT = "%d/%m/%Y"
DATE_LENGTH = 8
TODAY_STR = date.today().strftime("%d%m%Y")
TODAY = datetime.datetime.now().strftime("%d%m%Y")

MIN_PLAYER_AGE = 5
MIN_DATE_OF_BIRTH = date.today() - relativedelta(years=MIN_PLAYER_AGE)

MIN_ROUND = 1
MAX_ROUND = 20
DEFAULT_NUMBER_OF_ROUND = 4

MIN_PLAYERS = 2
SWISS_MAX_PLAYERS_BASE = 2

MIN_FIRST_NAME_LENGTH = 2
MAX_FIRST_NAME_LENGTH = 40

MIN_LAST_NAME_LENGTH = 2
MAX_LAST_NAME_LENGTH = 40

MIN_TOURNAMENT_NAME_LENGTH = 1
MAX_TOURNAMENT_NAME_LENGTH = 40

MIN_LOCATION_NAME_LENGTH = 2
MAX_LOCATION_NAME_LENGTH = 40

MAX_DESCRIPTION_LENGTH = 500

BYE_POINT = 0.5
DRAW_POINT = 0.5
WIN_POINT = 1.0
LOSE_POINT = 0.0

ENTER_FOR_CONTINUE = "continuer…"
ENTER_FOR_MAIN_MENU = "revenir au menu principal."
ENTER_FOR_RAPPORT = "revenir au menu des rapports."
