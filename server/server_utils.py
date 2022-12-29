from models import CardBase
from typing import List


def check_available(player_cards: List[CardBase], already_played: List[CardBase], highest: CardBase, know: bool = True):
    if already_played:
        if know:
            if already_played[0] == highest:
                playable = [card for card in player_cards if card == highest]
                if playable:
                    return playable
    return player_cards
