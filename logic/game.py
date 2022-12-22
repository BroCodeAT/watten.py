import time

from models import GameData
from network import NetworkServer


class GameLogic:
    def __init__(self, auto_setup: bool = True):
        self.server = NetworkServer()
        self.game_data = GameData()

        if auto_setup:
            self.setup()

    def setup(self):
        self.server.accept_clients()
        gl = list(self.server.clients)
        self.game_data.game_loop = gl
        self.game_data.team1["player"] = [gl[0], gl[2]]
        self.game_data.team2["player"] = [gl[1], gl[3]]

        for index, client in enumerate(self.game_data.game_loop):
            self.server.send_to("PLAYER_NAMES", client, players=self.game_data.game_loop[index:] + self.game_data.game_loop[:index])

    def start_game_loop(self):
        while True:
            self.start_new_round()

    def start_new_round(self):
        self.game_data.start()
        self.deal_round()

        self.server.send_all("SO_LOS_GEHTS")

        input("Debug")

    def deal_round(self):
        # Dealing the cards to the client (serverside)
        for cards in [3, 2]:
            for client in self.server.clients:
                deal_cards = self.game_data.card_dek.deal_top_card(cards)
                try:
                    self.game_data.game_player[client]["cards"].extend(deal_cards)
                except KeyError:
                    self.game_data.game_player[client] = {"cards": deal_cards}

        # sending cards to clients
        for client in self.server.clients:
            cards_to_send = self.game_data.game_player[client]["cards"]
            self.server.send_to("NEW_CARD", client, cards=list(map(int, cards_to_send)))