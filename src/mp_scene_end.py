# MEMORY PUZZLE: Ending Scene


import pygame
import constants as CST
from master_class_scene import Scene
from master_class_button import Button
from master_class_text import StaticText
import mp_background as bg




class GameEnd(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		HALF_SCREEN = CST.SCREEN_WIDTH//2
		ONETHIRD_SCREEN = CST.SCREEN_WIDTH//3
		FIRST_ROW = 100
		SECOND_ROW = 300
		THIRD_ROW = 400
		FOURTH_ROW = 600
		GRID = {
			"title": (HALF_SCREEN, FIRST_ROW),
			"b_size_label": (HALF_SCREEN, SECOND_ROW),
			"minus_button": (ONETHIRD_SCREEN-25, THIRD_ROW-25, 50, 50),
			"b_value": (HALF_SCREEN, THIRD_ROW),
			"plus_button": (ONETHIRD_SCREEN*2-25, THIRD_ROW-25, 50, 50),
			"start_button": (HALF_SCREEN-ONETHIRD_SCREEN//2, FOURTH_ROW, ONETHIRD_SCREEN, ONETHIRD_SCREEN//4),
			"quit_button": (),
		}

		self.BOARD_SIZES = list(CST.BOARD_SIZE.keys())
		self.board_size_index = 0
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}
		background = bg.Background()
		big_title = StaticText("You did it!", 64, GRID["title"], alignment=StaticText.CENTER)
		time_taken_label = StaticText("...and it only took", 32, GRID["b_size_label"], alignment=StaticText.CENTER)
		self.time_played_label = StaticText("Nope", 64, GRID["b_value"], alignment=StaticText.CENTER)
		start_button = Button("Menu", CST.BUTTON_STYLE, GRID["start_button"], self.button_start)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(big_title)
		self.updatelist.append(time_taken_label)
		self.updatelist.append(self.time_played_label)
		self.updatelist.append(start_button)



	def event_checking(self, this_event: pygame.event) -> None:
		super().event_checking(this_event)

		# Mouse click event checking
		if this_event.type == pygame.MOUSEBUTTONUP:
			for element in self.updatelist:
				if isinstance(element, Button):
					element.mouse_clicked(this_event.pos)
	
	def load_outside_params(self, params: dict) -> None:
		time_played = params["time_played"]
		# Converting to minutes and seconds
		minutes = int(time_played // 60)
		seconds = time_played
		if minutes > 0:
			seconds = time_played % 60
		seconds = round(seconds, 2)
		display_string = f"{minutes}m{seconds}s"
		self.time_played_label.set_text(display_string)
		

	# Buttons methods
	def button_start(self):
		new_next_scene_params = {
			"next_scene": CST.SCENES.GAMEMENU,
			"total_cards": self.BOARD_SIZES[self.board_size_index],
		}
		self.quit_loop(new_next_scene_params)





# TESTING
if __name__ == "__main__":

	test_end = GameEnd(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0, "time_played": 150.6}
	next_scene_params = test_end.run(next_scene_params)
	print("Next scene params:", next_scene_params)