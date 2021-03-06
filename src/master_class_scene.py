# Memory Puzzle: Scene Master class
# This class implements the basic methods for running a scene


import pygame, sys




class Scene:
    # Scenes list
    GAMEMENU = 0
    GAMELEVEL = 1
    GAMEEND = 2
    GAMECREDITS = 3
    
    def __init__(self, GAME_WINDOW: pygame.Surface) -> None:
        """ Inizalization phase, always call the super().__init__ at the beginning of an overridden __init__ """
        self.GAME_WINDOW = GAME_WINDOW
        self.looping_active = True
        self.updatelist = []


    def event_checking(self, this_event: pygame.event) -> None:
        """ Overridable to check different events """
        if this_event.type == pygame.QUIT: # Handling of quit event
            pygame.quit()
            sys.exit() # ensures we quit game AND program


    def quit_loop(self, data_to_return: dict) -> None:
        """ Method to exit from the run() loop that tells it what to return """
        self.looping_active = False

        KEY_NEEDED = ["next_scene",]
        # Validating style dict keys
        if not all(key in data_to_return for key in KEY_NEEDED):
            raise KeyError("Missing needed dictionary key")

        self.scene_return_data = data_to_return


    def reset_state(self) -> None:
        """ Method for resetting the state of a Scene after moving on """
        self.looping_active = True


    def text_to_update(self) -> None:
        """ To be overridden to update any text at the beginning of the scene """
        pass


    def load_outside_params(self, params: dict) -> None:
        """ Loads a dictionary of parameters from another scene """
        pass


    def run(self, outside_params: dict) -> int:
        """ Main loop method """
        self.load_outside_params(outside_params)
        self.text_to_update()
        
        gameclock = pygame.time.Clock()

        # Main game loop
        while self.looping_active:

            delta = gameclock.tick(60)

            for event in pygame.event.get():
                self.event_checking(event)

            cursor_pos = pygame.mouse.get_pos()

            # Drawing sequence
            for gameobj in self.updatelist:
                gameobj.game_tick_update(self.GAME_WINDOW, cursor_pos, delta) # All classes have this methods
            pygame.display.update()
                
        self.reset_state()
        return self.scene_return_data