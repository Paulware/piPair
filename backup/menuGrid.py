import random, sys, pygame, time, copy
from pygame.locals import *
import buttonClass
import os
import sys
import SF30

#buttons = buttonClass.ButtonsClass(0.2)
sf30 = SF30.SF30()
while not sf30.joystick_detected:
    time.sleep (1.0)
    print ("Waiting for joystick " )
print ("Joystick detected" )

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 480 # width of the program's window, in pixels
WINDOWHEIGHT = 320 # height in pixels
SPACESIZE = 50 # width & height of each space on the board, in pixels
BOARDWIDTH = 8 # how many columns of spaces on the game board
BOARDHEIGHT = 8 # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation
mouseX = 6 # start mouse block
mouseY = 6 # start mouse block
BOXSIZE = 50 # size of box height & width in pixels

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255,   0,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN
quit = False

def leftTopCoordsOfBox(boxx, boxy):
    left = (boxx * BOXSIZE) + XMARGIN
    top  = (boxy * BOXSIZE) + YMARGIN
    return (left, top)
    
def drawMouse ():
    global DISPLAYSURF
    global mouseX
    global mouseY
    global RED
    half = int(BOXSIZE * 0.5)  # syntactic sugar
    left, top = leftTopCoordsOfBox(mouseX, mouseY) # get pixel coords from board coords    
    pygame.draw.polygon(DISPLAYSURF, RED, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    pygame.display.update()
       
def handleButton(data):
    global mouseX
    global mouseY
    global BOXSIZE
    global YMARGIN
    global XMARGIN
    global quit
    
    BOARDWIDTH = 5 # number of columns of icons
    BOARDHEIGHT = 5 # number of rows of icons
    
    for event in [sf30.read()]: # buttons.eventGet(): # pygame.event.get():
        if event != None: 
           print ("handleButton, handle event: " + str(event)) 
           if event == sf30.START_PRESSED:
               quit = True
               data['quit'] = True

           if event == sf30.UP_PRESSED:
               print ("Up pressed" )
               if (mouseY > 0): 
                   mouseY = mouseY - 1
               #time.sleep (0.3)      
              
           if event == sf30.DOWN_PRESSED:
               print ("Down pressed" )
               if (mouseY + 1 < BOARDHEIGHT): 
                   mouseY = mouseY + 1
               #time.sleep (0.3)
              
           if event == sf30.LEFT_PRESSED:
               print ("Left pressed" )
               if (mouseX > 0): 
                   mouseX = mouseX - 1                
               #time.sleep (0.3)
              
           if event == sf30.RIGHT_PRESSED:
               print ("Right pressed" )
               if (mouseX + 1< BOARDWIDTH): 
                   mouseX = mouseX + 1
               #time.sleep (0.3)
                  
           if (event == sf30.A_PRESSED) or (event == sf30.B_PRESSED):
               print ("Got an A or B mouse clicked event" )
               data['mouseClicked'] = True
               left, top = leftTopCoordsOfBox(1, 1)
               data ['movexy'] = (mouseX,mouseY)
               data['mousex'] = (mouseX * BOXSIZE) + XMARGIN
               data['mousey'] = (mouseY * BOXSIZE) + YMARGIN
               #time.sleep (0.3)
       
def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE
    global mousex, mousey
    global WINDOWWIDTH, WINDOWHEIGHT
    
    mousex, mousey = leftTopCoordsOfBox (mouseX, mouseY)

    #print ("Wait 10 seconds")
    #time.sleep (10)
    print ("pygame.init")
    pygame.init()
    print ("get the clock")
    MAINCLOCK = pygame.time.Clock()
    print ("set width/height")
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    print ("toggle full screen mode" )
    pygame.display.toggle_fullscreen() 
       
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    runGame()

def runSelection (name):
    global DISPLAYSURF
    print ("Run " + name)
    pygame.quit()
    os.system ("python " + name + ".py")
    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))                   


