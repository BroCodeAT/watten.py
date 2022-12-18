import pygame

import utils
from client import NetworkClient

client = NetworkClient()
username: str = ""

pygame.init()
background = pygame.image.load(r"cards\background.png")
card_surfaces: list[pygame.Surface] = []

game_display = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
pygame.display.set_caption("Watten")
# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)


while True:
    game_display.blit(background, (0, 0))
    events = pygame.event.get()

    if not username:
        username = utils.text_input(game_display, clock)
        client.server_connect(username)

    if not client.que.empty():
        recv: dict = client.que.get()
        print(recv)

        match recv.get("command"):
            case "NEW_CARD":
                card_ids: list[int] = recv.get("cards")
                card_surfaces = utils.load_card_image(card_ids)

    if card_surfaces:
        x_start = 225
        for card_surface in card_surfaces:
            game_display.blit(card_surface, (x_start, 480))
            x_start += 110

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    pygame.display.update()
    clock.tick(60)
