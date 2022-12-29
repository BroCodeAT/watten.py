import math

COL = ["Schell", "Herz", "Eichel", "Laub"]
NUM = ["VII", "VIII", "IX", "X", "Unter", "Ober", "König", "Ass"]


def convert_to_readable(card_id):
    if card_id == 32:
        return "Schell", "Weli"
    return get_card_col(card_id), get_card_num(card_id)


def get_card_col(card_id, representation: bool = True, integer: bool = False) -> str | int | tuple[str, int]:
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
