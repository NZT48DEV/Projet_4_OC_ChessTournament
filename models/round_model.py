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
        Génère les appariements pour le round selon la logique suisse :
        1) Trier par tournament_score, mélanger ex-aequos.
        2) Tenter d’apparier sans rematch.
        3) Si nombre impair, donner un bye (0.5 pt) au plus faible (jamais exempté d’abord).
        4) Forcer les rematches en dernier recours.
        """
        # 1) Préparation du pool trié + mélange ex-æquos
        sorted_players = sorted(players, key=lambda p: p.tournament_score, reverse=True)
        pool: List[Player] = []
        groups: Dict[float, List[Player]] = {}
        for p in sorted_players:
            groups.setdefault(p.tournament_score, []).append(p)
        for grp in groups.values():
            random.shuffle(grp)
            pool.extend(grp)

        paired: Set[Player] = set()           # joueurs déjà appariés
        unpaired: List[Player] = []            # joueurs restants

        # 2) Première passe : appariements sans rematch
        for player_1 in pool:
            if player_1 in paired:
                continue
            found = False
            for player_2 in pool:
                if player_2 in paired or player_2 is player_1:
                    continue
                if player_2.id_national_chess in player_1.played_with:
                    continue
                # on appaire player_1/player_2
                paired.update({player_1, player_2})
                player_1.played_with.append(player_2.id_national_chess)
                player_2.played_with.append(player_1.id_national_chess)
                self.add_match(Match(f"{self.round_number} - Match", (player_1, player_2)))
                found = True
                break
            if not found:
                unpaired.append(player_1)

        # 3) Bye si nombre impair
        if len(unpaired) % 2 == 1:
            # ne choisir que parmi ceux qui n'ont pas encore eu de bye
            candidates = [p for p in unpaired if "tour de repos" not in p.played_with]
            if not candidates:
                candidates = unpaired  # si tous ont déjà eu un bye
            # choisir le plus faible score (ou random si ex-æquos)
            bye_player: Player = min(candidates, key=lambda p: p.tournament_score)
            bye_player.tournament_score += 0.5
            bye_player.played_with.append("tour de repos")
            unpaired.remove(bye_player)
            # enregistrer le “match” de repos
            self.add_match(Match(f"{self.round_number} - Repos", (bye_player, None)))

        # 4) Deuxième passe : appariements restants (rematch forcé si nécessaire)
        while len(unpaired) >= 2:
            player_1 = unpaired.pop(0)
            player_2 = None
            # tenter un adversaire sans rematch, sinon prendre premier
            for candidate in unpaired:
                if candidate.id_national_chess not in player_1.played_with:
                    player_2 = candidate
                    break
            if player_2 is None:
                player_2 = unpaired[0]  # rematch forcé
            unpaired.remove(player_2)

            # appairer player_1/player_2
            paired.update({player_1, player_2})
            player_1.played_with.append(player_2.id_national_chess)
            player_2.played_with.append(player_1.id_national_chess)
            # marquer si rematch
            name = f"{self.round_number} - Match"
            if player_2.id_national_chess in player_1.played_with[:-1]:  # si déjà rencontré
                name += " (rematch)"
            self.add_match(Match(name, (player_1, player_2)))


    def get_round_report(self) -> str:
        """Retourne un rapport textuel brut des matchs"""
        lines = [f"\n{self.round_number} - Matchs:\n"]
        for match in self.matches:
            lines.append(f"{repr(match)}\n")
        return "\n".join(lines)

    def get_formatted_end_time(self) -> str:
        """Formate end_time en 'DD/MM/YYYY à HH:MM:SS'"""
        return self.end_time.strftime("%d/%m/%Y à %H:%M:%S")

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