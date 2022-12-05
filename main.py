import pygame

pygame.init()

pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Watten")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pygame.display.update()
