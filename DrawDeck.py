import random
import pygame
from Deck import Deck

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
           
        self.save_position = (-1,0,0) # (index, x, y)
        
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
      
   def checkType ( self, value, typeName ): 
      typeValue = str(type(value))
      print ( 'typeValue: ' + typeValue )
      if typeValue.find ('str') > -1: 
         index = typeValue.find ( 'str' )
         assert index > -1, 'type(' + str(value) + ') should be string, but is:' + str(typeValue)
      elif typeValue.find ( 'int') > -1: 
         index = typeValue.find ( 'int' )
         assert index > -1, 'type(' + str(value) + ') should be int, but is:' + str(typeValue)
   
   def cycleTop (self,deckName):
      if self.numCards (deckName) > 0: 
         (topCard,_) = self.deckTop ( deckName,True)
         assert topCard > -1, 'Could not find topCard: ' + str(topCard) 
         print ( 'DrawDeck.cycleTop, change drawOrder of topCard to 0, and shift all others' )
         for card in self.data:
            if card.location == deckName: 
               card.drawOrder = card.drawOrder + 1
         self.data[topCard].drawOrder = 0
         self.data[topCard].hide = True 
         (topCard,_) = self.deckTop ( deckName, True )
         self.data[topCard].hide = False 
      

   def deal (self, deckName, numCards, width, height, startX, startY): 
      numDealtCards = 0
      print ( 'Deal out ' + str(numCards) + ' cards to deck: ' + deckName )
      drawOrder = 0 # drawOrder starts at 0
      for i in range (numCards):   
         index = self.getRandomIndex (len(self.data))
         count = 0 
                  
         cardsLeft = self.length ('')          
         #print ( 'cardsLeft: ' + str(cardsLeft))         
         assert cardsLeft > 0, 'Number of dealt cards: ' + str(numDealtCards) + ' Ran out of cards trying to deal, the number of cards remaining in this deck is: ' + str(cardsLeft)
         
         while self.data[index].location != '':
            count = count + 1
            index = self.getRandomIndex (len(self.data))
               
         try: 
            card = self.data[index]
         except IndexError:
            print ( 'This index of out of range: ' + str(index) )
            exit(1)
            
         numDealtCards = numDealtCards + 1   
         self.setCardInfo ( index, startX, startY, width, height, deckName, False, drawOrder)
         drawOrder      = drawOrder + 1 # drawOrder starts at 0
    
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
      assert str(type(deckName)).find ('str') > -1, \
         'DrawDeck.deckTop (type(deckName)), should be str, instead we got: ' + str(type(deckName))
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
         print ( 'deck ' + str(deckName) + ' does not exist, but will be created' )
      #assert top != -1, 'Could not find a top card for deck: [' + deckName + '], does deck ' + deckName + ' exist?' 
      if debugIt: 
         print ( 'deckTop [name,top,drawOrder]: [' + deckName + ',' + str(top) + ',' + str(drawOrder) + ']' )
      return (top,drawOrder)
  
   # Draw a specific deck name
   def draw ( self, deckName ):
      debugIt = False 
      if debugIt: 
         print ( 'DrawDeck.draw ' + deckName + ' which has ' + str ( self.length (deckName)) + ' cards' )
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
 
   def drawLocations (self):
      debugIt = False 
      locations = self.getLocations() 
      for location in locations:
         self.draw ( location )
               
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
         
   def dropDragList (self,dragList,dropIndex,xOffset,yOffset):
      x = self.data[dropIndex].x + xOffset
      y = self.data[dropIndex].y + yOffset 
      drawOrder = self.data[dropIndex].drawOrder
      location = self.data[dropIndex].location 
      for item in dragList: 
         index = item[0]
         self.move (index,(x,y))
         x = x + xOffset
         y = y + yOffset    
         drawOrder = drawOrder + 1
         self.data[index].drawOrder = drawOrder 
         self.data[index].location = location 
                                 
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
         
   def confirmDrawOrder (self,deckName):
      drawOrder = 0
      for card in self.data:    
         if card.location == deckName: 
            self.findDrawCard (deckName,drawOrder) # this does an assert check 
            drawOrder = drawOrder + 1            
      print ( 'DrawOrder confirmed for ' + deckName)
    
   def findDrawCard (self, deckName, drawOrder,debugIt=True ): 
      index = -1
      found = -1
      if self.length(deckName) > 0:          
         for card in self.data:
            index = index + 1
            if card.location == deckName: 
               if card.drawOrder == drawOrder:
                  found = index 
                  break
                  
         if (found == -1) and debugIt: 
            self.showInfo (deckName)
            message = 'Could not find drawOrder ' + str(drawOrder) + ' for deck: ' + deckName + ' deck len: ' + str(self.len(deckName))
            print ( message ) 
            
            assert False, 'Could not find drawOrder ' + str(drawOrder) + ' for deck: ' + deckName 
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
 
   def flipTop (self,deckName):
      if self.numCards (deckName) > 0: 
         (topCard,_) = self.deckTop ( deckName,True)
         assert topCard > -1, 'Could not find topCard: ' + str(topCard) 
         self.data[topCard].hide = False 
      
   def getImage (self,card):
      if card.hide: 
         image = pygame.transform.scale(self.coverImage, (self.width, self.height))                                     
      else: 
         image = pygame.transform.scale(card.image, (self.width, self.height)) 
      card.width  = image.get_width()
      card.height = image.get_height()      
      return image 
      
   def getLocations (self):
      locations = [] 
      for card in self.data: 
         location = card.location 
         if location != '': 
            if not location in locations:
               locations.append ( location )
      return locations
 
   # Note: This procedure should be overwritten by the child class 
   def getName (self,index): 
      return 'DrawDeck.getName: overwrite needed for ' + str(index) 
      
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
      
   # Create a list of all cards in this column that are after draw order 
   def listAfter (self,index):    
      drawOrder = self.data[index].drawOrder 
      afterList = [(index,drawOrder)]
      location = self.data[index].location
      while True:
         drawOrder = drawOrder + 1
         index = self.findDrawCard (location, drawOrder,False) 
         if index == -1: 
            break
         else:
            afterList.append ((index,drawOrder)) 
      print ( 'DrawDeck.listAfter, len(afterList): ' + str(len(afterList)) ) 
      return afterList
   
   def listFacing (self,location):    
      facingList = [] 
      index = 0
      for card in self.data:
         if (card.location == location) and not card.hide:
            # print ('card [index,hide]: [' + str(index) + ',' + str(card.hide) + ']' )             
            facingList.append ((index,card.drawOrder))
         index = index + 1      
      return facingList

   # Return a list of indexes of cards with the same location and are visible
   def locationList (self,location, showVisible = False): 
      debugIt = False
      if debugIt: 
         print ( 'listLocation [location,showVisible] : [' + location + ',' + str(showVisible) + ']' )
      locList = [] 
      index = 0
      for card in self.data:
         if card.location == location: 
            if (showVisible == False) or (card.hide == False): 
               locList.append ((index,card.drawOrder))
         index = index + 1
      
      if debugIt:       
         print ( [ '[index,drawOrder]: [' + str(x[0]) + ',' + str(x[1]) + ']' for x in locList] )      
      return locList
           
   def move (self,index,pos): 
      # print ( 'move [index]: ' + str(index)) 
      self.data[index].x = pos[0]
      self.data[index].y = pos[1]  
      
   # Note side effect: Changing the drawOrder 
   # This procedure while take a list of indexes, sort them by drawOrder and place them on a location 
   # if drawOrder is not -1, it will start with that drawOrder and increment each by one 
   def moveList (self,indexList,pos,xOffset,yOffset,drawOrder=-1 ): 
      debugIt = False 
      if debugIt:
         print ( 'moveList, pos: (' + str(pos[0]) + ',' + str(pos[1]) + ']'  )
      x = pos[0]
      y = pos[1] 
      # Create a list with drawOrder: 
      sortedList = self.sortLocationList (indexList)
      
      for item in sortedList: 
         index = item[0]
         self.move (index,(x,y))
         x = x + xOffset
         y = y + yOffset    
         if drawOrder != -1: 
            self.data[index].drawOrder = drawOrder 
            drawOrder = drawOrder + 1
   
   def moveTo (self, deckName, index ):
      self.placeOnTop (deckName,index)
   
   def numCards (self, deckName): 
      count = 0
      for card in self.data:
         if card.location == deckName: 
            count = count + 1
      return count
        
   def placeOnTop (self,deckName,index, pos=(0,0)):
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
         
      if newDeck:
         print ( 'Use pos: ' + str(pos)) 
         self.data[index].x = pos[0]
         self.data[index].y = pos[1]
      else:      
         if hasattr ( self.data[index], 'x'):  
            self.data[index].x = self.data[top].x
            self.data[index].y = self.data[top].y + 20
            print ( 'x attribute detected, incrementing y to: '  + str(self.data[index].y) )
         else:
            print ( 'Setting  [x,y] := [100,100]?' )
            # x/y should be set by redeal function 
            self.data[index].x = 100
            self.data[index].y = 100
      
      (top,drawOrder) = self.deckTop (deckName)       
      print ( 'Done in placeOnTop, new top: ' + str (top) )
   
   def pos (self,index):
      return ( self.data[index].x, self.data[index].y )
   
   # set the x/y locations of cards
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

   # restore 1 card that was already saved 
   def restorePosition (self):
      index = self.save_position [0]
      if index != -1: 
         x = self.save_position [1]
         y = self.save_position [2]
         self.data[index].x = x
         self.data[index].y = y

   def savePosition (self, index): 
      self.save_position = (index, self.data[index].x, self.data[index].y)
    
   # Note drawOrder starts at 0    
   def setCardInfo ( self, index, x,y,width,height,location,hide,drawOrder): 
      self.data[index].x = x
      self.data[index].y = y
      self.data[index].width = width
      self.data[index].height = height
      self.data[index].location = location
      self.data[index].hide = hide
      self.data[index].drawOrder = drawOrder 
   
   def showInfo ( self, deckName='*'): 
      print ( self.cardInfo ( deckName ) )
      print ( 'DrawDeck.showInfo, [deckName,len(self.data)]: [' + deckName + ',' + str(len(self.data)) + ']' )
      index = -1
      for card in self.data:
         index = index + 1
         if (card.location == deckName) or (deckName == '*'):
            print ( card.location + '.card (' + str(index) + '): [name,drawOrder], [' + self.getName(index) + ',' + \
            str(card.drawOrder) + ']')
            
   # Sort the list by drawOrder 
   def sortLocationList (self,locList):
      l = sorted (locList, key=lambda obj:obj[1])
      #print ( 'sortLocationList sort by drawOrder: ' )
      #print ( [ '[index,drawOrder]: [' + str(x[0]) + ',' + str(x[1]) + ']' for x in l] )            
      return l
      
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
                                   