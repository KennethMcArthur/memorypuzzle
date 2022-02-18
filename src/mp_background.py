# MEMORY PUZZLE: Background


import pygame
import constants as CST


class Background:
	def __init__(self):
		pass

	def game_tick_update(self, window:pygame.Surface, *other_params) -> None:
		window.fill(CST.color_db["background"])