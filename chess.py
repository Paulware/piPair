import inspect
def chessPage():
   global joining 
   global move 
   
   SQUAREWIDTH = 50
   BOARDY = 50
   BOARDX = 100 
   RADIUS = int((SQUAREWIDTH/2) - 10)
   OFFSET = 0   
   chessSheet = pygame.image.load('images/chessSheet.png')   
   whiteSelectedPiece = None
   blackSelectedPiece = None   
   
   def inBoard (x,y):
      insideBoard = False
      if (x >= BOARDX) and (y >= BOARDY):
         if (x <= (BOARDX+(8*SQUAREWIDTH))) and (y <= (BOARDY+(8*SQUAREWIDTH))): 
            insideBoard = True
      return insideBoard
      
   def legalMove (selectedIndex, x, y, color):
      legal = True
      if color == 'white':
         (fromX,fromY) = whiteLocations[selectedIndex]
      else:
         (fromX,fromY) = blackLocations[selectedIndex]
      if (fromX == x) and (fromY == y):
         showStatus ( 'Cannot move to same position' )
         legal = False
      return legal
    
   def xToPixel (x):
      return BOARDX + (x * SQUAREWIDTH)
      
   def yToPixel (y):
      return BOARDY + (y * SQUAREWIDTH)
      
   def posToXY (x,y):
      x = int((x - BOARDX)/ 50) 
      y = int((y - BOARDY)/ 50)
      return (x,y)   

   # (x,y) is board square location not pixels       
   def findBlackPiece (x,y):  
      piece = -1
      count = 0
      for location in blackLocations: 
         if (x == location[0]) and (y == location[1]):
            piece = count
            break
         count = count + 1
      return piece 

   # (x,y) is board square location (not pixels)      
   def findWhitePiece (x,y):  
      piece = -1
      count = 0
      for location in whiteLocations: 
         if (x == location[0]) and (y == location[1]):
            piece = count
            break
         count = count + 1
      return piece 
      
   def findSelectedPiece (x,y):
      (x,y) = posToXY (x,y)
      
      selectedIndex = None
      whiteSelectedPiece = None
      blackSelectedPiece = None
      count = findWhitePiece (x,y) 
      if count > -1:
         whiteSelectedPiece = count
         selectedIndex = count
         
      if whiteSelectedPiece == None: 
         count = findBlackPiece (x,y)
         if count > -1:
            selectedIndex = count
            blackSelectedPiece = count
            
      return (whiteSelectedPiece, blackSelectedPiece, selectedIndex)
   
   def drawPiece (piece,x,y): 
      pieces = {  \
                 'blackKing':(0,0),  'blackQueen':(50,0),  'blackRook':(100,0), 'blackBishop':(150,0), 'blackKnight':(200,0), 'blackPawn':(249,0), \
                 'whiteKing':(0,40), 'whiteQueen':(50,40), 'whiteRook':(100,40),'whiteBishop':(150,40),'whiteKnight':(200,40),'whitePawn':(249,40) \
               }  
      if (x >= 0) and (y >= 0):
         location = pieces[piece]
         if (piece == 'whitePawn') or (piece == 'blackPawn'):
            x = x - 10
         elif (piece == 'blackKnight') or (piece == 'whiteKnight'):
            x = x - 8
         elif (piece == 'whiteBishop') or (piece == 'blackBishop'):
            x = x - 3
            
         DISPLAYSURF.blit(chessSheet, (x, y), (location[0], location[1], 50, 50))   
   
   def drawBoard(): 
      DISPLAYSURF.fill((WHITE)) 
      y = BOARDY
      count = 0
      for i in range (8):
         for j in range (8):
            count = count + 1
            x = BOARDX + (j * SQUAREWIDTH)
            if (count % 2) == 0:
               pygame.draw.rect(DISPLAYSURF, DARKGREY, (x,y,SQUAREWIDTH, SQUAREWIDTH))
            else:                  
               pygame.draw.rect(DISPLAYSURF, RED, (x,y,SQUAREWIDTH, SQUAREWIDTH))
         y = y + SQUAREWIDTH
         count = count + 1 # stagger the colors   
   
      count = 0
      for piece in whitePieces:
         x = xToPixel (whiteLocations[count][0])
         y = yToPixel (whiteLocations[count][1])
         drawPiece (piece, x, y)
         count = count + 1
         
      count = 0
      for piece in blackPieces:
         x = xToPixel (blackLocations[count][0])
         y = yToPixel (blackLocations[count][1])
         drawPiece (piece, x, y)
         count = count + 1

      pygame.display.update()        
            
   # Show screen
   pygame.display.set_caption('Play Chess')        

   whitePieces = ['whiteRook', 'whiteKnight', 'whiteBishop', 'whiteKing', 'whiteQueen', 'whiteBishop', 'whiteKnight', 'whiteRook', \
                  'whitePawn', 'whitePawn',   'whitePawn',   'whitePawn', 'whitePawn',  'whitePawn',   'whitePawn',   'whitePawn']

   whiteLocations = [ \
                    [0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], \
                    [0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], \
                  ]
   blackPieces = ['blackRook', 'blackKnight', 'blackBishop', 'blackKing', 'blackQueen', 'blackBishop', 'blackKnight', 'blackRook', \
                  'blackPawn', 'blackPawn',   'blackPawn',   'blackPawn', 'blackPawn',  'blackPawn',   'blackPawn',   'blackPawn']

   blackLocations = [ \
                      [0,7], [1,7], [2,7], [3,7], [4,7], [5,7], [6,7], [7,7], \
                      [0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6] \
                    ]

   showStatus ( "Waiting for player to join")
   
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'Chess\']')
      joining = ''
      playerJoined = False
      move = (0,0) # Host can move first
      myTurn = True
   else:
      udpBroadcast ( 'exec:joining=\'Chess\'')
      joining = 'Chess' # Opponent should be waiting
      move = None
      myTurn = False

   drawBoard()
   (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )      
   pygame.display.update()

      
   quit = False    
   selectedIndex = None # necessary?
   joinTimeout = 0
   while not quit: 
      (eventType,data,addr) = getInput (100,100)
      
      if joining != 'Chess': 
         if time.time() > joinTimeout: 
            joinTimeout = time.time() + 1
            udpBroadcast ( 'exec:games=[\'Chess\']')
      
      if not myTurn and (move != None): #Opponent has moved 
         print ( "Got a move from opponent: " + str(move)) 
         selectedIndex = int(move[0])
         x = int(move[1])
         y = int(move[2])
         color = move[3]
         if color == 'white':
            piece = findBlackPiece (x,y)
            if piece != -1:
               blackLocations[piece] = (-1,-1) # indicate capture            
            
            whiteLocations[selectedIndex] = (x,y)
         else:
            blackLocations[selectedIndex] = (x,y)
            piece = findWhitePiece (x,y)
            if piece != -1:
               whiteLocations[piece] = (-1,-1) # indicate capture
            print ('blackLocations: ' + str(blackLocations) )
            
         drawBoard()
         (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
            
         showStatus ( 'Move ' + color + ' piece ' + str(selectedIndex) + ' to [' + \
                      str(x) + ',' + str(y) + ']' ) 
         myTurn = True
         move = None      
      
      if eventType == pygame.MOUSEBUTTONUP:
         if whiteSelectedPiece != None: 
            print ( 'Move white piece[' + str(whiteSelectedPiece) + '] to: ' + str(data) )
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            if legalMove (selectedIndex,x,y,'white'):             
               piece = findBlackPiece (x,y)
               if piece != -1:
                  blackLocations[piece]=(-1,-1) # indicate unit is gone
               whiteLocations[selectedIndex] = (x,y)
               
               drawBoard()
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)])
               move = None
               udpBroadcast ( 'exec:move=(' + str(selectedIndex) + ',' + str(x) + ',' + str(y) + ',\'white\')')               
               myTurn = False
            else:
               showStatus ('Red illegal move' )
         else: 
            print ( 'whiteSelectedPiece == None' )
            
         if blackSelectedPiece != None: 
            print ( 'Move black piece[' + str(blackSelectedPiece) + '] to: ' + str(data) )
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            if legalMove (selectedIndex,x,y,'black'): 
               piece = findWhitePiece (x,y)
               if piece != -1:
                  whiteLocations[piece]=(-1,-1) # indicate unit is gone
            
               blackLocations[selectedIndex] = (x,y)
               drawBoard()
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)])
               move = None
               udpBroadcast ( 'exec:move=(' + str(selectedIndex) + ',' + str(x) + ',' + str(y)+ ',\'black\')')               
               myTurn=False
            else:
               showStatus ( 'Black illegal move' )
         print ("None B")
         whiteSelectedPiece = None
         blackSelectedPiece = None  
         
      elif eventType == pygame.MOUSEBUTTONDOWN:
         if joining == 'Chess': 
            if myTurn: 
               (x,y) = posToXY (data[0],data[1]) 
               if iAmHost: 
                  piece = findBlackPiece (x,y)
                  if piece != -1: 
                     showStatus ( 'That is not your piece, you are white' )
                  else: 
                     (whiteSelectedPiece, blackSelectedPiece, selectedIndex) = findSelectedPiece (data[0], data[1]) 
               else:
                  piece = findWhitePiece (x,y)
                  if piece != -1:
                     showStatus ( 'That is not your piece, you are black' )
                  else:
                     (whiteSelectedPiece, blackSelectedPiece, selectedIndex) = findSelectedPiece (data[0], data[1]) 
            else:
               showStatus ( 'Waiting for other player to move' )                                  
         else:
            showStatus ( 'Waiting for other player to join')
      '''   
      elif eventType == pygame.MOUSEMOTION:
         if whiteSelectedPiece != None:
            if inBoard (data[0], data[1]): 
               whiteSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               whiteSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)            
               drawBoard()
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
         elif blackSelectedPiece != None:
            if inBoard (data[0], data[1]):
               blackSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               blackSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)
               drawBoard()
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                     
      '''    
      sprite = getSpriteClick (eventType, data, sprites ) 
      if sprite != -1: # Quit is the only other option           
         print ("Selected command: " + str(sprite))
         mainPage (True)
         quit = True  
         
CHESS=inspect.getsource(chessPage)