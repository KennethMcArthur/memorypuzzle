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




# GAME CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
MAINSCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, flags=pygame.SCALED, vsync=1)

_ASSETS_DIR = "assets"
_EVERY_SHAPE = load_image(_ASSETS_DIR, "spritesheettestblue.png").convert_alpha()
CARD_BACK = load_image(_ASSETS_DIR, "MemoryCardBackBorderless.png").convert_alpha()
TITLE_FONT = os.path.join(_ASSETS_DIR, "kongtext.ttf") # Font by codeman38 | cody@zone38.net | http://www.zone38.net/
TEXT_COLOR = (255,255,255) # White

FPS = 60

class SCENES:
    GAMEMENU = 0
    GAMELEVEL = 1


CARDCOLORS = (
    (255, 0, 0), # RED
    (0, 255, 0), # GREEN
    (0, 0, 255), # BLUE
    # ...add more
)

SHAPELIST = _get_shapes(_EVERY_SHAPE)


BUTTON_STYLE = {"button_color": (220, 0, 0),
                "button_color_hover": (255, 0, 0),
                "button_font": TITLE_FONT}


BOARD_SIZE = {
    4: 2,
    8: 4,
    12: 4,
    16: 4,
    20: 4,
    24: 4,
    30: 5,
    36: 6,
}

# Cheating by modifying a constant: this must be changed, it's a shame
max_combinations = len(CARDCOLORS) * len(SHAPELIST)
for size in BOARD_SIZE.copy():
    if size > max_combinations:
        BOARD_SIZE.pop(size)