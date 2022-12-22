from . import CardDek


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
