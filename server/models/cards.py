import random
import queue

from typing import Union

from cards_utils import *


class CardBase:
    """
    A class to represent a Card

    Color-Code:
     0 - Schell
     1 - Herz
     2 - Eichel
     3 - Laub

    Number-Code:
    -1 - VI
     0 - VII
     1 - VIII
     2 - IX
     3 - X
     4 - Unter
     5 - Ober
     6 - König
     7 - Ass

    ...

    Attributes
    ----------
    card_id : int
        The ID of the Card this object represents

    Methods
    -------
    col() -> int
        Return the integer representation of the color of the card

    num() -> int
        Return the integer representation of the number of the card

    ClassMethods
    ------------
    new_card(col: int, num: int) -> CardBase
        Get a new Card with the given number and Color
    """
    def __init__(self, card_id: int):
        """
        The initialization of a Card to represent a Playing-Card

        Parameters
        ----------
        card_id : int
            The ID of the Card
        """
        self.card_id: int = card_id

    def __int__(self) -> int:
        """
        Returns the ID of the given card

        Returns
        -------
        int : The ID of the given Card
        """
        return int(self.card_id)

    def __repr__(self) -> str:
        """
        Returns the representation of the given card

        Returns
        -------
        str : Representation of the given card
        """
        color, name = convert_to_readable(int(self))
        return f"<CardBase color={color}, name={name}>"

    def __eq__(self, other: Union["CardBase", int]) -> bool:
        """
        Checks if a card has the same color as another one

        Parameters
        ----------
        other : CardBase | int
            The other card or the integer representation of a color

        Returns
        -------
        bool : If the cards have the same color
        """
        if isinstance(other, CardBase):
            if math.floor(self.col()) == math.floor(other.col()):
                return True
            else:
                return False
        elif isinstance(other, int):
            if math.floor(self.card_id / 8) == math.floor(other / 8):
                return True
            else:
                return False
        else:
            raise NotImplementedError

    def __gt__(self, other: "CardBase") -> bool:
        """
        Check if the color of the cards are the same
        if so ->
        Check if the number of the given card is bigger than the other


        Parameters
        ----------
        other : CardBase
            The card to do the check on

        Returns
        -------
        bool : If other card beats the given card
        """
        if isinstance(other, CardBase):
            if other == self:
                if (self.num()) > (other.num()):
                    return True
                else:
                    return False
            return False

    def __lt__(self, other: "CardBase") -> bool:
        """
        Check if the color of the cards are the same
        if so ->
        Check if the number of the given card is smaller than the other


        Parameters
        ----------
        other : CardBase
            The card to do the check on

        Returns
        -------
        bool : If other card doesn't beat the given card
        """
        if isinstance(other, CardBase):
            if other == self:
                if (self.num()) < (other.num()):
                    return True
                else:
                    return False
            return False

    def col(self) -> int:
        """
        Resolve the Color of the given card

        Returns
        -------
        int : The Color of the Card
        """
        if self.card_id == -1:
            return -1
        elif self.card_id == 32:
            return 0
        else:
            return math.floor(int(self.card_id)/8) + 1

    def num(self) -> int:
        """
        Resolve the Number of the given card

        Returns
        -------
        int : The Number of the Card
        """
        if self.card_id == -1:
            return -1
        elif self.card_id == 32:
            return 0
        else:
            return (int(self.card_id) % 8) + 1

    @classmethod
    def new_card(cls, col: int, num: int) -> "CardBase":
        """
        Get a new card with the given color and number

        Parameters
        ----------
        col : int
            The color of the new card
        num : int
            The number of the new card
        """
        if col == -1 and num == -1:
            return cls(-1)
        elif col == 0 and num == 0:
            return cls(32)
        else:
            return cls((col - 1) * 8 + num - 1)


class CardDek:
    """
    A class to represent a CardDek

    ...

    Attributes
    ----------
    cards : list[CardBase]
        A list of all the cards in the dek
    cards_queue : queue.Queue
        A queue of all the cards in the dek (necessary to deal the top cards)

    Methods
    -------
    deal_top_card(cards=1) -> list[CardBase]
        Deal 'cards' of Cards to a player

    StaticMethods
    -------------
    mix(cards: list[CardBase]) -> list[CardBase]
        Mix a dek of cards and return the list

    ClassMethods
    ------------
    get_mixed_dek() -> CardDek
        Get a new mixed dek of cards
    """
    def __init__(self, cards: list[CardBase]):
        """
        Create a new deck of Cards

        :param cards: The list of cards a Dek includes
        """
        self.cards: list[CardBase] = cards
        self.cards_queue: queue.Queue = queue.Queue()
        for card in cards:
            self.cards_queue.put(card)

    def __repr__(self) -> str:
        """
        Return the representation of the card dek

        Returns
        -------
            str: The representation of the card dek
        """
        return f"<CardDek cards=len({len(self.cards)})>"

    def __iter__(self) -> list:
        """
        Get the list of the Cards as an iterable

        Returns
        -------
            list[CardBase]: The current cards of the player
        """
        return self.cards

    def __getitem__(self, item: int) -> CardBase:
        """
        Get the 'item' list of the cards list

        Parameters
        ----------
            item: int
                The index of the card you want to get

        Returns
        -------
            CardBase: The card you wanted to get
        """
        return self.cards[item]

    def __len__(self) -> int:
        """
        Get the length of the cards list

        Returns
        -------
            int: The length of the cards list
        """
        return len(self.cards)

    def deal_top_card(self, cards=1) -> list[CardBase]:
        """
        Returns a given amount of cards,
        Remove the cards from the dek

        Parameters
        ----------
        cards : int (default: 1)
            The amount of cards to deal

        Returns
        -------
            list[CardBase]: The cards that were delt
        """
        tc = []
        for i in range(cards):
            tc.append(self.cards_queue.get())
        self.cards = self.cards[cards:]
        return tc

    @staticmethod
    def mix(cards: list[CardBase]) -> list[CardBase]:
        """
        Mix the current dek of cards

        Parameters
        ----------
        cards: list[CardBase]
            The dek of cards to mix

        Returns
        -------
            list[CardBase] : The mixed card dek
        """
        random.shuffle(cards)
        return cards

    @classmethod
    def get_mixed_dek(cls):
        """
        Returns mixed Card Dek

        Returns
        -------
            CardDek: Mixed card Dek
        """
        cards = cls.mix([CardBase(i) for i in range(33)])
        return cls(cards=cards)
