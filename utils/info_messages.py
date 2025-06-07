from models.player_model    import Player
from models.tournament_model import Tournament
from rich.console           import Console

console = Console()

def player_info_text(player: Player) -> str:
    miss_info = "[Info manquante]"

    id_national_chess = player.id_national_chess

    first_name = (
        player.first_name
        if player.first_name is not None
        else miss_info
    )
    last_name = (
        player.last_name
        if player.last_name is not None
        else miss_info
    )
    date_of_birth = (
        player.date_of_birth
        if player.date_of_birth is not None
        else miss_info
    )

    return (
        f"  [b yellow]• IDN[/b yellow]               : {id_national_chess}\n"
        f"  [b yellow]• Prénom[/b yellow]            : {first_name}\n"
        f"  [b yellow]• Nom[/b yellow]               : {last_name}\n"
        f"  [b yellow]• Date de naissance[/b yellow] : {date_of_birth}\n"
    )

def player_already_exist_text() -> str:
    return(
        "\n[b yellow][INFO][/b yellow] [b]Le profil du joueur est déjà existant.[/b]\n"
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

def tournament_incomplete_text() -> str:
    return(
        "[b yellow][INFO][/b yellow] [b]Il manque des [underline]informations[/underline] pour ce tournoi.[/b]\n"
        "Veuillez ajouter les informations manquantes au tournoi\n"
    )

def tournament_info_text(tournament: Tournament) -> str:
    miss_info = "[Info manquante]"
    no_desc   = "[Pas de description]"

    # 1) Préparer chaque champ dans une variable “formatée”
    name = tournament.tournament_name

    location = (
        tournament.location
        if tournament.location is not None
        else miss_info
    )

    start_date = (
        tournament.start_date
        if tournament.start_date is not None
        else miss_info
    )

    end_date = (
        tournament.end_date
        if tournament.end_date is not None
        else miss_info
    )

    rounds = (
        tournament.number_of_rounds
        if tournament.number_of_rounds is not None
        else miss_info
    )

    if tournament.description is None:
        description = miss_info
    elif tournament.description == "":
        description = no_desc
    else:
        description = tournament.description

    return (
        f"  [b yellow]• Nom du tournoi[/b yellow]   : {name}\n"
        f"  [b yellow]• Lieu[/b yellow]             : {location}\n"
        f"  [b yellow]• Date de début[/b yellow]    : {start_date}\n"
        f"  [b yellow]• Date de fin[/b yellow]      : {end_date}\n"
        f"  [b yellow]• Nombre de rounds[/b yellow] : {rounds}\n"
        f"  [b yellow]• Description[/b yellow]      : {description}\n"
    )
