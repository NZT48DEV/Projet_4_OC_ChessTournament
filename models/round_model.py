import datetime
import random
from typing                 import List, Set, Dict
from models.match_model     import Match
from models.player_model    import Player

class Round:
    def __init__(self, round_number: str) -> None:
        self.round_number = round_number
        self.matches: List[Match] = []
        self.start_time: datetime.datetime = None
        self.end_time: datetime.datetime = None

    def start_round(self) -> None:
        """Enregistre l'heure de début du tour."""
        self.start_time = datetime.datetime.now()

    def end_round(self) -> None:
        """Enregistre l'heure de fin du tour."""
        self.end_time = datetime.datetime.now()

    def add_match(self, match: Match) -> None:
        """Ajoute un objet Match au round."""
        self.matches.append(match)

    def generate_pairings(self, players: List[Player]) -> None:
        """
        Génère les appariements pour le round selon la logique suisse, mais s'assure
        que le match de repos (bye) soit toujours créé en premier lorsqu'il y a un nombre impair de joueurs :
        
        1) Trier les joueurs par tournament_score (ex-æquos mélangés).
        2) Si nombre impair → choisir le bye (le plus faible n’ayant jamais eu de bye), le créer en premier.
        3) Tenter d’apparier tous les joueurs restants sans rematch.
        4) Si, parmi les restants, il y a encore un joueur non apparié (cas extrême), forcer un rematch.
        """
        # 1) Préparation du « pool » trié, mélange dans chaque groupe de score égal
        sorted_players = sorted(players, key=lambda p: p.tournament_score, reverse=True)
        pool: List[Player] = []
        groups: Dict[float, List[Player]] = {}
        for p in sorted_players:
            groups.setdefault(p.tournament_score, []).append(p)
        for grp in groups.values():
            random.shuffle(grp)
            pool.extend(grp)

        # 2) Gestion du bye **en tout premier** si le nombre de joueurs est impair
        #    (on retire le joueur choisi pour le bye de la liste pool avant tout pairing).
        if len(pool) % 2 == 1:
            # 2.a – Trouver parmi les unpaired (tous ici) les candidats n’ayant jamais eu de bye
            candidates = [p for p in pool if "tour de repos" not in p.played_with]
            # Si aucun candidat n’est disponible (tous ont déjà eu un bye), on prend alors
            # parmi l’ensemble le joueur le moins fort (score faible) pour faire le bye.
            if not candidates:
                candidates = pool
            bye_player = min(candidates, key=lambda p: p.tournament_score)

            # 2.b – On marque le bye sur le joueur (ajout dans played_with)
            #       (on ne fait pas +=0.5 ici, car Match.apply_result(0) s’en chargera).
            bye_player.played_with.append("tour de repos")

            # 2.c – On crée le match de repos **en premier** et on l’ajoute
            #       à la liste self.matches AVANT tout autre pairing.
            bye_match = Match(f"{self.round_number} - Repos", (bye_player, None))

            # On met déjà à jour les classements (dense rank) immédiatement après le bye
            ranked_players = sorted(players, key=lambda p: p.tournament_score, reverse=True)
            prev_score = None
            prev_rank = 0
            dense_rank = 1
            for p in ranked_players:
                if prev_score is None or p.tournament_score < prev_score:
                    p.rank = dense_rank
                    prev_score = p.tournament_score
                    prev_rank = dense_rank
                    dense_rank += 1
                else:
                    p.rank = prev_rank

            # On prend un snapshot pour le match de repos avant de le stocker
            bye_match.snapshot()
            self.add_match(bye_match)

            # 2.d – On retire ensuite ce bye_player de la liste « pool »
            pool.remove(bye_player)

        # 3) Appariements des joueurs restants (première passe sans rematch)
        paired: Set[Player] = set()    # ensemble des joueurs déjà appariés
        unpaired: List[Player] = []    # liste des joueurs qui n’ont pas trouvé d’adversaire sans rematch

        for player_1 in pool:
            if player_1 in paired:
                continue
            found = False
            for player_2 in pool:
                if player_2 in paired or player_2 is player_1:
                    continue
                # Si ce candidat n’a **jamais** été apparié contre player_1
                if player_2.id_national_chess in player_1.played_with:
                    continue
                # On appaire player_1 & player_2
                paired.update({player_1, player_2})
                player_1.played_with.append(player_2.id_national_chess)
                player_2.played_with.append(player_1.id_national_chess)
                self.add_match(Match(f"{self.round_number} - Match", (player_1, player_2)))
                found = True
                break
            if not found:
                # Aucun adversaire sans rematch trouvé, on garde player_1 pour la passe 2
                unpaired.append(player_1)

        # 4) Deuxième passe : appariements restants (force rematch si nécessaire)
        while len(unpaired) >= 2:
            player_1 = unpaired.pop(0)
            # On cherche d’abord un adversaire pour lequel il n’y a pas encore eu de rematch
            player_2 = None
            for candidate in unpaired:
                if candidate.id_national_chess not in player_1.played_with:
                    player_2 = candidate
                    break
            # Si on n’en trouve pas, on force un rematch avec le premier qui restait
            if player_2 is None:
                player_2 = unpaired[0]
            unpaired.remove(player_2)

            # Enregistrer le rematch, même si c’est contre un adversaire déjà rencontré
            paired.update({player_1, player_2})
            player_1.played_with.append(player_2.id_national_chess)
            player_2.played_with.append(player_1.id_national_chess)

            name = f"{self.round_number} - Match"
            match = Match(name, (player_1, player_2))
            self.add_match(match)


    def get_round_report(self) -> str:
        """
        Retourne un rapport textuel brut des matchs, avec colonnes alignées
        et une ligne vide entre chaque match. Cette version fait en sorte que
        le match de repos (bye) soit toujours affiché en premier.
        """
        # 1) Tri des matches pour que les byes arrivent en tête
        matches_ordonnes = sorted(
            self.matches,
            key=lambda m: (m.player_2 is not None)
        )

        # 2) Constituer une liste de « groupes », un groupe par match
        #    (soit un tuple pour le bye, soit deux tuples pour un match classique)
        groups: List[List[tuple]] = []
        for match in matches_ordonnes:
            if match.player_2 is None:
                # Cas "bye" : un seul tuple
                p1 = match.player_1
                name1  = f"{p1.first_name} {p1.last_name}"
                id1    = f"[{p1.id_national_chess}]"
                color1 = "(Repos)"
                score1 = f"{match.match_score_1:.1f}"
                groups.append([(name1, id1, color1, score1)])
            else:
                # Match classique : deux tuples (joueur 1 et joueur 2)
                p1 = match.player_1
                p2 = match.player_2

                name1  = f"{p1.first_name} {p1.last_name}"
                id1    = f"[{p1.id_national_chess}]"
                color1 = f"({match.color_player_1})"
                sc1    = match.match_score_1 if match.match_score_1 is not None else 0.0
                score1 = f"{sc1:.1f}"

                name2  = f"{p2.first_name} {p2.last_name}"
                id2    = f"[{p2.id_national_chess}]"
                color2 = f"({match.color_player_2})"
                sc2    = match.match_score_2 if match.match_score_2 is not None else 0.0
                score2 = f"{sc2:.1f}"

                groups.append([
                    (name1, id1, color1, score1),
                    (name2, id2, color2, score2),
                ])

        # 3) Calcul des largeurs maximales pour aligner les colonnes
        all_entries = [entry for group in groups for entry in group]
        max_name  = max(len(name)  for name, *_ in all_entries) if all_entries else 0
        max_idn   = max(len(idn)   for _, idn, *_ in all_entries) if all_entries else 0
        max_color = max(len(color) for *_, color, _ in all_entries) if all_entries else 0

        # 4) Construction des lignes finalisées,
        #    en insérant une ligne vide entre chaque match (sauf après le dernier).
        lines: List[str] = []
        lines.append(f"\n{self.round_number} – Matchs :\n")
        for idx, group in enumerate(groups):
            for name, idn, color, score in group:
                pad_name  = " " * (max_name  - len(name))
                pad_idn   = " " * (max_idn   - len(idn))
                pad_color = " " * (max_color - len(color))
                lines.append(f"{name}{pad_name} {idn}{pad_idn} {color}{pad_color} : {score}\n")
            # Ajoute une ligne vide entre deux groupes (deux matchs)
            if idx < len(groups) - 1:
                lines.append("\n")

        return "".join(lines)



    def get_formatted_end_time(self) -> str:
        """Formate end_time en 'DD/MM/YYYY à HH:MM:SS'"""
        return self.end_time.strftime("%d/%m/%Y à %H:%M:%S")
    
    def get_formatted_start_time(self) -> str:
        """Formate end_time en 'DD/MM/YYYY à HH:MM:SS'"""
        return self.start_time.strftime("%d/%m/%Y à %H:%M:%S")

    def get_serialized_round(self) -> dict:
        """
        Sérialise ce round pour JSON,
        en gérant start_time/end_time potentiellement à None.
        """
        return {
            "round_number": self.round_number,
            "start_time":   self.start_time.strftime("%d/%m/%Y %H:%M:%S") if self.start_time else None,
            "end_time":     self.end_time.strftime("%d/%m/%Y %H:%M:%S")   if self.end_time   else None,
            "matches":      [match.get_serialized_match() for match in self.matches]
        }