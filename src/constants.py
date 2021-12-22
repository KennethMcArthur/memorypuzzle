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
MAINSCREEN = pygame.display.set_mode((1024, 768))#, flags=pygame.SCALED, vsync=1)

_ASSETS_DIR = "assets"
_EVERY_SHAPE = load_image(_ASSETS_DIR, "spritesheettestblue.png").convert_alpha()
CARD_BACK = load_image(_ASSETS_DIR, "MemoryCardBackBorderless.png").convert_alpha()


FPS = 60

class SCENES:
    GAMEMENU = 0


CARDCOLORS = (
    (255, 0, 0), # RED
    (0, 255, 0), # GREEN
    (0, 0, 255), # BLUE
    # ...add more
)

SHAPELIST = _get_shapes(_EVERY_SHAPE)


BUTTON_STYLE = {"button_color": (220, 0, 0),
                "button_color_hover": (255, 0, 0),
                "button_font": "arial"}