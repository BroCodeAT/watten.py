import json

from cards import *
from server import NetworkServer

server = NetworkServer()
server.accept_clients()

card_dek: CardDek | None = None
player: dict[str, dict[str, list]] = {}

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
        server.send_to("NEW_CARD", client, cards=list(map(int, cards_to_send)))

    server.send_all("SO_LOS_GEHTS")

    input("Debug")
