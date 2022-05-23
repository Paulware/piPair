import inspect
import pygame
import time
import Communications
from Deck import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from SubDeck import SubDeck
 
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
# Show the Uno Pages
class Uno (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization Uno' )
       self.iAmHost     = True        
    
    def gameOver (self): 
       over = False
       return over
    
    def main (self):
       self.DISPLAYSURF.fill((BLACK))
       pygame.display.set_caption('Play Uno')        
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] ) 
       pygame.display.update()       
       
       deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52)   
   
       if self.iAmHost: 
          self.utilities.showStatus ( "Waiting for player to join")
          pygame.display.update()
          self.comm.waitFor ( 'join uno')
          hand = SubDeck (deck,7)
          hand.showSprites(100,600,80,120,self.DISPLAYSURF) 
          opponent = SubDeck (deck,7)
          opponent.changeImage ( 'images/unoFlip.jpg')          
          opponent.showSprites(100,100,80,120,self.DISPLAYSURF)
          inputStack = SubDeck (deck, 52 - 14)
          inputStack.changeImage ( 'images/unoFlip.jpg')
          inputStack.showStack (100,300,80,120,self.DISPLAYSURF)
       else: # Host goes first...
          self.utilities.showStatus ( "Waiting for host to deal")
          pygame.display.update()
          self.comm.waitForPeek ( 'deal uno')
       
       quit = False  
       joinTimeout = 0    
       print ( 'Start while loop' )
       myMove = True 
       while not quit and not self.gameOver(): 
          (event,data,addr) = self.utilities.getKeyOrUdp()
          if self.utilities.isMouseClick (event):           
             pos = data
             x = int(pos[0] / 100) - 2
             y = int(pos[1] / 100) - 1
             if (x >=0) and (y >=0) and (x <=2) and (y <= 2):
                if not myMove: 
                   self.utilities.showStatus ( 'Not your move' )
                else:   
                   if (self.taken[x][y] =='x') or (self.taken[x][y]=='o'): 
                      self.utilities.showStatus ( "Square already taken")
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
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52)   
   
   hand = SubDeck (deck,7)
   # hand.showSprites(100,100,50,100)   
   window = pygame.display.get_surface()
   
   while True: # len(deck.sprites) > 0:
      hand.showSprites(100,100,80,120,displaySurface) # Show and set their x/y locations
      (typeInput,data,addr) = utilities.read()
      if utilities.isMouseClick (typeInput): 
         pos = pygame.mouse.get_pos()
         x = pos[0]
         y = pos[1]
         index = hand.findSprite (x,y)
         if index != -1: 
             optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel'], x, y)
             selection = optionBox.getSelection()
             print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
             if selection == 'Cancel': 
                break
             elif selection == 'Discard':
                hand.data[index].deleted = True 
                # hand.discard (index) 
             elif selection == 'Use':
                # hand.discard (index)
                hand.data[index].deleted = True 
                hand.drawCard()

             window.fill ((0,0,0))