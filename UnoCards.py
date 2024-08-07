import pygame
from DrawDeck import DrawDeck
'''
   UnoCards is based on DrawDeck but customized to the standard uno deck   
'''
class UnoCards (DrawDeck):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, numColumns, numRows, numImages, width, height, displaySurface, startXY, \
                 xMultiplier=1.0, yMultiplier=0.0, coverIndex=None):
      print ( 'UnoCards.init' )
      DrawDeck.__init__ (self,'images/unoSpriteSheet.jpg', 10, 6, 52, 60,100,displaySurface,startXY,1.0,0.0,coverIndex=52)
      
      print ('UnoCards, total number of cards: ' + str(self.numImages)) 
      
      index = 0
      # Add attributes that are specific to UNO cards 
      for card in self.data:            
         card.name = self.cardName (card.sheetIndex)
         print ( 'Assigned name of: ' + card.name + ' to sheetIndex: ' + str(card.sheetIndex)) 
         index     = index + 1
      
   def canDrop (self,topIndex,bottomIndex): 
      ok = False 
      print ( 'canDrop [topIndex,name,bottomIndex,name]: [' + str(topIndex) + ',' + self.cardName(topIndex) + \
                        ',' + str(bottomIndex) + ',' + self.cardName(bottomIndex) + ']') 
      if (self.getColor (topIndex) == self.getColor(bottomIndex)) or \
         (self.getNumber(topIndex) == self.getNumber(bottomIndex)) or \
         (self.cardName(topIndex).find ( 'Joker') > -1) or \
         (self.cardName(bottomIndex).find ('Joker') > -1):
            ok = True
            print ( 'canDrop is ok...' )
      return ok
      
   def cardInfo (self,index): 
      card = self.data[index]
      return 'cardInfo for self.data[' + str(index) + '] [location, name, x, y, sheetIndex]: [' + card.location + \
             ',' + card.name + ',' + str(card.x) + ',' + str(card.y) + ',' + str(card.sheetIndex) + ']'
                         
   def cardName (self,sheetIndex): 
      name = 'unknown' + str(sheetIndex)
      if self.isNumber (sheetIndex):
         name = self.getColor (sheetIndex) + ' ' + str(self.getNumber(sheetIndex))       
      elif (sheetIndex == 9) or (sheetIndex == 19):
         name = 'Joker'
      elif (sheetIndex == 29) or (sheetIndex == 39):
         name = 'Joker+4'
      elif (sheetIndex >= 40) and (sheetIndex <= 43): 
         name = self.getColor(sheetIndex) + '0'
      elif (sheetIndex >= 44) and (sheetIndex <= 47):
         name = self.getColor(sheetIndex) + '+2'
      elif (sheetIndex >= 48) and (sheetIndex <= 51):
         name = self.getColor(sheetIndex) + 'reverse'
               
      return name 
   
   def getColor (self,index): 
      if (index == 9) or (index == 19) or (index == 29) or (index == 39):
         color = 'All'       
      elif (index < 10) or (index == 40) or (index == 44) or (index == 48):
         color = 'Red'
      elif (index < 20) or (index == 41) or (index == 45) or (index == 49):
         color = 'Orange'
      elif (index < 30) or (index == 42) or (index == 46) or (index == 50): 
         color = 'Blue'
      elif (index < 40) or (index == 43) or (index == 47) or (index == 51): 
         color = 'Green'        
      print ( 'getColor [color]: [' + color + ']' ) 
      return color
     
   def getInfo (self,index): 
      print ( self.cardInfo(index) ) 
           
   def getNumber (self,index): 
      value = 0
      if self.isNumber (index): 
         value = (index % 10) + 1
      print ( 'getNumber [number]: [' + str(value) + ']' )
      return value      
      

   def isNumber (self,index): 
      isNum = False
      if index < 39: 
         if (index % 10) != 9: 
            isNum = True 
      return isNum
      
   def length (self,deckName):
      count = 0 
      for card in self.data:
         if card.location == deckName:
            count = count + 1
      return count 
            
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      

   def showInfo (self, deckName):
      length = len(self.data)
      print ( 'There are ' + str(self.length(deckName)) + ' cards in : ' + deckName )
      i = 0
      for card in self.data: 
         if deckName == card.location:
            print ( str(i) + ') [name,x,y,sheetIndex,drawOrder]: [' + card.name + ',' + str(card.x) + ',' + str(card.y) + \
                             ',' + str(card.sheetIndex) + ',' + str(card.drawOrder) + ']')
            i = i + 1
     
