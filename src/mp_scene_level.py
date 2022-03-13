# MEMORY PUZZLE: Game level



import pygame
import random
import time
import board
from master_class_scene import Scene
from master_class_button import Button
from card import Card
import mp_background as bg



class Gamelevel(Scene):

	PARAMS_NEEDED = ["total_cards"]

	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

		self.SCREEN_SIZE = GAME_WINDOW.get_size()
		Card.generate_constants()

    	# Scene Elements
		self.background = bg.Background()

    	# Append order is draw order
		self.updatelist.append(self.background)
    
    
	def load_outside_params(self, params: dict) -> None:
		""" Loads a dictionary of parameters from another scene """
		# Validating parameter dict keys
		if not all(key in params for key in Gamelevel.PARAMS_NEEDED):
			raise KeyError("Missing key parameter")

		total_cards = params["total_cards"]
		board_row_length = board.get_optimal_row_length(total_cards)
		padding = 10
		board_rows = total_cards // board_row_length
		seed_color_pairs = board.get_combinations(total_cards, Card.CARD_COLORS, Card.SHAPELIST)
		random.shuffle(seed_color_pairs)
		self.pairs_left = total_cards // 2
		self.play_timer = time.time()
		self.card_list = board.generate_cards_on_board(self.SCREEN_SIZE, board_rows, board_row_length, padding, seed_color_pairs)
		self.updatelist.extend(self.card_list)


	def reset_state(self) -> None:
		super().reset_state()
		self.updatelist.clear()
		self.updatelist.append(self.background)
		del self.card_list


	def run(self, outside_params: dict) -> int:
		""" Main loop method """
		self.load_outside_params(outside_params)

		gameclock = pygame.time.Clock()

		selected_cards = []
		need_wrong_answer_delay = False
		got_wrong_pair = False

		# Main game loop
		while self.looping_active:

			delta = gameclock.tick(60)
			mousepos = pygame.mouse.get_pos()

			if got_wrong_pair:
				if all(card.is_fully_flipped() for card in selected_cards):
					selected_cards.clear()
					got_wrong_pair = False

			for event in pygame.event.get():
				self.event_checking(event)
				if event.type == pygame.MOUSEBUTTONUP:
					if len(selected_cards) < 2 and not got_wrong_pair:
						this_card = board.card_clicked_at(mousepos, self.card_list)
						if this_card:
							this_card.card_flip()
							selected_cards.append(this_card)

			# Card checking        
			if len(selected_cards) == 2 and all(card.is_fully_flipped() for card in selected_cards):
				card1, card2 = selected_cards
				if card1 == card2:
					card1.card_blocked = True
					card2.card_blocked = True
					selected_cards.clear()
					self.pairs_left -= 1
				else:
					need_wrong_answer_delay = True
					got_wrong_pair = True


			# Drawing sequence
			for gameobj in self.updatelist:
				gameobj.game_tick_update(self.GAME_WINDOW, mousepos, delta) # All classes have this methods
			pygame.display.update()

			if need_wrong_answer_delay:
				time_before_delay = time.time()
				pygame.time.wait(1000)
				time_after_delay = time.time()
				self.play_timer += time_after_delay - time_before_delay
				need_wrong_answer_delay = False
				card1.card_flip()
				card2.card_flip()
			
			if self.pairs_left <= 0:
				# Basically victory
				time_played = time.time() - self.play_timer
				pygame.time.wait(1000)
				next_scene_params = {"next_scene": Scene.GAMEEND, "time_played": time_played}
				self.quit_loop(next_scene_params)
                
		self.reset_state()
		return self.scene_return_data










# TESTING
if __name__ == "__main__":

	mainscreen = pygame.display.set_mode((768, 768))
	test_menu = Gamelevel(mainscreen)

	next_scene_params = {"next_scene": 0, "total_cards": 16}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene:", next_scene_params["next_scene"])