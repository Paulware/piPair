import inspect
# Show the Tic-Tac-Toe Pages
def tictactoePage ():
    global joining 
    global move
    taken = [[False, False, False],[False, False, False], [False, False, False]]
    
    drawingX = True
    def drawX (x,y):
       taken [x][y]=True       
       x = (x * 100) + 200
       y = (y * 100) + 100 
       print ( 'Draw X at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.line(DISPLAYSURF, RED, (x, y), (x+100, y+100))
       pygame.draw.line(DISPLAYSURF, RED, (x+100, y), (x, y+100))
       pygame.display.update()
    def drawO (x,y):
       taken [x][y]=True
       x = (x * 100) + 250
       y = (y * 100) + 150 
       print ( 'Draw O at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.circle(DISPLAYSURF, RED, (x, y), 50, 1)       
       pygame.display.update()
           
    # Show screen 
    DISPLAYSURF.fill((BLACK))
    pygame.display.set_caption('Play Tic Tac Toe')        
    pygame.draw.line(DISPLAYSURF, RED, (300, 100), (300, 400))
    pygame.draw.line(DISPLAYSURF, RED, (400, 100), (400, 400))
    pygame.draw.line(DISPLAYSURF, RED, (200, 200), (500, 200))
    pygame.draw.line(DISPLAYSURF, RED, (200, 300), (500, 300))
    pygame.display.flip()
    (images,sprites) = showImages (['quit.jpg'], [(400,500)] )      
    showStatus ( "Waiting for player to join")
    pygame.display.update()
    
    if iAmHost: 
       # Set opponents list of games
       udpBroadcast ( 'exec:games=[\'Tic Tac Toe\']')
       joining = ''
       playerJoined = False
       move = (0,0)
       myTurn = True
    else:
       udpBroadcast ( 'exec:joining=\'Tic Tac Toe\'')    
       joining = 'Tic Tac Toe' # Opponent should be waiting
       move = None
    
    quit = False  
    joinTimeout = 0    
    while not quit: 
       (eventType,data,addr) = getKeyOrUdp()
       if joining != 'Tic Tac Toe':
          if time.time() > joinTimeout: 
             joinTimeout = time.time() + 1
             udpBroadcast ( 'exec:games=[\'Tic Tac Toe\']')
       
       if eventType == pygame.MOUSEBUTTONUP:
          pos = data
          x = int(pos[0] / 100) - 2
          y = int(pos[1] / 100) - 1
          if (x >=0) and (y >=0) and (x <=2) and (y <= 2):
             if taken[x][y]: 
                showStatus ( "Square already taken")
             else:
                print ('pos: [' + str(x) + ',' + str(y) + ']' ) 
                if joining == 'Tic Tac Toe':
                   if move == None:
                      showStatus ( 'Waiting on opponent\'s move' )             
                   else:
                      print ( 'process: [' + str(x) + ',' + str(y) + ']' )
                      if drawingX: 
                         drawX (x,y)
                      else:
                         drawO (x,y)
                      drawingX = not drawingX
                      move = None
                      udpBroadcast ( 'exec:move=(' + str(x) + ',' + str(y) + ')')
                else:
                   print ( 'Waiting for player, joining: [' + joining + ']' )
                   showStatus ( 'Ignoring click, waiting for player to join')
                   # udpBroadcast ( 'exec:joining=\'Tic Tac Toe\'')             
       elif eventType == 'udp':
          if data.find ( 'move=') > -1: # Opponent has moved 
             if drawingX: 
                drawX (move[0], move[1])
             else:
                drawO (move[0], move[1])
             drawingX = not drawingX
             
          print ( 'Got a udp: [' + data + '] from: ' + addr )
           
       sprite = getSpriteClick (eventType, data, sprites ) 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
          
TICTACTOE=inspect.getsource(tictactoePage)