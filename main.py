import pygame
import pygame_textinput
from client import NetworkClient
import utils

client = NetworkClient()
username: str = ""

pygame.init()
background = pygame.image.load(r"cards\background.png")

game_display = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
pygame.display.set_caption("Watten")
# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)

username_input = utils.UsernameInputField()

while True:
    game_display.blit(background, (0,0))
    events = pygame.event.get()

    if not username:
        username_input.show(display=game_display, events=events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        elif username_input and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            username = username_input.input_field.value
            username_input = None
            client.server_connect(username)

    pygame.display.update()
    clock.tick(60)
