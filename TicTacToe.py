import inspect
import pygame
import Utilities
import time
import Communications
from TextBox import TextBox

# Show the Tic-Tac-Toe Pages
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
class TicTacToe (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization of TicTacToe' )
       self.taken       = [['','',''],['','',''], ['','','']]    
       self.drawingX    = True
       self.iAmHost     = True        
       
    def drawX (self,x,y):
       print ( 'drawX (' + str(x) + ',' + str(y) + ')' )
       self.taken [x][y] = 'x'
       x = (x * 100) + 200
       y = (y * 100) + 100 
       print ( 'Draw X at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.line(self.DISPLAYSURF, RED, (x, y), (x+100, y+100))
       pygame.draw.line(self.DISPLAYSURF, RED, (x+100, y), (x, y+100))
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] )             
       pygame.display.update()
       print ( 'Done in drawX' )
       
    def drawO (self,x,y):
       print ( 'drawO (' + str(x) + ',' + str(y) + ')' )
       self.taken [x][y] = 'o'
       x = (x * 100) + 250
       y = (y * 100) + 150 
       print ( 'Draw O at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.circle(self.DISPLAYSURF, RED, (x, y), 50, 1)       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] )      
       pygame.display.update()
        
    def gameOver (self,ch): 
       over = False
       # 0down, 1down, 2down, 0across, 1across, 2across, 1diagonal, 2diagonal
       combos = [ \
                   [[0,0], [0,1], [0,2]], \
                   [[1,0], [1,1], [1,2]], \
                   [[2,0], [2,1], [2,2]], \
                   [[0,0], [1,0], [2,0]], \
                   [[0,1], [1,1], [2,1]], \
                   [[0,2], [1,2], [2,2]], \
                   [[0,0], [1,1], [2,2]], \
                   [[2,0], [1,1], [0,2]]  \
                ]
       for combo in combos: 
          for i in range (3):
             # print ( 'combo[' + str(i) + ']:' + str(combo[i])) 
             x = combo[i][0]
             y = combo[i][1]
             print ( 'x: ' + str(x) + ',y: ' + str(y) ) 
             if (self.taken[x][y] == ch): 
                over = True 
             else:
                over = False 
                break
          if over:
             break
       return over
    
    def showStatus (self, message): 
       line = TextBox(message)
       line.clearLine()
       pos = line.draw()
       pygame.display.update()
       pygame.event.pump()        
    
    def gameOverXY(self): 
       gOver = False 
       if self.gameOver ('x'): 
          self.showStatus ( "X has won")
          self.utilities.waitForClick()
          gOver = True
       elif self.gameOver ('o'): 
          self.showStatus ( "O has won")
          self.utilities.waitForClick()
          gOver = True 
       return gOver 
       
    def main (self):
       # Show screen 
       print ( 'Show screen' )
       self.DISPLAYSURF.fill((BLACK))
       pygame.display.set_caption('Play Tic Tac Toe')        
       pygame.draw.line(self.DISPLAYSURF, RED, (300, 100), (300, 400))
       pygame.draw.line(self.DISPLAYSURF, RED, (400, 100), (400, 400))
       pygame.draw.line(self.DISPLAYSURF, RED, (200, 200), (500, 200))
       pygame.draw.line(self.DISPLAYSURF, RED, (200, 300), (500, 300))
       print ( 'flip' )
       pygame.display.flip()
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] )      
       print ( 'showStatus' )
       
       if self.iAmHost: 
          line = TextBox('Waiting for player to join')
          pos = line.draw()       
          # self.showStatus ( "Waiting for player to join")
          pygame.display.update()
          self.comm.waitFor ( 'join tictactoe')
          line.clearLast()

          line = TextBox ( 'Ready' )
          pos = line.draw()
          pygame.display.update()
          pygame.event.pump()          
       else: # Host goes first...
          self.showStatus ( "Waiting for host to move")
          pygame.display.update()
          self.comm.waitForPeek ( 'move tictactoe')
       
       quit = False  
       joinTimeout = 0    
       print ( 'Start while loop' )
       myMove = True 
       while not quit and not self.gameOverXY(): 
          (event,data,addr) = self.utilities.getKeyOrMqtt()       
          if event == pygame.MOUSEBUTTONUP:           
             pos = data
             x = int(pos[0] / 100) - 2
             y = int(pos[1] / 100) - 1
             if (x >=0) and (y >=0) and (x <=2) and (y <= 2):
                if not myMove: 
                   self.showStatus ( 'Not your move' )
                else:   
                   if (self.taken[x][y] =='x') or (self.taken[x][y]=='o'): 
                      self.showStatus ( "Square already taken")
                   else:
                      print ('pos: [' + str(x) + ',' + str(y) + ']' ) 
                      if self.drawingX: 
                         self.drawX (x,y)
                      else:
                         self.drawO (x,y)
                         
                      self.drawingX = not self.drawingX
                      myMove = False
                      self.comm.send ( 'move tictactoe ' + str(x) + ' ' + str(y))
                                
          # Use data above to determine sprite click?          
          sprite = self.utilities.getSpriteClick (event, sprites ) 
          if sprite != -1: # Quit is the only other option           
             print ("Selected command: " + str(sprite))
             quit = True    
                  
          # Waiting for opponent move in the format:
          # move tictactoe X Y 
          # X is in range 0..2, Y is in range 0..2          
          elif event == 'mqtt':
             if data.find ( 'move tictactoe') > -1: # Opponent has moved 
                move = data.split ( ' ' )
                print ( 'move : ' + str(move) ) 
                x = int (move[2])
                y = int (move[3])
                print ( 'x,y: ' + str(x) + ',' + str(y) ) 
                if self.drawingX: 
                   self.drawX (x,y)
                else:
                   self.drawO (x,y)
                self.drawingX = not self.drawingX
                
             myMove = True 
              
       print ( 'Go back to the main page...' )
    
if __name__ == '__main__':
   pygame.init()
   DISPLAYSURF = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities.Utilities (DISPLAYSURF, BIGFONT)
   comm = Communications.Communications ('messages', '192.168.4.1', 'laptop' )
   comm.debug = True # Do not wait for an acknowledge
   comm.connectBroker()  
   print ( 'Start tic tac toe' )
   ticTacToe = TicTacToe(DISPLAYSURF,utilities,comm)
   ticTacToe.main()