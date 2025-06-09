from rich.console   import Console

from config         import MAX_DESCRIPTION_LENGTH, MIN_ROUND, MAX_ROUND, DEFAULT_NUMBER_OF_ROUND, MIN_PLAYER_AGE


console = Console()


def invalid_name():
    console.print(
        "\n[b red][ERREUR][/b red] Le prénom/nom est [b]invalide.[/b]\n"
        "Il doit contenir [b]uniquement des lettres[/b]\n"
        "et avoir [b]au minimum 2 caractères,[/b] et au maximum [b]40 caractères.[/b]\n"
    )
    

def invalid_date_of_birth():
    console.print(
        "\n[b red][ERREUR][/b red] La date est [b]invalide.[/b]\n"
        "Elle doit contenir [b]uniquement 8 chiffres[/b]\n"
        "et être au format [b]JJMMAAAA[/b]\n"
        "Exemple : [b]01012020[/b]\n"
    )

def invalid_tournament_date():
    console.print(
        "\n[b red][ERREUR][/b red] La date est [b]invalide.[/b]\n"
        "Elle doit contenir [b]uniquement 8 chiffres[/b] et être au format [b yellow]JJMMAAAA[/b yellow].\n"
        "La date de [b yellow]début[/b yellow] doit être : [b]supérieur[/b] ou [b]égal[/b] à la date du jour\n"
        "La date de [b yellow]fin[/b yellow] doit être [b]supérieur[/b] ou [b]égal[/b] à la date de début\n"
        "[b]Exemple[/b] : Date de début : [b]10102030[/b] | Date de fin : [b]10102030 ou supérieur[/b]\n"
    )


def invalid_id_national_chess():
    console.print(
        "\n[b red][ERREUR][/b red] L'ID est [b]invalide.[/b]\n"
        "Il doit contenir [b]2 lettres[/b] et [b]5 chiffres.[/b]\n"
        "Exemple : [b]AB12345[/b]\n"
    )


def invalid_min_player_age():
    console.print(
        f"\n[b red][ERREUR][/b red] Âge minimal pour s'inscrire : [b]{MIN_PLAYER_AGE} ans[/b]."
    )


def invalid_tournament_name():
    console.print(
        "\n[b red][ERREUR][/b red] Le nom du tournoi est [b]invalide[/b].\n"
        "Il doit contenir [b]uniquement des lettres et/ou des chiffres[/b]\n"
        "et avoir [b]au minimum 1 caractère,[/b] et au maximum [b]40 caractères.[/b]\n"
        "Exemple : [b]Le tournoi des 6 nations[/b]\n"
    )


def invalid_location_name():
    console.print(
        "\n[b red][ERREUR][/b red] Le nom du lieu est [b]invalide[/b].\n"
        "Il doit contenir [b]uniquement des lettres et/ou des chiffres[/b]\n"
        "et avoir [b]au minimum 2 caractères,[/b] et au maximum [b]40 caractères.[/b]\n"
        "Exemples : [b]Aix-en-provence[/b] OU [b]Route 66[/b]\n"
    )


def invalid_number_of_rounds():
    console.print(
        "\n[b red][ERREUR][/b red] Le nombre de rounds est [b]invalide[/b].\n"
        f"Entrez un [b yellow]nombre[/b yellow] entre [b]{MIN_ROUND}[/b] et [b]{MAX_ROUND}[/b].\n"
        f"ou appuyez sur [b yellow]Entrée[/b yellow] pour utiliser la valeur par défaut ([b]{DEFAULT_NUMBER_OF_ROUND}[/b]).\n"
    )


def invalid_description():
    console.print(
        "\n[b red][ERREUR][/b red] La description est [b]invalide[/b].\n"
        f"Elle doit faire au maximum [b]{MAX_DESCRIPTION_LENGTH}[/b] caractères.\n"
        "Appuyez simplement sur [b yellow]Entrée[/b yellow] pour laisser vide.\n"
    )


def invalid_yes_no():
    console.print("\nRéponse invalide, [b yellow]Y[/b yellow] ou [b yellow]N[/b yellow] attendu.")




