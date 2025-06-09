from models.tournament_model import Tournament


def update_ranks(tournament: Tournament) -> None:
    """
    Recalcule et assigne les rangs (dense ranking) de tous les joueurs
    d'un tournoi en fonction de leur `tournament_score`.

    Principe dense ranking :
      - Score max → rank = 1
      - Score suivant → rank = 2 (même si plusieurs 1ers ex æquo)
      - etc.

    Modifie in-place : player.rank pour chaque Player dans tournament.list_of_players.
    """
    # Trie décroissant par score, puis par ID pour une ordre déterministe
    sorted_players = sorted(
        tournament.list_of_players,
        key=lambda p: (-p.tournament_score, p.id_national_chess)
    )
    prev_score = None
    current_dense_rank = 1
    last_assigned_rank = 1

    for player in sorted_players:
        if prev_score is None or player.tournament_score != prev_score:
            last_assigned_rank = current_dense_rank
        player.rank = last_assigned_rank
        prev_score = player.tournament_score
        current_dense_rank += 1
