import inspect
import pygame
import time
import Communications
from Deck import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from PlayingCards import PlayingCards
from SubDecks import SubDecks
 
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
class Solitaire (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization Solitaire' )
       self.iAmHost     = True        
       self.deck = Deck ('images/standardCardSprites.jpg', 13, 5, 52, 54) 
       if self.deck.coverImage is None: 
          print ( 'Could not find coverImage for deck...' )
          exit(1)          

       # Deal out the 7 columns of cards 
       x = 100        
       decks=[]
       columns = 7
       for i in range(columns):
          hand = PlayingCards (self.deck,columns-i,80,120,(x,100), DISPLAYSURF,xMultiplier=0.0, yMultiplier=0.25)
          hand.hideAll () 
          hand.data [hand.length()-1].hide = False 
          hand.x = x
          x = x + 100 
          hand.info (hand.topSheetIndex())
          decks.append (hand)

       # Get remaining cards and place them in the draw pile           
       hand = PlayingCards (self.deck, len(self.deck.data), 80, 120, (900,400), DISPLAYSURF, xMultiplier=0.0, yMultiplier=0.0)
       hand.showAll()
       decks.append (hand)                
       self.drawPile = hand      
       self.decks = SubDecks (decks)       
    
    def draw(self,dragDeck):
       window = pygame.display.get_surface()    
       window.fill ((0,0,0))     
       self.decks.draw() # updateDisplay (dragDeck, mousePos) 
       if not dragDeck is None: 
          dragDeck.draw()
          
       utilities.flip() 
       
    def gameOver (self): 
       over = False
       return over       
       
       
    def runMain (self): 
       # window = pygame.display.get_surface()
       quit = False 
       
       mousePos = (0,0)
       dragDeck = None
       dragging = None
       sourceDeck = None
       while not quit:  
          self.draw(dragDeck) # updateDisplay (dragDeck, mousePos) 

          events = utilities.readOne()
          for event in events:
             (typeInput,data,addr) = event
             # print ( 'typeInput: ' + str(typeInput) ) 
             
             if typeInput == 'move':
                if not dragging is None: 
                  deck.move (dragging,data)               
                mousePos = data
             elif typeInput == 'drag': 
                if dragDeck is None: 
                   print ( '\n\n***DRAG***\n\n' )
                   (deck,index) = self.decks.findSprite (data) # Returns index in list 
                   
                   sourceDeck = deck
                   mousePos = data
                   print ( 'Got an index of: ' + str(index)) 
                   dragging = index                    
                   if not index is None:                     
                      print ( 'Create a sub deck' )
                      dragDeck = PlayingCards (width=80,height=120,displaySurface=self.DISPLAYSURF,\
                                               xMultiplier=0.0, yMultiplier=0.25)
                      if index == deck.length() -1: # This is the top card, it can be dragged individually
                         dragDeck.addCard (deck,index)
                         deck.remove (index)
                         dragging = 0
                      else:
                         print ( 'Got drag index: ' + str(index))
                         group = deck.getGroup (index)
                         for card in group: 
                            dragDeck.addCard (deck,card)  
                         deck.removeHidden (False)
                      dragDeck.listCards()                           
                      deck = dragDeck
                      
             elif typeInput == 'drop': 
                face = dragDeck.face(dragDeck.bottomSheetIndex())
                print ( 'Bottom sheet face: ' + str(face))                    
                
                if face == 1:  
                   print ( 'You can drop Ace anywhere' )
                   self.decks.addDeck (dragDeck)
                   sourceDeck.revealTopCard() 
                else:   
                   emptyColumn = self.decks.emptyColumn() 
                   if (face==13) and (emptyColumn != -1): 
                      print ( 'You can place the king in an empty column yo' )
                      self.decks.addElements ( emptyColumn, dragDeck ) 
                      sourceDeck.revealTopCard()                         
                   else:
                      print ( '\n\n***DROP EVENT***\n\n' )
                      (deck,index) = self.decks.findSprite (data) # Where are we dropping
                      
                      dragSheetIndex = dragDeck.topSheetIndex()
                      dragSuit       = dragDeck.suit (dragSheetIndex)
                      dragFace       = dragDeck.face (dragSheetIndex)
                      
                      print ( 'Drag card' )
                      dragDeck.info (dragSheetIndex)
                   
                      if deck is None:
                         print ( 'Could not find a deck being dropped on' )
                         sourceDeck.appendDeck (dragDeck)
                      else:
                         dropSheetIndex = deck.data[index].sheetIndex
                         dropSuit       = deck.suit (dropSheetIndex)
                         dropFace       = deck.face (dropSheetIndex)
                         print ( 'Drop card' )
                         deck.info (dropSheetIndex)                         
                      
                         print ( 'Got drop index: ' + str(index))
                         print ( 'Destination deck has a top card of: ' + deck.cardName ( deck.topSheetIndex()) )
                         if deck.canDrop (dragDeck.bottomSheetIndex(), deck.topSheetIndex()): 
                            print ( 'Can drop ' + deck.cardName (dragDeck.bottomSheetIndex()) + ' on ' + \
                                    deck.cardName (deck.topSheetIndex()) )
                            deck.appendDeck(dragDeck) 
                            sourceDeck.revealTopCard() 
                         elif (dragSuit == dropSuit) and ((dragFace - dropFace ) == 1):
                            print ( 'Drop card on final pile' ) 
                            deck.appendDeck(dragDeck) 
                            sourceDeck.revealTopCard()
                         else:
                            print ( 'Cannot drop ' + deck.cardName (dragDeck.bottomSheetIndex()) + \
                            ' on ' + deck.cardName ( deck.topSheetIndex()) ) 
                            print ( 'Return dragDeck to originating deck' ) 
                            sourceDeck.appendDeck (dragDeck)
                                            
                dragDeck = None
                sourceDeck = None
                
             elif typeInput == 'select':
                print ( '\n\n***Select***\n\n' )
                (deck,index) = self.decks.findSprite (data)
                if deck == self.drawPile: 
                   deck.cycleTopCard()
                elif deck != None: 
                   optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel', 'Hide', 'Show'], data[0], data[1])
                   selection = optionBox.getSelection()
                   print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
                   if selection == 'Cancel': 
                      quit = True 
                      break
                   elif selection == 'Discard':
                      deck.discard (index) 
                   elif selection == 'Tap':                
                      deck.tap (index, True )
                   elif selection == 'Use':
                      deck.discard (index)
                      deck.drawCard()
                   elif selection == 'Hide':
                      deck.hide(index)
                   elif selection == 'Show':
                      deck.unhide(index)
          
    def main (self): # This main is for pages.py to call, it can probably be deleted
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
   solitaire = Solitaire (displaySurface,utilities,None)

   solitaire.runMain() 
