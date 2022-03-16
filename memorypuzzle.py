# MEMORY PUZZLE: main program file


import pygame, sys
sys.path.append("src")
from src import mp_scene_menu
from src import mp_scene_level
from src import mp_scene_end
from src import mp_scene_credits





def main_game():
    pygame.init()

    GAMEWINDOW = pygame.display.set_mode((768, 768))
    pygame.display.set_caption("Memory Puzzle")

    # Scene initialization
    scenelist = [
        mp_scene_menu.GameMenu(GAMEWINDOW),
        mp_scene_level.Gamelevel(GAMEWINDOW),
        mp_scene_end.GameEnd(GAMEWINDOW),
        mp_scene_credits.GameCredits(GAMEWINDOW)
    ]

    scene_params = {"next_scene": 0,}
    while scene_params["next_scene"] is not None:
        next_scene = scene_params["next_scene"]
        scene_params = scenelist[next_scene].run(scene_params)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main_game()
