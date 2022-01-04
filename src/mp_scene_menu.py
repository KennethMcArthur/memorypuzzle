# MEMORY PUZZLE: Menu Scene


import pygame
import constants as CST
from master_class_scene import Scene
from master_class_button import Button
import mp_background as bg




class GameMenu(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		background = bg.Background()
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}
		start_button = Button("Quit", CST.BUTTON_STYLE, (200,200,100,50), self.quit_loop, self.next_scene_params)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(start_button)


	def event_checking(self, this_event: pygame.event) -> None:
		super().event_checking(this_event)

		# Mouse click event checking
		if this_event.type == pygame.MOUSEBUTTONUP:
			for element in self.updatelist:
				if isinstance(element, Button):
					element.mouse_clicked(this_event.pos)





# TESTING
if __name__ == "__main__":

	test_menu = GameMenu(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene:", next_scene_params["next_scene"])