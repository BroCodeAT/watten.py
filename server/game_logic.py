from models import GameData, CardBase
from server_network import NetworkServer


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
        while not (self.game_data.team1.get("points") >= 11 or self.game_data.team2.get("points") >= 11):
            self.start_for_new_points()

        self.server.send_all("SO_LOS_GEHTS")

        input("Debug")

    def start_for_new_points(self):
        self.game_data.mixed_dek()
        self.deal_round()
        self.get_highest()

        input("DEBUG")

    def start_playing_cards(self):
        pass

    def deal_round(self):
        # Dealing the cards to the client (serverside)
        for cards in [3, 2]:
            for client in self.game_data.game_loop:
                deal_cards = self.game_data.card_dek.deal_top_card(cards)
                try:
                    self.game_data.game_player[client]["cards"].extend(deal_cards)
                except KeyError:
                    self.game_data.game_player[client] = {"cards": deal_cards}

        # sending cards to clients
        for client in self.server.clients:
            cards_to_send = self.game_data.game_player[client]["cards"]
            self.server.send_to("NEW_CARD", client, cards=list(map(int, cards_to_send)))

    def get_highest(self, send: bool = True):
        self.game_data.highest = CardBase.new_card(
            self.game_data.game_player[self.game_data.game_loop[-1]]["cards"][3].col(),
            self.game_data.game_player[self.game_data.game_loop[0]]["cards"][3].num()
        )
        if send:
            self.server.send_to("HIGHEST", self.game_data.game_loop[-1], highest=int(self.game_data.highest))
            self.server.send_to("HIGHEST", self.game_data.game_loop[0], highest=int(self.game_data.highest))

    def better_cards(self):
        for cards in [3, 2]:
            for client in [self.game_data.game_loop[0], self.game_data.game_loop[-1]]:
                deal_cards = self.game_data.card_dek.deal_top_card(cards)
                self.game_data.game_player[client]["cards"] = []
                self.game_data.game_player[client]["cards"].extend(deal_cards)
