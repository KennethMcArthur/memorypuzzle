# MEMORY PUZZLE: Board method collection


import pygame
from random import sample
from card import Card





def get_combinations(total_cards: int, colors_db: list, shape_db: list) -> list:
    """ Returns a list of every needed combination of (shape, color), in pairs """
    total_card_pairs = total_cards // 2
    total_comb = []

    for shape in shape_db:
        for color in colors_db:
            total_comb.append((shape, color))
    
    return sample(total_comb, total_card_pairs) * 2
        

def _get_origin_point(screen: tuple, card_size: int, rows: int, row_length: int, padding: int) -> tuple:
    """ Generates the coordinates of the first card on the board """
    SCREEN_WIDTH, SCREEN_HEIGHT = screen
    screen_center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
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


def generate_cards_on_board(screen: tuple, rows: int, row_length: int, padding: int, seed_color_pairs: list) -> list:
    """ Places each cards at their coordinates """
    SCREEN_WIDTH, SCREEN_HEIGHT = screen
    factor = max(row_length, rows)
    card_size = (SCREEN_HEIGHT - padding * (factor + 1)) // factor
    origin_point = _get_origin_point(screen, card_size, rows, row_length, padding)
    coords_list = _get_cards_coords(origin_point, card_size, rows, row_length, padding)
    
    # Placing cards in the output list
    final_card_list = []
    for i, pos in enumerate(coords_list):
        final_card_list.append(Card(pos, card_size, *seed_color_pairs[i]))
    
    return final_card_list


def card_clicked_at(coords: tuple, card_list: list) -> Card:
    """ Returns the card at the clicked point, or None if no card was there """
    for card in card_list:
        if card.mouseover(coords) and card.is_selectable():
            return card

    return None
        

def get_optimal_row_length(total_cards: int) -> int:
    """ Returns the optimal length of a board row based on total card pool
        Raises ValueError if total_cards is not valid """

    if total_cards % 2 != 0:
        raise ValueError("Odd numbers are not allowed.")

    possible_rows_number = (num for num in range(2, total_cards) if total_cards % num == 0)

    optimal_row_length = 2 # let's avoid single-carded rows
    for rows in possible_rows_number:
        row_length = total_cards // rows
        if rows <= row_length:
            optimal_row_length = row_length

    # Final validation before allowing the value
    # we avoid few looong rows in favor of a more "squarey" board
    rows = total_cards // optimal_row_length
    delta = optimal_row_length - rows
    if delta > rows:
        raise ValueError("Not equally divisible.")

    return optimal_row_length


def get_possible_board_sizes() -> list:
    """ Returns every possible sizes of a board based on total cards allowed """
    board_sizes = []
    Card.generate_constants() # pygame needs a display before loading assets
    total_cards = Card.MAX_PAIRS_ALLOWED

    for num in range(2, total_cards+1): # 2 is the minimum board size
        try:
            get_optimal_row_length(num)
        except ValueError:
            continue
        board_sizes.append(num)
    
    return board_sizes




# LOCAL TESTING
if __name__ == "__main__":

    import sys
    import random

    pygame.init()
    pygame.mixer.init()

    mainscreen = pygame.display.set_mode((768, 768))
    gameclock = pygame.time.Clock()
    looping = True

    Card.generate_constants()
    total_cards = 42
    board_row_length = get_optimal_row_length(total_cards)
    padding = 10
    board_row_number = total_cards // board_row_length
    seed_color_pairs = get_combinations(total_cards, Card.CARD_COLORS, Card.SHAPELIST)
    random.shuffle(seed_color_pairs)
    card_list = generate_cards_on_board(mainscreen.get_size(), board_row_number, board_row_length, padding, seed_color_pairs)


    selected_cards = []
    need_wrong_answer_delay = False
    got_wrong_pair = False

    while looping:
        delta = gameclock.tick(60)
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