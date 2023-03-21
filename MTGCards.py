import pygame
from SubDeck      import SubDeck
from MTGNames     import MTGNames
from Utilities    import Utilities
from SelectButton import SelectButton 
from ViewImage    import ViewImage 
from StatusBar    import StatusBar

'''
   MTGCards is based on SubDeck but customized to an MTG deck   
   Wherever SubDeck is used, MTGCards can be used instead.  
'''
class MTGCards (SubDeck):  
   
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
      
      
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis=None, numCards=0, width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[] ):
      self.mtgNames = MTGNames()
      print ( 'UnoCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier, cards=cards)
      print ('UnoCards, total number of cards: ' + str(self.numImages)) 
      
      
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      
              
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def tap (self,deckIndex,userInfo): 
      name = self.mtgNames.names[index]
      if (name == 'cliffsOfInsanity.jpg') or True: 
         buttons = ['Red', 'White']
         selection = SelectButton ('   Choose   ').go(100,50,'Please select mana color', buttons)
         if (selection == 'Red') or (selection == 'White'):
            print ( 'You selected the color: ' + selection )         
            # userInfo.mana.white = userInfo.mana.white + 1
            self.data[index].tapped = True
         
    
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
   
   deck        = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)      
   hand        = MTGCards (deck,  7, startXY=(100,400), displaySurface=displaySurface)   
   discardPile = MTGCards (deck,  1, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
   drawPile    = MTGCards (deck, 44, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
   drawPile.hideAll () 
      
   cards=[]
   cards.append (hand)
   cards.append (drawPile)   
   cards.append (discardPile)
   decks = SubDecks (cards)    
   
   TextBox('Opponent', x=100, y=  5).draw()
   TextBox('Discard',  x=100, y=175).draw()
   TextBox('Draw',     x=310, y=175).draw()
   TextBox('Hand',     x=100, y=375).draw() 
   window = pygame.display.get_surface()
   
   quit = False
   dragCard = None   
   bar = StatusBar ()
   
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      decks.draw() # Show and set their x/y locations
      bar.show (['Quit', 'Message'] )
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'move':
            if not dragCard is None:
               x = data[0]
               y = data[1]
               print ( 'Moving...' + str(dragCard) + ' to [' + str(x) + ',' + str(y) + ']')
               hand.move (dragCard,data)
                  
         elif typeInput == 'drag':
            bar.update (data) 
            if bar.selection != '':
               if bar.selection == 'Quit': 
                  quit = True
                  bar.consumeSelection()
            else: 
               if dragCard is None:
                  dragCard = hand.findSprite (data) 
                  print ( 'dragCard: ' + str(dragCard) ) 
                  if not dragCard is None:
                     sheetIndex = hand.data[dragCard].sheetIndex
                     hand.data[dragCard].drag = True 
                     print ( '\n\n***DRAG*** ' + hand.cardName(sheetIndex) + '\n\n' )
         elif typeInput == 'drop':
            (deck,index) = decks.findSprite (data) # Where are we dropping                                  
            if deck == discardPile: 
               dropSheetIndex = deck.data[index].sheetIndex
               if discardPile.canDrop ( sheetIndex, dropSheetIndex):                   
                  print ( 'Drop on discard Pile' ) 
               else:
                  print ( 'Illegal Uno drop' )
            else: 
               print ( 'Illegal drop yo' )
            dragCard = None
         elif typeInput == 'select': 
            # Determine which subdeck the card is in. 
            (deck,index) = decks.findSprite (data)
            print ( 'index: ' + str(index))             
            if index != -1: 
               x = deck.data[index].x
               y = deck.data[index].y
               sheetIndex = deck.data[index].sheetIndex
               if deck == hand: 
                  optionBox = OptionBox (['Play', 'Cast', 'View', 'Tap'], x, y)
               else:
                  optionBox = OptionBox (['View', 'Tap'], x, y)
                  
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True
                  print ( 'quit is now: ' + str(quit) )
                  break
               elif selection == 'Info':
                  print ( deck.getInfo (sheetIndex))
               elif selection == 'Tap': 
                  deck.tap(index,None)               
               elif selection == 'View':
                  name = deck.mtgNames.names[sheetIndex]
                  deck.view (sheetIndex, 'images/mtg/' + name)               
         else:
            print ( 'event: ' + typeInput)

