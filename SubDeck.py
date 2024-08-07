import pygame
import copy
from ViewImage import ViewImage
from TextBox import TextBox

# For self.shuffle function 
import random
import datetime 

class Object(object):
    pass

'''
   SubDeck is like a hand or a discard pile 
   It will use Decks ability to deal and will add the attributes x,y,width,height to each element in the dealt hand.
   There is no descriptive name on each element, that will be added based on id in the particular game class.   
'''

# SubDeck cannot be inherited from Deck because it is not a complete Deck, just part of one,  
# and focuses primarily on display capability
class SubDeck (): 

   # data is a list of objects that have an image and index attribute
   #    xMultiplier dictates how far apart each card will be in the horizontal (x) axis
   #    yMultiplier dictates how far apart each card will be in the vertical (y) axis
   #    Note: counter should not be found here because that is specific to MTG Cards  
   def __init__ (self, deckBasis=None, numCards=0, width=80, height=120, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[], empty=False , name = ''):                    
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
      print ( 'Setting name : ' + name )
      self.name           = name 
      if deckBasis is None: 
         self.coverImage = None
      else:
         self.coverImage = deckBasis.coverImage
      if self.coverImage is None: 
         print ( 'SubDeck has a None cover image' )
      
      self.data = [] 
      if (deckBasis is None) or empty:
         print ( 'SubDeck.init an empty deck' )      
      else:
         print ( 'Deal cards' )
         self.deck = deckBasis
         if not (deckBasis is None): 
            if len(cards) > 0:
               dealtCards = self.deck.dealList (cards, self.startX, self.startY) 
               numCards = len(cards)
            else:             
               if numCards == 0: # Deal all remaining cards 
                  numCards = self.deck.length()  
                                 
               dealtCards = self.deck.deal (numCards, self.startX, self.startY)                
            self.data = dealtCards

      self.coverIndex = deckBasis.coverIndex                      
      # print ( 'Self.data for ' + self.name + ' is : ' + str(self.data))    
      self.numImages = len(self.data)         
      print (self.name + ' has ' + str(self.numImages) + ' cards ') 
   
   def addCard (self,sourceDeck,index): 
      ind = self.addCardToDeck (sourceDeck.data[index])    
      return self.sourceDeck.data[ind]
   
   def addCardToDeck (self,card):    
      index                       = self.createCard()
      print ( 'addCardToDeck got an index of : ' + str(index)) 
      self.data[index].x          = card.x
      self.data[index].y          = card.y
      self.data[index].image      = card.image
      self.data[index].hide       = card.hide
      self.data[index].name       = card.name
      self.data[index].sheetIndex = card.sheetIndex 
      print ( 'addCardToDeck returning an index of : ' + str(index)) 
      return index   
   
   def addCoverCard (self, labelText, name='cover.jpg'): 
      ind = len(self.data)-1         
      if len(self.data) == 0: 
         x = 0
      else:
         obj.x = self.data[ind].x + self.width
      y = self.data[ind].y
      
      obj = self.copyCard (x,y,name,self.coverIndex,self.data[ind].image,False) 
      
      self.data.append (obj)  
      return obj 
   
   # add a card from the specified deck.data[index] to the top card of this deck       
   def addTopCard (self,deck,index):
      index = self.addCardToDeck ( deck[index].data )   
      

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

   def createCard (self): 
      obj = Object () 
      self.data.append (obj)
      index = len(self.data) - 1
      print ( 'createCard returning an index of: ' + str(index)) 
      return index    
                         
   # shift cards and place top card at the bottom of the deck    
   def cycleTopCard (self):
      print ( 'cycle top card, length of deck: ' + str(len(self.data)))
      if len(self.data) > 1: 
         topCard = self.data[len(self.data)-1]
         for i in range (len(self.data)-1): 
            # print ( 'self.data['  + str(i+1) + ' = self.data[' + str(i) + ']' )
            self.data[len(self.data)-i-1] = self.data[len(self.data)-i-2]
         self.data[0] = topCard
                               
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
      for card in self.data:
         count = count + 1
         image = self.getImage (card)
         if self.showLength and (count == 8): 
            print ( '[x,y] of card 8 [: ' + str(card.x) + ',' + str(card.y) + ']' ) 
         if debugIt: 
            print ( 'card (' + str(count) + ').[x,y,sheetIndex: [' + str(card.x) + ',' + str(card.y) + ',' + \
                    str (card.sheetIndex) + ']'  ) 
         self.displaySurface.blit (image, (card.x,card.y)) 
         if hasattr(card,"label"): 
            card.label.draw()
            
   def drawCard (self): 
      cards = self.deck.deal (1)
      self.data.append (cards[0]) 
         
   def findCard (self,name): 
      found = -1
      count = 0
      for card in self.data: 
         if card.name == name: 
            found = count
         count = count + 1
      if found == -1: 
         print ( 'SubDeck.findCard, could not find card: ' + name + ' in ' + self.name ) 
      else:
         print ( 'SubDeck.findCard, found card at: ' + str(found)) 
      return found
      
   #TODO: Why does favorLast not work?   
   def findSprite (self,pos,debugIt=False,favorLast=False): 
      found = -1
      if pos is None: 
         raise Exception ( 'ERR...SubDeck.findSprite, pos is None' )
      if len(pos) != 2: 
         raise Exception ( 'ERR...SubDeck.findSprite, pos is not correct [' + str(pos) + ']') 
      else:
         x = pos[0]
         y = pos[1]
         index = -1 
         if debugIt: 
            print ( 'findSprite (' + str(x) + ',' + str(y) + '), len(self.data): ' + str(len(self.data)) + \
                    ' sprite [x,y,width,height]: [' + str(self.data[0].x) + ',' + str(self.data[0].y) + \
                    ',' + str(self.data[0].width) + ',' + str(self.data[0].height) + ']' ) 
         for card in self.data: 
            width  = card.width
            height = card.height
            rect = pygame.Rect (card.x, card.y, width,height)               
            if debugIt:
               print ( 'rect: ' + str(rect)) 
            index = index + 1
            if rect.collidepoint (pos): 
               print ( 'rect.collidepoint(pos): ' + str(rect) + '.collidepoint(' + str(pos) + ')' )                
               print ( 'Found sprite at index: ' + str(index) + ' pos: ' + str(pos) + ' rect: ' + str(rect))
               self.showInfo()
               found = index 
               if not favorLast: # We will take the first match  
                  break
         if found > -1: 
            print ( self.name + '.findSprite found: ' + str(found) ) 
         return found 
      
   def getImage (self,sprite):
      if sprite.hide: 
         image = pygame.transform.scale(self.coverImage, (self.width, self.height))                                     
      else: 
         image = pygame.transform.scale(sprite.image, (self.width, self.height)) 
      sprite.width  = image.get_width()
      sprite.height = image.get_height()      
      return image 
      
   def getRandomIndex (self):
      listLength = len (self.data)    
      index = -1
      if listLength == 0: 
         print ( '***ERR SubDeck.getRandomIndex cannot get a random index of a list that is empty***' )
         exit(1)
      if listLength > 0:
         index = int ( random.random() * listLength)
      return index         
               
   def hide (self,index):
      self.data[index].hide = True 
      
   def hideAll (self):
      print ( 'hide ALL cards ' )
      for card in self.data:
         card.hide = True 
      print ( 'Done hiding all cards ' )
      
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

   # set the x location of cards
   def redeal (self, debugIt=False):  
      yOffset = self.yMultiplier * self.height  
      x = self.startX
      y = self.startY           
      print ( 'len(self.data): ' + str(len(self.data)) )
      cnt = 0    
      for card in self.data: # Set the width/height of each image 
         ind = cnt
         if debugIt:
            print ( 'self.data[' + str(ind) + '].x = ' + str(x) ) 
            print ( 'self.data[' + str(ind) + '].y = ' + str(y) )          
         
         self.data[ind].x = x
         self.data[ind].y = y
         card.x = x
         card.y = y 
         xOffset = self.width * self.xMultiplier
         c = self.data[ind]
         if debugIt: 
            print ( 'card (' + str(ind) + ') redeal [width,height,xMultipler, xOffset,x,y,sheetIndex]: [' + \
                    str(self.width) + ',' + str(self.height) + ',' + str(self.xMultiplier) + ',' + str(xOffset) + ',' + \
                    str(c.x) + ',' + str(c.y) + ',' + str(c.sheetIndex) + ']' )
         x = x + xOffset
         y = y + yOffset    
         cnt = cnt + 1

      self.nextX = x
      self.nextY = y

      print ( '\nSubDeck, ***Show deck after redeal' )       
      self.showInfo()
       
   def remove (self,i,redealCards=False): 
      print ( 'SubDeck (' + self.name + ').remove index: ' + str(i) )
      debugIt = False 
      if debugIt:
         print ( '*** SubDeck.remove (' + self.name + '), data before pop' )
         self.showData()
      if i == -1:
         raise Exception ( 'SubDeck.remove, index == -1' )
      self.data.pop (i)
      if debugIt: 
         print ( '***SubDeck.remove (' + self.name + ') data after pop' )
         self.showData()
         
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
     
   def retrieveCard (self,index):
      if index is None: 
         raise Exception ( 'ERR you cannot retrieve a card with index = [None]' )
      if index > (len(self.data)-1): 
         raise Exception ( 'Err...Retrieving non-existent data...[index,len(self.data)]: [' + \
                           str(index) + ',' + str(len(self.data)) + ']' )
      elif index < 0: 
         raise Exception ( 'Err...Cannot retrieve data element : ' + str(index)) 
      else:
         return self.data[index]
     
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
         
   def showCard (self, i, card):       
      print ( str(i) + ') [name,x,y]: [' + card.name + ',' + str(card.x) + ',' + str(card.y) + ']')
      
   def showData (self): 
      self.showInfo()
         
   def showInfo (self):
      length = len(self.data)
      print ( 'There are ' + str(length) + ' cards in : ' + self.name )
      i = 0
      for card in self.data: 
         self.showCard (i,card)
         i = i + 1
         
   def shuffle (self): 
      random.seed (datetime.datetime.now().timestamp())   
      for card in self.data: 
         index1 = self.getRandomIndex()
         index2 = self.getRandomIndex()
         
         d = self.data[index1]
         self.data[index1] = self.data[index2]
         self.data[index2] = d         
   
   '''   
   def shuffleTo (self, destinationDeck): 
      while self.length() > 0: 
         self.topToDeck (destinationDeck, False)
   '''
   
   def topSheetIndex (self): 
      print ( 'SubDeck.topIndex, return sheetIndex' )
      return self.data[self.length()-1].sheetIndex
    
   '''    
   def topToDeck (self,destinationDeck,reveal=False): 
      index = self.length()-1     
      self.moveToDeck (destinationDeck,index)
      if reveal: 
         destinationDeck.revealTopCard()
      exit1() 
   '''
   
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
         
    

