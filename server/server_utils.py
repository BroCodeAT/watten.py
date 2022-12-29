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
