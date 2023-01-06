import sys
import pygame


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


def text_input(screen: pygame.Surface, clock: pygame.time.Clock, length: int = 10) -> str:
    """
    Screen to enter a text input from the client

    Parameters
    ----------
    screen : pygame.Surface
        The screen where the text input should be placed on
    clock : pygame.time.Clock
        The clock, the game is synced to
    length : int (default: 10)
        The length of the text input

    Returns
    -------
    str : the text the user entered
    """
    click = False
    run = True
    username = ""
    while run:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(200, 200, 600, 300), 0, 5)

        draw_text("Welcome to Watten", (12, 255, 255), screen, 220, 220, 50)
        draw_text("Created by kloaChristoph/GozZzer", (12, 255, 255), screen, 220, 260, 20)
        draw_text("Insert your Username and press Start", (12, 255, 255), screen, 220, 310, 35)

        name_box = pygame.Rect(220, 350, 460, 60)
        pygame.draw.rect(screen, (0, 0, 0), name_box, 0, 5)
        input = pygame.font.Font(None, 50).render(username, True, (255, 255, 255))
        screen.blit(input, input.get_rect(center=name_box.center))

        start_button = pygame.Rect(220, 420, 130, 60)

        mx, my = pygame.mouse.get_pos()
        if start_button.collidepoint((mx, my)):
            if click:
                if username:
                    return username

        pygame.draw.rect(screen, (0, 161, 255), start_button, 0, 4)
        draw_text("START", (12, 255, 255), screen, 230, 435, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username:
                        return username
                else:
                    if len(username) < length:
                        username += event.unicode

        pygame.display.update()
        clock.tick(60)


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
        own_card = pygame.image.load(fr"cards/id_{card_id}.png")
        own_card = pygame.transform.scale(own_card, (100, 170))
        own_cards.append(own_card)

    card_back = pygame.image.load(r"cards/card_back.png")
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
    card_surface = pygame.image.load(fr"cards/id_{card_id}.png")
    card_surface = pygame.transform.scale(card_surface, (100, 170))

    return card_surface