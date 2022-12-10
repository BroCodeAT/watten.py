import pygame
import pygame_textinput 
from typing import List

class UsernameInputField():
    def __init__(self) -> None:
        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 13)
        self.input_field = pygame_textinput.TextInputVisualizer(manager=manager)

        self.input_field.cursor_blink_interval = 400
        self.input_field.value = "Username"
        
        

    def show(self, display: pygame.Surface, events: List[pygame.event.Event]):
        self.input_field.update(events)
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(335,330,330,40))
        display.blit(self.input_field.surface, (345,340))
        