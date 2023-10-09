import pygame

class GUIComponent(pygame.sprite.Sprite):
    """Class GUIComponent
    
    Class to representation component in interface
    """

    def __init__(self):
        """Init method
        """
        
        super().__init__()

    def handle_event(self, event):
        """Method to handle event
        
        Args:
            event (pygame.event): event
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def click(self):
        """Method to detect component clicked
        """
        
        pass
