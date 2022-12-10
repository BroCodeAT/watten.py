import pygame
import pygame_textinput 
from typing import List

class UsernameInputField():
    def __init__(self) -> None:
        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 5)
        self.input_field = pygame_textinput.TextInputVisualizer(manager=manager)

    def show(self, display: pygame.Surface, events: List[pygame.event.Event]):
        self.input_field.update(events)
        display.blit(self.input_field.surface, (500,350))