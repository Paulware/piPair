import inspect
import pygame
import time
import Communications
from Deck import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from SubDeck import SubDeck
from SubDecks import SubDecks
 
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
# TODO: Make a subdeck out of the drag group
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

       x = 100        
       decks=[]
       columns = 9
       for i in range(columns):
          hand = SubDeck (self.deck,columns-i,80,120,(x,100), DISPLAYSURF,xMultiplier=0.0, yMultiplier=0.25)
          hand.hideAll () 
          hand.data [hand.length()-1].hide = False 
          hand.x = x
          x = x + 100 
          self.info (hand.topSheetIndex())
          decks.append (hand)
          
       hand = SubDeck (self.deck, len(self.deck.data), 80, 120, (900,400), DISPLAYSURF, xMultiplier=0.0, yMultiplier=0.0)
       hand.hideAll()
       decks.append (hand)       
          
       self.decks = SubDecks (decks) 
       self.drawPile = hand 
       hand.data [hand.length()-1].hide = False 
       
    def emptyColumn(self):
       found = -1 
       count = 0 
       for deck in self.decks.decks:
          length = deck.length()
          if length == 0:
             found = count
             break
          else:
             print ( 'Length of column: ' + str(count) + ' = ' + str(length ))  
          count = count + 1
             
       if found == -1: 
          print ( 'No empty column found' )
       else:
          print ( 'Found an empty column' )
       return found 
       
    def cardName (self,index): 
       faces = ['ZERO', 'Ace', 'Deuce', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King'] 
       return faces[self.face(index)] + ' of ' + self.suit(index) 
    
    def canDrop (self,topIndex, bottomIndex): 
       ok = False 

       topFace = self.face(topIndex)
       bottomFace = self.face(bottomIndex)
       if bottomFace == (topFace + 1):
          if self.redBlack(topIndex) != self.redBlack(bottomIndex):
             ok = True 
             print ( 'canDrop is ok...' )
          else:
             print ( 'Cannot execute a normal drop because colors are the same' )
       else:
          print ( 'Cannot execute a normal drop because top face (' + str(bottomFace) + ') != (' + str(topFace) + ') + 1)' ) 
       return ok
    
    def draw(self,dragDeck,mousePos):
       self.decks.updateDisplay (dragDeck, mousePos)
       pygame.display.update()
       
    def face (self,index):
       value = (index % 13) + 1 
       print ( 'face of index: ' + str(index) + ' : ' + str(value)) 
       return value

    def gameOver (self): 
       over = False
       return over       
       
    def getGroup (self, deck, index ):
       print ( 'Get group associated with deck and card index: ' + str(index)) 
       print ( 'Make a deck associated with this index' )       
       group = []        
       startIndex = index
       # Find where the group starts 
       while True: 
         if startIndex == 0: 
            break
         print ( 'startIndex: ' + str(startIndex)) 
         if deck.data[startIndex].hide == False: 
            startIndex = startIndex - 1 
         else:
            break            
       # Copy the entire group             
       while True: 
         if not deck.data[startIndex].hide: 
            group.append (startIndex)
         startIndex = startIndex + 1
         if startIndex == deck.length(): 
            break         
       print ( 'Got a group: ' + str(group))                  
       return group
                                   
    def info (self,sheetIndex):
       print ( 'Info for card[' + str(sheetIndex) + ']: ' + self.suit(sheetIndex) + ',' + \
               'color: ' + self.redBlack(sheetIndex) + ', face: ' + str(self.face(sheetIndex)) )       
     
    def redBlack (self,index):
       s = self.suit (index)
       color = 'red'
       if (s == 'clubs') or (s == 'spades'): 
          color = 'black'
       return color
       
    def runMain (self): 
       window = pygame.display.get_surface()
       quit = False 
       
       mousePos = (0,0)
       dragDeck = None
       sourceDeck = None
       while not quit:
       
          self.draw(dragDeck,mousePos)
          events = utilities.readOne()
          for event in events:
             (typeInput,data,addr) = event
             if typeInput == 'move':
                mousePos = data
             if dragDeck != None:
                if typeInput == 'drop':
                   face = self.face(dragDeck.bottomSheetIndex())
                   print ( 'Bottom sheet face: ' + str(face))                    
                   
                   if face == 1:  
                      print ( 'You can drop Ace anywhere' )
                      self.decks.addDeck (dragDeck)
                      sourceDeck.revealTopCard() 
                   else:   
                      emptyColumn = self.emptyColumn() 
                      if (face==13) and (emptyColumn != -1): 
                         print ( 'You can place the king in an empty column yo' )
                         self.decks.addElement ( emptyColumn, dragDeck.data[0] ) 
                         sourceDeck.revealTopCard()                         
                      else:
                         print ( '\n\n***DROP EVENT***\n\n' )
                         (deck,index) = self.decks.findSprite (data) # Where are we dropping
                         suitsMatch = False
                         
                         dragSheetIndex = dragDeck.topSheetIndex()
                         dragSuit       = self.suit (dragSheetIndex)
                         dragFace       = self.face (dragSheetIndex)
                         
                         print ( 'Drag card' )
                         self.info (dragSheetIndex)
                      
                         if deck is None:
                            print ( 'Could not find a deck being dropped on' )
                            sourceDeck.appendDeck (dragDeck)
                         else:
                            dropSheetIndex = deck.data[index].sheetIndex
                            dropSuit       = self.suit (dropSheetIndex)
                            dropFace       = self.face (dropSheetIndex)
                            print ( 'Drop card' )
                            self.info (dropSheetIndex)                         
                         
                            print ( 'Got drop index: ' + str(index))
                            # print ( 'Add card: ' + str(dragging.sheetIndex) + ' to deck ' )  
                            print ( 'Destination deck has a top card of: ' + self.cardName ( deck.topSheetIndex()) )
                            if self.canDrop (dragDeck.bottomSheetIndex(), deck.topSheetIndex()): 
                               print ( 'Can drop ' + self.cardName (dragDeck.bottomSheetIndex()) + ' on ' + \
                                       self.cardName (deck.topSheetIndex()) )
                               deck.appendDeck(dragDeck) 
                               sourceDeck.revealTopCard() 
                            elif (dragSuit == dropSuit) and ((dragFace - dropFace ) == 1):
                               print ( 'Drop card on final pile' ) 
                               deck.appendDeck(dragDeck) 
                               sourceDeck.revealTopCard()
                            else:
                               print ( 'Cannot drop ' + self.cardName (dragDeck.bottomSheetIndex()) + \
                               ' on ' + self.cardName ( deck.topSheetIndex()) ) 
                               print ( 'Return dragDeck to originating deck' ) 
                               sourceDeck.appendDeck (dragDeck)
                                               
                   dragDeck = None
                   sourceDeck = None
             else:          
                if typeInput == 'drag': 
                   if dragDeck is None: 
                      print ( '\n\n***DRAG***\n\n' )
                      (deck,index) = self.decks.findSprite (data)
                      
                      sourceDeck = deck
                      mousePos = data
                      print ( 'Got an index of: ' + str(index)) 
                      if index > -1:
                         print ( 'Got drag index: ' + str(index))
                         group = self.getGroup (deck,index)
                         print ( 'Create a sub deck' )
                         dragDeck = SubDeck (width=80,height=120,displaySurface=self.DISPLAYSURF,xMultiplier=0.0, yMultiplier=0.25)
                         for card in group: 
                            dragDeck.addCard (deck,card)  
                         dragDeck.listCards()                           
                         deck.removeHidden (False)
                elif typeInput == 'select':
                   (deck,index) = self.decks.findSprite (data)
                   if deck != None: 
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
   
    def suit (self,index):
       suits = ['clubs','diamonds','hearts','spades']
       ind = int(index / 13) 
       value = suits[ind]
       return value
       
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
   solitaire = Solitaire (displaySurface,utilities,None)

   solitaire.runMain() 
