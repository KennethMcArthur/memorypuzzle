# MEMORY PUZZLE: Button Master Class



import pygame
import constants as CST
pygame.font.init()




class Button:

    STYLE_ATTR_NEEDED = ["button_color", "button_color_hover", "button_font"]

    def __init__(self, label: str, style: dict, pos_and_size: tuple, func_to_call=None, *func_parameters):
        """ Initializing button """
        
        # Validating style dict keys
        if not all(key in Button.STYLE_ATTR_NEEDED for key in style):
            raise KeyError("Missing style attribute")
        
        self.label = label
        self.style = style
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
            text_dim = pygame.font.Font(self.style["button_font"], size).size(self.label)
            size += 1

        self.font_surf = pygame.font.Font(self.style["button_font"], size-1)


    def _check_if_mouse_over(self, mousepos: tuple) -> bool:
        """ Returns if the mouse cursor is inside the button area """
        in_x = self.button_rect.x <= mousepos[0] <= self.button_rect.x + self.button_rect.width
        in_y = self.button_rect.y <= mousepos[1] <= self.button_rect.y + self.button_rect.height
        return in_x and in_y


    def mouse_clicked(self, mousepos: tuple):
        """ Calls the assigned method on button click, returns what that method returns """
        if self._check_if_mouse_over(mousepos):
            return self.func_to_call(*self.func_parameters)


    def game_tick_update(self, window: pygame.Surface, mousepos: tuple, delta: float):
        """ Updates the button each frame """

        mouse_is_over = self._check_if_mouse_over(mousepos)

        if mouse_is_over:
            actual_color = self.style["button_color_hover"]
        else:
            actual_color = self.style["button_color"]


        # Blitting on screen
        surf_to_blit = pygame.Surface((self.button_rect.width, self.button_rect.height))
        surf_to_blit.set_colorkey((0,0,0))
        surf_to_blit = self.font_surf.render(self.label, True, CST.color_db["button_text"])
        
        pygame.draw.rect(window, actual_color, self.button_rect, border_radius=self.button_border_radius)
        text_pos = (self.button_rect.centerx - surf_to_blit.get_width()//2, self.button_rect.centery - surf_to_blit.get_height()//2)
        window.blit(surf_to_blit, text_pos)









# TESTING
if __name__ == "__main__":
    import constants as CST
    import sys

    pygame.init()


    # dummy method
    def tell(what: str):
        print("I'm telling:", what)

    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True

    updatelist = [
        Button("Test1", CST.BUTTON_STYLE, (50,50, 150, 50), tell, "test1"),
        Button("Test2", CST.BUTTON_STYLE, (150,200, 150, 50), tell, "test2"),
        Button("This is a long text for a button", CST.BUTTON_STYLE, (300,300, 150, 50), tell, "looong text"),
        Button("Test4", CST.BUTTON_STYLE, (450,350, 150, 50), tell, "test 4"),
    ]

    while looping:
        delta = gameclock.tick(CST.FPS)
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
