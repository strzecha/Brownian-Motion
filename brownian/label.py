from brownian.gui_component import GUIComponent
from brownian.text import Text

class Label(GUIComponent):
    def __init__(self, text, pos_x, pos_y):
        super().__init__()

        self.text = Text(text, (0, 0, 0), pos_x=pos_x, pos_y=pos_y)

    def draw(self, screen):
        self.text.draw(screen)
