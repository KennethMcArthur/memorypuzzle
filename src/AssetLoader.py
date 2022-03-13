# Memory Puzzle: Asset loading class


import os
import pygame



class AssetLoader:
    """ A collection of asset loading methods """
    _ASSETS_DIR = "assets"

    @staticmethod
    def load_image(filename: str) -> pygame.Surface:
        """ Error handling image loading function """
        fullname = os.path.join(AssetLoader._ASSETS_DIR, filename)
        try:
            return pygame.image.load(fullname)
        except Exception as message:
            print("Cannot load image:", filename)
            raise SystemExit(message)
    
    @staticmethod
    def load_font(fontname: str) -> str:
        return os.path.join(AssetLoader._ASSETS_DIR, fontname)