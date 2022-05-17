from SubDeck import SubDeck 
class SubDecks():
   def __init__(self, decks):
      self.decks = decks 
      self.selected = None
      
   def findSprite (self, pos):
      index = -1
      found = None
      for deck in self.decks:
         index = deck.findSprite (pos[0], pos[1])
         if index != -1:
            found = deck
            break
      return (found,index)
      
   def showSprites (self): 
      for deck in self.decks: 
         deck.showSprites(xMultiplier=0.0, yMultiplier=1.0)
         

if __name__ == '__main__':
   import pygame
   from Deck import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
 
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
   while not quit:
      decks.showSprites()

      events = utilities.readOne()
      for event in events: 
         (typeInput, data, addr ) = event
         print ( 'typeInput: ' + str(typeInput))
         if dragging != None: 
            if typeInput == 'move':
               window.fill ((0,0,0))            
               decks.showSprites()
               displaySurface.blit (dragging, data)             
               pygame.display.update() 
            elif typeInput == 'drop':
               dragging = None
         else:          
            if typeInput == 'drag': 
               (deck,index) = decks.findSprite (data)
               print ( 'Got drag index: ' + str(index)) 
               dragging = deck.data[index].image 
            elif typeInput == 'drop': 
               (deck,index) = decks.findSprite (data) # Where are we dropping 
               print ( 'Got drop index: ' + str(index)) 
               exit(1)
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

                   window.fill ((0,0,0))
