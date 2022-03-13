# MEMORY PUZZLE: Menu Scene


import pygame
from master_class_scene import Scene
from master_class_button import Button
from master_class_text import StaticText
from board import get_possible_board_sizes
import mp_background as bg




class GameMenu(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

		SCREEN_WIDTH, SCREEN_HEIGHT = GAME_WINDOW.get_size()

    	# Scene Elements
		TITLE_SIZE = 80
		HALF_SCREEN = SCREEN_WIDTH//2
		ONETHIRD_SCREEN = SCREEN_WIDTH//3
		FIRST_ROW = 50
		SECOND_ROW = 350
		THIRD_ROW = 450
		FOURTH_ROW = 600
		GRID = {
			"title_up": (SCREEN_WIDTH * 0.15, FIRST_ROW),
			"title_down": (SCREEN_WIDTH * 0.85, FIRST_ROW+TITLE_SIZE),
			"b_size_label": (HALF_SCREEN, SECOND_ROW),
			"minus_button": (ONETHIRD_SCREEN-25, THIRD_ROW-25, 50, 50),
			"b_value": (HALF_SCREEN, THIRD_ROW),
			"plus_button": (ONETHIRD_SCREEN*2-25, THIRD_ROW-25, 50, 50),
			"start_button": (HALF_SCREEN-ONETHIRD_SCREEN//2, FOURTH_ROW, ONETHIRD_SCREEN, ONETHIRD_SCREEN//4),
			"credits_button": (SCREEN_WIDTH-50, SCREEN_HEIGHT-50, 50, 50),
		}

		self.BOARD_SIZES = [card * 2 for card in get_possible_board_sizes()] # pairs
		self.board_size_index = 0
		background = bg.Background()
		big_title_up = StaticText("Memory", TITLE_SIZE, GRID["title_up"], alignment=StaticText.LEFT)
		big_title_down = StaticText("Puzzle", TITLE_SIZE, GRID["title_down"], alignment=StaticText.RIGHT)
		board_size_label = StaticText("How many cards?", TITLE_SIZE//2, GRID["b_size_label"], alignment=StaticText.CENTER)
		self.board_size_value_label = StaticText(str(self.BOARD_SIZES[self.board_size_index]), TITLE_SIZE, GRID["b_value"], alignment=StaticText.CENTER)
		start_button = Button("Start", GRID["start_button"], self.button_start)
		plus_button = Button("+", GRID["plus_button"], self.button_plus)
		minus_button = Button("-", GRID["minus_button"], self.button_minus)
		credits_button = Button("i", GRID["credits_button"], self.button_credits)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(big_title_up)
		self.updatelist.append(big_title_down)
		self.updatelist.append(plus_button)
		self.updatelist.append(minus_button)
		self.updatelist.append(board_size_label)
		self.updatelist.append(self.board_size_value_label)
		self.updatelist.append(start_button)
		self.updatelist.append(credits_button)


	def event_checking(self, this_event: pygame.event) -> None:
		super().event_checking(this_event)

		# Mouse click event checking
		if this_event.type == pygame.MOUSEBUTTONUP:
			for element in self.updatelist:
				if isinstance(element, Button):
					element.mouse_clicked(this_event.pos)

	# Buttons methods
	def button_start(self):
		next_scene_params = {
			"next_scene": Scene.GAMELEVEL,
			"total_cards": self.BOARD_SIZES[self.board_size_index],
		}
		self.quit_loop(next_scene_params)

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
	
	def button_credits(self):
		next_scene_params = {
			"next_scene": Scene.GAMECREDITS,
		}
		self.quit_loop(next_scene_params)




# TESTING
if __name__ == "__main__":
	
	mainscreen = pygame.display.set_mode((768, 768))
	test_menu = GameMenu(mainscreen)
	

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene params:", next_scene_params)