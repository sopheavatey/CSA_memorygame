import pygame
import sys
import random
from pygame.locals import *

# Constants for game parameters
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 70
GAPSIZE = 10
BOARDWIDTH = 0
BOARDHEIGHT = 0
NUMICONS = 0
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
board_width = BOARDWIDTH
board_height = BOARDHEIGHT
num_icons = NUMICONS

# Color constants
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 102, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

# Color constants for the game
BGCOLOR = WHITE
LIGHTBGCOLOR = GRAY
BOXCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE

# Shape constants
# DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

# Lists of all possible colors and shapes
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (SQUARE, DIAMOND, LINES, OVAL)

# Difficulty levels
EASY = {board_width : 3, board_height : 4, num_icons : 4}
MEDIUM = {'BOARDWIDTH': 6, 'BOARDHEIGHT': 3, 'NUMICONS': 9}
HARD = {'BOARDWIDTH': 8, 'BOARDHEIGHT': 4, 'NUMICONS': 16}

# Other game constants
WHITE = (255, 255, 255)
BGCOLOR = WHITE

# Pygame initialization
pygame.init()

# Function to display the welcome screen and choose difficulty level
def welcomeScreen():
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Memory Game')

    # Welcome message and difficulty selection
    DISPLAYSURF.fill(BLACK)
    font = pygame.font.SysFont('arial', 42)
    titleText = font.render("Welcome to Memory Game!", True, WHITE)
    titleRect = titleText.get_rect()
    titleRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(titleText, titleRect)

    font = pygame.font.SysFont('arial', 28)
    easyText = font.render("Easy 3x4 grid", True, WHITE)
    easyRect = easyText.get_rect()
    easyRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(easyText, easyRect)

    mediumText = font.render("Medium 4x4 grid", True, WHITE)
    mediumRect = mediumText.get_rect()
    mediumRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 40)
    DISPLAYSURF.blit(mediumText, mediumRect)

    hardText = font.render("Hard 6x6 grid", True, WHITE)
    hardRect = hardText.get_rect()
    hardRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 80)
    DISPLAYSURF.blit(hardText, hardRect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if easyRect.collidepoint(mousex, mousey):
                    return EASY
                elif mediumRect.collidepoint(mousex, mousey):
                    return MEDIUM
                elif hardRect.collidepoint(mousex, mousey):
                    return HARD

# Function to start the game
def main():
    # difficulty = welcomeScreen()

    # BOARDWIDTH = difficulty['BOARDWIDTH']
    # BOARDHEIGHT = difficulty['BOARDHEIGHT']
    # NUMICONS = difficulty['NUMICONS']

    # Other game parameters
    BOXSIZE = 70
    NAVYBLUE = (60, 60, 100)
    BOXCOLOR = NAVYBLUE
    HIGHLIGHTCOLOR = (0, 0, 255)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Memory Game')
    
    # Initialize game
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mainBoard = getRandomizedBoard(NUMICONS)
    revealedBoxes = generateRevealedBoxesData(False)
    firstSelection = None

    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

            if mouseClicked:  # Ensure this block is inside the event handling loop
       
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx != None and boxy != None:
                    if not revealedBoxes[boxx][boxy]:
                        drawHighlightBox(boxx, boxy)
                    if not revealedBoxes[boxx][boxy] and mouseClicked:
                        revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                        revealedBoxes[boxx][boxy] = True
                        if firstSelection == None:
                            firstSelection = (boxx, boxy)
                        else:
                            icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                            icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                            if icon1shape != icon2shape or icon1color != icon2color:
                                pygame.time.wait(1000)
                                coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                                revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                                revealedBoxes[boxx][boxy] = False
                            elif hasWon(revealedBoxes):
                                displayBlankBoard(mainBoard)
                            firstSelection = None  # reset firstSelection variable

        pygame.display.update()
        FPSCLOCK.tick(FPS)



# Function to generate revealed boxes data
def generateRevealedBoxesData(val):
    """
    This function creates a 2D list that keeps track of which boxes on the game board have been revealed.
    The "val" parameter is the initial value for each element in the list (typically False for not revealed, or True for revealed)
    """
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)  # creates a list with "val" repeated BOARDHEIGHT times, and appends it to the revealedBoxes list
    # returns the completed 2D list of revealed boxes
    return revealedBoxes


# Function to generate a randomized game board
# Gameboard GUI
def getRandomizedBoard(numIcons):
    """
    Creates a randomized game board with a set of icons.
    The board is a 2D list of tuples, where each tuple contains a shape and a color.
    """
    icons = []  # Get a list of every possible shape in every possible color.
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons)  # randomize the order of the icons list
    numIconsUsed = int(numIcons / 2)  # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2  # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]  # remove the icons as we assign them
        board.append(column)
    return board

# Function to split a list into groups of a specified size
def splitIntoGroupsOf(groupSize, theList):
    """
    This function takes in two parameters, groupSize and theList.
    It splits theList into a list of lists, where the inner lists have at most groupSize number of items.
    """
    result = []  # initialize an empty list to store the split lists
    for i in range(0, len(theList), groupSize):  # iterate over theList with a step of groupSize
        result.append(theList[i:i + groupSize])  # append a slice of theList from i to i+groupSize to the result list
    return result  # return the final list of lists.


# Function to convert board coordinates to pixel coordinates
def leftTopCoordsOfBox(boxx, boxy):
    """
    Convert board coordinates to pixel coordinates
    boxx: x-coordinate of the box on the board (column)
    boxy: y-coordinate of the box on the board (row)
    returns: a tuple containing the left and top pixel coordinates of the box
    """
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


# Function to get box coordinates from pixel coordinates
def getBoxAtPixel(x, y):
    """
    Given x and y coordinates, this function returns the box number (in terms of
    column and row) that the coordinates belong to. If the coordinates do not belong
    to any box, it returns (None, None).
    """
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


# Function to draw an icon on a box
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)
    # if shape == DONUT:
    #     pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
    #     pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    if shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


# Function to get the shape and color of an icon at given coordinates
def getShapeAndColor(board, boxx, boxy):
    """
    Given the game board, and x, y coordinates for a box,
    this function returns the shape and color of the icon in that box
    """
    return board[boxx][boxy][0], board[boxx][boxy][1]


# Function to draw covered or revealed boxes
def drawBoxCovers(board, boxes, coverage):
    """
    Draws boxes being covered/revealed.
    board: the game board containing the icons
    boxes: a list of two-item lists, which have the x & y spot of the box.
    coverage: the amount of coverage for boxes, where 0 is fully revealed and BOXSIZE is fully covered
    """
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


# Function to reveal boxes with animation
def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


# Function to cover boxes with animation
def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


# Function to draw the game board
def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


# Function to draw a highlight box around a selected box
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


# Function to start the game animation
def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


# display the blankboard when the game is won
def displayBlankBoard(board):
    coveredBoxes = generateRevealedBoxesData(True)
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(board, coveredBoxes)
    pygame.display.update()

# Display the message the the user won the game
# def gameWonMessage():
#     font = pygame.font.Font(None, 36)
#     text = font.render("Congratulations! You've won the game!", True, BLACK)
#     textRect = text.get_rect()
#     textRect.center = (WINDOWWIDTH //2 , WINDOWHEIGHT //2)
#     DISPLAYSURF.blit(text, textRect)
#     pygame.display.update()
    


# Function to check if all boxes are revealed
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