def runGame():
    global mousex
    global mousey
    global DISPLAYSURF
    global MAINCLOCK
    global quit
    
    tetrisSurf = FONT.render('Tetris', True, TEXTCOLOR, TEXTBGCOLOR2)
    tetrisRect = tetrisSurf.get_rect()
    tetrisRect.topright = (90, 20)   

    othelloSurf = FONT.render('Othello', True, TEXTCOLOR, TEXTBGCOLOR2)
    othelloRect = othelloSurf.get_rect()
    othelloRect.topright = (85, 70)   
    
    memorySurf = FONT.render('Memory', True, TEXTCOLOR, TEXTBGCOLOR2)
    memoryRect = memorySurf.get_rect()
    memoryRect.topright = (85, 120) 

    zombieSurf = FONT.render('Zombie Hat', True, TEXTCOLOR, TEXTBGCOLOR2)
    zombieRect = zombieSurf.get_rect()
    zombieRect.topright = (85, 170) 

    ticTacToeSurf = FONT.render('TIC TAC TOE', True, TEXTCOLOR, TEXTBGCOLOR2)
    ticTacToeRect = ticTacToeSurf.get_rect()
    ticTacToeRect.topright = (85, 220) 

    pacmanSurf = FONT.render('Pacman', True, TEXTCOLOR, TEXTBGCOLOR2)
    pacmanRect = pacmanSurf.get_rect()
    pacmanRect.topright = (185, 20) 

    driverSurf = FONT.render('Driver', True, TEXTCOLOR, TEXTBGCOLOR2)
    driverRect = driverSurf.get_rect()
    driverRect.topright = (185, 70) 
    
    starSurf = FONT.render ('Star Pusher', True, TEXTCOLOR, TEXTBGCOLOR2)
    starRect = starSurf.get_rect()
    starRect.topright = (185, 120) 
    
    gpsSurf = FONT.render('GPS', True, TEXTCOLOR, TEXTBGCOLOR2)
    gpsRect = tetrisSurf.get_rect()
    gpsRect.topright = (185, 170)  

    aliensSurf = FONT.render ('Aliens', True, TEXTCOLOR, TEXTBGCOLOR2)
    aliensRect = aliensSurf.get_rect()
    aliensRect.topright = (185, 220)	 
    
    btSurf = FONT.render ('BT', True, TEXTCOLOR, TEXTBGCOLOR2)
    btRect = btSurf.get_rect()
    btRect.topright = (285, 20)	    

    tankSurf = FONT.render ('Tank', True, TEXTCOLOR, TEXTBGCOLOR2)
    tankRect = tankSurf.get_rect()
    tankRect.topright = (285, 70)	    

    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    turn = random.choice(['computer', 'player'])

    print ("Draw board 3" )
    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard)
    #playerTile, computerTile = enterPlayerTile()

    drawMouse ()
    print ("Waiting for left right up down on players turn")
    while not quit: # main game loop
        print ("Players turn") 
            
         # Keep looping until the player clicks on a valid space.
         boardToDraw = mainBoard

         data = {'mouseClicked':False,'quit':False,
                 'mousex':mousex,'mousey':mousey}
         mousex = data ['mousex']
         mousey = data ['mousey']
         print ("Got data: " + str(data) )
         handleButton(data)
         drawMouse()
         if quit:
             pygame.quit()
         
         if (data['mouseClicked']): 
             print ("Mouse was clicked [x,y]: [" + str(mousex) + "," + str(mousey) + "]")                
             #if newGameRect.collidepoint( (mousex, mousey) ):
             #    # Start a new game
             #    return True
             #elif hintsRect.collidepoint( (mousex, mousey) ):
             #    # Toggle hints mode
             #    showHints = not showHints
             # movexy is set to a two-item tuple XY coordinate, or None value
             #movexy = getSpaceClicked(mousex, mousey)
             movexy = data['movexy']
             print ("Got space clicked :" + str(movexy))
             if (movexy == (0,1)):
                os.chdir ("/boot/examples/tetris")
                runSelection ("tetris")
                os.chdir ("/boot")               
             elif (movexy == (0,2)):
                os.chdir ("/boot/examples/othello")
                runSelection ("othello")
                os.chdir ("/boot")               
             elif (movexy == (0,3)):
                runSelection ("memoryPuzzle")
             elif (movexy == (0,4)):
                runSelection ("zombieHat")
             elif (movexy == (0,5)):
                runSelection ("ticTacToe")
             elif (movexy == (2,1)):
                os.chdir("/home/pacman")
                runSelection ("runPacman")
                os.chdir("/boot")
             elif (movexy == (2,2)): 
                runSelection ("tankDriver")
             elif (movexy == (2,3)):
                os.chdir ("/home/starPusher")
                runSelection ("starpusher")
                os.chdir ("/boot")
             elif (movexy == (2,4)):
                os.chdir ("/home/gps")
                runSelection ("gps")
                os.chdir ("/boot")
             elif (movexy == (2,5)):
                os.chdir ("/home/aliens")
                runSelection ("aliens")
                os.chdir ("/boot")
             elif (movexy == (4,1)):
                runSelection ("buttonHC05")                   
             elif (movexy == (4,2)):
                print ("chdir /home/pi/examples/tankControlSF30" );
                quit = True
                pygame.quit()
                break
                os.chdir ("/home/pi/examples/tankControlSF30")
                pygame.quit()
                os.system ("python main.py") 
                
                pygame.init()

                   
            # Draw the game board.
            print ("Draw board 1" )
            drawBoard(boardToDraw)

            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(tetrisSurf, tetrisRect)
            DISPLAYSURF.blit(othelloSurf, othelloRect)
            DISPLAYSURF.blit(memorySurf, memoryRect)
            DISPLAYSURF.blit(zombieSurf, zombieRect)
            DISPLAYSURF.blit(ticTacToeSurf, ticTacToeRect)
            DISPLAYSURF.blit(pacmanSurf, pacmanRect)
            DISPLAYSURF.blit(driverSurf, driverRect)
            DISPLAYSURF.blit(starSurf, starRect)
            DISPLAYSURF.blit(gpsSurf, gpsRect)
            DISPLAYSURF.blit(aliensSurf, aliensRect)
            DISPLAYSURF.blit(btSurf, btRect)
            DISPLAYSURF.blit(tankSurf, tankRect)

            MAINCLOCK.tick(FPS)
            pygame.display.update()
    
    print ("Done in main while loop?") 
    
    if False:
       print ("Draw board 2" )
       # Display the final score.
       drawBoard(mainBoard)

       textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
       textRect = textSurf.get_rect()
       textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
       DISPLAYSURF.blit(textSurf, textRect)

       # Display the "Play again?" text with Yes and No buttons.
       text2Surf = BIGFONT.render('Play again? (A=yes,B=no)', True, TEXTCOLOR, TEXTBGCOLOR1)
       text2Rect = text2Surf.get_rect()
       text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

       print("Second while true ?" )
       while True:
       
           # Process events until the user clicks on Yes or No.
           #if buttons.checkKey ("B"):
           #   return False
              
           #if button.checkKey ("A"):
           #   return True
              
           DISPLAYSURF.blit(textSurf, textRect)
           DISPLAYSURF.blit(text2Surf, text2Rect)
           DISPLAYSURF.blit(yesSurf, yesRect)
           DISPLAYSURF.blit(noSurf, noRect)
           DISPLAYSURF.blit(driverSurf, driverRect)
           pygame.display.update()
           MAINCLOCK.tick(FPS)


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def drawBoard(board):
    global DISPLAYSURF
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    


'''
def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
'''

def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break # break out of while loop, continue in for loop
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = EMPTY_SPACE # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}

'''
def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = FONT.render('Do you want to be white(A) or black(B)?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        if buttons.checkKey ("A"):
           print ("A button detected" )
           return [WHITE_TILE, BLACK_TILE]
        if buttons.checkKey ("B"):
           print ("B button detected")          
           return [BLACK_TILE, WHITE_TILE]
           
        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
'''

def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == BOARDWIDTH and y == 0) or \
           (x == 0 and y == BOARDHEIGHT) or \
           (x == BOARDWIDTH and y == BOARDHEIGHT)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

if __name__ == '__main__':
    main()