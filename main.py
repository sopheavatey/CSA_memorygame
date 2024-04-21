import random, pygame, sys
from pygame.locals import *

# set up the constants
FPS = 30 # frames per second, controls the overall speed of the game
WINDOWWIDTH = 700 # width of the game window in pixels
WINDOWHEIGHT = 500 # height of the game window in pixels
REVEALSPEED = 10 # speed at which boxes reveal and cover in pixels per frame
BOXSIZE = 70 # size of each box (height and width) in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 0 # number of columns of boxes on the game board
BOARDHEIGHT = 0 # number of rows of boxes on the game board
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board must have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) # calculate the x-coordinate of the top left corner of the game board
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2) # calculate the y-coordinate of the top left corner of the game board

#            R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,  0,  0)
GRAY     = (100, 100, 100)
RED      = (255,   0,   0)
GREEN    = (  0, 102,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
LIGHTGRAY= (240, 240, 240)
DARKGRAY = ( 40,  40,  40)

BGCOLOR = (250, 248, 226)
LIGHTBGCOLOR = GRAY
BOXCOLOR = DARKGRAY
HIGHLIGHTCOLOR = (127, 146, 158)

SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, BLACK)
ALLSHAPES = (SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF
    global BOARDWIDTH, BOARDHEIGHT,BOXSIZE
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Memory Game')

    while True:
        DISPLAYSURF.fill(BGCOLOR) 

        font = pygame.font.SysFont('comic sans', 42, bold = True)
        titleText = font.render("WELCOME TO MEMORY GAME ", True,BLACK )  
        titleRect = titleText.get_rect()
        titleRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 5)
        DISPLAYSURF.blit(titleText, titleRect)

        font = pygame.font.SysFont('comic sans', 28)
        choiceText = font.render("PLEASE CHOOSE THE DIFFICULTY MODE", True, BLACK)#(229, 99, 143))  # Use tuple for color
        choiceRect = choiceText.get_rect()
        choiceRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + 40)
        DISPLAYSURF.blit(choiceText, choiceRect)

        font = pygame.font.SysFont('comic sans', 28)
        easyText = font.render("Easy", True, (87, 240, 60))  # Use tuple for color
        easyRect = easyText.get_rect()
        easyRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 40)
        DISPLAYSURF.blit(easyText, easyRect)

        mediumText = font.render("Medium", True, (30, 160, 255))  # Use tuple for color
        mediumRect = mediumText.get_rect()
        mediumRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100)
        DISPLAYSURF.blit(mediumText, mediumRect)

        hardText = font.render("Hard", True, (255, 10, 10))  # Use tuple for color
        hardRect = hardText.get_rect()
        hardRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 160)
        DISPLAYSURF.blit(hardText, hardRect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if easyRect.collidepoint(mousex, mousey):
                    BOXSIZE = 110
                    BOARDWIDTH = 4
                    BOARDHEIGHT = 2
                    calculateMargins()
                    return game()
                elif mediumRect.collidepoint(mousex, mousey):
                    BOXSIZE = 90
                    BOARDWIDTH = 4
                    BOARDHEIGHT = 4
                    calculateMargins()
                    return game()
                elif hardRect.collidepoint(mousex, mousey):
                    BOARDWIDTH = 6
                    BOARDHEIGHT = 6
                    calculateMargins()
                    return game()

def game():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        if showCongratulations():  # If player chooses to continue playing
                            return main()
                        else:  # If player chooses to quit
                           showThankYouMessage()
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    """
    This function creates a 2D list that keeps track of which boxes on the game board have been revealed.
    The "val" parameter is the initial value for each element in the list (typically False for not revealed, or True for revealed)
    """
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT) # creates a list with "val" repeated BOARDHEIGHT times, and appends it to the revealedBoxes list
    # returns the completed 2D list of revealed boxes
    return revealedBoxes


