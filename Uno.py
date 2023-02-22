import inspect
import pygame
import time
from Communications import Communications

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
       def handleSubdeck (name,cardsStr):
          print ( 'handleSubdeck [name,cardsStr]: [' + name + ',' + str(cardsStr) + ']' )
          if self.comm.gotPeek ('subdeck uno'):   
             message = self.comm.pop()
             print ( 'handleSubdeck, got message: [' + message + ']')
             cards = [] 
             for c in cardsStr: 
                cards.append (int(c))             
             if name == 'hand': 
                d = SubDeck (deck, startXY=(100,400), displaySurface=displaySurface, cards=cards)             
             elif name == 'opponent': 
                d = SubDeck (deck, startXY=(100,50),  displaySurface=displaySurface, cards=cards) 
             elif name == 'discardPile': 
                d = SubDeck (deck,  startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0, cards=cards)
             elif name == 'drawPile': 
                d = SubDeck (deck,  startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0, cards=cards)
             return d
             
       print ( 'Uno.main' )
       self.DISPLAYSURF.fill((BLACK))
       displaySurface = self.DISPLAYSURF # refactor out?
       if self.iAmHost: 
          pygame.display.set_caption('Play Uno I am host:' + self.comm.target)        
       else:
          pygame.display.set_caption('Play Uno I am player:' + self.comm.target)        
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,600)] )
       pygame.display.update()

       deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)
                 
       if self.iAmHost: 
          state = 1   
          self.utilities.showStatus ( "Host, Waiting for player to join")
          hand        = SubDeck (deck,  7, startXY=(100,400), displaySurface=displaySurface)
          opponent    = SubDeck (deck,  7, startXY=(100,50),  displaySurface=displaySurface)
          discardPile = SubDeck (deck,  1, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
          # All remaining cards go into the draw pile 
          drawPile    = SubDeck (deck,  0, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
          drawPile.hideAll () 
          
          # creates decks array 
          cards=[]
          cards.append (hand)
          cards.append (opponent)
          cards.append (drawPile)   
          cards.append (discardPile)
          decks = SubDecks (cards)    
          
        
          pygame.display.update()
       else: # Host goes first...
          hand = type('SubDeck', (object,), {})()       
          opponent = type('SubDeck', (object,), {})()       
          state = 2
          self.comm.send ( 'join uno' )
          self.utilities.showStatus ( "Waiting for host to deal")
          cards=[]
       
       joinTimeout = 0    
       quit = False 
       # Get/Send Decks        
       self.utilities.showStatus ( "Get/Give Cards")
       while True:
          if state == 1: # host 
             if self.comm.gotPeek ( 'join uno' ):
                self.utilities.showStatus ( 'TBD: send cards to opponent' )
                self.comm.send ( 'subdeck uno opponent '    + hand.cardsToStr () )
                self.comm.send ( 'subdeck uno hand '        + opponent.cardsToStr () )
                self.comm.send ( 'subdeck uno drawPile '    + drawPile.cardsToStr () )                 
                self.comm.send ( 'subdeck uno discardPile ' + discardPile.cardsToStr() )
                break
          elif state == 2: # player 
             if self.comm.gotPeek ('subdeck uno'): 
                message = self.comm.peek ()
                data = message.split (' ')
                print ( 'data: ' + str(data) ) 
                name     = data[2]                 
                cardsStr = data[3:]
                
                if name == 'opponent': 
                   opponent    = handleSubdeck (name, cardsStr)                 
                elif name == 'hand': 
                   hand        = handleSubdeck (name, cardsStr )
                elif name == 'discardPile': 
                   discardPile = handleSubdeck (name, cardsStr )
                elif name == 'drawPile': 
                   drawPile    = handleSubdeck (name, cardsStr )
                   drawPile.hideAll () 
                   
                # creates decks array 
                if name == 'discardPile': 
                   cards=[]
                   cards.append (hand)
                   cards.append (opponent)
                   cards.append (drawPile)   
                   cards.append (discardPile)
                   decks = SubDecks (cards)    
                   decks.draw()
                   break

 
       print ( 'Start while loop state: ')
       myMove = self.iAmHost 
       if myMove: 
          self.utilities.showStatus ( "Play")
       else:
          self.utilities.showStatus ( 'Waiting for opponents move' )
       dragging   = None
       dragDeck   = None
       sourceDeck = None
       while not self.utilities.quit and not self.gameOver() and not quit:
          window = pygame.display.get_surface()    
          window.fill ((0,0,0))  
          TextBox('Opponent', x=100, y=  5).draw()
          TextBox('Discard',  x=100, y=175).draw()
          TextBox('Draw',     x=310, y=175).draw()
          TextBox('Hand',     x=100, y=375).draw()                    
          decks.draw() # Show and set their x/y locations 
          sprites = self.utilities.showImages (['quit.jpg'], [(400,600)] )       
          self.utilities.flip() 
                 
          # pygame.display.update()
          events = self.utilities.readOne()
          for event in events:
             (typeInput,data,addr) = event                                
             # Use data above to determine sprite click?                
             if typeInput == 'drag':  
                sprite = self.utilities.findSpriteClick (event[1], sprites ) 
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
                elif typeInput == 'drag':
                   if myMove:
                      self.utilities.showStatus ( 'Nice move: ' + typeInput )                   
                   else: 
                      self.utilities.showStatus ('Err, not your move' )
                   if dragDeck is None: 
                      print ( '\n\n***DRAG***\n\n' )
                      (deck,index) = decks.findSprite (data) # Returns index in list 
                   
                      sourceDeck = deck
                      mousePos = data
                      self.utilities.showStatus ( 'Got an index of: ' + str(index)) 
                      dragging = index                    
                      
             elif typeInput == 'move':
                self.utilities.showStatus ( 'Moving...')
                if not dragging is None: 
                  deck.move (dragging,data)               
                mousePos = data  
             elif typeInput == 'drop':
                dragging = None             
             else:
                self.utilities.showStatus ( 'Unknown event: [' + str(event) + ']' )
                                         
          if self.utilities.quit:
             print ( 'self.utilities.quit' )
          elif self.gameOver(): 
             print ( 'self.gameOver' )
          elif quit: 
             print ( 'quit == True' )          
       print ( 'Go back to the main page...' ) 
    
if __name__ == '__main__':
   try: 
      import sys
      numParameters = len(sys.argv)
      print ( 'number of parameters: ' + str(numParameters) ) 
      
      pygame.init()
      displaySurface = pygame.display.set_mode((1200, 800))
      BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
      
      name = 'pi7'   
      comm = Communications ('messages', 'localhost', name )
      comm.connectBroker()
      comm.setTarget ( 'laptop' )
      print ( 'Back from connectBroker' )
      
      utilities = Utilities (displaySurface, BIGFONT)   
      utilities.comm = comm
      
      uno = Uno(displaySurface,utilities,comm)
      uno.iAmHost = True
      uno.main()       
      
      '''
      deck        = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)      
      hand        = SubDeck (deck,  7, startXY=(100,400), displaySurface=displaySurface)   
      discardPile = SubDeck (deck,  1, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
      drawPile    = SubDeck (deck, 44, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
      drawPile.hideAll () 
      
      # creates decks array 
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
      
      comm.send ( 'join uno')   
      comm.waitFor ( 'deal uno')      
      
      print ( 'Got deal uno')
      print ( 'Waiting for cards' )
      
      while not quit: # len(deck.sprites) > 0:
         decks.draw() # Show and set their x/y locations
         pygame.display.update() 
         
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
      '''
   finally: 
      comm.disconnect()