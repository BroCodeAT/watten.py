import pygame


class ClientGameData:
    def __init__(self):
        self.username: str = ""
        self.player_names: list[str] = []

        self.card_ids: list[int] = []

        self.game_display = pygame.display.set_mode((1000, 700))
        self.player_cards_surfaces = {}
