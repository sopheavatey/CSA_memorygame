import random, pygame, sys
from pygame.locals import *

# Constants for game parameters
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 70
GAPSIZE = 10
BOARDWIDTH = 2
BOARDHEIGHT = 2
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

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
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

# Lists of all possible colors and shapes
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

# Main function to start the game
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # Initialize mouse coordinates
    mousex = 0
    mousey = 0

    # Set window caption
    pygame.display.set_caption('Memory Game')

    # Generate random game board and initialize revealed boxes
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None  # stores the (x, y) of the first box clicked.

    # Start game animation
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    # Main game loop
    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)  # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  # event handling loop
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
                revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                if firstSelection == None:  # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else:  # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):  # check if all pairs found
                        # gameWonAnimation(mainBoard)
                        # pygame.time.wait(2000)
                        displayBlankBaord(mainBoard)
                        # pygame.time.wait(10000)
                        gameWonMessage()
                        
                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None  # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
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
def getRandomizedBoard():
    """
    Creates a randomized game board with a set of icons.
    The board is a 2D list of tuples, where each tuple contains a shape and a color.
    """
    icons = []  # Get a list of every possible shape in every possible color.
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons)  # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # calculate how many icons are needed
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
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
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


# Function for the game won animation
# def gameWonAnimation(board):
#     coveredBoxes = generateRevealedBoxesData(True)
#     color1 = LIGHTBGCOLOR
#     color2 = BGCOLOR

#     for i in range(13):  # 13 iterations of animation
#         color1, color2 = color2, color1  # swap colors for each iteration
#         DISPLAYSURF.fill(color1)  # fill the background with the current color
#         drawBoard(board, coveredBoxes)  # draw the board with all boxes covered
#         pygame.display.update()  # update the display with the new background color and board
#         pygame.time.wait(300)  # wait for 300 milliseconds before swapping colors again

# display the blankboard when the game is won
def displayBlankBaord(board):
    coveredBoxes = generateRevealedBoxesData(True)
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(board, coveredBoxes)
    pygame.display.update()

# Display the message the the user won the game
def gameWonMessage():
    font = pygame.font.Font(None, 36)
    text = font.render("Congratulations! You've won the game!", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH //2 , WINDOWHEIGHT //2)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()
    # pygame.time.wait(2000)


# Function to check if all boxes are revealed
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
