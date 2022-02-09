# MEMORY PUZZLE: Board element


import pygame
import constants as CST
from math import sqrt
from card import Card





def rowify(card_total: int) -> int:
    """ Splits the number of cards into equal rows """
    row_length = int(sqrt(card_total))
    
    for i in range(row_length, 0, -1):
        if card_total % i == 0:
            row_length = i
            break

    return row_length


def get_combinations(total_cards: int, colors_db: list, shape_db: list) -> list:
    """ Returns a list of every needed combination of (seed, color) """
    total_card_couples = total_cards // 2
    seeds_needed = total_card_couples // len(colors_db) +1 # Using every color possible first
    
    total_comb = []

    for seed_index in range(seeds_needed):
        for color in colors_db:
            total_comb.append((shape_db[seed_index], color))
            total_comb.append((shape_db[seed_index], color))

    return total_comb[:total_cards]
        


def generate_cards_on_board(rows: int, row_length: int, padding: int, seed_color_pairs: list) -> list:
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
    
    
    # Placing cards in the output list
    final_card_list = []
    i = 0
    for pos in coords_list:
        final_card_list.append(Card(pos, card_size, *seed_color_pairs[i], CST.CARD_BACK))
        i += 1
    
    return final_card_list


def card_clicked_at(coords: tuple, card_list: list) -> Card:
    """ Returns the card at the clicked point, or None if no card was there """
    # Checking if the mouse is over a card
    clicked_card = None
    for card in card_list:
        if card.mouseover(coords):
            clicked_card = card
            break
    
    # Checking if the card is clickable (not yet selected)
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


    total_cards = 16
    board_row_length = rowify(total_cards)
    board_row_number = total_cards // board_row_length
    seed_color_pairs = get_combinations(total_cards, CST.CARDCOLORS, CST.SHAPELIST)
    random.shuffle(seed_color_pairs)
    card_list = generate_cards_on_board(board_row_number, board_row_length,  30, seed_color_pairs)


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