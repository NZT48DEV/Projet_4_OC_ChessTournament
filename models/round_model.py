import datetime
import random
from typing import Dict, List, Set, Tuple

from models.match_model import Match
from models.player_model import Player


class Round:
    """
    Représente un tour (round) d'un tournoi d'échecs.
    Gère la génération des appariements selon la méthode suisse,
    l'enregistrement des horaires et la sérialisation.
    """

    def __init__(self, round_number: str) -> None:
        """
        Initialise un Round.

        Args:
            round_number: Identifiant textuel du tour (ex: "Round 1").
        """
        self.round_number: str = round_number
        self.matches: List[Match] = []
        self.start_time: datetime.datetime | None = None
        self.end_time: datetime.datetime | None = None

    def generate_pairings(self, players: List[Player]) -> None:
        """
        Génère les appariements pour ce round selon la logique suisse :
          1) Trie par score, mélange par ex-æquo.
          2) Si nombre impair, crée un bye pour un joueur admissible.
          3) Appariements sans rematch.
          4) En dernier recours, force rematch.

        Args:
            players: Liste des joueurs participants.
        """
        pool = self._build_shuffled_pool(players)
        if len(pool) % 2 == 1:
            self._create_bye(players, pool)
        self._pair_players(pool)

    def _build_shuffled_pool(self, players: List[Player]) -> List[Player]:
        """
        Trie les joueurs par score descendant, mélange les ex-æquo.
        """
        groups: Dict[float, List[Player]] = {}
        for p in players:
            groups.setdefault(p.tournament_score, []).append(p)
        pool: List[Player] = []
        for score, grp in sorted(groups.items(), key=lambda x: -x[0]):
            random.shuffle(grp)
            pool.extend(grp)
        return pool

    def _create_bye(self, players: List[Player], pool: List[Player]) -> None:
        """
        Crée et enregistre un match de repos pour un joueur admissible.
        Met à jour le classement dense et prend un snapshot.
        """
        candidates = [p for p in pool if "tour de repos" not in p.played_with]
        if not candidates:
            candidates = pool
        bye_player = min(candidates, key=lambda p: p.tournament_score)
        bye_player.played_with.append("tour de repos")
        bye_match = Match(f"{self.round_number} - Repos", (bye_player, None))
        # mise à jour des ranks dense
        ranked = sorted(players, key=lambda p: p.tournament_score, reverse=True)
        prev_score = None
        prev_rank = 0
        dense_rank = 1
        for p in ranked:
            if prev_score is None or p.tournament_score < prev_score:
                prev_score = p.tournament_score
                prev_rank = dense_rank
                dense_rank += 1
            p.rank = prev_rank
        # snapshot et ajout
        bye_match.snapshot()
        self.add_match(bye_match)
        pool.remove(bye_player)

    def _pair_players(self, pool: List[Player]) -> None:
        """
        Apparie les joueurs restants en deux passes :
        - d'abord sans rematch
        - ensuite en forçant les rematchs si nécessaire
        """
        paired, unpaired = self._pair_without_rematch(pool)
        self._pair_with_rematch(unpaired, paired)

    def _pair_without_rematch(self, pool: List[Player]) -> Tuple[Set[Player], List[Player]]:
        """
        Tente de créer des matchs sans rematch entre joueurs.

        Args:
            pool: Liste des joueurs à apparier.

        Returns:
            Un tuple contenant :
            - le set des joueurs déjà appariés
            - la liste des joueurs restants non appariés
        """
        paired: Set[Player] = set()
        unpaired: List[Player] = []

        for p1 in pool:
            if p1 in paired:
                continue
            for p2 in pool:
                if p2 in paired or p2 is p1:
                    continue
                if p2.id_national_chess in p1.played_with:
                    continue
                paired.update({p1, p2})
                p1.played_with.append(p2.id_national_chess)
                p2.played_with.append(p1.id_national_chess)
                self.add_match(Match(f"{self.round_number} - Match", (p1, p2)))
                break
            else:
                unpaired.append(p1)

        return paired, unpaired

    def _pair_with_rematch(self, unpaired: List[Player], paired: Set[Player]) -> None:
        """
        Force des appariements même s'ils impliquent un rematch.

        Args:
            unpaired: Liste de joueurs non appariés après la première passe.
            paired: Set des joueurs déjà appariés.
        """
        while len(unpaired) >= 2:
            p1 = unpaired.pop(0)
            p2 = next((c for c in unpaired if c.id_national_chess not in p1.played_with), None)
            if p2 is None:
                p2 = unpaired[0]
            unpaired.remove(p2)
            paired.update({p1, p2})
            p1.played_with.append(p2.id_national_chess)
            p2.played_with.append(p1.id_national_chess)
            self.add_match(Match(f"{self.round_number} - Rematch", (p1, p2)))

    def add_match(self, match: Match) -> None:
        """
        Ajoute un match au round.

        Args:
            match: Instance de Match à ajouter.
        """
        self.matches.append(match)

    def start_round(self) -> None:
        """
        Définit l'heure de début du round à maintenant.
        """
        self.start_time = datetime.datetime.now()

    def end_round(self) -> None:
        """
        Définit l'heure de fin du round à maintenant.
        """
        self.end_time = datetime.datetime.now()

    def get_formatted_start_time(self) -> str:
        """
        Format 'DD/MM/YYYY à HH:MM:SS'.
        """
        return self.start_time.strftime("%d/%m/%Y à %H:%M:%S")

    def get_formatted_end_time(self) -> str:
        """
        Format 'DD/MM/YYYY à HH:MM:SS'.
        """
        return self.end_time.strftime("%d/%m/%Y à %H:%M:%S")

    def get_serialized_round(self) -> dict:
        """
        Prépare l’objet pour sérialisation JSON,
        avec start_time et end_time en str ou None.
        """
        return {
            "round_number": self.round_number,
            "start_time": self.start_time.strftime("%d/%m/%Y %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%d/%m/%Y %H:%M:%S") if self.end_time else None,
            "matches": [m.get_serialized_match() for m in self.matches]
        }
