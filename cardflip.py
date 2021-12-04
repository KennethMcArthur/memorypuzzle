# Pygame card flip test



import pygame, sys



pygame.init()

FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0 , 0)
WHITE = (255, 255, 255)


CARDCOLORS = (
    (255, 0, 0), # RED
    (0, 255, 0), # GREEN
    (0, 0, 255), # BLUE
)




def get_shapes(spritesheet: pygame.Surface) -> list:
    """ Returns a list of shape sprites """
    width, height = spritesheet.get_size()
    num_shapes = width // height
    
    shapelist = []

    for i in range(num_shapes):
        single_shape = pygame.Surface((height, height)).convert_alpha()
        single_shape.set_colorkey(BLACK)
        single_shape.blit(spritesheet, (0,0), area=(height*i, 0, height, height))
        shapelist.append(single_shape)

    return shapelist





class Card:
    def __init__(self, coords: tuple, width: int, shape_sprite: pygame.Surface):
        """ Defines a card object """
        self.width = width # We assume cards are regular squares
        self.mask_margin = int(width * 0.8) # 80% of the card surface
        self.x = coords[0]
        self.y = coords[1]

        self.card_face = shape_sprite
        self.card_face = pygame.transform.scale(self.card_face, (self.width, self.width))
        self.card_back = pygame.image.load("assets\\MemoryCardBackBorderless.png")
        self.card_back = pygame.transform.scale(self.card_back, (self.width, self.width))

        self.animation_counter = 0 # 0 face down card, self.width*2 face up card
        self.animation_speed = 5
        self.increment = 0


    def animate_face_up(self) -> None:
        """ Starts the animation forcing to flip the card face up """
        self.increment = self.animation_speed


    def animate_face_down(self) -> None:
        """ Starts the animation forcing to flip the card face down """
        self.increment = -self.animation_speed


    def card_flip(self):
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

    def game_tick_update(self, window: pygame.Surface, mousepos: tuple) -> None:
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
            color_surface.fill(CARDCOLORS[1])
        
        side_to_blit = pygame.transform.scale(side_to_blit, (currentwidth,self.width))
        side_to_blit.set_colorkey(BLACK)
        
        self.animation_counter += self.increment
        # Checking if animation is over
        if self.animation_counter <= 0 or self.animation_counter >= self.width*2:
            self.increment = 0
        
        final_x = self.x - currentwidth//2
        final_y = self.y - self.width//2

        if color_surface:
            window.blit(color_surface, (final_x, self.y - self.mask_margin//2))
        window.blit(side_to_blit, (final_x, final_y))







def main():

    mainscreen = pygame.display.set_mode((300, 300))#, flags=pygame.SCALED, vsync=1)
    gameclock = pygame.time.Clock()
    looping = True

    shapes_db = pygame.image.load("assets\\spritesheettestblue.png").convert_alpha()
    SHAPELIST = get_shapes(shapes_db)

    dummycircle = Card((64, 64), 128, SHAPELIST[4])
    dummycard = Card((200,200), 64, SHAPELIST[5])


    while looping:
        gameclock.tick(FPS)
        mousepos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                if dummycircle.mouseover(mousepos):
                    dummycircle.card_flip()
                if dummycard.mouseover(mousepos):
                    dummycard.card_flip()
        


        mainscreen.fill((125,125,125))
        dummycircle.game_tick_update(mainscreen, mousepos)
        dummycard.game_tick_update(mainscreen, mousepos)
        pygame.display.update()

    pygame.quit()
    sys.exit()






if __name__ == "__main__":
    main()
