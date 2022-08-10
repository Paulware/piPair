import pygame

'''
   SubDeck is like a hand or a discard pile 
   It will use Decks ability to deal and will add the attributes x,y,width,height to each element in the dealt hand.
   There is no descriptive name on each element, that will be added based on id in the particular game class.   
'''
# SubDeck cannot be inherited from Deck because it is really just a piece of Deck 
# plus display capability
class SubDeck (): 
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis=None, numCards=0, width=80, height=120, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0 ):
      print ( 'SubDeck.init' )
      if displaySurface is None: 
         print ( 'You should specify displaySurface when subdeck is created' )
         exit (1)
      self.width = width
      self.height = height 
      self.selected = -1
      print ( 'startXY: ' + str(startXY) ) 
      self.startX = startXY [0]
      self.startY = startXY [1]
      self.displaySurface = displaySurface
      self.xMultiplier = xMultiplier
      self.yMultiplier = yMultiplier
      if deckBasis is None: 
         self.coverImage = None
      else:
         self.coverImage = deckBasis.coverImage
      if self.coverImage is None: 
         print ( 'SubDeck has a None cover image' )
      
      print ( 'Deal cards' )
      if deckBasis is None: 
         self.data = [] 
         self.numImages = 0
      else:
         self.deck = deckBasis
         if not (self.deck is None): 
            dealtCards = self.deck.deal (numCards)
               
            self.data = dealtCards
            for card in self.data: # Set the width/height of each image 
               card.image = pygame.transform.scale(card.image, (width, height))                                     
               card.angle = 0
               card.hide  = False
               card.tapped = False 
            self.numImages = len(self.data)
         
      print ('Total number of cards: ' + str(self.numImages)) 
      
   def addCard (self,deck,index): 
      print ( 'addCard from deck with index: ' + str(index) + ' and tapped value: ' + str(deck.data[index].tapped)) 
      self.data.append (deck.data[index])
      print ( 'addCard, self.data: ' + str(self.data)) 

   def append (self, element): 
      self.data.append (element)
      
   def appendDeck (self, deck): 
      for element in deck.data: 
         self.append (element)
      
   def bottomSheetIndex(self):   
      return self.data[0].sheetIndex
      
   # shift cards and place top card at the bottom of the deck    
   def cycleTopCard (self):
      print ( 'cycle top card, length of deck: ' + str(len(self.data)))
      if len(self.data) > 1: 
         topCard = self.data[len(self.data)-1]
         for i in range (len(self.data)-1): 
            # print ( 'self.data['  + str(i+1) + ' = self.data[' + str(i) + ']' )
            self.data[len(self.data)-i-1] = self.data[len(self.data)-i-2]
         self.data[0] = topCard
                               
   def drawCard (self): 
      cards = self.deck.deal (1)
      self.data.append (cards[0]) 
               
   def discard (self,index): 
      self.remove (index)
   
   def drag (self,index, value):
      self.data[index].drag = value
      self.selected = index 
      
   def dropAll (self):
      print ( 'Dropping all cards')
      for card in self.data:
         card.drag = False 
   
   def findSprite (self,x,y):
      debugIt = True 
      index = 0 
      found = -1
      if debugIt: 
         print ( 'findSprite (' + str(x) + ',' + str(y) + ')' ) 
      for sprite in self.data: 
         if debugIt:
            print ( '[x,y,spritex,spritey]: [' + str(x) + ',' + str(y) + ',' + str(sprite.x) + ',' + str(sprite.y) + ']' )
            width = sprite.image.get_width()
            print ( 'width: ' + str(width) ) 
            height = sprite.image.get_height()
            print ( 'height: ' + str(height) )             
         if ((x > sprite.x) and (x < (sprite.x + sprite.image.get_width())) and \
             (y > sprite.y) and (y < (sprite.y + sprite.image.get_height()))):
            if debugIt:             
               print ( 'Found sprite at index: ' + str(index))
            found = index 
         index = index + 1
      print ( 'Done in findSprite: ' + str(found) ) 
      return found 
      
   def getImage (self,sprite):
      if sprite.hide: 
         image = pygame.transform.scale(self.coverImage, (self.width, self.height))                                     
      else: 
         image = pygame.transform.scale(sprite.image, (self.width, self.height)) 
         
      if sprite.tapped:          
         image = self.rotate (image,90) 
      return image 
      
   def hide (self,index):
      self.data[index].hide = True 
      
   def hideAll (self):
      for card in self.data:
         card.hide = True 
   
   def showAll (self):
      for card in self.data:
         card.hide = False
   
   def length (self):
      print ( 'Length of deck: ' + str(len(self.data)))       
      return len(self.data)
         
   def listCards (self):
      count = 0
      for card in self.data: 
         print ( 'self.data[' + str(count) + '].index: ' + str(card.sheetIndex))  
         count = count + 1
         
   def remove (self,index): 
      self.data.pop (index)
      
   def removeHidden (self, hide): 
      found = True 
      
      while found: 
         found = False 
         index = 0
         for card in self.data: 
            if card.hide == hide:
               self.remove (index)
               found = True 
               break
            index = index + 1

      print ( 'Removed all cards with .hide = ' + str(hide))                
         
   def revealTopCard (self):
      length = len(self.data)
      if length > 0: 
         self.data[length-1].hide = False 
      
   def rotate (self, image, angle): 
      # calculate the axis aligned bounding box of the rotated image
      w, h       = image.get_size()
      originPos  = (w//2,h//2)
      box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
      box_rotate = [p.rotate(angle) for p in box]
      min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
      max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

      # calculate the translation of the pivot 
      pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
      pivot_rotate = pivot.rotate(angle)
      pivot_move   = pivot_rotate - pivot
       
      # get a rotated image
      rotated_image = pygame.transform.rotate(image, angle)      
      return rotated_image  

   # Show the sprites at specified start position and update the location of each   
   def showSprites (self): 
      debugIt = False
      x = self.startX
      y = self.startY
      if debugIt:         
         print ('showSprites, self.data: ' + str(self.data)) 

      index = 0      
      for sprite in self.data:
         image = self.getImage (sprite)
         xOffset = self.xMultiplier * image.get_width()
         yOffset = self.yMultiplier * image.get_height()         
         if sprite.drag:
            if debugIt:
               print ( 'sprite is draggable' )          
            pos = pygame.mouse.get_pos()        
            self.displaySurface.blit (image,pos)
            sprite.x = pos[0]
            sprite.y = pos[1]         
         else:
            if debugIt:
               print ( 'sprite is not draggable' )
            self.displaySurface.blit (image, (x,y)) 
            # Update location so it can be found later
            sprite.x = x
            sprite.y = y
            x = x + xOffset  
            y = y + yOffset            
         index = index + 1
      
   def tap (self,index,value): 
      print ( 'self.data[' + str(index) + '].tapped = ' + str(value))
      self.data[index].tapped = value
   
   def topSheetIndex (self): 
      print ( 'SubDeck.topIndex, return sheetIndex' )
      return self.data[self.length()-1].sheetIndex
      
   def unhide (self,index):
      self.data[index].hide = False 
      
if __name__ == '__main__':
   from Deck import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   print ( 'Make deck' )
   deckBasis = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)
   print ( 'Deal' )
   startXY = (100,100)
   hand = SubDeck (deckBasis,7,80,120,startXY,displaySurface)  
   print ( 'Done dealing ' )
   window = pygame.display.get_surface()
   
   while True:
      window.fill ((0,0,0))
      hand.showSprites() # Show and set their x/y locations
      pygame.display.update()
      (typeInput,data,addr) = utilities.read()
      if utilities.isMouseClick (typeInput): 
         pos = pygame.mouse.get_pos()
         x = pos[0]
         y = pos[1]
         index = hand.findSprite (x,y)
         if index != -1: 
             optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel', 'Hide', 'Show'], x, y)
             selection = optionBox.getSelection()
             print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
             if selection == 'Cancel': 
                break
             elif selection == 'Discard':
                hand.discard (index) 
             elif selection == 'Tap':                
                hand.tap (index, True )
             elif selection == 'Use':
                hand.discard (index)
                hand.drawCard()
             elif selection == 'Hide':
                hand.hide(index)
             elif selection == 'Show':
                hand.unhide(index)

