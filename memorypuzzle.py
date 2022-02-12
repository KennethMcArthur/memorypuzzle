# MEMORY PUZZLE: main program file


import pygame, sys
sys.path.append("src")
from src import constants as CST
from src import mp_scene_menu
from src import mp_scene_level


pygame.init()



def main_game():

    GAMEWINDOW = CST.MAINSCREEN

    # Scene initialization
    gamemenu = mp_scene_menu.GameMenu(GAMEWINDOW)
    gamelevel = mp_scene_level.Gamelevel(GAMEWINDOW)
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
