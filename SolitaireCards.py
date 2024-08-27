import pygame
from PlayingCards import PlayingCards
'''
   SolitaireCards is based on Standard Playing Cards   
'''
class SolitaireCards (PlayingCards):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, displaySurface, startXY, xMultiplier=1.0, yMultiplier=0.0, coverIndex=None):   
      print ( 'SolitaireCards.init' )    
      PlayingCards.__init__ (self,60, 100, displaySurface,startXY,1.0,0.0)      
      print ( 'SolitaireCards, total number of cards: ' + str(self.numImages)) 
      self.deal ()
            
   def canDrop (self,bottomIndex,topIndex): 
      ok = False 
      
      name = deck.cardName (topIndex) 
      dropIndex = deck.findCard (data,ignoreCard=topIndex) # Where are we dropping 
      bottomColor = ''
      topColor = ''
      ok = False
      bottomLocation = deck.data[bottomIndex].location
      bottomSuit     = deck.suit (bottomIndex)
      topSuit        = deck.suit (topIndex)
      topFace        = deck.face (topIndex)
      bottomFace     = deck.face (bottomIndex)
      print ( '[bottomIndex, topIndex, bottomLocation,bottomSuit,topSuit,topFace,bottomFace]: [' + \
              str(bottomIndex) + ',' + str(topIndex) + ',' + bottomLocation + \
              ',' + str(bottomSuit) + ',' + str(topSuit) + ',' + str(topFace) + ',' + str(bottomFace) + ']' )
      if (bottomLocation == 'draw') and (bottomIndex > -1): 
         print ( 'No drop on location: draw' )
      else:
         if (bottomLocation.find ( 'ace') > -1) and (bottomSuit == topSuit) and (topFace == (bottomFace+1)): # Dropping on an Ace Column 
            ok = True  
            print ( 'Ok dropping on ace column ' )
         elif name.find ( 'Ace' ) > -1: 
            print ( 'Dropping an ace on:' + str(dropIndex) )
            if dropIndex == -1: # Not dropping ace on any card    
              ok = True         
              print ( 'Ok dropping an ace anywhere' )
         else:
            if (bottomIndex != -1) and (topIndex != -1): 
               bottomColor = self.getColor (bottomIndex)
               topColor    = self.getColor (topIndex)
               location = self.data[bottomIndex].location
               if bottomColor != topColor:
                  bottomFace = self.face (bottomIndex)
                  topFace    = self.face (topIndex)
                  if bottomFace == (topFace + 1): 
                     ok = True 
                  else:
                     print ( 'SolitaireCards.canDrop, no drop a [bottomFace,topFace]: [' + str(bottomFace) + ',' + str(topFace) + ']' )
               else: 
                  face1 = self.face (bottomIndex)
                  face2 = self.face (topIndex)                
                  print ( '[location,face1,face2]: [ ' + location + ',' + str(face1) + ',' + str(face2) + ']' )               
                  if (location.find ( 'Ace') > -1) and (face2 == (face1+1)): # We are dropping on an Ace column 
                     ok = True                                 
            else:
               print ( 'SolitaireCards.canDrop, no drop b [bottomColor,topColor]: [' + bottomColor + ',' + topColor + ']' )
      return ok 

   def deal (self): 
      y = 200
      
      self.setCardInfo (0,180,y,60,120,'column1',False,0) # index 0 = Ace of Clubs
      self.setCardInfo (2,260,y,60,120,'column2',True,0)
      self.setCardInfo (1,260,y,60,120,'column2',False,1)
      
      column = 3
      columns = 5
      for i in range(columns):
         columnName = 'column' + str(column)
         startX = (column*80) + 100         
         PlayingCards.deal ( self,columnName, column, 60, 120, startX, y )
         self.hideName ( columnName)
         (topCard,drawOrder) = self.deckTop (columnName)
         self.data[topCard].hide = False 
         column = column + 1
         
      PlayingCards.deal (self,'draw', 24, 60, 120, 300, 50) 
      PlayingCards.hideAll (self, 'draw')       
   
   def drawAll (self): 
      columns = 7
      y = 200
      for i in range(columns):
         deckName = 'column' + str(i+1)
         startX = (i*80) + 100         
         self.draw (deckName)

   def emptyColumn (self): 
      columns = ['column1', 'column2', 'column3', 'column4', 'column5', 'column6', 'column7']
      value = ''
      for column in columns:
         if self.length(column) == 0:
            value = column
            break
      return value
   
   def findX (self, location): 
      x = 0
      for card in self.data:
         if card.location == location: 
            x = card.x
            break
      return x            
      
   def findY (self, location): 
      y = -1
      for card in self.data:
         if card.location == location: 
            # find the minimum y
            if y == -1: 
               y = card.y
            elif card.y < y: 
               y = card.y
      print ( '[location,y]: [' + location + ',' + str(y) + ']' )
      if y == -1:
         y = 0 
      return y
   
   def placeOnTop ( self,deckName,index,pos=(0,0)): 
      (top,drawOrder) = self.deckTop (deckName)     
      PlayingCards.placeOnTop (self,deckName,index,pos)
      # Place new card 20 pixels down
      if (pos[0] == 0) and (pos[1] == 0): 
         y = self.data[top].y + 20
         (top,drawOrder) = self.deckTop (deckName)     
         self.data[top].y = y
      else: 
         print ( 'SolitaireCards.placeOnTop, pos was specified: ' + str(pos)) 
   def redeal (self):
      columns = 7
      y = 200
      for i in range(columns):
         deckName = 'column' + str(i+1)
         startX = (i*80) + 100         
         self.redealColumn ( self, deckName, startX, y, 0, 20 )
  
   # set the x location of cards
   # Maintain the draw order...Does redeal care? 
   def redealColumn (self, deckName ):
      xOffset = 0
      yOffset = 20
      
      x = self.findX (deckName)
      y = self.findY (deckName)
      
      print ( 'SolitaireCards.redealColumn [deckName,x,y,xOffset,yOffset]: [' + deckName + ',' + \
              str(x) + ',' + str(y) + ',' + str(xOffset) + ',' + str(yOffset) + ']' )
      debugIt = True
      drawOrder = 0 # drawOrder starts at 0
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
            if not drawCard.hide:
               y = y + yOffset
               print ( 'offset y for not hidden card' )               
            drawOrder = drawOrder + 1 # next drawOrder card
   
