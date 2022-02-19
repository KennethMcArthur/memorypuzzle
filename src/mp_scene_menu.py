# MEMORY PUZZLE: Menu Scene


import pygame
import constants as CST
from master_class_scene import Scene
from master_class_button import Button
from master_class_text import StaticText
import mp_background as bg




class GameMenu(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		TITLE_SIZE = 80
		HALF_SCREEN = CST.SCREEN_WIDTH//2
		ONETHIRD_SCREEN = CST.SCREEN_WIDTH//3
		FIRST_ROW = 50
		SECOND_ROW = 350
		THIRD_ROW = 450
		FOURTH_ROW = 600
		GRID = {
			"title_up": (CST.SCREEN_WIDTH * 0.15, FIRST_ROW),
			"title_down": (CST.SCREEN_WIDTH * 0.85, FIRST_ROW+TITLE_SIZE),
			"b_size_label": (HALF_SCREEN, SECOND_ROW),
			"minus_button": (ONETHIRD_SCREEN-25, THIRD_ROW-25, 50, 50),
			"b_value": (HALF_SCREEN, THIRD_ROW),
			"plus_button": (ONETHIRD_SCREEN*2-25, THIRD_ROW-25, 50, 50),
			"start_button": (HALF_SCREEN-ONETHIRD_SCREEN//2, FOURTH_ROW, ONETHIRD_SCREEN, ONETHIRD_SCREEN//4),
		}

		self.BOARD_SIZES = list(CST.BOARD_SIZE.keys())
		self.board_size_index = 0
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}
		background = bg.Background()
		big_title_up = StaticText("Memory", TITLE_SIZE, GRID["title_up"], alignment=StaticText.LEFT)
		big_title_down = StaticText("Puzzle", TITLE_SIZE, GRID["title_down"], alignment=StaticText.RIGHT)
		board_size_label = StaticText("Choose board size", TITLE_SIZE//2, GRID["b_size_label"], alignment=StaticText.CENTER)
		self.board_size_value_label = StaticText(str(self.BOARD_SIZES[self.board_size_index]), TITLE_SIZE, GRID["b_value"], alignment=StaticText.CENTER)
		start_button = Button("Start", CST.BUTTON_STYLE, GRID["start_button"], self.button_start)
		plus_button = Button("+", CST.BUTTON_STYLE, GRID["plus_button"], self.button_plus)
		minus_button = Button("-", CST.BUTTON_STYLE, GRID["minus_button"], self.button_minus)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(big_title_up)
		self.updatelist.append(big_title_down)
		self.updatelist.append(plus_button)
		self.updatelist.append(minus_button)
		self.updatelist.append(board_size_label)
		self.updatelist.append(self.board_size_value_label)
		self.updatelist.append(start_button)


	def event_checking(self, this_event: pygame.event) -> None:
		super().event_checking(this_event)

		# Mouse click event checking
		if this_event.type == pygame.MOUSEBUTTONUP:
			for element in self.updatelist:
				if isinstance(element, Button):
					element.mouse_clicked(this_event.pos)

	# Buttons methods
	def button_start(self):
		new_next_scene_params = {
			"next_scene": CST.SCENES.GAMELEVEL,
			"total_cards": self.BOARD_SIZES[self.board_size_index],
		}
		self.quit_loop(new_next_scene_params)

	def button_plus(self):
		self.board_size_index += 1
		if self.board_size_index >= len(self.BOARD_SIZES):
			self.board_size_index = 0
		self.board_size_value_label.set_text(str(self.BOARD_SIZES[self.board_size_index]))

	def button_minus(self):
		self.board_size_index -= 1
		if self.board_size_index < 0:
			self.board_size_index = len(self.BOARD_SIZES)-1
		self.board_size_value_label.set_text(str(self.BOARD_SIZES[self.board_size_index]))




# TESTING
if __name__ == "__main__":

	test_menu = GameMenu(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene params:", next_scene_params)