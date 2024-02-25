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
           print ( 'You should specify displaySurface when drawdeck is created' )
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
           card.location = ''
           card.x        = 0
           card.y        = 0
        
        print ('Deck has ' + str(self.numImages) + ' cards ') 
        self.lastDrawMessage = '' # For debugging only 

   def cardInfo ( self, index): 
      line = 'DrawDeck.cardInfo, [index]: [' + str(index) + ']'
      card = self.data[index]
      line = line + '\r' + card.location + '.card (' + str(index) + '): [drawOrder], [' + str(card.drawOrder) + ']'
      return line 
   
   def cardsToStr (self,deckName):
      message = ''
      drawOrder = 0
      for card in self.data: 
         if card.location == deckName:
            if message != '': 
               message = message + ' '
            index = self.findDrawCard (deckName, drawOrder )
            sheetIndex = self.data[index].sheetIndex            
            message = message + str(sheetIndex)
            drawOrder = drawOrder + 1
            
      print ( 'cardsToStr got: ' + message )
      return message 
      
   def checkDrawOrder (self,deckName): 
      index = -1 
      for card in self.data: 
         index = index + 1 
         if card.location == deckName:
            drawOrder = card.drawOrder 
            # print ( 'card (' + str(index) + ')drawOrder: ' + str(card.drawOrder) ) 
            ind = -1
            for crd in self.data: 
               ind = ind + 1
               if crd.location == deckName: 
                  if crd.drawOrder == drawOrder:
                     if (ind != index): 
                        assert False, 'Deck ' + deckName + ' has a double drawOrder: ' + \
                                      str(drawOrder)                  
      print ( 'Deck ' + deckName + ' checks out ok' )   
      
   def deal (self, deckName, numCards, width, height, startX, startY): 
      print ( 'Deal out ' + str(numCards) + ' cards to deck: ' + deckName )
      drawOrder = 0
      for i in range (numCards):   
         index = self.getRandomIndex (len(self.data))
         count = 0 
         
         
         cardsLeft = self.length ('')          
         #print ( 'cardsLeft: ' + str(cardsLeft))         
         assert cardsLeft > 0, 'Ran out of cards trying to deal, the number of cards remaining in this deck is: ' + str(cardsLeft)
         
         while self.data[index].location != '':
            count = count + 1
            index = self.getRandomIndex (len(self.data))
               
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
    
         print ( str(i) + ' of ' + str(numCards) + ' just dealt ' + deckName + ' card with index: ' + str(card.sheetIndex) + \
         ' [drawOrder,x,y]: [' + str(card.drawOrder) + ',' + str(card.x) + ',' + str(card.y) + ']'  ) 
      print ( 'Done in ' + deckName + ' deal' )
   
   def decrementOrder ( self, deckName, drawOrder): 
      index = -1 
      for card in self.data: 
         index = index + 1 
         if card.location == deckName:
            if card.drawOrder >= drawOrder:        
               #print ( 'decrementing drawOrder: ' + str(card.drawOrder) ) 
               card.drawOrder = card.drawOrder - 1
               #print ( ' to: ' + str(card.drawOrder) ) 
                                  
   def deckTop (self,deckName,debugIt=False): 
      top = -1
      drawOrder = -1
      index = -1
      for card in self.data: 
         index = index + 1
         if card.location == deckName:       
            if card.drawOrder > drawOrder:
               top       = index
               drawOrder = card.drawOrder
               
      if top == -1: 
         print ( 'deck ' + deckName + ' does not exist, but will be created' )
      #assert top != -1, 'Could not find a top card for deck: [' + deckName + '], does deck ' + deckName + ' exist?' 
      if debugIt: 
         print ( 'deckTop [name,top,drawOrder]: [' + deckName + ',' + str(top) + ',' + str(drawOrder) + ']' )
      return (top,drawOrder)
  
   def draw ( self, deckName ):
      debugIt = False
      count = 0
      for card in self.data:
         if card.location == deckName:
            index = self.findDrawCard (deckName, count)
            if index == -1:
               break
            else:
               card = self.data[index]
               image = self.getImage (card)              
               self.displaySurface.blit (image, (card.x,card.y))
               
            count = count + 1
      
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
  
   def drawTop (self, deckName): 
      debugIt = False 
      (top,drawOrder) = self.deckTop (deckName)
      if top == -1: 
         assert True, 'Could not find a top for deck: ' + deckName 
      
      card = self.data[top]
      if debugIt:
         print ( 'drawTop, card (' + str(top) + ').[location,x,y,sheetIndex: [' + card.location + ',' + \
                 str(card.x) + ',' + str(card.y) + ',' + str (card.sheetIndex) + ']'  ) 
      image = self.getImage (card)
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
            card = self.data[found]
            print ( '.findCard found: ' + str(found) + ' in deck: ' + deckName ) 
            print ( 'Using: [found,card.drawOrder, self.data[found].drawOrder]: [' + \
                                   str(found) + ',' + str(card.drawOrder) + ',' + \
                                   str(self.data[found].drawOrder) + ']') 
         return found 
   
   def findDrawCard (self, deckName, drawOrder ): 
      index = -1
      found = -1
      for card in self.data:
         index = index + 1
         if card.location == deckName: 
            if card.drawOrder == drawOrder:
               found = index 
               break
      if found == -1: 
         message = 'Could not find drawOrder ' + str(drawOrder) + ' for deck: ' + deckName
         assert True, 'Could not find drawOrder ' + str(drawOrder) + ' for deck: ' + deckName 
         if message != self.lastDrawMessage:
            print (message)
            self.lastDrawMessage = message
            self.showInfo (deckName)
            
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

   def hideName ( self,deckName): 
      for card in self.data:
         if deckName == card.location:
            card.hide = True          
   
   def length (self,deckName):
      count = 0 
      for card in self.data:
         if card.location == deckName: 
            count = count + 1
      return count 

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
   
   def moveTo (self, deckName, index ):
      self.placeOnTop (deckName,index)
   
   def placeOnTop (self,deckName,index):
      debugIt = True  
      newDeck = False 
      top = -1
      if self.length ( deckName ) == 0: 
         print ( 'Create this deck: ' + deckName )
         newDeck = True 
         drawOrder = -1 
      else:          
         (top,drawOrder) = self.deckTop (deckName)  
         
      print ( 'Deck ' + deckName + ' has a [top,drawOrder]: [' + str(top) + ',' + str(drawOrder) + ']' )      
      sourceDeck  = self.data[index].location
      if hasattr (self.data[index],'drawOrder'): 
         sourceOrder = self.data[index].drawOrder
         self.decrementOrder (sourceDeck,sourceOrder)
      # By moving this card, we create a hole in the draw order of the sourceDeck 
      self.data[index].location = deckName # We now have a hole in the draw order
      print ( 'Old drawOrder: ' + str(drawOrder) )            
      drawOrder = drawOrder + 1 # Adding to top of deck
      print ( 'Moving card: [' + str(index) + '] with drawOrder: ' + \
              ' to deck: ' + deckName + ' drawOrder: ' + str(drawOrder))
      self.data[index].drawOrder = drawOrder
      print ( 'New drawOrder: ' + str(drawOrder) ) 
      if hasattr ( self.data[index], 'x'):  
         self.data[index].x = self.data[top].x
         self.data[index].y = self.data[top].y
      else:
         # x/y should be set by redeal function 
         self.data[index].x = 100
         self.data[index].y = 100
      print ( 'Done in placeOnTop' )
   
   def pos (self,index):
      return ( self.data[index].x, self.data[index].y )
   
   # set the x location of cards
   # Maintain the draw order...Does redeal care? 
   def redeal (self, deckName, x, y, xOffset, yOffset):
      print ( 'DrawDeck.redeal [deckName,x,y,xOffset,yOffset]: [' + deckName + ',' + \
              str(x) + ',' + str(y) + ',' + str(xOffset) + ',' + str(yOffset) + ']' )
      debugIt = True
      drawOrder = 0
      index = 0
      for card in self.data: # Set the width/height of each image 
         if deckName == card.location: 
            index = self.findDrawCard (deckName, drawOrder)
            drawCard = self.data[index]
            if debugIt:
               print ( 'self.data[' + str(index) + '].x = ' + str(x) ) 
               print ( 'self.data[' + str(index) + '].y = ' + str(y) )          
            
            drawCard.x = x
            drawCard.y = y 

            if debugIt: 
               print ( 'card (' + str(drawOrder) + ') redeal [location,width,height,xMultipler, xOffset,x,y,sheetIndex,drawOrder]: [' + \
                       drawCard.location + ',' + \
                       str(self.width) + ',' + str(self.height) + ',' + str(self.xMultiplier) + ',' + \
                       str(xOffset) + ',' + str(drawCard.x) + ',' + str(drawCard.y) + ',' + \
                       str(drawCard.sheetIndex) + ',' + str(drawCard.drawOrder) + ']' )
            x = x + xOffset
            y = y + yOffset    
            drawOrder = drawOrder + 1 # drawOrder starts at 0

      self.nextX = x
      self.nextY = y
      if debugIt: 
         print ( '\nDrawDeck, ***Show deck after redeal' )   

   def showInfo ( self, deckName='*'): 
      print ( self.cardInfo ( deckName ) )
      print ( 'DrawDeck.showInfo, [deckName,len(self.data)]: [' + deckName + ',' + str(len(self.data)) + ']' )
      index = -1
      for card in self.data:
         index = index + 1
         if (card.location == deckName) or (deckName == '*'):
            print ( card.location + '.card (' + str(index) + '): [drawOrder], [' + \
            str(card.drawOrder) + ']')

   def topToDeck ( self, topDeck, destinationDeck ):
      print ( ' Move a card from ' + topDeck + ' to ' + destinationDeck )
      (index, drawOrder) =  self.deckTop ( topDeck )
      self.placeOnTop ( destinationDeck, index )      
               
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
   deck.deal ( 'hand', 7, 80, 120, 100, 100)
   deck.deal ( 'opponent', 7, 80, 120, 100,100)
   deck.redeal ('hand', 100, 300, 60, 0)
   deck.redeal ( 'opponent', 100,100,60,0)   
   
   dragCard = None
   quit = False
   while not quit:
      displaySurface.fill ((0,0,0))
      deck.draw ('hand')
      deck.draw ('opponent')
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
               optionBox = OptionBox (['Use', 'Hide', 'Tap', 'Cancel'], x, y) # , 'Discard'], x, y)
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True 
               elif selection == 'Use':
                  deck.show
                  deck.placeOnTop ( 'opponent', index )
                  deck.redeal ( 'hand',     100, 300, 60, 0)
                  deck.checkDrawOrder ('hand')
                  deck.redeal ( 'opponent', 100, 100, 60, 0) 
                  deck.checkDrawOrder ( 'opponent')
               elif selection == 'Hide':
                  deck.data[index].hide = not deck.data[index].hide
               elif selection == 'Tap':                
                  deck.data[index].tapped = not deck.data[index].tapped
                                   