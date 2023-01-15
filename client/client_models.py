import os
import pygame
import string
from dataclasses import dataclass, field


class StateInstance:
    def __init__(self, pos: tuple[int, int], surface: pygame.Surface,
                 state_images: str = r"assets"):
        pass

class TextInput:
    def __init__(self, pos: tuple[int, int], surface: pygame.Surface,
                 min_length: int = 3, max_length: int = 10, hide: bool = False,
                 input_images: str = r"assets/images/login/input",
                 font: str = r"assets/font/default.ttf", text_size: int = 40):
        self.pos = [p - 6 for p in pos]
        self.surface = surface
        self.click: bool = False
        self.selected: bool = False
        self.next_selected: bool = False

        self.font = pygame.font.Font(os.path.abspath(font), text_size)
        self.hide = hide
        if hide:
            self.hidden = ""
        self.text = ""
        self.min_length = min_length
        self.max_length = max_length

        self.images = self.load_state_images(input_images)
        self.rect: pygame.Rect | None = None
        self.current_state = "default"

        self.others: List["TextInput"] = []

    def display_current_state(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif self.selected:
                    if event.key == pygame.K_BACKSPACE:
                        if self.hide:
                            self.hidden = self.hidden[:-1]
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(self.text) >= self.min_length:
                            self.selected = False
                            self.current_state = "default"
                    else:
                        if len(self.text) <= self.max_length:
                            if self.hide:
                                self.hidden += "*"
                            if event.unicode in string.printable:
                                self.text += event.unicode

        if self.next_selected:
            self.selected = True
            self.current_state = "selected"
            self.next_selected = False

        if self.rect:
            if self.rect.collidepoint(*mouse_pos):
                if self.click:
                    self.next_selected = True
                else:
                    if not self.selected:
                        self.current_state = "hover"
            else:
                if not self.selected:
                    self.current_state = "default"
        self.check_others_selected()

        if self.current_state == "default":
            self.rect = self.surface.blit(self.images.get(self.current_state), [x + 6 for x in self.pos])
        else:
            self.rect = self.surface.blit(self.images.get(self.current_state), self.pos)
        if self.hide:
            obj = self.font.render(self.hidden, True, "black")
        else:
            obj = self.font.render(self.text, True, "black")
        rect = obj.get_rect()
        rect.topleft = (self.pos[0] + 10, self.pos[1] + 7)
        self.surface.blit(obj, rect)

    def check_others_selected(self):
        for other in self.others:
            if other.next_selected:
                self.selected = False

    @staticmethod
    def load_state_images(path: str) -> dict[str, pygame.Surface]:
        states: dict[str, pygame.Surface] = {}
        for image in os.listdir(path):
            states[image[:-4]] = pygame.image.load(fr"{path}\{image}")
        return states


@dataclass
class ClientGameData:
    """
    A dataclass to represent a Client including all the needed client Data.

    ...

    Attributes
    ----------
    username: str = ""
        The name of the client
    player_names: list[str] (default: list)
        The names of all the clients
    card_ids: list[int] (default: list)
        A list of the cards the player currently has
    played_ids: list[int] (default: list)
        The cards that have been played already
    highlighted_pos: list[int] (default: list)
        The positions of the highlighted cards
    game_display: pygame.Surface
        The whole game surface
    player_cards_surfaces: dict (default: dict)
        The surfaces of the cards of the players
    """
    username: str = ""
    player_names: list[str] = field(default_factory=list)
    card_ids: list[int] = field(default_factory=list)
    played_ids: list[int] = field(default_factory=list)
    highlighted_pos: list[int] = field(default_factory=list)
    game_display: pygame.Surface = pygame.display.set_mode((440, 300))
    player_cards_surfaces: dict[str, list[pygame.Surface]] = field(default_factory=dict)
    in_turn: str = ""
    click: bool = False
    highest: int = field(default_factory=int)
    highest_surface: pygame.Surface = None

    username_inp: TextInput = field(default=TextInput)
    password_inp: TextInput = field(default=TextInput)
