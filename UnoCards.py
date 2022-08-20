import pygame
from SubDeck import SubDeck

'''
   PlayingCards is based on SubDeck but customized to the standard 52 card deck of French style playing cards.
   This contains 4 suits of 13 cards each.   
'''
class UnoCards (SubDeck):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis=None, numCards=0, width=80, height=120, startXY=(0,0), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0 ):
      print ( 'UnoCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier)
      print ('UnoCards, total number of cards: ' + str(self.numImages)) 
      
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def isNumber (self,index): 
      isNum = False
      if index < 39: 
         if (index % 10) != 9: 
            isNum = True 
      return isNum

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
      return color
      

   def getNumber (self,index): 
      value = 0
      if self.isNumber (index): 
         value = (index % 10) + 1
      return value      
     
   def cardName (self,index): 
      name = 'unknown' + str(index)
      if self.isNumber (index):
         name = self.getColor (index) + ' ' + str(self.getNumber(index))       
      elif (index == 9) or (index == 19):
         name = 'Joker'
      elif (index == 29) or (index == 39):
         name = 'Joker+4'
      elif (index >= 40) and (index <= 43): 
         name = self.getColor(index) + '0'
      elif (index >= 44) and (index <= 47):
         name = self.getColor(index) + '+2'
      elif (index >= 48) and (index <= 51):
         name = self.getColor(index) + 'reverse'
               
      return name 
   
   def canDrop (self,topIndex,bottomIndex): 
      ok = False 
      topFace = self.face(topIndex)
      bottomFace = self.face(bottomIndex)
      if (self.getColor (topFace) == self.getColor(bottomFace)) or \
         (self.getNumber(topFace) == self.getNumber(bottomFace)) or \
         (self.getName(topFace).find ( 'Joker') > -1):
            ok = True
            print ( 'canDrop is ok...' )
      return ok
      
   def emptyColumn(self):
      return (self.length() == 0)

   def getInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      
    
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
   hand = UnoCards (deckBasis,7,startXY=(100,400),displaySurface=displaySurface)  
   print ( 'Done dealing ' )
   window = pygame.display.get_surface()
   
   quit = False
   while not quit:
      window.fill ((0,0,0))
      hand.showSprites() # Show and set their x/y locations
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'select':      
            index = hand.findSprite (data)  
            if index != -1: 
               x = hand.data[index].x
               y = hand.data[index].y
               sheetIndex = hand.data[index].sheetIndex
               optionBox = OptionBox (['Play', 'Cancel','Info'], x, y)
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True
                  print ( 'quit is now: ' + str(quit) )
                  break
               elif selection == 'Info':
                  print ( hand.getInfo (sheetIndex)) 
               #elif selection == 'Play':
               #   discardPile.addCard (hand,index)
               #   hand.data[index].deleted = True 
               #   # hand.discard (index) 
               #   hand.addCard (drawPile, drawPile.topCard())

               window.fill ((0,0,0))

