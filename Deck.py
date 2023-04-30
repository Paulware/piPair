import random
import copy
from SpriteSheet import SpriteSheet

# import SubDeck is not required, but knowledge of Subdeck routines might be necessary

class Object(object):
    pass


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
class Deck (SpriteSheet): 
      
   def deal (self, numCards): 
      print ( 'Deck.deal ' + str(numCards) ) 
      hand = []
      print ( 'Deal out ' + str(numCards) + ' cards from the deck' )
      for i in range (numCards):
         # obj = type ('Object', (object,), {})
            
         index = self.getRandomIndex (len(self.data))
         try: 
            obj = self.data[index]
         except IndexError:
            print ( 'This index of out of range: ' + str(index) )
            exit(1)
         obj.tapped = False
         obj.x = 0
         obj.y = 0
         print ( str(i) + ') just dealt card with index: ' + str(obj.sheetIndex) + ' from random number: ' + str(index) ) 
         hand.append (obj) # TODO: Do I need a copy?
         self.data.pop (index)
            
      return hand
      

   def dealList (self, cards, x=0, y=0): 
      numCards = len(cards)
      print ( 'Deck.dealList ' + str(numCards) ) 
      print ( 'Deck.dealList: ' + str(cards)) 
      hand = []
      print ( 'Deal out ' + str(numCards) + ' cards from the deck' )
      count = 0 
      for ind in cards:
         obj = Object()

         try: 
            obj.x          = x
            obj.y          = y
            obj.sheetIndex = self.data[ind].sheetIndex
            obj.image      = self.data[ind].image 
            obj.hide       = False 
            # obj.unique = count
            obj.tapped     = False 
         except IndexError:
            print ( 'This index of out of range: ' + str(ind) )
            exit()
           
         count = count + 1
         print ( str(count) + ') just dealt card with index: ' + str(obj.sheetIndex)  ) 
         hand.append (obj)
         
      print ( 'show Cards: ' ) 
      count = 0 
      for card in hand:
         print ( 'card (' + str(count) +  ' [x,y,sheetIndex]: [' + str(card.x) + ',' + \
              str(card.y) + ',' + str(card.sheetIndex) +  ']' )
         count = count + 1              
        
      return hand
   

   # colors is a list of colors that cards must include 
   def limitDeck ( self, colors): 
      colors = []
      
      
   def getRandomIndex (self,listLength):         
      index = -1
      if listLength == 0: 
         print ( '***ERR Deck.getRandomIndex cannot get a random index of a list that is empty***' )
         exit(1)
      if listLength > 0:
         index = int ( random.random() * listLength)
      # print ( 'Got a random index: ' + str(index))
      return index
   
   # numImages is the number of images in the deck that is dealt to a player 
   def __init__ (self, filename, numColumns, numRows, numImages, coverIndex=None):
      if coverIndex is None: 
         raise Exception("ERR coverIndex not specified in deck creation")
         
      SpriteSheet.__init__ (self,filename,numColumns,numRows,numImages,coverIndex)
      print ( 'Done in Deck.init' ) 
     
if __name__ == '__main__':
   print ( '***Deck __main__' ) 
   import pygame
   import Utilities
   from OptionBox import OptionBox 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities.Utilities (displaySurface, BIGFONT)   
      
   deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52, 52)
   
   hand = deck.deal(2) 
   for card in hand: 
      print ( 'Got card: ' + str(card.sheetIndex)) 
  