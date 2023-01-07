from models import CardBase


def check_available(player_cards: list[CardBase], already_played: list[CardBase], highest: CardBase, know: bool = True) -> list[CardBase]:
    """
    Check which cards the player is allowed to play

    Parameters
    ----------
    player_cards : list[CardBase]
        The list of the cards the player currently owns
    already_played : list[CardBase]
        The cards that were already played
    highest : CardBase
        The current highest card (Rechter)
    know : bool
        If the player knows the highest card

    Returns
    -------
    list[CardBase] : All the cards the player is allowed to play
    """
    if already_played:
        if know:
            if already_played[0] == highest:
                playable = [card for card in player_cards if card == highest]
                if playable:
                    return playable
    return player_cards


def check_winner(played_cards: list[CardBase], highest: CardBase) -> int:
    """
    Check which index won the turn

    Parameters
    ----------
    played_cards : list[CardBase]
        All the played cards in the current turn
    highest : CardBase
        The current highest card

    Returns
    -------
    int : The index of the card that won the turn
    """
    current_highest = played_cards[0]
    for card in played_cards[1:]:
        # Check if the played_card is some type of the highest
        if card.num() == highest.num():
            # If the card is the highest
            if card == highest:
                return played_cards.index(card)
            else:
                # If the card is one of the highest and
                # the current highest is not one of the highest
                if current_highest.num() != highest.num():
                    current_highest = card
        else:
            # If the card is bigger than the current highest and
            # has the same color
            if card > current_highest and current_highest.num() != highest.num():
                current_highest = card
            else:
                # the current highest is not the highest color and
                # the card is one of the highest color
                if card.col() == highest.col() and current_highest.col() != highest.col() and current_highest.num() != highest.num():
                        current_highest = card
                else:
                    pass

    return played_cards.index(current_highest)
