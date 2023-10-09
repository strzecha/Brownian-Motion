import pygame

from brownian.gui_component import GUIComponent

class CheckBox(GUIComponent):
    """Class CheckBox
    
    Class to representation of checkbox in interface
    """

    def __init__(self, pos_x, pos_y, radius):
        """Init method
        
        Args:
            pos_x (int): x position of checkbox
            pos_y (int): y position of checkbox
            radius (int): radius of checkbox
        """

        super().__init__()

        self.radius = radius
        self.pos = (pos_x, pos_y)

        self.checked = False

        self.rect = pygame.Rect(pos_x - radius, pos_y - radius, radius * 2, radius * 2)
        self.list_to_unchecked = list()

    def set_list_to_unchecked(self, list_unchecked):
        """Method to set list to uncheked
        """
        
        self.list_to_unchecked = list_unchecked

    def update(self):
        """Update method
        """
        
        self.mouse = pygame.mouse.get_pos()

    def draw(self, screen):
        """Method to draw checkbox on screen
        
        Args:
            screen (pygame.display): screen
        """

        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius)

        if self.checked:
            pygame.draw.circle(screen, (0, 0, 0), self.pos, self.radius // 2)

    def click(self):
        """Method to detect checkbox clicked
        """
        
        if self.rect.collidepoint(self.mouse):
            self.checked = not self.checked

            for elemenent in self.list_to_unchecked:
                elemenent.checked = not elemenent.checked
