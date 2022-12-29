import math
from typing import Tuple

COL = ["Schell", "Herz", "Eichel", "Laub"]
NUM = ["VII", "VIII", "IX", "X", "Unter", "Ober", "König", "Ass"]


def convert_to_readable(card_id: int) -> tuple[str, str]:
    """
    Convert the ID of a card to a human-readable version

    Parameters
    ----------
    card_id : int
        The ID of the card to convert

    Returns
    -------
    tuple[str]: a tuple (len=2) including the Color and the Number
    """
    if card_id == 32:
        return "Schell", "Weli"
    return get_card_col(card_id), get_card_num(card_id)


def get_card_col(card_id: int, representation: bool = True, integer: bool = False) -> str | int | tuple[str, int]:
    """
    Convert the ID of a card to different types of representations of the color

    Parameters
    ----------
    card_id : int
        The ID of the card to get the color of
    representation : bool (default: True)
        If you want the human-readable representation of the Card
    integer : bool (default: False)
        If you want the integer representation of the Color of the Card

    Returns
    -------
    str : The human-readable representation of the Color of the Card
    int : The integer representation of the Color of the Card
    str, int : The human-readable representation and the integer representation of the Color of the Card
    """
    if card_id == 32:
        if integer and representation:
            return "Schell", 0
        elif integer:
            return 0
        else:
            return "Schell"
    if integer and representation:
        return COL[math.floor(int(card_id) / 8)], math.floor(int(card_id) / 8)
    elif integer:
        return math.floor(int(card_id) / 8)
    else:
        return COL[math.floor(int(card_id) / 8)]


def get_card_num(card_id, representation: bool = True, integer: bool = False) -> str | int | tuple[str, int]:
    """
    Convert the ID of a card to different types of representations of the number

    Parameters
    ----------
    card_id : int
        The ID of the card to get the number of
    representation : bool (default: True)
        If you want the human-readable representation of the Number of the Card
    integer : bool (default: False)
        If you want the integer representation of the Number of the Card

    Returns
    -------
    str : The human-readable representation of the Number of the Card
    int : The integer representation of the Number of the Card
    str, int : The human-readable representation and the integer representation of the Number of the Card
    """
    if card_id == 32:
        if integer and representation:
            return "Weli", -1
        elif integer:
            return -1
        else:
            return "Weli"
    if integer and representation:
        return NUM[(int(card_id) % 8)], int(card_id) % 8
    elif integer:
        return int(card_id) % 8
    else:
        return NUM[(int(card_id) % 8)]
