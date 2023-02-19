import sys
import argon2
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
    card_back = pygame.image.load(r"assets/images/game/cards/card_back.png")
    card_back = pygame.transform.scale(card_back, (100, 170))
    card_back_rot = pygame.transform.rotate(card_back, 90)

    half_card_back = pygame.image.load(r"assets/images/game/cards/card_back_half.png")
    half_card_back = pygame.transform.scale(half_card_back,(100,85))
    half_card_back_rot = pygame.transform.rotate(half_card_back, 90)


    own_cards: list = []
    for card_id in card_ids:
        own_card = pygame.image.load(fr"assets/images/game/cards/id_{card_id}.png")
        own_card = pygame.transform.scale(own_card, (100, 170))
        own_cards.append(own_card)
        

    player_cards_surfaces: dict = {player_names[0]: own_cards,
                                   player_names[1]: [card_back_rot for i in range(5)],
                                   player_names[2]: [card_back for i in range(5)],
                                   player_names[3]: [half_card_back_rot for i in range(5)]}
    return player_cards_surfaces


def load_singe_card(card_id: int) -> pygame.Surface:
    card_surface = pygame.image.load(fr"assets/images/game/cards/id_{card_id}.png")
    card_surface = pygame.transform.scale(card_surface, (100, 170))

    return card_surface


def get_hashed_password(clear_password: str) -> bytes:
    hashed_password = argon2.hash_password(bytes(clear_password,'utf-8'))
    return hashed_password