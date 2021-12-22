# MEMORY PUZZLE: main program file


import pygame, sys
from src import constants as CST
from src import board
from src import card


pygame.init()



def main_game():

    window = CST.MAINSCREEN

    # Scene initialization
    gamemenu = None
    gamelevel = None
    gameendscreen = None

    scenelist = [
        gamemenu,
        gamelevel,
        gameendscreen,
    ]

    next_scene = 0
    while next_scene != None:
        next_scene = scenelist[next_scene].run()
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main_game()
