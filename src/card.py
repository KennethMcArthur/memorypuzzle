# MEMORY PUZZLE: CARD OBJECT

import pygame
from AssetLoader import AssetLoader



class Card(AssetLoader):

    CARD_COLORS = (
        pygame.Color("#FF0000"), # red
        pygame.Color("#DEFF0A"), # yellow
        pygame.Color("#0AFF58"), # green
        pygame.Color("#147DF5"), # blue
        pygame.Color("#FFFFFF"), # white
        pygame.Color("#BE0AFF"), # light purple
        pygame.Color("#FF8700"), # orange
    )

    @staticmethod
    def generate_constants():
        """ Call this before creating cards, assets cannot be loaded without display """
        Card._EVERY_SHAPE = AssetLoader.load_image("shapemask.png", transparency=True)
        Card.SHAPELIST = AssetLoader.get_card_shapes(Card._EVERY_SHAPE)
        Card.CARD_BACK = AssetLoader.load_image("MemoryCardBack.png", transparency=True)
        Card.CARD_FLIP_SOUND = AssetLoader.load_audio_sfx("Card-flip-sound-effect.ogg")
        Card.MAX_PAIRS_ALLOWED = len(Card.SHAPELIST) * len(Card.CARD_COLORS)
        

    def __init__(self, coords: tuple,
                width: int,
                shape_sprite: pygame.Surface,
                card_color: pygame.Color) -> None:
        """ Defines a card object """

        self.width = width # We assume cards are regular squares
        self.mask_margin = int(width * 0.8) # 80% of the card surface
        self.x = coords[0]
        self.y = coords[1]

        self.card_color = card_color
        self.card_shape = shape_sprite
        self.card_face = pygame.transform.scale(shape_sprite, (self.width, self.width))
        self.card_back = pygame.transform.scale(Card.CARD_BACK, (self.width, self.width))

        self.animation_counter = 0 # 0 face down card, self.width*2 face up card
        self.animation_speed = self.width // 10
        self.increment = 0

        self.card_blocked = False


    def animate_face_up(self) -> None:
        """ Starts the animation forcing to flip the card face up """
        self.increment = self.animation_speed


    def animate_face_down(self) -> None:
        """ Starts the animation forcing to flip the card face down """
        self.increment = -self.animation_speed


    def card_flip(self) -> None:
        """ Starts the animation based on current state """
        if self.card_blocked:
            return
        if self.animation_counter <= 0: # Card is face down
            self.increment = self.animation_speed
        elif self.animation_counter >= self.width * 2: # Card is face up
            self.increment = -self.animation_speed
        Card.CARD_FLIP_SOUND.play()


    def is_selectable(self) -> bool:
        """ Returns of the card is not blocked or yet to be selected """
        return not self.card_blocked and self.animation_counter <= 0


    def is_animation_over(self) -> bool:
        """ Used to check if any animation is over """
        return self.animation_counter <= 0 or self.animation_counter >= self.width*2


    def is_fully_flipped(self) -> bool:
        return self.increment == 0 and self.is_animation_over()


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


    def game_tick_update(self, window: pygame.Surface, mousepos: tuple, delta: float) -> None:
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
            currentwidth = min(self.animation_counter - self.width, self.width) # Clamping to self.width
            side_to_blit = self.card_face
            color_surface = pygame.Surface((currentwidth, self.mask_margin))
            color_surface.fill(self.card_color)
        
        side_to_blit = pygame.transform.scale(side_to_blit, (currentwidth, self.width))
        side_to_blit.set_colorkey((0, 0, 0)) # setting black as transparent
        
        self.animation_counter += self.increment
        # Checking if animation is over
        if self.is_animation_over():
            self.increment = 0
        
        final_x = self.x - currentwidth//2
        final_y = self.y - self.width//2

        if color_surface:
            window.blit(color_surface, (final_x, self.y - self.mask_margin//2))
        window.blit(side_to_blit, (final_x, final_y))













# LOCAL TESTING
def main_tests():

    import sys

    pygame.init()

    mainscreen = pygame.display.set_mode((768, 768))
    gameclock = pygame.time.Clock()
    looping = True

    Card.generate_constants()
    a_color = Card.CARD_COLORS[0]

    dummycard = Card((200,200), 64, Card.SHAPELIST[4], a_color)
    dummybigcard = Card((64, 64), 128, Card.SHAPELIST[4], a_color)

    print("The two cards have the same color and shape: ", dummybigcard == dummycard)

    while looping:
        delta = gameclock.tick(60) # fps
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
        dummybigcard.game_tick_update(mainscreen, mousepos, delta)
        dummycard.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()


    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    main_tests()