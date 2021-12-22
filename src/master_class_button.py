# MEMORY PUZZLE: Button Master Class



import pygame





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

        # TODO: add font render
        pygame.draw.rect(window, actual_color, self.button_rect, border_radius=self.button_border_radius)
        window.blit(surf_to_blit, (self.button_rect.x, self.button_rect.y))