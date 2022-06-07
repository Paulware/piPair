import pygame
from SubDeck import SubDeck

'''
   PlayingCards is based on SubDeck but customized to the standard 52 card deck of French style playing cards.
   This contains 4 suits of 13 cards each.   
'''
class PlayingCards (SubDeck): 
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis=None, numCards=0, width=0, height=0, startXY=(0,0), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0 ):
      print ( 'PlayingCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier)
      print ('PlayingCards, total number of cards: ' + str(self.numImages)) 
      
   def cardName (self,index): 
      faces = ['ERR', 'Ace', 'Deuce', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King'] 
      return faces[self.face(index)] + ' of ' + self.suit(index) 
   
   def canDrop (self,topIndex, bottomIndex): 
      ok = False 

      topFace = self.face(topIndex)
      bottomFace = self.face(bottomIndex)
      if bottomFace == (topFace + 1):
         if self.redBlack(topIndex) != self.redBlack(bottomIndex):
            ok = True 
            print ( 'canDrop is ok...' )
         else:
            print ( 'Cannot execute a normal drop because colors are the same' )
      else:
         print ( 'Cannot execute a normal drop because top face (' + str(bottomFace) + ') != (' + str(topFace) + ') + 1)' ) 
      return ok
      
   def emptyColumn(self):
      return (self.length() == 0)
      
   def face (self,index):
      value = (index % 13) + 1 
      print ( 'face of index: ' + str(index) + ' : ' + str(value)) 
      return value

   def getGroup (self, index ):
      print ( 'Get deck group associated with card index: ' + str(index)) 
      group = []        
      startIndex = index
      # Find where the group starts 
      while True: 
        if startIndex == 0: 
           break
        print ( 'startIndex: ' + str(startIndex)) 
        if self.data[startIndex].hide == False: 
           startIndex = startIndex - 1 
        else:
           break            
      # Copy the entire group             
      while True: 
        if not self.data[startIndex].hide: 
           group.append (startIndex)
        startIndex = startIndex + 1
        if startIndex == self.length(): 
           break         
      print ( 'Got a group: ' + str(group))                  
      return group
                                  
   def info (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + self.suit(sheetIndex) + ',' + \
              'color: ' + self.redBlack(sheetIndex) + ', face: ' + str(self.face(sheetIndex)) )       
    
   def redBlack (self,index):
      s = self.suit (index)
      color = 'red'
      if (s == 'clubs') or (s == 'spades'): 
         color = 'black'
      return color
     
   def suit (self,index):
      suits = ['clubs','diamonds','hearts','spades']
      ind = int(index / 13) 
      value = suits[ind]
      return value
       
if __name__ == '__main__':
   from Deck import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   print ( 'Make deck' )
   deckBasis = Deck ('images/standardCardSprites.jpg', 13, 5, 52, 54) 
   print ( 'Deal' )
   startXY = (100,100)
   hand = PlayingCards (deckBasis,7,80,120,startXY,displaySurface)  
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

