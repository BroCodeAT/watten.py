import socket

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
            turns : The amount of turns this team won (default: 0)
    team2 : dict[str, list | int]
        The stats of the Second team
        values :
            player : The list of players in this team (default: [])
            rounds : The amount of rounds this team won (default: 0)
            points : The points in one round this team currently has (default: 0)
            turns : The amount of turns this team won (default: 0)
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

        self.played_cards: list[CardBase] = []

        self.team1: dict = {
            "player": [],
            "rounds": 0,
            "points": 0,
            "turns": 0
        }
        self.team2: dict = {
            "player": [],
            "rounds": 0,
            "points": 0,
            "turns": 0
        }

        self.game_player: dict[str, PlayerData] = {}
        self.turn_loop: list[str] = []
        self.last_won_point: list[str] = None

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


class ClientData:
    """
    A class to represent a Client including all the needed client Data.

    ...

    Attributes
    ----------
    name : str
        The name of the Client
    conn : socket.socket (default: None)
        The connection to the Client
    addr : tuple[str, int] (default: None)
        The address the connection was established to (client side)

    ClassMethod
    -----------
    new_conn(name: str, conn: socket.socket, addr: tuple[str, int]) -> ClientData
        Create a new Data object using the given parameters
    """
    def __init__(self, name: str, conn: socket.socket = None, addr: tuple[str, int] = None):
        """
        Initialize all necessary attributes for the client object

        Parameters
        ----------
        name : str
            The name of the Client
        conn : socket.socket (default: None)
            The connection to the Client
        addr : tuple[str, int] (default: None)
            The address the connection was established to (client side)
        """
        self.name: str = name
        self.conn: socket.socket | None = conn
        self.addr: tuple[str, int] | None = addr

    @classmethod
    def new_conn(cls, name: str, conn: socket.socket, addr: tuple[str, int]) -> "ClientData":
        """
        A new connection was established and all the wanted data is saved in this object

        Parameters
        ----------
        name : str
            The name of the Client
        conn : socket.socket (default: None)
            The connection to the Client
        addr : tuple[str, int] (default: None)
            The address the connection was established to (client side)

        Returns
        -------
        ClientData : The new ClientData object
        """
        return cls(
            name,
            conn,
            addr
        )
