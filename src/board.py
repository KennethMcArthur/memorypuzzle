# MEMORY PUZZLE: Board element


import pygame
import constants as CST
from math import sqrt


from card import Card





class Board:
    def __init__(self, num_cards: int, padding: int) -> None:
        """ Defines a board object, with the number of cards and padding between them """
        self.total_cards = num_cards
        self.card_row_length = self.rowify(num_cards)
        self.card_rows = num_cards // self.card_row_length
        self.card_list = []
        #self.card_pos = self.generate_cards_positions(self.card_rows, self.card_row_length, padding)


    def rowify(self, card_total: int) -> int:
        """ Splits the number of cards into equal rows """
        row_length = int(sqrt(card_total))
        
        for i in range(row_length, 0, -1):
            if card_total % i == 0:
                row_length = i
                break

        return row_length


    def get_combinations(self, total_cards: int) -> list:
        """ Returns a list of every needed combination of (seed, color) """
        total_card_couples = total_cards // 2
        seeds_needed = total_card_couples // len(CST.CARDCOLORS) +1 # Using every color possible first
        
        total_comb = []

        for seed_index in range(seeds_needed):
            for color in CST.CARDCOLORS:
                total_comb.append((CST.SHAPELIST[seed_index], color))
                total_comb.append((CST.SHAPELIST[seed_index], color))
            

        return total_comb[:total_cards]
        


    def generate_cards_positions(self, rows: int, row_length: int, padding: int) -> list:
        """ Places each cards at their coordinates """
        game_field_width = min(CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT)
        card_size = (game_field_width - padding * (row_length + 1)) // row_length

        screen_center = (CST.SCREEN_WIDTH//2, CST.SCREEN_HEIGHT//2)
        board_size = card_size * row_length + padding * (row_length-1)
        origin_point = (screen_center[0] - board_size // 2 + card_size // 2,
                        screen_center[1] - board_size // 2 + card_size // 2)

        coords_list = []
        for row in range(row_length):
            for col in range(row_length):
                this_coord = (origin_point[0] + (card_size + padding)*col,
                              origin_point[1] + (card_size + padding)*row)
                coords_list.append(this_coord)
        
        
        seed_and_color = self.get_combinations(rows * row_length)
        
        # Placing cards
        i = 0
        for pos in coords_list:
            self.card_list.append(Card(pos, card_size, *seed_and_color[i], CST.CARD_BACK))
            i += 1


    def card_clicked_at(self, coords: tuple) -> Card:
        """ Returns the card at the clicked point, or None if no card was there """
        # Checking if the mouse is over a card
        clicked_card = None
        for card in self.card_list:
            if card.mouseover(coords):
                clicked_card = card
                break
        
        # Checking if rthe card is clickable (not yet selected)
        if clicked_card is not None and clicked_card.is_selectable():
            return clicked_card

        return None


    def game_tick_update(self, window: pygame.Surface, mousepos: tuple, delta: float) -> None:
        for card in self.card_list:
            card.game_tick_update(window, mousepos, delta)
        












# LOCAL TESTING
if __name__ == "__main__":

    import sys

    pygame.init()

    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True

    dummyboard = Board(16, 5)
    dummyboard.generate_cards_positions(4, 4,  30)

    print(len(dummyboard.get_combinations(16)))

    selected_cards = []

    while looping:
        delta = gameclock.tick(CST.FPS)
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                if len(selected_cards) < 2:
                    this_card = dummyboard.card_clicked_at(mousepos)
                    if this_card:
                        this_card.card_flip()
                        selected_cards.append(this_card)


        # Card checking
        need_wrong_answer_delay = False
        if len(selected_cards) == 2 and all(card.is_fully_flipped() for card in selected_cards):
            if selected_cards[0] == selected_cards[1]:
                selected_cards[0].card_blocked = True
                selected_cards[1].card_blocked = True
            else:
                need_wrong_answer_delay = True
                selected_cards[0].card_flip()
                selected_cards[1].card_flip()                
            selected_cards.clear()


        mainscreen.fill((125,125,125))
        dummyboard.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()

        if need_wrong_answer_delay:
            pygame.time.wait(1500)


    pygame.quit()
    sys.exit()