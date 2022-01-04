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

    scene_params = {"next_scene": 0,}
    while scene_params["next_scene"] != None:
        scene_params = scenelist[scene_params["next_scene"]].run(scene_params)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main_game()
