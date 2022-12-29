import pygame

from models.cards import CardDek, CardBase


class GameData:
    """
    A class to represent a Game including all the needed game Data.

    ...

    Attributes
    ----------
    card_dek : CardDek | None (default: None)
        The Dek that is currently played on
    played_cards : list[CardBase]
        family name of the person (default: [])
    team1 : dict[str, list | int]
        The stats of the First team
        values :
            player : The list of players in this team (default: [])
            rounds : The amount of rounds this team won (default: 0)
            points : The points in one round this team currently has (default: 0)
    team2 : dict[str, list | int]
        The stats of the Second team
        values :
            player : The list of players in this team (default: [])
            rounds : The amount of rounds this team won (default: 0)
            points : The points in one round this team currently has (default: 0)
    game_player : dict[str, dict[str, list]] (default: {})
        An overview of every player in the game including the PlayerData
    game_loop : list[str]
        A list of the names of the player in order to who plays after who
    highest : CardBase (default: None)
        The highest card (Rechter)

    Methods
    -------
    mixed_dek():
        Receive a new mixed dek of cards and overwrite the old one
    """
    def __init__(self):
        """
        Create all the necessary attributes for the game data.

        """
        self.card_dek: CardDek | None = None

        self.played_cards: List[CardBase] = []

        self.team1: dict = {
            "player": [],
            "rounds": 0,
            "points": 0
        }
        self.team2: dict = {
            "player": [],
            "rounds": 0,
            "points": 0
        }

        self.game_player: dict[str, PlayerData] = {}
        self.game_loop: list[str] = []

        self.highest: CardBase | None = None

    def mixed_dek(self) -> None:
        """
        Create a new mixed dek of cards

 |      Returns
 |      -------
 |      None
        """
        self.card_dek = CardDek.get_mixed_dek()


class PlayerData:
    """
    A class to represent a Player including all the needed player Data.

    ...

    Attributes
    ----------
    name : str
        The name of the Player
    cards : list[CardBase] (default: [])
        The list of the current cards of the player
    """
    def __init__(self, name: str):
        """
        Initialize all necessary attributes for the player object

        Parameters
        ----------
            name : str
                the name of the player
        """
        self.name: str = name
        self.cards: list[CardBase] | None = []
