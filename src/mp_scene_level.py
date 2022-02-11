# MEMORY PUZZLE: Game level



import pygame
import random
import constants as CST
import board
from master_class_scene import Scene
from master_class_button import Button
import mp_background as bg



class Gamelevel(Scene):

	PARAMS_NEEDED = ["total_cards"]

	def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
		super().__init__(GAME_WINDOW)

    	# Scene Elements
		background = bg.Background()
		self.next_scene_params = {"next_scene": CST.SCENES.GAMEMENU,}

    	# Append order is draw order
		self.updatelist.append(background)
    
    
	def load_outside_params(self, params: dict) -> None:
		""" Loads a dictionary of parameters from another scene """
		# Validating parameter dict keys
		if not all(key in params for key in Gamelevel.PARAMS_NEEDED):
			raise KeyError("Missing key parameter")

		total_cards = params["total_cards"]
		board_row_length = board.rowify(total_cards)
		board_row_number = total_cards // board_row_length
		seed_color_pairs = board.get_combinations(total_cards, CST.CARDCOLORS, CST.SHAPELIST)
		random.shuffle(seed_color_pairs)
		self.card_list = board.generate_cards_on_board(board_row_number, board_row_length, 30, seed_color_pairs)
		self.updatelist.extend(self.card_list)

	def run(self, outside_params: dict) -> int:
		""" Main loop method """
		self.load_outside_params(outside_params)
		self.load_and_start_music() # Starting music only when Scene is active

		gameclock = pygame.time.Clock()

		selected_cards = []
		need_wrong_answer_delay = False
		got_wrong_pair = False

        # Main game loop
		while self.looping_active:

			delta = gameclock.tick(CST.FPS)
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
				if selected_cards[0] == selected_cards[1]:
					selected_cards[0].card_blocked = True
					selected_cards[1].card_blocked = True
					selected_cards.clear()
				else:
					need_wrong_answer_delay = True
					got_wrong_pair = True
					selected_cards[0].card_flip()
					selected_cards[1].card_flip()

            # Drawing sequence
			for gameobj in self.updatelist:
				gameobj.game_tick_update(self.GAME_WINDOW, mousepos, delta) # All classes have this methods
			pygame.display.update()

			if need_wrong_answer_delay:
				pygame.time.wait(1000)
				need_wrong_answer_delay = False
                
		self.reset_state()
		return self.scene_return_data






# TESTING
if __name__ == "__main__":

	test_menu = Gamelevel(CST.MAINSCREEN)

	next_scene_params = {"next_scene": 0, "total_cards": 16}
	next_scene_params = test_menu.run(next_scene_params)
	print("Next scene:", next_scene_params["next_scene"])