# MEMORY PUZZLE: Credits Scene


import pygame
from master_class_scene import Scene
from master_class_button import Button
from master_class_text import StaticText
import mp_background as bg




class GameCredits(Scene):
	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

		SCREEN_WIDTH, SCREEN_HEIGHT = GAME_WINDOW.get_size()

    	# Scene Elements
		HALF_SCREEN = SCREEN_WIDTH//2
		ONETHIRD_SCREEN = SCREEN_WIDTH//3
		VERTICAL_GRID_UNIT = SCREEN_HEIGHT // 20
		TEXTSIZE_SMALL = 14
		TEXTSIZE_BIG = 20
		TEXTSIZE_TITLE = 80
		TITLE_ROW = VERTICAL_GRID_UNIT * 2
		G_A_TITLE_ROW = VERTICAL_GRID_UNIT * 5
		G_A_CREDIT_ROW = VERTICAL_GRID_UNIT * 6
		FONT_TITLE_ROW = VERTICAL_GRID_UNIT * 9
		FONT_CREDIT1_ROW = VERTICAL_GRID_UNIT * 10
		FONT_CREDIT2_ROW = VERTICAL_GRID_UNIT * 11
		SOUND_TITLE = VERTICAL_GRID_UNIT * 14
		SOUND_CREDIT = VERTICAL_GRID_UNIT * 15
		MENU_BUTTON_ROW = VERTICAL_GRID_UNIT * 18
		GRID = {
			"title": (HALF_SCREEN, TITLE_ROW),
			"g_a_title": (HALF_SCREEN, G_A_TITLE_ROW),
			"g_a_credit": (HALF_SCREEN, G_A_CREDIT_ROW),
			"font_title": (HALF_SCREEN, FONT_TITLE_ROW),
			"font_credit_1": (HALF_SCREEN, FONT_CREDIT1_ROW),
			"font_credit_2": (HALF_SCREEN, FONT_CREDIT2_ROW),
			"sound_title": (HALF_SCREEN, SOUND_TITLE),
			"sound_credit": (HALF_SCREEN, SOUND_CREDIT),
			"menu_button": (HALF_SCREEN-ONETHIRD_SCREEN//2, MENU_BUTTON_ROW, ONETHIRD_SCREEN, ONETHIRD_SCREEN//4),
		}

		background = bg.Background()
		big_title = StaticText("Credits", TEXTSIZE_TITLE, GRID["title"], StaticText.CENTER)
		g_a_title = StaticText("< Game and Art >", TEXTSIZE_BIG, GRID["g_a_title"], StaticText.CENTER)
		g_a_credit = StaticText("Simone 'Kenneth' Canova", TEXTSIZE_SMALL, GRID["g_a_credit"], StaticText.CENTER)
		font_title = StaticText("< Font >", TEXTSIZE_BIG, GRID["font_title"], StaticText.CENTER)
		font_credit1 = StaticText("codeman38", TEXTSIZE_SMALL, GRID["font_credit_1"], StaticText.CENTER)
		font_credit2 = StaticText("www.zone38.net", TEXTSIZE_SMALL, GRID["font_credit_2"], StaticText.CENTER)
		sound_title = StaticText("< Sound >", TEXTSIZE_BIG, GRID["sound_title"], StaticText.CENTER)
		sound_credit = StaticText("notification-sounds.com", TEXTSIZE_SMALL, GRID["sound_credit"], StaticText.CENTER)
		menu_button = Button("Menu", GRID["menu_button"], self.button_menu)

    	# Append order is draw order
		self.updatelist.append(background)
		self.updatelist.append(big_title)
		self.updatelist.append(g_a_title)
		self.updatelist.append(g_a_credit)
		self.updatelist.append(font_title)
		self.updatelist.append(font_credit1)
		self.updatelist.append(font_credit2)
		self.updatelist.append(sound_title)
		self.updatelist.append(sound_credit)
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
		next_scene_params = {
			"next_scene": Scene.GAMEMENU,
		}
		self.quit_loop(next_scene_params)









# TESTING
if __name__ == "__main__":

	mainscreen = pygame.display.set_mode((768, 768))
	test_creds = GameCredits(mainscreen)

	next_scene_params = {"next_scene": 0,}
	next_scene_params = test_creds.run(next_scene_params)
	print("Next scene params:", next_scene_params)