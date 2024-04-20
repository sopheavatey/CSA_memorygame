'''run the program here'''
import pygame
import sys
from pygame.locals import *
from tkinter import *
import easy, medium, hard,main


WINDOWWIDTH = 700 
WINDOWHEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("WELCOME TO MEMORY GAME")



def welcomeScreen():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Memory Game')

    
    while True:
        DISPLAYSURF.fill((0, 0, 0))  # Use tuple for color


        font = pygame.font.SysFont('comic sans', 42)
        titleText = font.render("WELCOME TO MEMORY GAME ", True, (255, 255, 255))  # Use tuple for color
        titleRect = titleText.get_rect()
        titleRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 5)
        DISPLAYSURF.blit(titleText, titleRect)

        font = pygame.font.SysFont('comic sans', 30)
        choiceText = font.render("PLEASE CHOOSE THE DIFFICULTY MODE", True, (255, 255, 255))  # Use tuple for color
        choiceRect = titleText.get_rect()
        choiceRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + 40)
        DISPLAYSURF.blit(choiceText, choiceRect)

        font = pygame.font.SysFont('comic sans', 28)
        easyText = font.render("Easy", True, (255, 255, 255))  # Use tuple for color
        easyRect = easyText.get_rect()
        easyRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 20)
        DISPLAYSURF.blit(easyText, easyRect)

        mediumText = font.render("Medium", True, (255, 255, 255))  # Use tuple for color
        mediumRect = mediumText.get_rect()
        mediumRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 60)
        DISPLAYSURF.blit(mediumText, mediumRect)

        hardText = font.render("Hard", True, (255, 255, 255))  # Use tuple for color
        hardRect = hardText.get_rect()
        hardRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100)
        DISPLAYSURF.blit(hardText, hardRect)

        exText = font.render("Experiment", True, (255, 255, 255))  # Use tuple for color
        exRect = mediumText.get_rect()
        exRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 140)
        DISPLAYSURF.blit(exText, exRect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if easyRect.collidepoint(mousex, mousey):
                    return easy.main()
                elif mediumRect.collidepoint(mousex, mousey):
                    return medium.main()
                elif hardRect.collidepoint(mousex, mousey):
                    return hard.main()
                elif exRect.collidepoint(mousex, mousey):
                    return main.main()

welcomeScreen()