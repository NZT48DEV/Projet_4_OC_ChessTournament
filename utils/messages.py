from rich.console import Console


console = Console()


def invalide_name_message():
    console.print(
        "\n[bold red][ERREUR][/bold red] Le nom/prénom est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]uniquement des lettres[/bold]\n"
        "et avoir [bold]au moins 2 caractères.[/bold]\n"
    )
    

def invalid_date_message():
    console.print(
        "\n[bold red][ERREUR][/bold red] La date est [bold]invalide.[/bold]\n"
        "Elle doit contenir [bold]uniquement 8 chiffres[/bold]\n"
        "et être au format [bold]JJMMAAAA[/bold]\n"
        "Exemple : [bold]01012020[/bold]"
    )


def invalide_id_national_chess():
    console.print(
        "\n[bold red][ERREUR][/bold red] L'ID est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]2 lettres[/bold] et [bold]5 chiffres.[/bold]\n"
        "Exemple : [bold]AB12345[/bold]\n"
    )