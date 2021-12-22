# MEMORY PUZZLE: Background


import pygame



class Background:
	def __init__(self):
		pass

	def game_tick_update(self, window:pygame.Surface, *other_params) -> None:
		window.fill((125,125,125)) # TODO: add a proper background