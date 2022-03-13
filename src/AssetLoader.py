# Memory Puzzle: Asset loading class


import os
import pygame



class AssetLoader:
    """ A collection of asset loading methods """
    pygame.mixer.init()
    pygame.font.init()

    _ASSETS_DIR = "assets"

    @staticmethod
    def load_image(filename: str, transparency=False) -> pygame.Surface:
        """ Error handling image loading function """
        fullname = os.path.join(AssetLoader._ASSETS_DIR, filename)
        try:
            if transparency:
                return pygame.image.load(fullname).convert_alpha()
            else:
                return pygame.image.load(fullname)
        except Exception as message:
            print("Cannot load image:", filename)
            raise SystemExit(message)


    @staticmethod
    def load_audio_sfx(filename: str) -> pygame.mixer.Sound:
        """ Error handling audio loading function """
        fullname = os.path.join(AssetLoader._ASSETS_DIR, filename)
        try:
            return pygame.mixer.Sound(fullname)
        except Exception as message:
            print("Cannot load audio:", filename)
            raise SystemExit(message)


    @staticmethod
    def load_font(fontname: str) -> str:
        return os.path.join(AssetLoader._ASSETS_DIR, fontname)


    @staticmethod
    def get_card_shapes(spritesheet: pygame.Surface) -> list:
        """ Splits the spritesheet, returning a list of single sprites """
        width, height = spritesheet.get_size()
        num_shapes = width // height
        
        shapelist = []

        for i in range(num_shapes):
            single_shape = pygame.Surface((height, height)).convert_alpha()
            single_shape.set_colorkey((0,0,0))
            single_shape.blit(spritesheet, (0,0), area=(height*i, 0, height, height))
            shapelist.append(single_shape)

        return shapelist