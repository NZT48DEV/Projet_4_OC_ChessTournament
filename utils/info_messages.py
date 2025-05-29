from models.player_model    import Player
from rich.console           import Console

console = Console()


def player_added_message(player: Player) -> str:
    console.print(
        "\n[bold yellow][INFO][/bold yellow] [bold]Joueur créé avec succès.[/bold]\n"
        f"IDN : [bold]{player.id_national_chess}[/bold]\n"
        f"Prénom : [bold]{player.first_name}[/bold]\n"
        f"Nom : [bold]{player.last_name}[/bold]\n"
        f"Date de naissance : [bold]{player.date_of_birth}[/bold]"
    )


def player_already_exists_message(player: Player) -> str:
    return (
        f"Joueur déjà existant !\n"
        f"Identifiant : {player.id_national_chess}"
    )