import pygame

import client_utils as utils

from client_network import NetworkClient
from client_models import ClientGameData


class ClientLogic:
    """
    A class to handle the logic of the game (client side)

    ...

    Attributes
    ----------
    clock: pygame.time.Clock (default: None)
        The pygame clock the game is synced to
    client: NetworkClient
        The network part of the client
    game_data: ClientGameData
        The data the game needs ot be playable
    debug : bool
        If the client should send debug messages
    background : pygame.Surface
        The image loaded as a surface

    Methods
    -------
    setup() -> None
        Initialize pygame, set a caption, get the clock and enable key repeat
    start_game_loop() -> None
        The game loop that is running endless will be started
    connect_to_server() -> None
        Try to connect to the Server after username input
    resolve_server_commands() -> None
        Handle the commands received from the server
    view_events(events: list[pygame.event.Event]) -> None
        React to the events that happened
    display_cards() -> None
        Display the cards of every player on the screen
    display_player_names() -> None
        Display the Player Names on the Screen

    new_player_names(data: dict) -> None
        Add the player names to the game_data
    new_cards(data: dict) -> None
        Add new cards to the cards of the player
    highlight_cards(data: dict) -> None
        Add cards to the highlighted cards in the game_data
    """
    def __init__(self, auto_setup: bool = True, debug: bool = True):
        """
        Initialize a new GameLogic

        Parameters
        ----------
        auto_setup: bool (default: True)
            Automatically run the setup method
        debug : bool (default: True)
            If there should be debug messages or no cmd output
        """
        self.clock = None
        self.client = NetworkClient()
        self.game_data = ClientGameData()

        self.debug = debug

        self.background = pygame.image.load(r"client/cards/background.png")

        if auto_setup:
            self.setup()

    def setup(self) -> None:
        """
        Initialize pygame, set a caption, get the clock and enable key repeat

        Returns
        -------
        None
        """
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Watten")
        # Pygame now allows natively to enable key repeat:
        pygame.key.set_repeat(200, 25)

    def start_game_loop(self) -> None:
        """
        The game loop that is running endless will be started

        Returns
        -------
        None
        """
        while True:
            self.game_data.game_display.blit(self.background, (0, 0))
            events = pygame.event.get()

            self.connect_to_server()

            self.resolve_server_commands()

            self.view_events(events)

            self.display_cards()

            self.display_player_names()

            pygame.display.update()
            self.clock.tick(60)

    def connect_to_server(self) -> None:
        """
        Try to connect to the Server after username input

        Returns
        -------
        None
        """
        if not self.game_data.username:
            self.game_data.username = utils.text_input(self.game_data.game_display, self.clock)
            conn = self.client.server_connect(self.game_data.username)
            if conn is False:
                self.game_data.username = ""

    def resolve_server_commands(self) -> None:
        """
        Handle the commands received from the server

        Returns
        -------
        None

        """
        if not self.client.que.empty():
            recv: dict = self.client.que.get()
            if self.debug:
                print(recv)

            match recv.get("command"):
                case "PLAYER_NAMES":
                    self.new_player_names(recv)
                case "NEW_CARD":
                    self.new_cards(recv)
                case "PLAYER_TURN":
                    self.client.send_to_server("TURN", self.game_data.username, card=recv.get("available")[0])
                    self.highlight_cards(recv)

    def view_events(self, events: list[pygame.event.Event]) -> None:
        """
        React to the events that happened

        Parameters
        ----------
        events : list[pygame.event.Event]
            All events that happened

        Returns
        -------
        None
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

    def display_cards(self) -> None:
        """
        Display the cards of every player on the screen

        Returns
        -------
        None
        """
        if self.game_data.player_cards_surfaces.values():
            # [[player_id , x_start, x_step, y_start, y_step],...]
            player_card_coordinates = [
                [0, 225, 110, 480, 0],
                [1, -85, 0, 100, 80],
                [2, 290, 80, -85, 0],
                [3, 915, 0, 100, 80]]

            for player, x_start, x_step, y_start, y_step in player_card_coordinates:
                for card_surface in self.game_data.player_cards_surfaces.get(self.game_data.player_names[player]):
                    if player == 0:
                        if self.game_data.player_cards_surfaces.get(self.game_data.player_names[player]).index(card_surface) in self.game_data.highlighted_pos:
                            y_start = 460
                        else:
                            y_start = 480
                    self.game_data.game_display.blit(card_surface, (x_start, y_start))
                    x_start += x_step
                    y_start += y_step

    def display_player_names(self) -> None:
        """
        Display the Player Names on the Screen

        Returns
        -------
        None
        """
        if not self.game_data.player_names:
            return

        rects = [pygame.Rect(225, 430, 540, 60), pygame.Rect(0, 40, 200, 60), pygame.Rect(290, 75, 420, 60), pygame.Rect(800, 40, 200, 60)]
        texts = [pygame.font.Font(None, 50).render(self.game_data.player_names[0], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[1], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[2], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[3], True, (12, 255, 255))]

        self.game_data.game_display.blit(texts[0], texts[0].get_rect(center=rects[0].center))
        self.game_data.game_display.blit(texts[1], texts[1].get_rect(bottomleft=rects[1].bottomleft))
        self.game_data.game_display.blit(texts[2], texts[2].get_rect(center=rects[2].center))
        self.game_data.game_display.blit(texts[3], texts[3].get_rect(bottomright=rects[3].bottomright))

    def new_player_names(self, data: dict) -> None:
        """
        Add the player names to the game_data

        Parameters
        ----------
        data : dict
            The command data including the 'players' key

        Returns
        -------
        None
        """
        self.game_data.player_names = data.get("players")

    def new_cards(self, data: dict) -> None:
        """
        Add new cards to the cards of the player

        Parameters
        ----------
        data : dict
            The command data including the 'cards' key

        Returns
        -------
        None
        """
        self.game_data.card_ids = data.get("cards")
        self.game_data.player_cards_surfaces = utils.load_card_image(self.game_data.player_names, self.game_data.card_ids)

    def highlight_cards(self, data: dict) -> None:
        """
        Add cards to the highlighted cards in the game_data
        Only these cards are allowed to be player

        Parameters
        ----------
        data : dict
            The command data including the 'available' key

        Returns
        -------
        None
        """
        to_highlight = data.get("available")

        for card_id in to_highlight:
            pos = self.game_data.card_ids.index(card_id)
            self.game_data.highlighted_pos.append(pos)
        print("debug")
        