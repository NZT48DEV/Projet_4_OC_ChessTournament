from rich.console import Console


console = Console()


def invalide_name_message():
    console.print(
        "[bold red][ERREUR][/bold red] Le nom/prénom est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]uniquement des lettres[/bold]\n"
        "et avoir [bold]au moins 2 caractères.[/bold]\n"
    )
    

def invalid_date_message():
    console.print(
        "[bold red][ERREUR][/bold red] La date est [bold]invalide.[/bold]\n"
        "Elle doit contenir [bold]uniquement 8 chiffres[/bold]\n"
        "et être au format [bold]JJMMAAAA[/bold]\n"
        "Exemple : [bold]01012020[/bold]"
    )


def invalide_id_national_chess():
    console.print(
        "[bold red][ERREUR][/bold red] L'ID est [bold]invalide.[/bold]\n"
        "Il doit contenir [bold]2 lettres[/bold] et [bold]5 chiffres.[/bold]\n"
        "Exemple : [bold]AB12345[/bold]\n"
    )


def invalid_min_player_age_message():
    console.print(
        "[bold yellow][INFO][/bold yellow] Âge minimal pour s'inscrire : [bold]5 ans[/bold]."
    )