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

        #self.card_pos = self.generate_cards_positions(self.card_rows, self.card_row_length, padding)


    def rowify(self, card_total: int) -> int:
        """ Splits the number of cards into equal rows """
        row_length = int(sqrt(card_total))
        
        for i in range(row_length, 0, -1):
            if card_total % i == 0:
                row_length = i
                break

        return row_length


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
        
        
        # Placing cards
        self.card_list = []
        for pos in coords_list:
            self.card_list.append(Card(pos, card_size,CST.SHAPELIST[4], CST.CARDCOLORS[0], CST.CARD_BACK))

        

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


    while looping:
        delta = gameclock.tick(CST.FPS)
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                for card in dummyboard.card_list:
                    if card.mouseover(mousepos):
                        card.card_flip()


        mainscreen.fill((125,125,125))
        dummyboard.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()


    pygame.quit()
    sys.exit()