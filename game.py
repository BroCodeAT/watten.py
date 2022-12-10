from server import NetworkServer
from cards import *
import json

server = NetworkServer()
server.accept_clients()

card_dek: CardDek | None = None
player: dict = {}

playing = True

while playing:
    card_dek = CardDek.get_mixed_dek()
    for cards in [3, 2]:
        for client in server.clients:
            deal_cards = card_dek.deal_top_card(cards)
            player_name = server.clients[client]["name"]
            try:
                player[player_name]["cards"].append(deal_cards)
            except KeyError:
                player[player_name] = {"cards": deal_cards}
            server.send_to("NEW_CARD", client, cards=deal_cards)
