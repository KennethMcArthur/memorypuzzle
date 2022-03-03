# MEMORY PUZZLE: Background


import pygame
import constants as CST


class Background:

	def game_tick_update(self, window: pygame.Surface, *other_params) -> None:
		window.fill(CST.COLOR.BACKGROUND)