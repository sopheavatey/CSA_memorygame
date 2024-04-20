'''run the program here'''
import pygame
import sys
from pygame.locals import *
from tkinter import *
import easy, medium, hard


WINDOWWIDTH = 640 
WINDOWHEIGHT = 480
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


        font = pygame.font.SysFont('arial', 42)
        titleText = font.render("Welcome to MEMORY GAME", True, (255, 255, 255))  # Use tuple for color
        titleRect = titleText.get_rect()
        titleRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)
        DISPLAYSURF.blit(titleText, titleRect)

        font = pygame.font.SysFont('arial', 28)
        easyText = font.render("Easy 3x4 grid", True, (255, 255, 255))  # Use tuple for color
        easyRect = easyText.get_rect()
        easyRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        DISPLAYSURF.blit(easyText, easyRect)

        mediumText = font.render("Medium 4x4 grid", True, (255, 255, 255))  # Use tuple for color
        mediumRect = mediumText.get_rect()
        mediumRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 40)
        DISPLAYSURF.blit(mediumText, mediumRect)

        hardText = font.render("Hard 6x6 grid", True, (255, 255, 255))  # Use tuple for color
        hardRect = hardText.get_rect()
        hardRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 80)
        DISPLAYSURF.blit(hardText, hardRect)

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

welcomeScreen()