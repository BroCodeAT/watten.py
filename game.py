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
            try:
                player[server.clients[client]["name"]]["cards"].append(deal_cards)
            except ValueError:
                player[server.clients[client]["name"]] = {"cards": deal_cards}
            server.send_to("NEW_CARD", client, cards=deal_cards)
