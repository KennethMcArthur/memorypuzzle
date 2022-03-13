# MEMORY PUZZLE: Button Master Class


import pygame
from AssetLoader import AssetLoader




class Button(AssetLoader):

    # Style constants
    COLOR = pygame.Color("#264653")
    COLOR_HOVER = pygame.Color("#38677A")
    FONT = AssetLoader.load_font("kongtext.ttf")
    TEXT_COLOR = pygame.Color("#F4A261")

    def __init__(self, label: dict, pos_and_size: tuple, func_to_call=None, *func_parameters):
        """ Initializing button """        
        self.label = label
        self.button_rect = pygame.Rect(pos_and_size)
        self.button_border_radius = min(self.button_rect.width, self.button_rect.height) // 4
        self.func_to_call = func_to_call
        self.func_parameters = func_parameters

        # Text Surface generation (we adapt its size to button size)
        margin = self.button_rect.height // 5
        size = 1 # starting size
        text_dim = (0,0)
        max_width = self.button_rect.width - margin
        max_height = self.button_rect.height - margin

        while text_dim[0] < max_width and text_dim[1] < max_height:
            text_dim = pygame.font.Font(Button.FONT, size).size(self.label)
            size += 1

        self.FONT_SURFACE = pygame.font.Font(Button.FONT, size-1)


    def _is_mouse_over(self, mousepos: tuple) -> bool:
        """ Returns if the mouse cursor is inside the button area """
        in_x = self.button_rect.x <= mousepos[0] <= self.button_rect.x + self.button_rect.width
        in_y = self.button_rect.y <= mousepos[1] <= self.button_rect.y + self.button_rect.height
        return in_x and in_y


    def mouse_clicked(self, mousepos: tuple):
        """ Calls the assigned method on button click, returns what that method returns """
        if self._is_mouse_over(mousepos):
            return self.func_to_call(*self.func_parameters)


    def game_tick_update(self, window: pygame.Surface, mousepos: tuple, delta: float):
        """ Updates the button each frame """

        mouse_is_over = self._is_mouse_over(mousepos)

        if mouse_is_over:
            actual_color = Button.COLOR_HOVER
        else:
            actual_color = Button.COLOR

        # Blitting on screen
        surf_to_blit = pygame.Surface((self.button_rect.width, self.button_rect.height))
        surf_to_blit.set_colorkey((0,0,0))
        surf_to_blit = self.FONT_SURFACE.render(self.label, True, Button.TEXT_COLOR)
        
        pygame.draw.rect(window, actual_color, self.button_rect, border_radius=self.button_border_radius)
        text_pos = (self.button_rect.centerx - surf_to_blit.get_width()//2, self.button_rect.centery - surf_to_blit.get_height()//2)
        window.blit(surf_to_blit, text_pos)









# TESTING
if __name__ == "__main__":
    import sys

    pygame.init()


    # dummy method
    def tell(what: str):
        print("I'm telling:", what)

    mainscreen = pygame.display.set_mode((768, 768))
    gameclock = pygame.time.Clock()
    looping = True

    updatelist = [
        Button("Test1", (50,50, 150, 50), tell, "test1"),
        Button("Test2", (150,200, 150, 50), tell, "test2"),
        Button("This is a long text for a button", (300,300, 150, 50), tell, "looong text"),
        Button("Test4", (450,350, 150, 50), tell, "test 4"),
    ]

    while looping:
        delta = gameclock.tick(60) # 60 fps
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                for element in updatelist:
                    if isinstance(element, Button):
                        element.mouse_clicked(mousepos)

        mainscreen.fill((125,125,125))
        for element in updatelist:
            element.game_tick_update(mainscreen, mousepos, delta)
        pygame.display.update()


    pygame.quit()
    sys.exit()
