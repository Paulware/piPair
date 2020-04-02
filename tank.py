import inspect

def tankPage():
   global joining 
   global move 
   
   SQUAREWIDTH = 50
   BOARDY = 50
   BOARDX = 100 
   RADIUS = int((SQUAREWIDTH/2) - 10)
   OFFSET = 0   
   shot = None   
   Object = type('Object', (object,), {} ) # Generic object definition
   showStatus ( 'Shoot the bad guy' )    
      
   pieces = [  #   id,  image,            image,                                          x   y    angle, health \
                ['white',extractImage ('images/tanks.png', 0, 0, 164, 212, 60, 80) ,     (100,100), 45,   100],\
                ['black',extractImage ('images/tanks.png', 168, 428, 340, 605, 60, 80),  (400,400), 135,  100] \
            ]
            
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
      

   def drawBoard(shot): 
      DISPLAYSURF.fill((WHITE)) 
   
      count = 0
      for piece in pieces:
         x = piece[2][0]
         y = piece[2][1]
         img = piece[1]
         angle = piece[3]
         blitRotate (img, (x,y), angle) # Rotate image to current angle
         (w,h) = img.get_size()
         rect = pygame.Rect ( x, y, w, h) 
         if shot != None: 
            if rect.collidepoint ( (shot.x,shot.y) ):
               image = pygame.image.load ( 'images/explosion.png').convert_alpha()
               DISPLAYSURF.blit (image, (shot.x-100, shot.y-150 ))
               showStatus ( "You Win Yo" )
               shot = None
         count = count + 1
      
      if shot != None:      
         pygame.draw.circle(DISPLAYSURF, BLACK, (shot.x,shot.y), 2, 2)
      
      pygame.display.update()        
      return shot
         
   def angleXY(x,y,speed,degrees):
      degrees = degrees - 90.0# adjust for picture direction
      degrees = int(degrees) % 360
      angle_in_radians = float(degrees) / 180.0 * math.pi
      new_x = x + int(float(speed)*math.cos(angle_in_radians))
      new_y = y - int(float(speed)*math.sin(angle_in_radians))
      return new_x, new_y
         
   # Show screen
   pygame.display.set_caption('Play Tank Combat')         
   showStatus ( "Waiting for player to join")
   
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'Tank\']')
      joining = ''
      playerJoined = False
      move = (0,0) # Host can move first
      myTurn = True
   else:
      udpBroadcast ( 'exec:joining=\'Tank\'')
      joining = 'Tank' # Opponent should be waiting
      move = None
      myTurn = False

   shot = drawBoard(shot)
   (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )      
   pygame.display.update()

      
   autoKey = ''
   quit = False    
   selectedIndex = None # necessary?
   autoTime = time.time()
   moveTimeout = 0.09
   shotTimeout = time.time() + 0.01
   shotLifeTimeout = time.time()
   while not quit: 
      (eventType,data,addr) = getKeyOrUdp()
            
      if not myTurn and (move != None): #Opponent has moved 
         print ( "Got a move from opponent: " + str(move)) 
         selectedIndex = int(move[0])
         x = int(move[1])
         y = int(move[2])
         color = move[3]
            
         shot = drawBoard(shot)
         (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
            
         showStatus ( 'Move ' + color + ' piece ' + str(selectedIndex) + ' to [' + \
                      str(x) + ',' + str(y) + ']' ) 
         myTurn = True
         move = None      
         
      if (eventType == pygame.KEYUP):
         autoKey = ''
         print ( 'Turning off autoKey' )

      if time.time() > autoTime: 
         if autoKey != '':
            print ( 'Detected autokey: ' + autoKey )
            autoTime = time.time() + moveTimeout
            eventType = 'key'
            data = autoKey
            addr = 'key'

      if shot != None: 
         if time.time() > shotTimeout:          
            shotTimeout = time.time() + 0.01
            (shot.x,shot.y) = angleXY(shot.x, shot.y, 10, shot.angle)
            if (shot.x >= DISPLAYWIDTH) or (shot.y >= DISPLAYHEIGHT) or (shot.x <= 0) or (shot.y <= 0): 
               shot.angle = int(shot.angle + 90) % 360                 
            else: 
               shot = drawBoard(shot)
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              

         if time.time() > shotLifeTimeout: 
            shot = None
            shot = drawBoard(shot)
            (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] ) 
            
      if eventType == 'key':
         pieceInde = 1
         if iAmHost:
            pieceIndex = 0
         x = pieces[pieceIndex][2][0]
         y = pieces[pieceIndex][2][1]
         angle = pieces[pieceIndex][3]
         if (data == ' '): 
            print ("Fire!" )
            shot = Object()
            shot.x = x
            shot.y = y
            shot.angle = angle
            for i in range(7): 
                # make sure shot starts outside of the firing tank location
               (shot.x,shot.y) = angleXY(shot.x, shot.y, 13, shot.angle)            
            shotLifeTimeout = time.time() + 2.0
            
         elif (data == chr(273)) or (data == 'w'):
            autoKey = 'w'
            autoTime = time.time() + moveTimeout
            print ( 'Go forward' )
            x,y = angleXY(x,y,10,angle)
            pieces[pieceIndex][2]= (x,y)
            shot = drawBoard(shot)
            (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
         elif (data == chr(274)) or (data == 's'):
            autoKey = 's'
            autoTime = time.time() + moveTimeout
            print ( 'Go backward' )
            x,y = angleXY(x,y,10,angle+180)   
            pieces[pieceIndex][2]= (x,y)
            shot = drawBoard(shot)
            (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
         elif (data == chr(275)) or (data == 'd'):
            autoKey = 'd'
            autoTime = time.time() + moveTimeout
            pieces[pieceIndex][3] = int(angle - 10) % 360
            print ( 'Go Right' )
            shot = drawBoard(shot)
            (images,sprites) = showImages (['images/quit.jpg'], [(400,500)])             
         elif (data == chr(276)) or (data == 'a'):
            autoKey = 'a'
            autoTime = time.time() + 0.19
            pieces[pieceIndex][3] = int(angle + 10) % 360
            print ( 'Go Left' )
            shot = drawBoard(shot)
            (images,sprites) = showImages (['images/quit.jpg'], [(400,500)])
       
      ''' 
      elif eventType == pygame.MOUSEBUTTONUP:

         if whiteSelectedPiece != None: 
            print ( 'Move white piece[' + str(whiteSelectedPiece) + '] to: ' + str(data) )
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            if legalMove (selectedIndex,x,y,'white'):             
               piece = findBlackPiece (x,y)
               if piece != -1:
                  blackLocations[piece]=(-1,-1) # indicate unit is gone
               whiteLocations[selectedIndex] = (x,y)
               
               shot = drawBoard(shot)
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
               shot = drawBoard(shot)
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
         if joining == 'Tank': 
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
         
      elif eventType == pygame.MOUSEMOTION:
         if whiteSelectedPiece != None:
            if inBoard (data[0], data[1]): 
               whiteSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               whiteSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)            
               shot = drawBoard(shot)
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                              
         elif blackSelectedPiece != None:
            if inBoard (data[0], data[1]):
               blackSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               blackSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)
               shot = drawBoard(shot)
               (images,sprites) = showImages (['images/quit.jpg'], [(400,500)] )                     
      '''    
      sprite = getSpriteClick (eventType, data, sprites ) 
      if sprite != -1: # Quit is the only other option           
         print ("Selected command: " + str(sprite))
         mainPage (True)
         quit = True  
         
TANK=inspect.getsource(tankPage)