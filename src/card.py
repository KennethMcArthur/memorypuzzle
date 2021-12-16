# MEMORY PUZZLE: CARD OBJECT

import pygame
#



class Card:
    def __init__(self, coords: tuple,
                width: int,
                shape_sprite: pygame.Surface,
                card_color: pygame.Color,
                card_back: pygame.Surface) -> None:
        """ Defines a card object """

        self.width = width # We assume cards are regular squares
        self.mask_margin = int(width * 0.8) # 80% of the card surface
        self.x = coords[0]
        self.y = coords[1]

        self.card_color = card_color
        self.card_shape = shape_sprite
        self.card_face = pygame.transform.scale(shape_sprite, (self.width, self.width))
        self.card_back = pygame.transform.scale(card_back, (self.width, self.width))

        self.animation_counter = 0 # 0 face down card, self.width*2 face up card
        self.animation_speed = self.width // 10
        self.increment = 0


    def animate_face_up(self) -> None:
        """ Starts the animation forcing to flip the card face up """
        self.increment = self.animation_speed


    def animate_face_down(self) -> None:
        """ Starts the animation forcing to flip the card face down """
        self.increment = -self.animation_speed


    def card_flip(self) -> None:
        """ Starts the animation based on current state """
        if self.animation_counter <= 0: # Card is face down
            self.increment = self.animation_speed
        elif self.animation_counter >= self.width * 2: # Card is face up
            self.increment = -self.animation_speed


    def mouseover(self, current_mouse_pos: tuple) -> bool:
        """ Returns whether or not the mouse is inside this card area """
        x_area = self.x - self.width // 2
        y_area = self.y - self.width // 2
        x_check = x_area <= current_mouse_pos[0] <= x_area + self.width
        y_check = y_area <= current_mouse_pos[1] <= y_area + self.width
        return x_check and y_check


    def __eq__(self, other) -> bool:
        """ Overrides == operator to compare two cards """
        return self.card_shape == other.card_shape and self.card_color == other.card_color


    def game_tick_update(self, window: pygame.Surface, mousepos: tuple) -> None:
        """ Updates the object each frame """
        side_to_blit = None
        color_surface = None
        currentwidth = None
        
        if self.animation_counter <= self.width:
            # Drawing card back
            currentwidth = self.width - self.animation_counter
            side_to_blit = self.card_back
        if self.animation_counter >= self.width:
            # Drawing card face
            currentwidth = self.animation_counter - self.width
            side_to_blit = self.card_face
            color_surface = pygame.Surface((currentwidth, self.mask_margin))
            color_surface.fill(self.card_color)
        
        side_to_blit = pygame.transform.scale(side_to_blit, (currentwidth,self.width))
        side_to_blit.set_colorkey((0, 0, 0)) # setting black as transparent
        
        self.animation_counter += self.increment
        # Checking if animation is over
        if self.animation_counter <= 0 or self.animation_counter >= self.width*2:
            self.increment = 0
        
        final_x = self.x - currentwidth//2
        final_y = self.y - self.width//2

        if color_surface:
            window.blit(color_surface, (final_x, self.y - self.mask_margin//2))
        window.blit(side_to_blit, (final_x, final_y))














# LOCAL TESTING
def main_tests():

    import constants as CST
    import sys

    pygame.init()

    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True

    a_color = CST.CARDCOLORS[0]

    dummycard = Card((200,200), 64, CST.SHAPELIST[4], a_color, CST.CARD_BACK)
    dummybigcard = Card((64, 64), 128, CST.SHAPELIST[4], a_color, CST.CARD_BACK)

    print("The two cards have the same color and shape: ", dummybigcard == dummycard)

    while looping:
        gameclock.tick(CST.FPS)
        mousepos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                if dummybigcard.mouseover(mousepos):
                    dummybigcard.card_flip()
                if dummycard.mouseover(mousepos):
                    dummycard.card_flip()
        

        mainscreen.fill((125,125,125))
        dummybigcard.game_tick_update(mainscreen, mousepos)
        dummycard.game_tick_update(mainscreen, mousepos)
        pygame.display.update()


    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    main_tests()