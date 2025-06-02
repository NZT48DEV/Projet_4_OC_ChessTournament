from rich.console   import Console
from config         import MAX_DESCRIPTION_LENGTH, MIN_ROUND, MAX_ROUND


console = Console()


def invalid_name():
    console.print(
        "\n[bold red][ERREUR][/bold red] Le nom/prénom est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]uniquement des lettres[/bold]\n"
        "et avoir [bold]au minimum 2 caractères,[/bold] et au maximum [bold]40 caractères.[/bold]"
    )
    

def invalid_date():
    console.print(
        "\n[bold red][ERREUR][/bold red] La date est [bold]invalide.[/bold]\n"
        "Elle doit contenir [bold]uniquement 8 chiffres[/bold]\n"
        "et être au format [bold]JJMMAAAA[/bold]\n"
        "Exemple : [bold]01012020[/bold]"
    )


def invalid_id_national_chess():
    console.print(
        "\n[bold red][ERREUR][/bold red] L'ID est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]2 lettres[/bold] et [bold]5 chiffres.[/bold]\n"
        "Exemple : [bold]AB12345[/bold]"
    )


def invalid_min_player_age():
    console.print(
        "\n[bold red][ERREUR][/bold red] Âge minimal pour s'inscrire : [bold]5 ans[/bold]."
    )


def invalid_tournament_name():
    console.print(
        "\n[bold red][ERREUR][/bold red] Le nom du tournoi est [bold]invalide[/bold].\n"
        "Il doit contenir [bold]uniquement des lettres et/ou des chiffres[/bold]\n"
        "et avoir [bold]au minimum 1 caractère,[/bold] et au maximum [bold]40 caractères.[/bold]\n"
        "Exemple : [bold]Le tournoi des 6 nations[/bold]"
    )


def invalid_location_name():
    console.print(
        "\n[bold red][ERREUR][/bold red] Le nom du lieu est [bold]invalide[/bold].\n"
        "Il doit contenir [bold]uniquement des lettres et/ou des chiffres[/bold]\n"
        "et avoir [bold]au minimum 2 caractères,[/bold] et au maximum [bold]40 caractères.[/bold]\n"
        "Exemples : [bold]Aix-en-provence[/bold] OU [bold]Route 66[/bold]"
    )


def invalid_number_of_rounds():
    console.print(
        "\n[bold red][ERREUR][/bold red] Le nombre de rounds est [bold]invalide[/bold].\n"
        f"Entrez un nombre entre [bold]{MIN_ROUND}[/bold] et [bold]{MAX_ROUND}[/bold].\n"
        "ou appuyez sur [bold]Entrée[/bold] pour utiliser la valeur par défaut ([bold]4 rounds[/bold])."
    )


def invalid_description():
    console.print(
        "\n[bold red][ERREUR][/bold red] La description est [bold]invalide[/bold].\n"
        f"Elle doit faire au maximum [bold]{MAX_DESCRIPTION_LENGTH}[/bold] caractères "
        "Appuyez simplement sur [bold]Entrée[/bold] pour laisser vide."
    )


def invalid_yes_no():
    """
    Message d’erreur à afficher quand on attend uniquement "Y" ou "N".
    """
    console.print("\nRéponse invalide, [b yellow]Y[/b yellow] ou [b yellow]N[/b yellow] attendu.")
