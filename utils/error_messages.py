from rich.console import Console

from config import (
    MAX_DESCRIPTION_LENGTH, 
    MIN_ROUND, MAX_ROUND, 
    DEFAULT_NUMBER_OF_ROUND, 
    MIN_PLAYER_AGE,
    MIN_DATE_OF_BIRTH,
    TODAY_STR,
    MAX_TOURNAMENT_NAME_LENGTH,
    MIN_TOURNAMENT_NAME_LENGTH,
    MAX_LOCATION_NAME_LENGTH,
    MIN_LOCATION_NAME_LENGTH,
    DATE_LENGTH,
    MIN_FIRST_NAME_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MIN_LAST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH
)
from utils.ui_helpers import (
    show_id_national_chess,
    show_first_name,
    show_last_name,
    show_date_of_birth,
    show_tournament_name,
    show_location,
    show_start_date,
    show_end_date,
    show_number_of_rounds,
    show_description,
)


console = Console()


def invalid_first_name():
    show_first_name()
    console.print(
        "\n[b red][ERREUR][/b red] Le prénom est [b]invalide.[/b]\n"
        "Il doit contenir [b]uniquement des lettres[/b]\n"
        f"et avoir [b]au minimum {MIN_FIRST_NAME_LENGTH} caractères,[/b]" 
        f" et au maximum [b]{MAX_FIRST_NAME_LENGTH} caractères.[/b]\n"
    )

def invalid_last_name():
    show_last_name()
    console.print(
        "\n[b red][ERREUR][/b red] Le nom est [b]invalide.[/b]\n"
        "Il doit contenir [b]uniquement des lettres[/b]\n"
        f"et avoir [b]au minimum {MIN_LAST_NAME_LENGTH} caractères,[/b]"
        f" et au maximum [b]{MAX_LAST_NAME_LENGTH} caractères.[/b]\n"
    )


def invalid_date_of_birth():
    show_date_of_birth()
    console.print(
        "\n[b red][ERREUR][/b red] La date est [b]invalide.[/b]\n"
        f"Elle doit contenir [b]uniquement {DATE_LENGTH} chiffres[/b]\n"
        "et être au format [b]JJMMAAAA[/b]\n"
        f"Âge minimal pour s'inscrire : [b]{MIN_PLAYER_AGE} ans[/b]\n"
        f"Exemple : [b]Entre 01011900 et {MIN_DATE_OF_BIRTH.strftime("%d%m%Y")}[/b]\n"
    )


def invalid_tournament_start_date():
    show_start_date()
    console.print(
        "\n[b red][ERREUR][/b red] La date est [b]invalide.[/b]\n"
        f"Elle doit contenir [b]uniquement {DATE_LENGTH} chiffres[/b] et être au format [b yellow]JJMMAAAA[/b yellow].\n"
        "La date de [b yellow]début[/b yellow] doit être : [b]supérieur[/b] ou [b]égal[/b] à la date du jour\n"
        f"[b]Exemple[/b] : Date de début : [b][{TODAY_STR}][/b] | Date de fin : [b]{TODAY_STR} ou supérieur[/b]\n"
    )


def invalid_tournament_end_date():
    show_end_date()
    console.print(
        "\n[b red][ERREUR][/b red] La date est [b]invalide.[/b]\n"
        f"Elle doit contenir [b]uniquement {DATE_LENGTH} chiffres[/b]" 
        " et être au format [b yellow]JJMMAAAA[/b yellow].\n"
        "La date de [b yellow]fin[/b yellow] doit être [b]supérieur[/b] ou [b]égal[/b] à la date de début\n"
        f"[b]Exemple[/b] : Date de début : [b]{TODAY_STR}[/b] | Date de fin : [b][{TODAY_STR}] ou supérieur[/b]\n"
    )

def invalid_id_national_chess():
    show_id_national_chess()
    console.print(
        "\n[b red][ERREUR][/b red] L'ID est [b]invalide.[/b]\n"
        "Il doit contenir [b]2 lettres[/b] et [b]5 chiffres.[/b]\n"
        "Exemple : [b]AB12345[/b]\n"
    )


def invalid_tournament_name():
    show_tournament_name()
    console.print(
        "\n[b red][ERREUR][/b red] Le nom du tournoi est [b]invalide[/b].\n"
        "Il doit contenir [b]uniquement des lettres et/ou des chiffres[/b]\n"
        f"et avoir au minimum [b]{MIN_TOURNAMENT_NAME_LENGTH}[/b] caractère(s)," 
        f" et au maximum [b]{MAX_TOURNAMENT_NAME_LENGTH}[/b] caractère(s).\n"
        "Exemple : [b]Le tournoi des 6 nations[/b]\n"
    )


def invalid_location_name():
    show_location()
    console.print(
        "\n[b red][ERREUR][/b red] Le nom du lieu est [b]invalide[/b].\n"
        "Il doit contenir [b]uniquement des lettres et/ou des chiffres[/b]\n"
        f"et avoir au minimum [b]{MIN_LOCATION_NAME_LENGTH}[/b] caractère(s),"
        f" et au maximum [b]{MAX_LOCATION_NAME_LENGTH}[/b] caractère(s).\n"
        "Exemples : [b]Aix-en-provence[/b] OU [b]Route 66[/b]\n"
    )


def invalid_number_of_rounds():
    show_number_of_rounds()
    console.print(
        "\n[b red][ERREUR][/b red] Le nombre de rounds est [b]invalide[/b].\n"
        f"Entrez un [b yellow]nombre[/b yellow] entre [b]{MIN_ROUND}[/b] et [b]{MAX_ROUND}[/b].\n"
        f"ou appuyez sur [b yellow]Entrée[/b yellow]"
        f" pour utiliser la valeur par défaut ([b]{DEFAULT_NUMBER_OF_ROUND}[/b]).\n"
    )


def invalid_description():
    show_description()
    console.print(
        "\n[b red][ERREUR][/b red] La description est [b]invalide[/b].\n"
        f"Elle doit faire au maximum [b]{MAX_DESCRIPTION_LENGTH}[/b] caractères.\n"
        "Appuyez simplement sur [b yellow]Entrée[/b yellow] pour laisser vide.\n"
    )


def invalid_yes_no():
    console.print("\nRéponse invalide, [b yellow]Y[/b yellow] ou [b yellow]N[/b yellow] attendu.")
