# MEMORY PUZZLE: Board element


import pygame
from random import sample
import constants as CST
from math import sqrt
from card import Card





def get_combinations(total_cards: int, colors_db: list, shape_db: list) -> list:
    """ Returns a list of every needed combination of (shape, color), in pairs """
    total_card_pairs = total_cards // 2
    total_comb = []

    for shape in shape_db:
        for color in colors_db:
            total_comb.append((shape, color))
    
    return sample(total_comb, total_card_pairs) * 2
        

def _get_origin_point(card_size: int, rows: int, row_length: int, padding: int) -> tuple:
    """ Generates the coordinates of the first card on the board """
    screen_center = (CST.SCREEN_WIDTH//2, CST.SCREEN_HEIGHT//2)
    board_width = card_size * row_length + padding * (row_length - 1)
    board_height = card_size * rows + padding * (rows - 1)

    origin_x = screen_center[0] - board_width // 2 + card_size // 2
    origin_y = screen_center[1] - board_height // 2 + card_size // 2

    return (origin_x, origin_y)


def _get_cards_coords(origin_point: tuple, card_size: int, rows: int, row_length: int, padding: int) -> list:
    """ Generates a placing point on the screen for each cards """
    coords_list = []

    for row in range(rows):
        for col in range(row_length):
            this_x = origin_point[0] + (card_size + padding) * col
            this_y = origin_point[1] + (card_size + padding) * row
            coords_list.append((this_x, this_y))
    
    return coords_list


def generate_cards_on_board(rows: int, row_length: int, padding: int, seed_color_pairs: list) -> list:
    """ Places each cards at their coordinates """
    factor = max(row_length, rows)
    card_size = (CST.SCREEN_HEIGHT - padding * (factor + 1)) // factor
    origin_point = _get_origin_point(card_size, rows, row_length, padding)
    coords_list = _get_cards_coords(origin_point, card_size, rows, row_length, padding)
    
    # Placing cards in the output list
    final_card_list = []
    for i, pos in enumerate(coords_list):
        final_card_list.append(Card(pos, card_size, *seed_color_pairs[i], CST.CARD_BACK))
    
    return final_card_list


def card_clicked_at(coords: tuple, card_list: list) -> Card:
    """ Returns the card at the clicked point, or None if no card was there """
    # Checking if the mouse is over a card
    clicked_card = None
    for card in card_list:
        if card.mouseover(coords):
            clicked_card = card
            break

    if clicked_card is not None and clicked_card.is_selectable():
        return clicked_card

    return None
        










# LOCAL TESTING
if __name__ == "__main__":

    import sys
    import random

    pygame.init()

    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True


    total_cards = 42
    board_row_length, padding = CST.BOARD_SIZE.get(total_cards)
    board_row_number = total_cards // board_row_length
    seed_color_pairs = get_combinations(total_cards, CST.COLOR.CARDCOLORS, CST.SHAPELIST)
    random.shuffle(seed_color_pairs)
    card_list = generate_cards_on_board(board_row_number, board_row_length, padding, seed_color_pairs)


    selected_cards = []
    need_wrong_answer_delay = False
    got_wrong_pair = False

    while looping:
        delta = gameclock.tick(CST.FPS)
        mousepos = pygame.mouse.get_pos()

        if got_wrong_pair:
            if all(card.is_fully_flipped() for card in selected_cards):
                selected_cards.clear()
                got_wrong_pair = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                if len(selected_cards) < 2 and not got_wrong_pair:
                    this_card = card_clicked_at(mousepos, card_list)
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

        mainscreen.fill((125,125,125))
        for card in card_list:
            card.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()

        if need_wrong_answer_delay:
            pygame.time.wait(1000)
            need_wrong_answer_delay = False





    pygame.quit()
    sys.exit()