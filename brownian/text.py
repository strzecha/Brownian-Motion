import pygame

class Text:
    """Class Text
    
    Class to representation of text in GUI components
    """

    def __init__(self, text, color, hover_color=None, font_name="Corbel", font_size=20, pos_x=0, pos_y=0):
        """Init method

        Args:
            text (str): contents of text
            color (tuple): color of text
            hover_color (tuple, optional): hover color of text. Defaults to None.
            font_name (str, optional): name of font of text. Defaults to "Corbel".
            font_size (int, optional): size of font. Defaults to 20.
            pos_x (int, optional): x position of text. Defaults to 0.
            pos_y (int, optional): y position of text. Defaults to 0.
        """

        self.color = color
        self.hover_color = color if not hover_color else hover_color

        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.update()

        self.set_pos(pos_x, pos_y)

    def set_pos(self, pos_x, pos_y):
        """Position setter
        """
        
        self.pos = (pos_x, pos_y)

    def update(self):
        """Update method
        """
        
        self.text_rendered = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """Method to draw text on screen

        Args:
            screen (Window): screen
        """
        
        screen.blit(self.text_rendered, self.pos)
