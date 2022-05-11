from cgitb import text
from window import Window
from button import Button
from text import Text

import pygame

pygame.init()

win = Window(800, 600, (0, 0, 0), (55, 55, 55))

text = Text("Click", (55, 55, 55), pos_x = 860, pos_y=105)
but = Button(75, 30, 850, 100, text)

win.add_component(but)

go = True

while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
    win.update()
    win.draw()