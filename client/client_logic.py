import pygame

import client_utils as utils

from client_network import NetworkClient
from client_models import ClientGameData, TextInput


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
    display_played_cards() -> None
        Show all the already_played cards in the middle of the screen
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

        self.background = pygame.image.load(r"assert/images/login/LoginWindow.png")

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

        self.game_data.username_inp = TextInput((179, 113), self.game_data.game_display)
        self.game_data.password_inp = TextInput((179, 171), self.game_data.game_display, hide=True)
        self.game_data.username_inp.others.append(self.game_data.password_inp)
        self.game_data.password_inp.others.append(self.game_data.username_inp)

    def start_game_loop(self) -> None:
        """
        The game loop that is running endless will be started

        Returns
        -------
        None
        """
        while True:
            self.game_data.game_display.fill("white")
            self.game_data.game_display.blit(self.background, (0, 0))
            events = pygame.event.get()

            self.connect_to_server(events)

            self.resolve_server_commands()

            self.view_events(events)

            self.display_cards()

            self.display_played_cards()

            self.display_player_names()

            self.display_highest()

            self.display_game_stats()

            pygame.display.update()
            self.clock.tick(60)

    def connect_to_server(self, events: list[pygame.event.Event]) -> None:
        """
        Try to connect to the Server after username input

        Returns
        -------
        None
        """
        if not self.game_data.username:

            pos = pygame.mouse.get_pos()
            self.game_data.username_inp.display_current_state(pos, events)
            self.game_data.password_inp.display_current_state(pos, events)
            start = pygame.Rect(100, 250, 200, 50)
            pygame.draw.rect(self.game_data.game_display, (0, 0, 0), start)

            mouse_pos = pygame.mouse.get_pos()
            if start.collidepoint(mouse_pos):
                self.game_data.username = self.game_data.username_inp.text

                conn = self.client.server_connect(self.game_data.username)
                if conn is False:
                    self.game_data.username = ""
                else:
                    self.background = pygame.image.load(r"assert\images\game\background.png")
                    pygame.display.set_mode((1000, 700))

    def resolve_server_commands(self) -> None:
        """
        Handle the commands received from the server

        Returns
        -------
        None

        """
        if not self.client.que.empty():
            recv: dict = self.client.que.get()

            match recv.get("command"):
                case "PLAYER_NAMES":
                    self.new_player_names(recv)
                case "NEW_CARD":
                    self.new_cards(recv)
                case "PLAYER_TURN":
                    self.highlight_cards(recv)
                case "HIGHEST":
                    self.load_highest(recv)
                case "UPDATE_TURN":
                    self.update_turn(recv)
                case "TURN_WINNER":
                    self.turn_winner(recv)
                #TODO: add point_winner command

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_data.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.game_data.click = False   

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
                #get player name
                player_name = self.game_data.player_names[player]
                #get the card surfaces of the player 
                player_surfaces = self.game_data.player_cards_surfaces.get(player_name)

                for card_surface in player_surfaces:
                    if player == 0:
                        pointer = pygame.mouse.get_pos()
                        reference_rect = card_surface.get_rect().move(x_start, y_start)
                        if player_surfaces.index(card_surface) in self.game_data.highlighted_pos and reference_rect.collidepoint(pointer) and self.game_data.in_turn == self.game_data.username:
                            y_start = 460
                            if self.game_data.click:
                                self.play_card(player_surfaces.index(card_surface), player_name)
                        else:
                            y_start = 480
                    self.game_data.game_display.blit(card_surface, (x_start, y_start))
                    x_start += x_step
                    y_start += y_step

    def display_played_cards(self) -> None:
        """
        Show all the already_played cards in the middle of the screen

        Returns
        -------
        None
        """
        x_start = 200
        y_start = 225
        x_step = 110
        for index, card in enumerate(self.game_data.played_ids):
            img = pygame.image.load(fr"assert/images/game/cards/id_{card}.PNG")
            img = pygame.transform.scale(img, (100, 170))
            self.game_data.game_display.blit(img, (x_start + x_step*index, y_start))

    def display_player_names(self) -> None:
        """
        Display the Player Names on the Screen

        Returns
        -------
        None
        """
        if not self.game_data.player_names:
            return

        # List of the rectangular to center the text to
        rects = [pygame.Rect(225, 640, 540, 60), pygame.Rect(0, 40, 200, 60), pygame.Rect(290, 75, 420, 60), pygame.Rect(800, 40, 200, 60)]
        texts = [pygame.font.Font(None, 50).render(self.game_data.player_names[0], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[1], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[2], True, (12, 255, 255)),
                 pygame.font.Font(None, 40).render(self.game_data.player_names[3], True, (12, 255, 255))]

        self.game_data.game_display.blit(texts[0], texts[0].get_rect(center=rects[0].center))
        self.game_data.game_display.blit(texts[1], texts[1].get_rect(bottomleft=rects[1].bottomleft))
        self.game_data.game_display.blit(texts[2], texts[2].get_rect(center=rects[2].center))
        self.game_data.game_display.blit(texts[3], texts[3].get_rect(bottomright=rects[3].bottomright))

    def display_highest(self) -> None:
        if self.game_data.highest_surface:
            self.game_data.game_display.blit(self.game_data.highest_surface, (900,615))
        else:
            pass

    def display_game_stats(self) -> None:
        stats_background = pygame.Rect(1001,0,299,700)
        pygame.draw.rect(self.game_data.game_display, "white", stats_background)

        pygame.draw.line(self.game_data.game_display, "black", (1050,70), (1250,70), width=4)


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
        self.game_data.card_ids = data.get("assert/images/game/cards")
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
        self.game_data.in_turn = self.game_data.username

        to_highlight = data.get("available")

        for card_id in to_highlight:
            pos = self.game_data.card_ids.index(card_id)
            self.game_data.highlighted_pos.append(pos)
    
    def play_card(self, played_pos: int, player_name: str):
        self.game_data.highlighted_pos.clear()
        card_id = self.game_data.card_ids.pop(played_pos)
        self.game_data.player_cards_surfaces[player_name].pop(played_pos)

        self.client.send_to_server("PLAY_CARD", self.game_data.username, card=card_id)

    def update_turn(self, data: dict):
        self.game_data.played_ids = data.get("played")
        last_player: str = data.get("last_played")
        if last_player != self.game_data.username:
            self.game_data.player_cards_surfaces[last_player].pop(0)

    def turn_winner(self, data: dict):
        self.game_data.played_ids.clear()
        #TODO: show turn at the player who won the turn

    def load_highest(self, data: dict):
        self.game_data.highest = data.get("highest")
        self.game_data.highest_surface = utils.load_singe_card(self.game_data.highest)

