import pygame
from client import NetworkClient

client = NetworkClient()

pygame.init()
background = pygame.image.load(r"cards\background.png")

game_display = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Watten")

while True:
    game_display.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pygame.display.update()
