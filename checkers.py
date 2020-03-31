import inspect
def checkersPage():
   global joining 
   global move 
   
   SQUAREWIDTH = 50
   BOARDY = 50
   BOARDX = 100 
   RADIUS = int((SQUAREWIDTH/2) - 10)
   OFFSET = 0   
      
   def inBoard (x,y):
      insideBoard = False
      if (x >= BOARDX) and (y >= BOARDY):
         if (x <= (BOARDX+(8*SQUAREWIDTH))) and (y <= (BOARDY+(8*SQUAREWIDTH))): 
            insideBoard = True
      return insideBoard
      
   def legalMove (selectedIndex, x, y, color):
      legal = True
      if color == 'red':
         fromX = redLocations[selectedIndex][0]
         fromY = redLocations[selectedINdex][1]
      else:
         fromX = redLocations[selectedIndex][0]
         fromY = redLocations[selectedINdex][1]
      if (fromX == x) and (fromY == y):
         showStatus ( 'Cannot move to same position' )
         legal = False
      return legal
    
   def xToPixel (x):
      return BOARDX + (x * SQUAREWIDTH)
      
   def yToPixel (y):
      return BOARDY + (y * SQUAREWIDTH)
    
   def drawBoard(): 
      DISPLAYSURF.fill((WHITE)) 
      y = BOARDY
      count = 0
      for i in range (8):
         for j in range (8):
            count = count + 1
            x = BOARDX + (j * SQUAREWIDTH)
            if (count % 2) == 1:
               pygame.draw.rect(DISPLAYSURF, BLACK, (x,y,SQUAREWIDTH, SQUAREWIDTH))
            else:                  
               pygame.draw.rect(DISPLAYSURF, RED, (x,y,SQUAREWIDTH, SQUAREWIDTH))
         y = y + SQUAREWIDTH
         count = count + 1 # stagger the colors   
   
      count = 0
      for piece in redPieces:
         x = xToPixel (redLocations[count][0])
         y = yToPixel (redLocations[count][1])
         DISPLAYSURF.blit (redImages[count], (x,y))         
         count = count + 1
         
      count = 0
      for piece in blackPieces:
         x = xToPixel (blackLocations[count][0])
         y = yToPixel (blackLocations[count][1])
         DISPLAYSURF.blit (blackImages[count], (x,y))
         count = count + 1

      pygame.display.update()        
            
   # Show screen
   pygame.display.set_caption('Play Checkers')        

   (redImages,redPieces) = showImages (['redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png'], \
                           [(BOARDX+OFFSET,BOARDY+OFFSET) , \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET), \
                            (BOARDX+OFFSET,                BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+SQUAREWIDTH)  \
                           ] ) 
   redLocations = [ \
                    [0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], \
                    [0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], \
                  ]

   (blackImages,blackPieces) = showImages (['blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png'], \
                           [(BOARDX+OFFSET,BOARDY+OFFSET+(SQUAREWIDTH*6)) , \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET,                BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+(SQUAREWIDTH*7))  \
                           ] ) 
   blackLocations = [ \
                      [0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6], \
                      [0,7], [1,7], [2,7], [3,7], [4,7], [5,7], [6,7], [7,7], \
                    ]

   showStatus ( "Waiting for player to join")
   
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'Checkers\']')
      joining = ''
      playerJoined = False
      move = (0,0) # Host can move first
      myTurn = True
   else:
      udpBroadcast ( 'exec:joining=\'Checkers\'')
      joining = 'Checkers' # Opponent should be waiting
      move = None
      myTurn = False

   drawBoard()
   (images,sprites) = showImages (['quit.jpg'], [(400,500)] )      
   pygame.display.update()

      
   quit = False    
   redSelectedPiece = None
   blackSelectedPiece = None
   selectedIndex = None # necessary?
   while not quit: 
      (eventType,data,addr) = getInput (100,100)
      
      if not myTurn and (move != None): #Opponent has moved 
         print ( "Got a move from opponent: " + str(move)) 
         selectedIndex = int(move[0])
         x = int(move[1])
         y = int(move[2])
         color = move[3]
         if color == 'red':
            redLocations[selectedIndex] = (x,y)
         else:
            blackLocations[selectedIndex] = (x,y)
            
         drawBoard()
         (images,sprites) = showImages (['quit.jpg'], [(400,500)] )                              
            
         showStatus ( 'Move ' + color + ' piece ' + str(selectedIndex) + ' to [' + \
                      str(x) + ',' + str(y) + ']' ) 
         myTurn = True
         move = None      
      
      if eventType == pygame.MOUSEBUTTONUP:
         if redSelectedPiece != None: 
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            if legalMove (x,y,x,y): 
               redLocations[selectedIndex] = (x,y)
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)])
               move = None
               udpBroadcast ( 'exec:move=(' + str(selectedIndex) + ',' + str(x) + ',' + str(y) + ',\'red\')')               
               myTurn = False
            else:
               showStatus ('Red illegal move' )
            
         if blackSelectedPiece != None: 
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            if legalMove (x,y,x,y): 
               blackLocations[selectedIndex] = (x,y)
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)])
               move = None
               udpBroadcast ( 'exec:move=(' + str(selectedIndex) + ',' + str(x) + ',' + str(y)+ ',\'black\')')               
               myTurn=False
            else:
               showStatus ( 'Black illegal move' )
         redSelectedPiece = None
         blackSelectedPiece = None  
         
      elif eventType == pygame.MOUSEBUTTONDOWN:
         if joining == 'Checkers': 
            if myTurn: 
               piece = getSpriteClick (eventType, data, redPieces)          
               if piece != -1:
                  selectedIndex = piece
                  redSelectedPiece = redPieces[piece]
                  
               piece = getSpriteClick (eventType, data, blackPieces)          
               if piece != -1:
                  selectedIndex = piece
                  blackSelectedPiece = blackPieces[piece]
            else:
               showStatus ( 'Waiting for other player to move' )                                  
         else:
            showStatus ( 'Waiting for other player to join')
         
      elif eventType == pygame.MOUSEMOTION:
         if redSelectedPiece != None:
            if inBoard (data[0], data[1]): 
               redSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               redSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)            
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)] )                              
         elif blackSelectedPiece != None:
            if inBoard (data[0], data[1]):
               blackSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               blackSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)] )                     
          
      sprite = getSpriteClick (eventType, data, sprites ) 
      if sprite != -1: # Quit is the only other option           
         print ("Selected command: " + str(sprite))
         mainPage (True)
         quit = True    
CHECKERS=inspect.getsource(checkersPage)