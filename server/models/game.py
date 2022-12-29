import pygame

from models.cards import CardDek, CardBase


class GameData:
    def __init__(self):
        self.card_dek: CardDek | None = None

        self.played_cards: List[CardBase] = []

        self.team1: dict = {
            "player": [],
            "rounds": 0,
            "points": 0
        }
        self.team2: dict = {
            "player": [],
            "rounds": 0,
            "points": 0
        }

        self.game_player: dict[str, dict[str, list]] = {}
        self.game_loop: list[str] = []

        self.highest: CardBase | None = None

    def mixed_dek(self):
        self.card_dek = CardDek.get_mixed_dek()
