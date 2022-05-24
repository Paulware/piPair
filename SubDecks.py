from SubDeck import SubDeck 
import pygame
import time
class SubDecks():
   def __init__(self, decks):
      self.decks = decks 
      self.selected = None
      self.displaySurface = pygame.display.get_surface()
      self.showTime = 0
      
   def findSprite (self, pos):
      index = -1
      found = None
      for deck in self.decks:
         index = deck.findSprite (pos[0], pos[1])
         if index != -1:
            found = deck
            break
      return (found,index)
      
   def showSprites (self,xMultiplier=0.0,yMultiplier=1.0):
      for deck in self.decks:
         deck.showSprites(xMultiplier, yMultiplier)
                
   def updateDisplay(self, dragging, pos, xMultiplier=0.0, yMultiplier=1.0):
      if time.time() > self.showTime:
         self.displaySurface.fill ((0,0,0))
         self.showSprites(xMultiplier,yMultiplier)

         if dragging != None:
            self.displaySurface.blit (dragging.image, pos)
         
         self.showTime = time.time() + 0.05
         pygame.display.update()

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
     
   parts = Deck ('images/unoSpriteSheet.jpg', 10, 6, 53) 
   parts.coverIndex = 52 
   parts1 = SubDeck (parts,2,80,120, (100,100), displaySurface)  
   parts2 = SubDeck (parts,3,80,120, (200,100), displaySurface)  
   decks = SubDecks([parts1,parts2])
         
   window = pygame.display.get_surface()
   quit = False 
   dragging = None    
   
   mousePos = (0,0)
   while not quit:
      decks.updateDisplay(dragging,mousePos)
      events = utilities.readOne()
      for event in events: 
         (typeInput, data, addr ) = event
         if typeInput == 'move': 
            mousePos = data
         if dragging != None: 
            if typeInput == 'drop':
               (deck,index) = decks.findSprite (data) # Where are we dropping               
               if deck is None: 
                  print ( 'Deck is none' ) 
               else:                   
                  print ( 'Got drop index: ' + str(index))  
                  print ( 'Add card: ' + str(dragging.index) + ' to deck: ' )  
                  deck.append(dragging)                 
                  dragging = None
         else:          
            if typeInput == 'drag': 
               if dragging is None: 
                  (deck,index) = decks.findSprite (data)
                  mousePos = data
                  if index > -1: 
                     print ( 'Got drag index: ' + str(index)) 
                     deck.data[index].deleted = True
                     dragging = deck.data[index]
                     deck.remove (index)                   
            elif typeInput == 'select':
               (deck,index) = decks.findSprite (data)
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