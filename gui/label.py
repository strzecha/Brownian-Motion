from gui.gui_component import GUIComponent
from gui.text import Text

class Label(GUIComponent):
    """Class Label
    
    Class to representation of label in interface
    """

    def __init__(self, text, pos_x, pos_y):
        """Init method
        
        Args:
            text (str): text in label
            pos_x (int): x position of label
            pos_y (int): y position of label
        """

        super().__init__()

        self.text = Text(text, (0, 0, 0), pos_x=pos_x, pos_y=pos_y)

    def draw(self, screen):
        """Method to draw label on screen
        
        Args:
            screen (pygame.display): screen
        """
        
        self.text.draw(screen)
