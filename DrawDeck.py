import random
import pygame
from Deck import Deck

#class Object(object):
#    pass


'''
   Responsibility of the deck is to read a sprite sheet and parse it into
      all the cards. 

   Functions are exposed that allow you to chop the deck into subdecks, such as deal            
   The deck will not display the cards, but that is the responsibility of the sub-deck.
   
   Part of a deck can be moved to a sub-deck randomly, with those cards removed from the deck.
     
      
   Original data is stored in the sheet.data element which is a list object
      This class will add not add any attributes to that sheet.data
      
   This class will also have a coverImage attribute which is the image on the back of the card
'''
class DrawDeck (Deck): 
   def __init__ (self, filename, numColumns, numRows, numImages, width, height, displaySurface, startXY, \
                 xMultiplier=1.0, yMultiplier=0.0, coverIndex=None):
        print ( 'DrawDeck numImages: ' + str(numImages) ) 
        Deck.__init__ (self,filename,numColumns,numRows,numImages,coverIndex)      
        if displaySurface is None: 
           print ( 'You should specify displaySurface when subdeck is created' )
           exit (1)
        self.width          = width
        self.height         = height 
        self.selected       = -1 
        self.startX         = startXY [0]
        self.startY         = startXY [1]    
        self.nextX          = self.startX
        self.nextY          = self.startY      
        self.displaySurface = displaySurface
        self.xMultiplier    = xMultiplier
        self.yMultiplier    = yMultiplier
        self.showLength     = False
        if self.coverImage is None: 
           print ( 'DrawDeck has a None cover image' )
           raise Exception ( 'No cover image specified')
        
        self.numImages = len(self.data)        
        for card in self.data:
           card.width    = width
           card.height   = height
        
        print ('Deck has ' + str(self.numImages) + ' cards ') 
        
   def deal (self, deckName, numCards, width, height, startX, startY): 
      print ( 'Deal out ' + str(numCards) + ' cards to deck: ' + deckName )
      drawOrder = 0
      for i in range (numCards):   
         index = self.getRandomIndex (len(self.data))
         while self.data[index].location != '':
            index = self.getRandomIndex (len(self.data))
         print ( 'index: ' + str(index)) 
         
         try: 
            card = self.data[index]
         except IndexError:
            print ( 'This index of out of range: ' + str(index) )
            exit(1)
            
         card.x         = startX
         card.y         = startY
         card.width     = width
         card.height    = height
         card.location  = deckName
         card.hide      = False
         card.drawOrder = drawOrder
         drawOrder      = drawOrder + 1
    
         print ( str(i) + ') just dealt card with index: ' + str(card.sheetIndex) + ' from random number: ' + str(index) ) 
  
   def drawInfo (self,deckName):
      count = 0
      maxIndex = -1
      minIndex = -1 
      for card in self.data: 
         if card.location == deckName:
            count = count + 1
            if minIndex == -1: 
               minIndex = count 
            elif card.drawOrder < self.data[minIndex].drawOrder: 
               minIndex = count 
            if maxIndex == -1:
               maxIndex = count
            elif card.drawOrder > self.data[maxIndex].drawOrder: 
               maxIndex = count
               
      return (count,minIndex,maxIndex)
  
   def deckTop (self,deckName): 
      top = -1
      drawOrder = 0
      index = -1
      for card in self.data: 
         index = index + 1
         if card.location == deckName:       
            if top == -1: 
               top       = index
               drawOrder = card.drawOrder 
            elif top < card.drawOrder:
               top       = index
               drawOrder = card.drawOrder 
      return (top,drawOrder)

   
   #TODO: Maintain the drawOrder...   
   def draw ( self, deckName ): 
      debugIt = False 
      count = 0 
      for card in self.data:
         if card.location == deckName: 
            count = count + 1
            image = self.getImage (card)
            if debugIt: 
               print ( 'card (' + str(count) + ').[x,y,sheetIndex: [' + str(card.x) + ',' + str(card.y) + ',' + \
                       str (card.sheetIndex) + ']'  ) 
            card.drawOrder = count
            if not card.hide: 
               self.displaySurface.blit (image, (card.x,card.y))           
               
   def drawTop (self, deckName): 
      debugIt = False 
      (top,drawOrder) = self.deckTop (deckName)
      if top == -1: 
         raise Exception ( "Could not find a top for deck: " + deckName )
      else: 
         card = self.data[top]
         image = self.getImage (card)
         if debugIt: 
            print ( 'drawTop, card (' + str(top) + ').[location,x,y,sheetIndex: [' + card.location + ',' + \
                    str(card.x) + ',' + str(card.y) + ',' + str (card.sheetIndex) + ']'  ) 
         if not card.hide: 
            self.displaySurface.blit (image, (card.x,card.y))           
      
                           
   def findCard (self,pos,ignoreCard=-1):
      debugIt   = False 
      found     = -1
      drawOrder    = -1
      if pos is None: 
         raise Exception ( 'ERR...DrawDeck.findCard, pos is None' )
      if len(pos) != 2: 
         raise Exception ( 'ERR...DrawDeck.findCard, pos is not correct [' + str(pos) + ']') 
      else:
         x = pos[0]
         y = pos[1]
         if debugIt: 
            print ( 'findCard(' + str(x) + ',' + str(y) + '), len(self.data): ' + str(len(self.data)) + \
                    ' sprite [x,y,width,height]: [' + str(self.data[0].x) + ',' + str(self.data[0].y) + \
                    ',' + str(self.data[0].width) + ',' + str(self.data[0].height) + ']' ) 
         index = -1 
         deckName = ''
         for card in self.data: 
            index = index + 1
            if (ignoreCard == -1) or (ignoreCard != index): 
               if card.location != '':
                  width  = card.width
                  height = card.height
                  rect = pygame.Rect (card.x, card.y, width,height)               
                  if debugIt:
                     print ( 'rect: ' + str(rect)) 
                  if rect.collidepoint (pos): 
                     deckName = card.location
                     if found == -1: 
                        found = index                     
                     else: 
                        if card.drawOrder > self.data[found].drawOrder:
                           found = index 
                           
         if found > -1: 
            print ( '.findCard found: ' + str(found) + ' in deck: ' + deckName ) 
            print ( 'Using: [found,card.drawOrder, self.data[found].drawOrder]: [' + \
                                   str(found) + ',' + str(card.drawOrder) + ',' + \
                                   str(self.data[found].drawOrder) + ']') 
         return found 
         
   def findLeftCard (self, deckName):
      found = -1
      count = -1
      for card in self.data:    
         count = count + 1
         if deckName == card.location:
            if found == -1:
               found = count
            elif self.data[found].x > card.x:
               found = count 
      print ( 'left most card is card: ' + str(found) ) 
      return found        

   def getImage (self,card):
      if card.hide: 
         image = pygame.transform.scale(self.coverImage, (self.width, self.height))                                     
      else: 
         image = pygame.transform.scale(card.image, (self.width, self.height)) 
      card.width  = image.get_width()
      card.height = image.get_height()      
      return image 
      
   def move (self,index,pos): 
      self.data[index].x = pos[0]
      self.data[index].y = pos[1]  
      
   def placeOnTop (self,deckName,index):
      debugIt = True       
      (top,drawOrder) = self.deckTop (deckName)   
      self.data[index].location = deckName
      self.data[index].drawOrder = drawOrder + 1
      self.data[index].x = self.data[top].x
      self.data[index].y = self.data[top].y
      print ( 'TODO: maintain draw order' ) 
                   
   # set the x location of cards
   # Todo: Maintain the draw order... 
   def redeal (self, deckName, x, y, xOffset, yOffset):
      debugIt = True      
      if debugIt:        
         print ( 'len(self.data): ' + str(len(self.data)) )
         
      cnt = 0    
      for card in self.data: # Set the width/height of each image 
         if deckName == card.location: 
            ind = cnt
            if debugIt:
               print ( 'self.data[' + str(ind) + '].x = ' + str(x) ) 
               print ( 'self.data[' + str(ind) + '].y = ' + str(y) )          
            
            card.x = x
            card.y = y 

            if debugIt: 
               print ( 'card (' + str(ind) + ') redeal [width,height,xMultipler, xOffset,x,y,sheetIndex]: [' + \
                       str(self.width) + ',' + str(self.height) + ',' + str(self.xMultiplier) + ',' + str(xOffset) + ',' + \
                       str(card.x) + ',' + str(card.y) + ',' + str(card.sheetIndex) + ']' )
            x = x + xOffset
            y = y + yOffset    
            cnt = cnt + 1

      self.nextX = x
      self.nextY = y
      if debugIt: 
         print ( '\nSubDeck, ***Show deck after redeal' )   
                    
