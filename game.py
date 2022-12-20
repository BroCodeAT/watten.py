import json

from cards import *
from utils import check_available
from server import NetworkServer

server = NetworkServer()

card_dek: CardDek | None = None
player: dict[str, dict[str, list]] = {}
cur_player_index: int | None = None
cur_player: dict[str, list] = {}
highest: CardBase | None = None
highest_col: int | None = None
highest_num: int | None = None

if __name__ == '__main__':
    server.accept_clients()
    playing = True

    while playing:
        card_dek = CardDek.get_mixed_dek()

        # dealing cards
        for cards in [3, 2]:
            for client in server.clients:
                deal_cards = card_dek.deal_top_card(cards)
                player_name = server.clients[client]["name"]
                try:
                    player[player_name]["cards"].extend(deal_cards)
                except KeyError:
                    player[player_name] = {"cards": deal_cards}

        # sending cards to clients
        for client in server.clients:
            player_name = server.clients[client]["name"]
            cards_to_send = player[player_name]["cards"]
            player_list = list(player)
            player_index = player_list.index(player_name)
            server.send_to("PLAYER_NAMES", client, players=player_list[player_index:] + player_list[:player_index])
            server.send_to("NEW_CARD", client, cards=list(map(int, cards_to_send)))

        # for rounds in range(5):
        #     round_played = []
        #     for turns in range(4):
        #         if cur_player_index:
        #             cur_player_index += 1
        #         else:
        #             cur_player_index = 0
        #
        #         cur_player = player.get(list(player)[cur_player_index])
        #         server.send_to("PLAYER_TURN", list(server.clients)[cur_player_index], available=check_available(cur_player["cards"], round_played))


        server.send_all("SO_LOS_GEHTS")

        input("Debug")
