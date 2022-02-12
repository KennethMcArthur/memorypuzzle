# Memory Puzzle: Text Master class
# This class implements the basic methods for displaying text

import pygame
import constants as CST



class StaticText:
    """ Class for text """
    # Alignment Constants
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    def __init__(self, text: str, size: int, position: tuple, alignment: int = 0) -> None:
        self.alignment = alignment # Default is left
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.set_text(text)

    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        self.titletext = self.titlefont.render(new_text, True, CST.TEXT_COLOR)
        self.place_text()

    def place_text(self):
        """ Places the text at the proper coords based on alignment """
        self.titlerect = self.titletext.get_rect()
        if self.alignment == StaticText.LEFT:
            self.titlerect.topleft = (self.pos_x, self.pos_y)
        elif self.alignment == StaticText.CENTER:
            self.titlerect.center = (self.pos_x, self.pos_y)
        elif self.alignment == StaticText.RIGHT:
            self.titlerect.topright = (self.pos_x, self.pos_y)

    def game_tick_update(self, window: pygame.Surface, mouse_pos: tuple, delta: float) -> None:
        window.blit(self.titletext, self.titlerect)












# Local Testing
if __name__ == "__main__":
    import sys

    pygame.init()

    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True

    dummytext = StaticText("This is a test", 48, (100,100))

    while looping:
        delta = gameclock.tick(CST.FPS)
        mousepos = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False



        mainscreen.fill((125,125,125))
        dummytext.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()


    pygame.quit()
    sys.exit()