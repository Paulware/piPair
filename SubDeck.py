import pygame
from ViewImage import ViewImage

'''
   SubDeck is like a hand or a discard pile 
   It will use Decks ability to deal and will add the attributes x,y,width,height to each element in the dealt hand.
   There is no descriptive name on each element, that will be added based on id in the particular game class.   
'''
# SubDeck cannot be inherited from Deck because it is not a complete Deck, just part of one,  
# and focuses primarily on display capability
class SubDeck (): 
      
   def addCard (self,deck,index): 
      print ( 'addCard from deck with index: ' + str(index) + ' and tapped value: ' + str(deck.data[index].tapped)) 
      ind = len(self.data)-1
      if ind >= 0:
         if self.xMultiplier == 0.0: 
            x = self.data[ind].x
         else: 
            x = self.data[ind].x + self.width
         y = self.data[ind].y
         print ( 'xMultiplier: ' + str(self.xMultiplier) ) 
         if self.xMultiplier == 0.0: 
            deck.data[index].x = x
         else:
            deck.data[index].x = x * self.xMultiplier
         deck.data[index].y = y
      self.data.append (deck.data[index])
      print ( 'addCard, len(self.data): ' + str(len(self.data))) 

   # add a card from the specified deck.data[index] to the top card of this deck       
   def addTopCard (self,deck,index): 
      print ( 'addTopCard [index,sheetIndex,tapped]: [' + str(index) + ',' + str(deck.data[index].sheetIndex) + ',' + \
              str(deck.data[index].tapped) + ']') 
      ind = len(self.data)-1 # Get new location from the top card of this deck 
      if ind >= 0:
         if self.xMultiplier == 0.0: 
            x = self.data[ind].x
         else: 
            x = self.data[ind].x + self.width
         y = self.data[ind].y
         print ( 'xMultiplier: ' + str(self.xMultiplier) ) 
         if self.xMultiplier == 0.0: 
            deck.data[index].x = x
         else:
            deck.data[index].x = x * self.xMultiplier
         deck.data[index].y = y
      #self.data.insert (0,deck.data[index])
      self.data.append (deck.data[index]) 
      count = 0 
      print ( 'addTopCard, new self.data: ' )
      for d in self.data: 
         count = count + 1
         print ( 'self.data[' + str(count) + '].sheetIndex:' + str(d.sheetIndex) ) 

   def append (self, element): 
      self.data.append (element)
      
   def appendDeck (self, deck): 
      for element in deck.data: 
         self.append (element)
      
   def bottomSheetIndex(self):   
      return self.data[0].sheetIndex
   
   def cardsToStr (self):
      message = ''
      for card in self.data: 
         if message != '': 
            message = message + ' '
         message = message + str(card.sheetIndex)
      print ( 'cardsToStr got: ' + message )
      return message 
          
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
      
   # Show the sprites at specified start position and update the location of each   
   def draw (self, debugIt=False):
      if debugIt:         
         print ('draw, self.data: ' + str(self.data)) 

      count = 0      
      for sprite in self.data:
         count = count + 1
         image = self.getImage (sprite)
         if self.showLength and (count == 8): 
            print ( '[x,y] of card 8 [: ' + str(sprite.x) + ',' + str(sprite.y) + ']' ) 
         if debugIt: 
            print ( 'card (' + str(count) + ').sheetIndex: ' + str (sprite.sheetIndex) ) 
         self.displaySurface.blit (image, (sprite.x,sprite.y)) 
               
   def dropAll (self):
      print ( 'Dropping all cards')
      for card in self.data:
         card.drag = False 
   
   def findSprite (self,pos):
      debugIt = False 
   
      found = None
      if pos is None: 
         print ( 'ERR...SubDeck.findSprite, pos is None' )
      if len(pos) != 2: 
         print ( 'ERR...SubDeck.findSprite, pos is not correct [' + str(pos) + ']') 
      else:
         x = pos[0]
         y = pos[1]
         index = 0 
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
      
   # data is a list of objects that have an image and index attribute
   #    xMultiplier dictates how far apart each card will be in the horizontal (x) axis
   #    yMultiplier dictates how far apart each card will be in the vertical (y) axis
   def __init__ (self, deckBasis=None, numCards=0, width=80, height=120, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[] ):
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
      self.showLength = False
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
            if len(cards) > 0:
               dealtCards = self.deck.dealList (cards) 
               numCards = len(cards)
            else:             
               if numCards == 0: # Deal all remaining cards 
                  numCards = self.deck.length()         
         
               dealtCards = self.deck.deal (numCards)
               
            self.data = dealtCards
            
            self.redeal ()
            '''
            xOffset = self.xMultiplier * width
            yOffset = self.yMultiplier * height  
            x = self.startX
            y = self.startY 
            first = True             
            for card in self.data: # Set the width/height of each image 
               card.image = pygame.transform.scale(card.image, (width, height))                                     
               card.angle = 0
               card.hide  = False
               card.tapped = False
               card.x = x
               card.y = y
               x = x + xOffset
               y = y + yOffset 
            '''                                  
            self.numImages = len(self.data)
         
      print ('Total number of cards: ' + str(self.numImages)) 
            
   def hide (self,index):
      self.data[index].hide = True 
      
   def hideAll (self):
      for card in self.data:
         card.hide = True 
   
   def length (self):
      # print ( 'Length of deck: ' + str(len(self.data)))       
      return len(self.data)
         
   def listCards (self):
      count = 0
      for card in self.data: 
         print ( 'self.data[' + str(count) + '].index: ' + str(card.sheetIndex))  
         count = count + 1
         
   def move (self,index,pos): 
      self.data[index].x = pos[0]
      self.data[index].y = pos[1]    
                  
   def pos (self,index): 
      return ( self.data[index].x, self.data[index].y )    
   
   def redeal (self): 
      xOffset = self.xMultiplier * self.width
      yOffset = self.yMultiplier * self.height  
      x = self.startX
      y = self.startY            
      for card in self.data: # Set the width/height of each image 
         card.image = pygame.transform.scale(card.image, (self.width, self.height))                                     
         card.x = x
         card.y = y
         x = x + xOffset
         y = y + yOffset    
         
   def remove (self,index,redealCards=False): 
      self.data.pop (index)
      if redealCards: 
         self.redeal()
      
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
      
   def showAll (self):
      for card in self.data:
         card.hide = False
         
   def shuffleTo (self, destinationDeck): 
      while self.length() > 0: 
         self.topToDeck (destinationDeck, False)
      #TODO: Need to actually shuffle the cards 
             
   # Note: Tap should be for a specific game.   
   def tap (self,index,value): 
      print ( 'self.data[' + str(index) + '].tapped = ' + str(value))
      self.data[index].tapped = value

   def topSheetIndex (self): 
      print ( 'SubDeck.topIndex, return sheetIndex' )
      return self.data[self.length()-1].sheetIndex
   
   def topToDeck (self,deck,reveal=False): 
      if reveal: 
         self.revealTopCard()

      index = self.length() -1
      deck.addCard (self,index)
      self.remove (index)  
   
   def unhide (self,index):
      self.data[index].hide = False 
      
   def view (self,index, name ):
      ViewImage (name)
      print ( 'view card: ' + name + '[' + str(index) + ']') 
      
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
   dragCard = None
   quit = False    
   while not quit:
      displaySurface.fill ((0,0,0))
      hand.draw()
      utilities.flip()
      pygame.display.update()
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event      
         if typeInput == 'drag': 
            if dragCard is None:
               dragCard = hand.findSprite (data) 
               sheetIndex = hand.data[dragCard].sheetIndex 
               print ( '\n\n***DRAG*** ' + str(dragCard) + '.' + str(sheetIndex) + '\n\n' )
         elif typeInput == 'drop':
            print ( '\n***DROP*** ' + str(dragCard) + '.' + str(sheetIndex) ) 
            dragCard = None 
         elif typeInput == 'move':
            if not dragCard is None:
               hand.move (dragCard,data)         
         elif typeInput == 'right': 
            pos = pygame.mouse.get_pos()
            index = hand.findSprite (pos)
            if index != -1: 
               x = pos[0]
               y = pos[1]
               optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel', 'Hide', 'Show'], x, y)
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True 
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
         
    

