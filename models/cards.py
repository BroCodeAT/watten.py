from common.cards import *


class CardBase:
    def __init__(self, card_id: int):
        """
        The Base Class of a Card to represent a Playing-Card

        :param card_id: The id of the card
        """
        self.card_id: int = card_id

    def __int__(self):
        # Returns the id of the given card
        return int(self.card_id)

    def __repr__(self):
        # Returns the representation of the given card
        color, name = convert_to_readable(int(self))
        return f"<CardBase color={color}, name={name}>"

    def __eq__(self, other):
        # Checks if a card has the same color as another one
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

    def __gt__(self, other):
        if isinstance(other, CardBase):
            if other == self:
                if (self.num()) > (other.num()):
                    return True
                else:
                    return False
            return False
        else:
            raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, CardBase):
            if other == self:
                if (self.num()) < (other.num()):
                    return True
                else:
                    return False
            return False
        else:
            raise NotImplementedError

    def col(self):
        if self.card_id == -1:
            return -1
        elif self.card_id == 32:
            return 0
        else:
            return math.floor(int(self.card_id)/8) + 1

    def num(self):
        if self.card_id == -1:
            return -1
        elif self.card_id == 32:
            return 0
        else:
            return (int(self.card_id) % 8) + 1

    @classmethod
    def new_card(cls, col: int, num: int):
        if col == -1 and num == -1:
            return cls(-1)
        elif col == 0 and num == 0:
            return cls(32)
        else:
            return cls((col - 1) * 8 + num - 1)


class CardDek:
    def __init__(self, cards: list[CardBase], cards_q: queue.Queue):
        """
        Create a new deck of Cards

        :param cards: The list of cards a Dek includes
        """
        self.cards: list[CardBase] = cards
        self.cards_queue: queue.Queue[CardBase] = cards_q

    def __repr__(self):
        return f"<CardDek cards=len({len(self.cards)})>"

    def __iter__(self):
        return self.cards

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        return len(self.cards)

    def deal_top_card(self, cards=1) -> list[CardBase]:
        """
        Return an amount of cards and delete them from the deck

        :param cards: The amount of cards
        :return: The selected cards
        """
        tc = []
        for i in range(cards):
            tc.append(self.cards_queue.get())
        self.cards = self.cards[cards:]
        return tc

    @staticmethod
    def mix(cards: list[CardBase]) -> list[CardBase]:
        """
        Mix a deck of cards

        :param cards: The dek of cards to mix
        :return: The mixed dek
        """
        random.shuffle(cards)
        return cards

    @classmethod
    def get_mixed_dek(cls):
        """
        Returns mixed Card Dek

        :return: CardDek object with mixed cards
        """
        cards = cls.mix([CardBase(i) for i in range(33)])
        q = queue.Queue(maxsize=33)
        for c in cards:
            q.put(c)
        return cls(cards=cards, cards_q=q)