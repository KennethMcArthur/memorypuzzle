# CONSTANTS



import pygame, os




# HELPER METHODS

def load_image(asset_folder: str, filename: str) -> pygame.Surface:
    """ Error handling image loading function """
    fullname = os.path.join(asset_folder, filename)
    try:
        return pygame.image.load(fullname)
    except Exception as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)

def _get_shapes(spritesheet: pygame.Surface) -> list:
    """ Returns a list of shape sprites """
    width, height = spritesheet.get_size()
    num_shapes = width // height
    
    shapelist = []

    for i in range(num_shapes):
        single_shape = pygame.Surface((height, height)).convert_alpha()
        single_shape.set_colorkey((0,0,0))
        single_shape.blit(spritesheet, (0,0), area=(height*i, 0, height, height))
        shapelist.append(single_shape)

    return shapelist

def _get_board_sizes(colors : list, shapes: list) -> dict:
    """ Builds the board size constant, based on current possible combinations """
    sizes = {
        # Format: total cards: (length of a board row, padding in pixels)
        4: (2, 30),
        8: (4, 30),
        12: (4, 30),
        16: (4, 30),
        20: (5, 30),
        24: (6, 10),
        30: (6, 10),
        36: (6, 10),
        42: (7, 10),
    }
    # Removing entries above the maximum possible combinations of color/shape
    max_combinations = len(colors) * len(shapes)
    for this_size in sizes.copy():
        if this_size > max_combinations:
            sizes.pop(this_size)
    
    return sizes




# GAME CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 768, 768
MAINSCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, flags=pygame.SCALED, vsync=1)

color_db = {
    "background": pygame.Color("#2A9D8F"),
    "regular_text": pygame.Color("#E9C46A"),
    "button_idle": pygame.Color("#264653"),
    "button_hover": pygame.Color("#38677A"),
    "button_text": pygame.Color("#F4A261"),
}


_ASSETS_DIR = "assets"
_EVERY_SHAPE = load_image(_ASSETS_DIR, "spritesheettestblue.png").convert_alpha()
CARD_BACK = load_image(_ASSETS_DIR, "MemoryCardBack.png").convert_alpha()
TITLE_FONT = os.path.join(_ASSETS_DIR, "kongtext.ttf") # Font by codeman38 | cody@zone38.net | http://www.zone38.net/
TEXT_COLOR = color_db["regular_text"]

FPS = 60

class SCENES:
    GAMEMENU = 0
    GAMELEVEL = 1
    GAMEEND = 2


CARDCOLORS = (
    pygame.Color("#FF0000"), # red, ok
    pygame.Color("#DEFF0A"), # yellow, ok
    pygame.Color("#0AFF58"), # green, ok
    pygame.Color("#147DF5"), # blue, ok
    pygame.Color("#FFFFFF"), # white, ok
    pygame.Color("#BE0AFF"), # light purple, ok
    pygame.Color("#FF8700"), # orange, ok
)

SHAPELIST = _get_shapes(_EVERY_SHAPE)


BUTTON_STYLE = {"button_color": color_db["button_idle"],
                "button_color_hover": color_db["button_hover"],
                "button_font": TITLE_FONT}


BOARD_SIZE = _get_board_sizes(CARDCOLORS, SHAPELIST)
