from models.player_model    import Player
from rich.console           import Console

console = Console()

def player_info_text(player: Player) -> str:
    return (
        f"  [b yellow]• IDN[/b yellow]               : {player.id_national_chess}\n"
        f"  [b yellow]• Prénom[/b yellow]            : {player.first_name}\n"
        f"  [b yellow]• Nom[/b yellow]               : {player.last_name}\n"
        f"  [b yellow]• Date de naissance[/b yellow] : {player.date_of_birth}\n"
    )

def player_already_exist_text() -> str:
    return(
        "\n[b yellow][INFO][/b yellow] [b]Le profil du joueur est déjà existant.[/b]\n"
    )
    

def show_player_registration(MIN_PLAYERS: int, max_players: int) -> None:
    """
    Affiche un message d'information pour l'inscription des joueurs
    avec stylisation Rich.
    """
    console.print(
        "[b yellow][INFO][/b yellow]\n"
        f"[b]Minimum[/b] : {MIN_PLAYERS} joueurs\n" 
        f"[b]Maximum[/b] : {max_players} joueurs"
    )


def player_added_text() -> str:
    return(
        "\n[b yellow][INFO][/b yellow] [b]Joueur créé avec succès.[/b]\n"
    )


def player_updated_text() -> str:
    return(
        "\n[b yellow][INFO][/b yellow] [b]Profil du joueur complété avec succès.[/b]\n"
    )


def player_incomplete_text() -> str:
    return(
        "[b yellow][INFO][/b yellow] [b]Ce joueur existe déjà, mais ses informations sont [underline]incomplètes[/underline].[/b]\n"
        "Veuillez ajouter les informations manquantes au profil de l'utilisateur\n"
    )

def player_added_to_chesstournament_text(id_national: str) -> str:
    return(
        f"[b yellow][INFO][/b yellow] Le joueur ({id_national}) a été ajouté au tournoi.\n")


def player_nonexistent_text(id_national: str) -> str:
    return(
        f"\n[b yellow][INFO][/b yellow] [b]Aucun profil de joueur trouvé pour cet ID : {id_national}.[/b]\n"
        "Veuillez créer un nouveau profil pour ce joueur."
    )