if __name__ == '__main__':
   from Deck      import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   from SubDecks  import SubDecks
   from TextBox   import TextBox
   import time   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   

   deck = UnoCards (10, 6, 52, 60,100,displaySurface,(100,100),1.0,0.0,coverIndex=52)
   deck.deal   ( 'hand', 7, 60, 120, 100, 400,)
   deck.redeal ( 'hand', 100, 400, 60, 0)
   deck.deal   ( 'discard', 1, 60, 120, 100, 200)
   deck.redeal ( 'discard', 100, 200, 60, 0)
   deck.deal   ( 'draw', 43, 60, 120, 300, 200)

   mouseOffset = (0,0)      
   quit = False
   dragCard = None
   
   while not quit:   

      displaySurface.fill ((0,0,0)) 
      TextBox('Opponent', x=100, y=  5).draw()
      TextBox('Discard',  x=100, y=175).draw()
      TextBox('Draw',     x=310, y=175).draw()
      TextBox('Hand',     x=100, y=375).draw() 
      deck.draw('hand')
      deck.drawTop('discard')
      deck.drawTop('draw')
      
      pygame.display.update() 
   
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'move':
            if not dragCard is None:
               x = data[0] - mouseOffset[0]
               y = data[1] - mouseOffset[1]
               # print ( 'Moving...' + str(dragCard) + ' to [' + str(x) + ',' + str(y) + ']')
               deck.move (dragCard,(x,y))
               pygame.display.update()
                 
         elif typeInput == 'drag':
            if dragCard is None:
               dragCard = deck.findCard (data) 
               print ( deck.cardInfo (dragCard) ) 
               if dragCard > -1: 
                  sheetIndex = deck.data[dragCard].sheetIndex
                  # deck.data[dragCard].drag = True
                  startPos = (deck.data[dragCard].x,deck.data[dragCard].y)                  
                  print ( '\n\n***DRAG*** ' + deck.cardName(sheetIndex) + '\n\n' )                                 
                  mouseOffset = (data[0]-deck.data[dragCard].x,data[1]-deck.data[dragCard].y)
                  print ( 'mouseOffset : ' + str(mouseOffset) ) 
                  
         elif typeInput == 'drop':
            dropIndex = deck.findCard (data,dragCard) # Where are we dropping                                  
            if dropIndex == -1:
               print ( 'No drop target found' )
               deck.redeal ( 'hand', 100, 400, 60, 0)               
            else:               
               if deck.data[dropIndex].location == 'draw': 
                  print ( '***drop this card...' )
                  print (deck.cardInfo (dragCard) )                   
                  deck.placeOnTop ( 'hand', dragCard )
                  deck.redeal ('hand', 100, 400, 60, 0) 
               elif deck.data[dropIndex].location == 'discard': 
                  dropSheetIndex = deck.data[dropIndex].sheetIndex
                  if deck.canDrop ( sheetIndex, dropSheetIndex):  
                     deck.placeOnTop ('discard', dragCard )
                     deck.redeal ('discard', 100, 200, 0, 0) # Snap to 
                     print ( 'Drop on discard Pile' )
                     deck.drawTop ('discard', )  
                     deck.redeal ( 'hand', 100, 400, 60, 0)
                  else:                      
                     deck.data[dragCard].x = startPos[0]
                     deck.data[dragCard].y = startPos[1]                 
                     print ( 'Illegal Uno drop' )
               else: 
                  deck.data[dragCard].x = startPos[0]
                  deck.data[dragCard].y = startPos[1]                 
                  print ( 'Illegal drop to ' + deck.data[dropIndex].location )
                  deck.getInfo ( dropIndex)
                  
            dragCard = None
         elif typeInput == 'select':      
            index = deck.findCard (data)  
            if index > -1: 
               x = deck.data[index].x
               y = deck.data[index].y
               sheetIndex = deck.data[index].sheetIndex
               optionBox = OptionBox (['Play', 'Cancel','Info'], x, y)
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel':
                  quit = True
                  print ( 'quit is now: ' + str(quit) )
                  break
               elif selection == 'Info':
                  print ( 'Deck found: ' + deck.data[index].location)
                  deck.getInfo (index)
                  # deck.showInfo ( 'draw' )
               elif selection == 'Play':
                  deck.placeOnTop ( 'discard', index )
                  deck.redeal     ( 'discard', 100, 400, 60, 0)
                  deck.redeal     ( 'hand',    100, 400, 60, 0) 
               displaySurface.fill ((0,0,0))
         else:
            print ( 'event: ' + typeInput)

