import pygame

from common import utils
from network import NetworkClient
from models import ClientGameData


class ClientLogic:
    def __init__(self, auto_setup: bool = True, debug: bool = True):
        self.player_names = None
        self.player_cards_surfaces = None
        self.game_display = None
        self.clock = None
        self.client = NetworkClient()
        self.game_data = ClientGameData()

        self.debug = debug

        self.background = pygame.image.load(r"././cards/background.PNG")

        if auto_setup:
            self.setup()

    def setup(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Watten")
        # Pygame now allows natively to enable key repeat:
        pygame.key.set_repeat(200, 25)

    def start_game_loop(self):
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

    def connect_to_server(self):
        if not self.game_data.username:
            self.game_data.username = utils.text_input(self.game_data.game_display, self.clock)
            conn = self.client.server_connect(self.game_data.username)
            if conn is False:
                self.game_data.username = ""

    def resolve_server_commands(self):
        if not self.client.que.empty():
            recv: dict = self.client.que.get()
            if self.debug:
                print(recv)

            match recv.get("command"):
                case "PLAYER_NAMES":
                    self.new_player_names(recv)
                case "NEW_CARD":
                    self.new_cards(recv)

    def view_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

    def display_cards(self):
        if self.game_data.player_cards_surfaces.values():
            # [[x_start, x_step, y_start, y_step],...]
            player_card_coordinates = [
                [0, 225, 110, 480, 0],
                [1, -85, 0, 100, 80],
                [2, 290, 80, -85, 0],
                [3, 915, 0, 100, 80]]

            for player, x_start, x_step, y_start, y_step in player_card_coordinates:
                for card_surface in self.game_data.player_cards_surfaces.get(self.game_data.player_names[player]):
                    self.game_data.game_display.blit(card_surface, (x_start, y_start))
                    x_start += x_step
                    y_start += y_step

    def display_player_names(self):
        if not self.game_data.player_names:
            return
        # player_card_coordinates = [
        #     [0, 225, 110, 480, 0],
        #     [1, -85, 0, 100, 80],
        #     [2, 290, 80, -85, 0],
        #     [3, 915, 0, 100, 80]
        #     ]

        rects = [pygame.Rect(225, 560, 550, 60), pygame.Rect(230, 100, 60, 340), pygame.Rect(290, 95, 340, 60), pygame.Rect(825, 100, 60, 340)]
        texts = [pygame.font.Font(None, 50).render(self.game_data.player_names[0], True, (255, 255, 255)),
                 pygame.font.Font(None, 50).render(self.game_data.player_names[1], True, (255, 255, 255)),
                 pygame.font.Font(None, 50).render(self.game_data.player_names[2], True, (255, 255, 255)),
                 pygame.font.Font(None, 50).render(self.game_data.player_names[3], True, (255, 255, 255))]
        rotations = [0, 90, 0, 180]
        for text, rect, rotation in zip(texts, rects, rotations):
            pygame.transform.rotate(text, rotation)
            self.game_data.game_display.blit(text, text.get_rect(center=rect.center))

    def new_player_names(self, data: dict):
        self.game_data.player_names = data.get("players")

    def new_cards(self, data: dict):
        self.game_data.card_ids = data.get("cards")
        self.game_data.player_cards_surfaces = utils.load_card_image(self.game_data.player_names, self.game_data.card_ids)
