from models.player_model    import Player
from rich.console           import Console

console = Console()


def player_already_exists_message(player: Player) -> str:
    return (
        f"Joueur déjà existant !\n"
        f"Identifiant : {player.id_national_chess}"
    )

def show_player_registration(MIN_PLAYERS: int, max_players: int) -> None:
    """
    Affiche un message d'information pour l'inscription des joueurs
    avec stylisation Rich.
    """
    console.print(
        "[bold yellow][INFO][/bold yellow]\n"
        f"[bold]Minimum[/bold] : {MIN_PLAYERS} joueurs\n" 
        f"[bold]Maximum[/bold] : {max_players} joueurs"
    )