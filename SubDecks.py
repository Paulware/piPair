from SubDeck import SubDeck 
import pygame
import time
class SubDecks():
   def __init__(self, decks):
      self.decks = decks 
      self.selected = None
      self.displaySurface = pygame.display.get_surface()
      self.showTime = 0
      
   def addDeck (self,deck):
      self.decks.append (deck)   
      
   def addElement (self,deckIndex,element): 
      self.decks[deckIndex].append(element)
      
   def addElements (self,targetDeckIndex, deck):
      for element in deck.data:
         self.addElement (targetDeckIndex, element )      
         
   def draw (self):      
      for deck in self.decks:          
         deck.draw ()
      
   def emptyColumn(self):
      found = -1 
      count = 0 
      for deck in self.decks:
         if deck.emptyColumn (): 
            found = count
            break
         count = count + 1
            
      if found == -1: 
         print ( 'No empty column found in any deck' )
      else:
         print ( 'Found an empty column in deck: ' + str(count) )
      return found       
            
   def findSprite (self, pos):
      debugIt = True
      if debugIt: 
         print ( 'SubDecks.findSprite (' + str(pos) + ')' )
      found = None
      if pos is None: 
         print ( 'SubDecks.findSprite, pos == None' )
      elif len(pos) != 2: 
         print ( 'SubDecks.findSprite, pos is not correct: ' + str(len(pos)) ) 
      else:
      
         for deck in self.decks:           
            index = deck.findSprite (pos)
            if not index is None:
               found = deck
               break
            
      if found is None:
         print ( 'This deck has no sprite associated with this position: ' + str(pos) ) 
      else:
         print ( 'SubDecks.findSprite, found: ' + str(found) ) 
         print ( 'SubDecks.findSprite, found a match at position: ' + str(pos) + ', index: ' + str(index)) 
         
      return (found,index)
   
   '''            
   def updateDisplay(self, dragDeck, pos):
      if time.time() > self.showTime:
         self.displaySurface.fill ((0,0,0))
         self.draw()
         if dragDeck != None: 
            dragDeck.startX = pos[0]
            dragDeck.startY = pos[1]
            dragDeck.draw()
         self.showTime = time.time() + 0.05
         pygame.display.update()
   '''
   
if __name__ == '__main__':
   import pygame
   from Deck import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   import time
 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
     
   parts = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 50) 
   parts.coverIndex = 52 
   parts1 = SubDeck (parts,2,80,120, (100,100), displaySurface)  
   parts2 = SubDeck (parts,3,80,120, (300,100), displaySurface)  
   decks  = SubDecks([parts1,parts2])
         
   window = pygame.display.get_surface()
   quit = False 
   
   # dragging: index to a card in the deck where deck is the 
   #           last deck selected
   dragging = None
         
   mousePos = (0,0)
   while not quit:
      window.fill ((0,0,0))   
      decks.draw()
      utilities.flip()
      
      events = utilities.readOne()
      for event in events: 
         (typeInput, data, addr ) = event
         if typeInput == 'move': 
            if not dragging is None: 
               deck.move (dragging,data)               
            mousePos = data
         elif typeInput == 'drop':
            print ( '*** DROP *** ' )
            (deck,index) = decks.findSprite (data) # Where are we dropping               
            if deck is None: 
               print ( 'Drop Event, could not find an associated deck' ) 
            else:                   
               print ( 'Got drop index: ' + str(index))  
               print ( 'Add card: ' + str(deck.data[dragging].sheetIndex) + ' to deck ' )  
               deck.append(deck.data[dragging])                 
            dragging = None
         elif typeInput == 'drag': 
            if dragging is None: 
               (deck,index) = decks.findSprite (data)
               dragging = index
         elif typeInput == 'right':
            print ( '*** RIGHT *** ')
            (deck,index) = decks.findSprite (data)
            if not deck is None: 
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