if __name__ == '__main__':
   from Utilities import Utilities
   from OptionBox import OptionBox
    
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   print ( 'Make deck' )
   startXY = (100,100)
   deck = DrawDeck ('images/unoSpriteSheet.jpg', 10, 6, 52, 60,100,displaySurface,startXY,1.0,0.0,coverIndex=52)
   deck.deal ( 'hand', 7, 80, 120, 100, 100,)
   
   deck.redeal ('hand', 100, 100, 60, 0)
   
   dragCard = None
   while True:
      displaySurface.fill ((0,0,0))
      deck.draw('hand')
      utilities.flip()
      pygame.display.update()
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event      
         if typeInput == 'drag': 
            if dragCard is None:
               dragCard = deck.findCard (data) 
               sheetIndex = deck.data[dragCard].sheetIndex 
               print ( '\n\n***DRAG*** ' + str(dragCard) + '.' + str(sheetIndex) + '\n\n' )
         elif typeInput == 'drop':
            print ( '\n***DROP*** ' + str(dragCard) + '.' + str(sheetIndex) ) 
            dragCard = None 
         elif typeInput == 'move':
            if not dragCard is None:
               deck.move (dragCard,data) 
               print ( 'Moving [' + str (dragCard) + '] to: ' + str(data) )                
         elif typeInput == 'right': 
            pos = pygame.mouse.get_pos()
            index = deck.findCard (pos)
            if index != -1: 
               x = pos[0]
               y = pos[1]
               optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel', 'Hide', 'Show'], x, y)
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True 
               elif selection == 'Discard':
                  deck.data[index].location = 'discardPile' 
                  #TODO change x/y location 
               elif selection == 'Tap':                
                  deck.data[index].tapped = not deck.data[index].tapped
               elif selection == 'Use':
                  deck.data[index].location = 'discardPile'
                  #TODO change x/y location 
               elif selection == 'Hide':
                  deck.data[index].hide = True
               elif selection == 'Show':
                  deck.data[index].hide = False 