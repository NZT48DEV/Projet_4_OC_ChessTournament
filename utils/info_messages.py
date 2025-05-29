from models.player_model    import Player
from rich.console           import Console

console = Console()

def player_added_message(player: Player) -> str:
    return (
        f"Joueur {player.first_name} {player.last_name}\n"
        f"ID : {player.id_national_chess}\n"
        f"Ajouté avec succès."
    )


def player_already_exists_message(player: Player) -> str:
    return (
        f"Joueur déjà existant !\n"
        f"Identifiant : {player.id_national_chess}"
    )