# MEMORY PUZZLE: Background


import pygame



class Background:

	BG_COLOR = pygame.Color("#2A9D8F")

	def game_tick_update(self, window: pygame.Surface, *other_params) -> None:
		window.fill(Background.BG_COLOR)