if __name__ == '__main__':
   from Deck      import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   from SubDecks  import SubDecks
   from TextBox   import TextBox
   from Labels    import Labels   
   import time  

   def draw(): 
      window.fill ((0,0,0))  
      deck.drawLocations()
      
      labels.draw  ()      
      pygame.display.update()   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   

   deck = SolitaireCards (displaySurface,(100,100),1.0,0.0,coverIndex=52)
   deck.showInfo ()
   
   print ( 'Done dealing ' )
   window = pygame.display.get_surface()
   
   labels = Labels()
   labels.addLabel ('Hand'    , 300, 175)     
   labels.addLabel ('Draw'    , 300, 25)

   quit = False   
   dragCard = None

   while not quit:
      draw()   
           
      events = utilities.readOne()
      
      for event in events:
         (typeInput,data,addr) = event       
          
         if typeInput == 'move':
            if not dragCard is None: 
               deck.moveList (afterList,data,0,35) 
          
         elif typeInput == 'drag':            
            if dragCard is None:
               dragCard = deck.findCard (data) 
               # print ( deck.cardInfo (dragCard) ) 
               if dragCard > -1: 
                  if deck.data[dragCard].hide: 
                     print ( 'Unhide a card in ' + deck.data[dragCard].location )
                     deck.data[dragCard].hide = False 
                     dragCard = None
                  else:
                     location = deck.data[dragCard].location
                     if location == 'draw': 
                        deck.data[dragCard].hide = False
                     sheetIndex = deck.data[dragCard].sheetIndex
                     deck.savePosition (dragCard)
                     print ( '\n\n***DRAG*** ' + deck.cardName(sheetIndex) + '\n\n' )                                 
                     print ( deck.cardInfo (dragCard) )
                     mouseOffset = (data[0]-deck.data[dragCard].x,data[1]-deck.data[dragCard].y)
                     print ( 'mouseOffset : ' + str(mouseOffset) ) 
                     dragList = deck.sortLocationList(deck.listFacing (location))
                     afterList =  deck.listAfter (dragCard)
            else:
               dragList = [] 
          
         elif (typeInput == 'drop') and not (dragCard is None):
            #TODO: There is an index which is like an array index for a deck
            #      And there is an index like a data[index].   Why do we need 
            #      a deck array index?   Should we get rid of this concept?
            name = deck.cardName (dragCard) 
            dropIndex = deck.findCard (data,ignoreCard=dragCard) # Where are we dropping 

            if deck.canDrop ( dropIndex, dragCard):
               sourceLocation = deck.data[dragCard].location           
               destinationLocation = deck.data[dropIndex].location
               if dropIndex == -1: 
                  print ( 'Drop an ace yo' )
                  x = data[0]
                  y = data[1]
                  deck.setCardInfo ( dragCard, x,y,60,120,'ace'+str(dragCard),False,0)
                  deck.flipTop ( sourceLocation)                
               else: 
                  print ( '***canDrop = ok, dropIndex: ' + str(dropIndex) ) 
                  print ( 'Drop ok from: ' + sourceLocation + ' length of afterList: ' + str(len(afterList)) )
                  deck.dropDragList ( afterList,dropIndex,0,25)
                  print ( 'finished dropDragList' )                   

                  deck.flipTop (sourceLocation)                  
                  print ( 'Confirm drawOrder on source and destination ' )
                  deck.confirmDrawOrder (sourceLocation)        # Check Source 
                  deck.confirmDrawOrder (destinationLocation )  # Check Destination 
                  print ( 'Draw order confirmed on [source,destination]: [' + sourceLocation + ',' + destinationLocation + ']' )
            else:
               if name.find ('King') > -1: 
                  emptyColumn = deck.emptyColumn()
                  if emptyColumn != '':
                     deck.setCardInfo ( dragCard, data[0], data[1], 60, 120, emptyColumn, False, 0)
                     deck.flipTop (sourceLocation)
                  else:
                     # restore Positions?
                     deck.restorePosition()
                     location = deck.data[dragCard].location 
                     allCards = deck.locationList (location, showVisible=True) 
                     pos = (deck.save_position[1],deck.save_position[2])
                     deck.moveList (allCards,pos,0,35) 
                     if location == 'draw':
                        (topCard,_) = deck.deckTop ( location,True)
                        if True: #if deck.data[topCard].hide: 
                           print ( 'Cycle a draw card' )
                           deck.cycleTop (location)                     
               else:
                  print ( '***can not drop ***' )
                  print ( 'emptyColumn: ' + deck.emptyColumn() )
                  # restore Positions?
                  pos = (deck.save_position[1],deck.save_position[2])
                  deck.moveList (afterList,pos,0,35) 
                  location = deck.data[dragCard].location
                  if deck.data[dragCard].hide: 
                     print ( 'Hide detected' )                  
                     #pos = (deck.save_position[1],deck.save_position[2])
                     #deck.moveList (afterList,pos,0,35) 
                  elif location == 'draw':
                     (topCard,_) = deck.deckTop ( location,True)
                     if True: #if deck.data[topCard].hide: 
                        print ( 'Cycle a draw card' )
                        deck.cycleTop (location)

            dragCard = None
                 
      
   
   