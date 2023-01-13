import random
import time

from models import GameData, CardBase, PlayerData
from server_utils import check_available, check_winner
from server_network import NetworkServer


class GameLogic:
    """
    A class to handle the logic of the game

    Synonyms:
        round -> playing until one team has 11 points
        point -> playing five turns -> all cards (team with 3 turns won get a point)
        turn -> every player plays one card

    ...

    Attributes
    ----------
    server : NetworkServer
    game_data : GameData

    Methods
    -------
    setup() -> None
        Setup the game
    start_game_loop() -> None
        Start rounds until the players stop playing
    start_new_round(self) -> None
        Check if a team won 11 points and start new points
    start_for_new_points() -> None
        Mixing the dek, dealing the cards and playing one point
    start_player_turns() -> None
        Wait for every client to do their turn
    deal_round() -> None
        Deal 5 cards to the clients
    get_highest(send: bool = True) -> None
        Update the current highest card and send it if wanted
    ask_for_start(delay: int = 10) -> None
        Wait 'delay' seconds for the first and the last player to approve their cards
    handle_all_responses(self) -> None
        Handle every open command from the queue
    handle_response(data: dict) -> None
        Handle a command received from a client
    better_cards() -> None
        The server deals new cards to the first and the last player
    """
    def __init__(self, auto_setup: bool = True):
        """
        Initialize a new Game

        Parameters
        ----------
        auto_setup : bool (default: True)
            If the setup method should start automatically
        """
        self.server = NetworkServer()
        self.game_data = GameData()

        if auto_setup:
            self.setup()

    def setup(self) -> None:
        """
        Setup the game

        accept_clients, divide the clients into teams, send the names of the clients to every player

        Returns
        -------

        """
        self.server.accept_clients()
        gl = list(self.server.clients)
        self.game_data.turn_loop = gl
        self.game_data.turn_loop = gl
        self.game_data.team1["player"] = [gl[0], gl[2]]
        self.game_data.team2["player"] = [gl[1], gl[3]]

        for index, client in enumerate(self.game_data.turn_loop):
            self.server.send_to("PLAYER_NAMES", client, players=self.game_data.turn_loop[index:] + self.game_data.turn_loop[:index])

    def start_game_loop(self) -> None:
        """
        Start rounds until the players stop playing

        Returns
        -------
        None
        """
        while True:
            self.start_new_round()

    def start_new_round(self) -> None:
        """
        Check if a team won 11 points and start new points

        when 11 points are reached,
        the round attribute of the team is raised and another round starts

        Returns
        -------
        None
        """
        while not (self.game_data.team1.get("points") >= 11 or self.game_data.team2.get("points") >= 11):
            self.start_for_new_points()

        if self.game_data.team1.get("points") > self.game_data.team2.get("points"):
            self.game_data.team1["rounds"] += 1

            start_player: str = random.choice(self.game_data.team2.get("player"))
            start_index = self.game_data.turn_loop.index(start_player)
            self.game_data.turn_loop = self.game_data.turn_loop[start_index:] + self.game_data.turn_loop[:start_index]

            self.server.send_all("ROUND_WINNER", winner=self.game_data.team1.get("player"))
        else:
            self.game_data.team2["rounds"] += 1
            self.game_data.last_won_point = self.game_data.team2.get("player")

            start_player: str = random.choice(self.game_data.team1.get("player"))
            start_index = self.game_data.turn_loop.index(start_player)
            self.game_data.turn_loop = self.game_data.turn_loop[start_index:] + self.game_data.turn_loop[:start_index]

            self.server.send_all("ROUND_WINNER", winner=self.game_data.team2.get("player"))

        self.game_data.team1["points"] = 0
        self.game_data.team2["points"] = 0

    def start_for_new_points(self) -> None:
        """
        Mixing the dek, dealing the cards and playing one point

        Returns
        -------
        None
        """
        self.game_data.mixed_dek()
        self.deal_round()
        self.get_highest()
        # self.ask_for_start()
        for i in range(5):
            self.start_player_turns()
            self.resolve_turn_winner()

        if self.game_data.team1.get("turns") > self.game_data.team2.get("turns"):
            self.game_data.team1["points"] += 2
            self.server.send_all("POINT_WINNER", winner=self.game_data.team1.get("player"))
        else:
            self.game_data.team2["points"] += 2
            self.server.send_all("POINT_WINNER", winner=self.game_data.team2.get("player"))

        self.game_data.team1["turns"] = 0
        self.game_data.team2["turns"] = 0

    def start_player_turns(self) -> None:
        """
        Wait for every client to do their turn
        (order: game_loop)

        Returns
        -------
        None
        """
        for client in self.game_data.turn_loop:
            available_cards = check_available(
                self.game_data.game_player.get(client).cards,
                self.game_data.played_cards,
                self.game_data.highest,
                True if list(self.game_data.turn_loop).index(client) in [0, 3] else False
            )
            self.server.send_to("PLAYER_TURN", client, available=list(map(int, available_cards)))
            data = self.server.receive_from_client(client)
            self.handle_response(data)
            # input("turn")

    def deal_round(self) -> None:
        """
        Deal 5 cards to the clients
        (First 3 then 2)

        Returns
        -------
        None
        """
        # Dealing the cards to the client (serverside)
        for cards in [3, 2]:
            for client in self.game_data.turn_loop:
                deal_cards = self.game_data.card_dek.deal_top_card(cards)
                try:
                    self.game_data.game_player[client].cards.extend(deal_cards)
                except KeyError:
                    data = PlayerData(client)
                    data.cards.extend(deal_cards)
                    self.game_data.game_player[client] = data

        # sending cards to clients
        for client in self.server.clients:
            cards_to_send = self.game_data.game_player[client].cards
            self.server.send_to("NEW_CARD", client, cards=list(map(int, cards_to_send)))

    def get_highest(self, send: bool = True) -> None:
        """
        Update the current highest card and send it if wanted

        Parameters
        ----------
        send : bool (default: True)
            If the highest card should be sent to the first and the last player

        Returns
        -------
        None
        """
        self.game_data.highest = CardBase.new_card(
            self.game_data.game_player[self.game_data.turn_loop[-1]].cards[0].col(),
            self.game_data.game_player[self.game_data.turn_loop[0]].cards[0].num()
        )
        if send:
            self.server.send_to("HIGHEST", self.game_data.turn_loop[-1], highest=int(self.game_data.highest))
            self.server.send_to("HIGHEST", self.game_data.turn_loop[0], highest=int(self.game_data.highest))

    def ask_for_start(self, delay: int = 10) -> None:
        """
        Wait 'delay' seconds for the first and the last player to approve their cards

        Returns
        -------
        None
        """
        players = [self.game_data.turn_loop[0], self.game_data.turn_loop[-1]]
        self.server.allow_responses_from(*players)
        time.sleep(delay)
        self.server.stop_responses()
        self.handle_all_responses()

    def handle_all_responses(self) -> None:
        """
        Handle every open command from the queue

        Returns
        -------
        None
        """
        while self.server.que.not_empty:
            self.handle_response(self.server.que.get())

    def handle_response(self, data: dict) -> None:
        """
        Handle a command received from a client

        Parameters
        ----------
        data : dict
            The data of the command to handle

        Returns
        -------
        None
        """
        print(data)
        if not data:
            return
        match data.get("command"):
            case "PLAY_CARD":
                self.game_data.played_cards.append(CardBase(data.get("card")))
                int_cards = list(map(int, self.game_data.game_player.get(data.get("from")).cards))
                index = int_cards.index(data.get("card"))
                self.game_data.game_player.get(data.get("from")).cards.pop(index)
                self.server.send_all("UPDATE_TURN", played=tuple(map(int, self.game_data.played_cards)), last_played=data.get("from"))
            case "BETTER_CARDS":
                pass

    def better_cards(self) -> None:
        """
        The server deals new cards to the first and the last player

        The players did not like their cards

        Returns
        -------
        None
        """
        for cards in [3, 2]:
            for client in [self.game_data.turn_loop[0], self.game_data.turn_loop[-1]]:
                deal_cards = self.game_data.card_dek.deal_top_card(cards)
                self.game_data.game_player[client].cards = []
                self.game_data.game_player[client].cards.extend(deal_cards)

    def resolve_turn_winner(self):
        winner_index = check_winner(self.game_data.played_cards, self.game_data.highest)
        self.server.send_all("TURN_WINNER", winner=list(self.game_data.turn_loop)[winner_index])
        self.game_data.turn_loop = self.game_data.turn_loop[winner_index:] + self.game_data.turn_loop[:winner_index]
        self.game_data.played_cards = []
