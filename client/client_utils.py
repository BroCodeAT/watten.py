import sys
import pygame
from client_models import TextInput


def draw_text(text: str, color: tuple[int, int, int], surface: pygame.Surface, x: int, y: int, text_size: int = 30) -> pygame.rect.Rect:
    """
    Draw text with the given color on the given surface to the given coordination's

    Parameters
    ----------
    text : str
        The text to display
    color : tuple[int, int, int]
        The RGB code of the color of the text
    surface : pygame.Surface
        The surface on witch the text should be drawn
    x : int
        The x-coordinate the text should be drawn to
    y : int
        The y-coordinate the text should be drawn to
    text_size : int (default: 30)
        The size of the text

    Returns
    -------
    pygame.rect.Rect : The Rectangular of the text
    """
    font = pygame.font.SysFont(None, text_size)
    obj = font.render(text, True, color)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)
    return rect


def load_card_image(player_names: list[str], card_ids: list[int]) -> dict[str, list[pygame.Surface]]:
    """
    Load the cards to the screen

    Parameters
    ----------
    player_names : list[str]
        The list of the names of every player
    card_ids : list[int]
        The list of the cards of the player

    Returns
    -------
    dict[str, list[pygame.Surface]]: The name associated to a list of the surfaces of the cards
    """
    own_cards: list = []
    for card_id in card_ids:
        own_card = pygame.image.load(fr"assets/images/game/cards/id_{card_id}.png")
        own_card = pygame.transform.scale(own_card, (100, 170))
        own_cards.append(own_card)

    card_back = pygame.image.load(r"assets/images/game/cards/card_back.png")
    card_back = pygame.transform.scale(card_back, (100, 170))
    card_back_rot = pygame.transform.rotate(card_back, 90)

    card_backsides: list = []
    for i in range(5):
        card_backsides.append(card_back)

    card_backsides_rot: list = []
    for i in range(5):
        card_backsides_rot.append(card_back_rot)

    player_cards_surfaces: dict = {player_names[0]: own_cards,
                                   player_names[1]: card_backsides_rot,
                                   player_names[2]: card_backsides,
                                   player_names[3]: card_backsides_rot.copy()}
    return player_cards_surfaces


def load_singe_card(card_id: int) -> pygame.Surface:
    card_surface = pygame.image.load(fr"assets/images/game/cards/id_{card_id}.png")
    card_surface = pygame.transform.scale(card_surface, (100, 170))

    return card_surface
