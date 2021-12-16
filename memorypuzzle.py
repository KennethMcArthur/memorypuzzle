# MEMORY PUZZLE: main program file


import pygame, sys
from src import constants as CST
from src import board
from src import card


pygame.init()




def main_program():


    mainscreen = CST.MAINSCREEN
    gameclock = pygame.time.Clock()
    looping = True

    a_color = CST.CARDCOLORS[0]

    cardlist = [
        card.Card((200,200), 64, CST.SHAPELIST[4], a_color, CST.CARD_BACK),
        card.Card((64, 64), 128, CST.SHAPELIST[4], a_color, CST.CARD_BACK),
    ]


    while looping:
        gameclock.tick(CST.FPS)
        mousepos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False

            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                for singlecard in cardlist:
                    if singlecard.mouseover(mousepos):
                        singlecard.card_flip()
                        break        

        mainscreen.fill((125,125,125))

        for singlecard in cardlist:
            singlecard.game_tick_update(mainscreen, mousepos)
        
        pygame.display.update()


    pygame.quit()
    sys.exit()









if __name__ == "__main__":
    main_program()