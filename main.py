from brownian.window import Window
from brownian.button import Button
from brownian.text import Text
from brownian.simulation import Simulation

import pygame

pygame.init()

def main():
    win = Window(800, 600, (0, 0, 0), (125, 125, 125))
    text = Text("Click", (0, 0, 0), pos_x = 860, pos_y=105)
    but = Button(75, 30, 850, 100, text, (100, 100, 100), (80, 80, 80))
    win.add_component(but)

    sim = Simulation(win, 500, 5)
    sim.run()



main()