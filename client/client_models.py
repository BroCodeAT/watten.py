import pygame
from dataclasses import dataclass, field


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
    game_display: pygame.Surface = pygame.display.set_mode((1300, 700))
    player_cards_surfaces: dict[str, list[pygame.Surface]] = field(default_factory=dict)
    in_turn: bool = False
    click: bool = False
    highest: int = field(default_factory=int)
    highest_surface: pygame.Surface = None
