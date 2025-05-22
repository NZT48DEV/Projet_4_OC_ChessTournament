from datetime import datetime

from config import MAX_NAME_LENGTH, DATE_INPUT_FORMAT, DATE_STORAGE_FORMAT


def format_first_name(first_name: str) -> str:
    first_name = first_name.strip().title()
    return first_name[:MAX_NAME_LENGTH]


def format_last_name(last_name: str) -> str:
    last_name = last_name.strip().upper()
    return last_name[:MAX_NAME_LENGTH]


def format_id_national_chess(id_national_chess: str) -> str:
    return id_national_chess.strip().upper()


def format_date(date_str: str) -> str | None:
    date_str = date_str.strip()
    for separator in [" ", "-", ".", "/"]:
        date_str = date_str.replace(separator, "")

    if len(date_str) == 8:
        try:
            date = datetime.strptime(date_str, DATE_INPUT_FORMAT)
            return date.strftime(DATE_STORAGE_FORMAT)
        except ValueError:
            return None   
    else:
        return None
