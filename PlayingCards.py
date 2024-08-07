import pygame
from DrawDeck import DrawDeck

'''
   PlayingCards is based on DrawDeck but customized to the standard 52 card deck of French style playing cards.
   This contains 4 suits of 13 cards each.   
'''
class PlayingCards (DrawDeck): 
   #TODO: Pass in filename for bigger or different decks
   def __init__ (self, width=0, height=0, displaySurface=None, startXY=(0,0), xMultiplier=1.0, yMultiplier=0.0, coverIndex=54 ):
                 
      # print ( 'PlayingCards.init' )
      DrawDeck.__init__ (self,filename='images/standardCardSprites.jpg', numColumns=13, numRows=5, numImages=52,\
                         width=60,height=100, displaySurface=displaySurface,startXY=startXY,\
                         xMultiplier=xMultiplier,yMultiplier=yMultiplier,coverIndex=coverIndex)
                         
      print ('PlayingCards, total number of cards: ' + str(self.numImages)) 
      
   def cardInfo ( self, index):
      card = self.data[index]
      name = self.cardName (index)
      line = 'PlayingCards.cardInfo, [index,location,cardName]: [' + str(index) + ',' + card.location + ',' + name + ']'
      # print ( line )
      return line       
      
   def cardName (self,index):    
      assert str(type(index)).find ('tuple') == -1, 'PlayingCards.cardName (index) is a tuple'          
      faces = ['ERR', 'Ace', 'Deuce', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King'] 
      name = faces[self.face(index)] + ' of ' + self.suit(index)
      print ( 'cardName(' + str(index) + '): ' + name )
      return name 
   
   def deal1 (self): 
      (index,drawOrder) = deck.deckTop ('draw') 
      deck.moveTo ( 'hand', index ) 
  
   def deal (self, groupName, numCards, width, height, startX, startY ): 
      DrawDeck.deal ( self,groupName, numCards, width, height, startX, startY )      
      index = 0 
      # Add the name to each card
      for card in self.data: 
         if card.location == groupName:       
            card.name = self.cardName (index)
            print ( 'The name of card[' + str(index) + '] is: ' + card.name )
         index = index + 1
         
   def emptyColumn(self):
      return (self.length() == 0)
      
   def face (self,index):
      print ( 'type(index): ' + str(type(index)) ) 
      print ( 'index: ' + str (index))
      value = (index % 13) + 1 
      return value

   def getColor (self,index):
      suitName = self.suit (index)   
      color = 'red'
      if suitName in ['clubs','spades']:
         color = 'black'
      return color 
      
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
 
   def hide (self,index):
      self.data[index].hide = True 
      
   def hideAll (self,deckName):
      for card in self.data:
         if card.location == deckName: 
            card.hide = True 
      
   def info (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + self.suit(sheetIndex) + ',' + \
              'color: ' + self.redBlack(sheetIndex) + ', face: ' + str(self.face(sheetIndex)) )       

   def placeOnTop (self,deckName,index, pos=(0,0)):   
      # For each of the cards in the list, also move them to the top 
      allCards = self.locationList (self.data[index].location, showVisible=True) 
      print ( 'PlayingCards.placeOnTop, allCards: ' + str(allCards)) 
      for card in allCards: 
         index = card[0]
         print ( 'PlayingCards.py, placeOnTop, index: ' + str(index) ) 
         DrawDeck.placeOnTop (self,deckName,index, pos )         

   def redBlack (self,index):
      s = self.suit (index)
      color = 'red'
      if (s == 'clubs') or (s == 'spades'): 
         color = 'black'
      return color

   def showCard ( self, index ): 
      card = self.data[index]
      print ('[deckName,index,x,y,drawOrder,name]: [' + card.location + ',' + str(index) + ',' + \
             str(card.x) + ',' + str(card.y) + ',' + \
             str(card.drawOrder) + ',' + self.cardName(index) + ']' )
      
   def showInfo ( self, deckName='*' ): 
      (top,drawOrder) = self.deckTop (deckName,True)
      
      print ( 'PlayingCards.showInfo, Show this deck: ' + deckName )
      index = -1
      for card in self.data:
         index = index + 1
         if (card.location == deckName) or ((deckName=='*') and (card.location != '')):
            print ('[deckName,index,x,y,drawOrder,name,hide]: [' + card.location + ',' + str(index) + ',' + \
                   str(card.x) + ',' + str(card.y) + ',' + \
                   str(card.drawOrder) + ',' + self.cardName(index) + ',' + str(card.hide) + ']' )
          
   def suit (self,index):
      suits = ['clubs','diamonds','hearts','spades']
      ind = int(index / 13) 
      value = suits[ind]
      print ( 'suit of ' + str(index) + '=' + value )
      return value
      
   def tap (self,index):
      self.data[index].tapped = True      
       
if __name__ == '__main__':
   from Utilities import Utilities
   from OptionBox import OptionBox
   from Labels    import Labels
 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   print ( 'Make deck' )
   startXY = (100,100)
   deck = PlayingCards (60,100,displaySurface,startXY,1.0,0.0,52)
 
   print ( 'Deal' )
   
   deck.deal ( 'hand', 7, 60, 120, 100, 200 )
   deck.deal ( 'discard', 1, 60, 120, 100,50 )
   deck.deal ( 'draw', 52-8, 60, 120, 100, 5 )
   print ( 'Done dealing ' )
   window = pygame.display.get_surface()
   
   quit = False
   
   labels = Labels()
   labels.addLabel ('Discard' , 50,  70)
   labels.addLabel ('Hand'    , 50, 190)     
   labels.addLabel ('Draw'    , 50, 320)
   
   while not quit:
      window.fill ((0,0,0))  

      # Draw the decks 
      deck.redeal  ('discard', 200, 50,  0, 0)
      deck.draw    ('discard')
      deck.redeal  ('hand'   , 200, 170, 60, 0)
      deck.draw    ('hand') 
      deck.redeal  ('draw',    200, 300, 0, 0)
      deck.draw    ('draw') 
      labels.draw()
      
      pygame.display.update()
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event       
       
         # print ( 'Read something' )
         x = data[0]
         y = data[1]
         
         if typeInput == 'drag': 
            index = deck.findCard ((x,y))
            if index > -1: 
                optionBox = OptionBox (['Use', 'Discard', 'Show', 'Tap', 'Cancel', 'Hide', 'Show'], x, y)
                selection = optionBox.getSelection()
                print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
                if selection == 'Cancel': 
                   break
                elif selection == 'Discard':
                   deck.moveTo ( 'discard', index)
                elif selection == 'Show':
                   print ( 'What is the top card in the draw deck?' )
                   (index,drawOrder) = deck.deckTop ('draw')
                   print ( 'Name of card: ' + deck.cardName (index) ) 
                   deckName = deck.data[index].location                   
                   deck.showInfo (deckName)
                elif selection == 'Tap':  
                   deck.tap (index)                
                elif selection == 'Use':
                   (index,drawOrder) = deck.deckTop ('draw')
                   deck.moveTo ( 'hand', index )
                elif selection == 'Hide':
                   deck.hide(index)
                elif selection == 'Show':
                   deck.data[index].hide = False
         