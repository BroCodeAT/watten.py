import pygame

from models.cards import CardDek, CardBase


class ClientGameData:
    def __init__(self):
        self.username: str = ""
        self.player_names: list[str] = []

        self.card_ids: list[int] = []

        self.game_display = pygame.display.set_mode((1000, 700))
        self.player_cards_surfaces = {}


class GameData:
    def __init__(self):
        self.card_dek: CardDek | None = None

        self.team1: dict = {
            "player": [],
            "points": 0,
            "games": 0
        }
        self.team2: dict = {
            "player": [],
            "points": 0,
            "games": 0
        }

        self.game_player: dict[str, dict[str, list]] = {}
        self.game_loop: list[str] = []

        self.highest: CardBase | None = None

    def start(self):
        self.card_dek = CardDek.get_mixed_dek()
