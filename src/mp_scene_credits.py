# MEMORY PUZZLE: Credits Scene


import pygame
import constants as CST
from master_class_scene import Scene
from master_class_button import Button
from master_class_text import StaticText
import mp_background as bg




class GameCredits(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		HALF_SCREEN = CST.SCREEN_WIDTH//2
		ONETHIRD_SCREEN = CST.SCREEN_WIDTH//3
		VERTICAL_GRID_UNIT = CST.SCREEN_HEIGHT // 16
		TEXTSIZE_SMALL = 24
		TEXTSIZE_BIG = 40
		TEXTSIZE_TITLE = 80
		TITLE_ROW = VERTICAL_GRID_UNIT * 2
		G_A_TITLE_ROW = VERTICAL_GRID_UNIT * 5
		G_A_CREDIT_ROW = VERTICAL_GRID_UNIT * 6
		FONT_TITLE_ROW = VERTICAL_GRID_UNIT * 8
		FONT_CREDIT1_ROW = VERTICAL_GRID_UNIT * 9
		FONT_CREDIT2_ROW = VERTICAL_GRID_UNIT * 10
		MENU_BUTTON_ROW = VERTICAL_GRID_UNIT * 13
		GRID = {
			"title": (HALF_SCREEN, TITLE_ROW),
			"g_a_title": (HALF_SCREEN, G_A_TITLE_ROW),
			"g_a_credit": (HALF_SCREEN, G_A_CREDIT_ROW),
			"font_title": (HALF_SCREEN, FONT_TITLE_ROW),
			"font_credit_1": (HALF_SCREEN, FONT_CREDIT1_ROW),
			"font_credit_2": (HALF_SCREEN, FONT_CREDIT2_ROW),
			"menu_button": (HALF_SCREEN-ONETHIRD_SCREEN//2, MENU_BUTTON_ROW, ONETHIRD_SCREEN, ONETHIRD_SCREEN//4),
		}

		self.BOARD_SIZES = list(CST.BOARD_SIZE.keys())
		self.board_size_index = 0
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}
		background = bg.Background()
		big_title = StaticText("Credits", TEXTSIZE_TITLE, GRID["title"], StaticText.CENTER)
		g_a_title = StaticText("< Game and Art >", TEXTSIZE_BIG, GRID["g_a_title"], StaticText.CENTER)
		g_a_credit = StaticText("Simone 'Kenneth' Canova", TEXTSIZE_SMALL, GRID["g_a_credit"], StaticText.CENTER)
		font_title = StaticText("< Font >", TEXTSIZE_BIG, GRID["font_title"], StaticText.CENTER)
		font_credit1 = StaticText("codeman38", TEXTSIZE_SMALL, GRID["font_credit_1"], StaticText.CENTER)
		font_credit2 = StaticText("http://www.zone38.net/", TEXTSIZE_SMALL, GRID["font_credit_2"], StaticText.CENTER)
		menu_button = Button("Menu", CST.BUTTON_STYLE, GRID["menu_button"], self.button_menu)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(big_title)
		self.updatelist.append(g_a_title)
		self.updatelist.append(g_a_credit)
		self.updatelist.append(font_title)
		self.updatelist.append(font_credit1)
		self.updatelist.append(font_credit2)
		self.updatelist.append(menu_button)



	def event_checking(self, this_event: pygame.event) -> None:
		super().event_checking(this_event)

		# Mouse click event checking
		if this_event.type == pygame.MOUSEBUTTONUP:
			for element in self.updatelist:
				if isinstance(element, Button):
					element.mouse_clicked(this_event.pos)
		

	# Buttons methods
	def button_menu(self):
		new_next_scene_params = {
			"next_scene": CST.SCENES.GAMEMENU,
		}
		self.quit_loop(new_next_scene_params)





# TESTING
if __name__ == "__main__":

	test_creds = GameCredits(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_creds.run(next_scene_params)
	print("Next scene params:", next_scene_params)