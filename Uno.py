import inspect
import pygame
import time
import Communications

from Deck      import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from SubDeck   import SubDeck
from SubDecks  import SubDecks
from TextBox   import TextBox
 
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
       print ( 'Uno.main' )
       self.DISPLAYSURF.fill((BLACK))
       pygame.display.set_caption('Play Uno')        
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] ) 
       pygame.display.update()       

       deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)   
          
          
       if self.iAmHost: 
          state = 1   
          self.utilities.showStatus ( "Waiting for player to join")
          '''
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
          '''
       else: # Host goes first...
          state = 2
          '''
          self.utilities.showStatus ( "Waiting for host to deal")
          pygame.display.update()
          self.comm.waitForPeek ( 'deal uno')
          '''
       
       joinTimeout = 0    
       print ( 'Start while loop' )
       myMove = True 
       quit = False 
       while not self.utilities.quit and not self.gameOver() and not quit: 
          if state == 1: 
             if not self.comm.empty(): 
                msg = self.comm.pop()
                if msg.find ('join uno') > -1: 
                   state = 3 
                   print ( 'found: ' + message + ' in ' + msg)
          elif state == 2: 
             if not self.comm.empty(): 
                msg = self.comm.peek()
                if msg.find ('deal uno') > -1: 
                   state = 3 
                   print ( 'found: ' + message + ' in ' + msg)
       
          events = self.utilities.readOne()
          for event in events:
             (typeInput,data,addr) = event

             '''
             (event,data,addr) = self.utilities.getKeyOrUdp()
             if self.utilities.isMouseClick (event) and (state == 3):           
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
             '''
                                
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
   
   deck        = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)      
   hand        = SubDeck (deck,  7, startXY=(100,400), displaySurface=displaySurface)   
   discardPile = SubDeck (deck,  1, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
   drawPile    = SubDeck (deck, 44, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
   drawPile.hideAll () 
   
   cards=[]
   cards.append (hand)
   cards.append (drawPile)   
   cards.append (discardPile)
   decks = SubDecks (cards)    
   
   TextBox('Opponent', x=100, y=  5).draw()
   TextBox('Discard',  x=100, y=175).draw()
   TextBox('Draw',     x=310, y=175).draw()
   TextBox('Hand',     x=100, y=375).draw()   
   window = displaySurface # pygame.display.get_surface()   
   quit = False
   while not quit: # len(deck.sprites) > 0:
      decks.draw() # Show and set their x/y locations
      pygame.display.update() 
      
      #pygame.display.flip()
      #pygame.event.pump() 
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         # print ( 'typeInput: ' + str(typeInput))
         if typeInput == 'select':
            print ( '\n\n***Select***\n\ndata: ' + str(data)   )
            index = hand.findSprite (data)  
            if index != -1: 
                x = hand.data[index].x
                y = hand.data[index].y
                optionBox = OptionBox (['Play', 'Cancel'], x, y)
                selection = optionBox.getSelection()
                print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
                if selection == 'Cancel': 
                   quit = True
                   print ( 'quit is now: ' + str(quit) )
                   break
                elif selection == 'Play':
                   discardPile.addCard (hand,index)
                   hand.data[index].deleted = True 
                   # hand.discard (index) 
                   hand.addCard (drawPile, drawPile.topCard())

                window.fill ((0,0,0))
            
   print ( 'Done yo' )