def getRandomizedBoard():
    """
    Creates a randomized game board with a set of icons.
    The board is a 2D list of tuples, where each tuple contains a shape and a color.
    """
    icons = [] # Get a list of every possible shape in every possible color.
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

def calculateMargins():
    global XMARGIN, YMARGIN
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

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


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # this variable is used as syntactic sugar for referencing 1/4 of the box size
    half =    int(BOXSIZE * 0.5)   # get pixel coordinates from board coordinates

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords

    if shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half  , BOXSIZE - half  ))  # draw the square
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))  # draw the diamond
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top)) # draw the diagonal line from top left to bottom right
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))  # draw the diagonal line from bottom left to top right
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half)) # draw the oval


def getShapeAndColor(board, boxx, boxy):
    """
    Given the game board, and x, y coordinates for a box,
    this function returns the shape and color of the icon in that box
    """
    return board[boxx][boxy][0], board[boxx][boxy][1]


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
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):      # For each iteration, coverage decreases by REVEALSPEED. This causes the boxes to appear to slide open
        drawBoxCovers(board, boxesToReveal, coverage)  # Draw the boxes with the updated coverage value. This causes the boxes to appear to slide open


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    # Loop through a range of values, incrementing by the REVEALSPEED variable
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage) #     # Draw the box covers with the current coverage level


def drawBoard(board, revealed):
    # Iterate through each column (boxx) and row (boxy) on the game board
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            # Get the left and top pixel coordinates of the current box
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # If the box is not revealed, draw a covered box using the BOXCOLOR
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # If the box is revealed, draw the icon at that position using the shape and color from the board
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    #Draws a highlighted border around the box at the given x and y coordinates on the board
    left, top = leftTopCoordsOfBox(boxx, boxy)
    # Draw a rectangle with a 4 pixel wide border, offset by 5 pixels from the box coordinates
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    #Draw the initial state of the game board with all boxes covered
    drawBoard(board, coveredBoxes) 


def hasWon(revealedBoxes):
    """
    Returns True if all the boxes have been revealed, otherwise False
    Input: revealedBoxes (list) - a 2D list that keeps track of the state of each box (True if revealed, False if covered)
    Output: True if all boxes are revealed, False otherwise
    """
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True

def showCongratulations():
    # Display congratulatory message and options for continuing or quitting
    while True:
        DISPLAYSURF.fill(BGCOLOR)

        font = pygame.font.SysFont('comic sans', 42, bold=True)
        congratulationText = font.render("Congratulations! You've won!", True, BLACK)
        congratulationRect = congratulationText.get_rect()
        congratulationRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)
        DISPLAYSURF.blit(congratulationText, congratulationRect)

        font = pygame.font.SysFont('comic sans', 28)
        continueText = font.render("Want to play again?", True, (27, 160, 69))
        continueRect = continueText.get_rect()
        continueRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 20)
        DISPLAYSURF.blit(continueText, continueRect)

        yesText = font.render("Yes", True, (38, 47, 255))
        yesRect = yesText.get_rect()
        yesRect.center = (WINDOWWIDTH // 2 - 50, WINDOWHEIGHT // 2 + 40)
        DISPLAYSURF.blit(yesText, yesRect)

        noText = font.render("No", True, (255, 10, 10))
        noRect = noText.get_rect()
        noRect.center = (WINDOWWIDTH // 2 + 50, WINDOWHEIGHT // 2 + 40)
        DISPLAYSURF.blit(noText, noRect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint(mousex, mousey):
                    return True  # Continue playing
                elif noRect.collidepoint(mousex, mousey):
                    return False  # Quit the game
                
def showThankYouMessage():
    # Display "thank you" message before quitting the game
    DISPLAYSURF.fill(BGCOLOR)

    font = pygame.font.SysFont('comic sans', 42)
    thankYouText = font.render("Thank you for playing!", True, (80, 31, 142))
    thankYouRect = thankYouText.get_rect()
    thankYouRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(thankYouText, thankYouRect)

    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 seconds before quitting
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()