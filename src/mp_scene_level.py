# MEMORY PUZZLE: Game level



import pygame
import constants as CST
from master_class_scene import Scene
from master_class_button import Button
import mp_background as bg



class Gamelevel(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		background = bg.Background()
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}

    	# Append order is draw order
		self.updatelist.append(background)
    
    
	def load_outside_params(self, params: dict) -> None:
		""" Loads a dictionary of parameters from another scene """
		pass









# TESTING
if __name__ == "__main__":

	test_menu = Gamelevel(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene:", next_scene_params["next_scene"])