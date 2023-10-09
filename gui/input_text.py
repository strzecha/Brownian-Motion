import pygame

from gui.gui_component import GUIComponent
from gui.text import Text

class InputText(GUIComponent):
    """Class InputText
    
    Class to representation text input in interface
    """

    def __init__(self, width, height, pos_x, pos_y, default=0):
        """Init method
        
        Args:
            width (int): width of text input
            height (int): height of text input
            pos_x (int): x position of text_input
            pos_y (int): y position of text_input
            default (int, optional): default contents of text input. Defaults to 0.
        """

        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.active = False

        self.pos = (pos_x, pos_y)

        self.text = Text(str(default), (0, 0, 0))
        self.set_text()

    def click(self):
        """Method to detect text input clicked
        """
        
        if self.rect.collidepoint(self.mouse):
            self.active = not self.active
        else:
            self.active = False

    def update(self):
        """Update method
        """
        
        self.text.update()
        self.set_text()
        self.mouse = pygame.mouse.get_pos()

        if self.active:
            self.image.fill((255, 255, 255))
        else:
            self.image.fill((210, 210, 210))

    def handle_event(self, event):
        """Method to handle events
        
        Args:
            event (pygame.event): event
        """

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text.text = self.text.text[:-1]
                else:
                    self.text.text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def draw(self, screen):
        """Method to draw text input on screen
        
        Args:
            screen (pygame.display): screen
        """

        screen.blit(self.image, self.rect)
        self.text.draw(screen)

    def set_text(self):
        """Text setter
        """
        
        text_width, text_height = self.text.text_rendered.get_size()

        margin_x = self.rect.x + (self.rect.width - text_width) // 2
        margin_y = self.rect.y + (self.rect.height - text_height) // 2

        self.text.set_pos(margin_x, margin_y)

    def get_text(self):
        """Text getter
        """

        return self.text.text
