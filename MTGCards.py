import pygame
from SubDeck      import SubDeck
from Utilities    import Utilities
from SelectButton import SelectButton 
from ViewImage    import ViewImage 
from StatusBar    import StatusBar
from Labels       import Labels 
from images.mtg.CardInfo import CardInfo 

'''
   MTGCards is based on SubDeck but customized to an MTG deck   
   Wherever SubDeck is used, MTGCards can be used instead.  
'''
class MTGCards (SubDeck):  

   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[], empty=False ):
      data = []
      numCards = 0
      self.cardInfo = CardInfo()
      
      if filename != '': 
         f = open ( filename, 'r' )
         line = f.readline()
         f.close 
         data = line.split ( ',' )
         numCards = len(data) 
         
      cards = [] 
      for d in data: 
         cards.append ( int(d)) 
         
      print ( 'MTGCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier, cards=cards, empty=empty)
                        
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__') 
      
      
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      
              
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def tap (self,deckIndex,userInfo):       
      name = self.cardInfo.idToName (deckIndex) 
      if (name == 'cliffsOfInsanity.jpg') or True: 
         buttons = ['Red', 'White']
         selection = SelectButton ('   Choose   ').go(100,50,'Please select mana color', buttons)
         if (selection == 'Red') or (selection == 'White'):
            print ( 'You selected the color: ' + selection )         
            # userInfo.mana.white = userInfo.mana.white + 1
            self.data[deckIndex].tapped = True
         
    
if __name__ == '__main__':
   from Deck      import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   from SubDecks  import SubDecks
   from TextBox   import TextBox
   from MTGSetup  import MTGSetup
   import time   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = MTGSetup(utilities).chooseDeckFilename('redDeck.txt')   
   drawPile     = MTGCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
   
   drawPile.hideAll()
   hand         = MTGCards (deck, 0, startXY=(100,600), displaySurface=displaySurface)
   
   for i in range (7):
      drawPile.topToDeck (hand, True)
   
   #inplay      = MTGCards (deck,  0, startXY=(100,400), displaySurface=displaySurface, empty=True)   
   discardPile = MTGCards (deck,  0, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0)
      
   cards=[]
   #cards.append (hand)
   cards.append (drawPile)   
   cards.append (discardPile)
   #cards.append (inplay)
   decks = SubDecks (cards)    
   
   window = pygame.display.get_surface()
   
   quit = False
   dragCard = None   
   bar = StatusBar ()
   
   labels = Labels()
   labels.addLabel ('Opponent', 100, 5)
   labels.addLabel ('Discard' , 100, 175)
   labels.addLabel ('Draw'    , 310, 175)
   labels.addLabel ('In Play' , 100, 375)
   labels.addLabel ('Hand'    , 100, 575)
   
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      labels.show ()
      pygame.time.Clock().tick(60)   
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
            (deck,index) = decks.findSprite (data) # Returns index in list             
            if bar.selection != '':
               if bar.selection == 'Quit': 
                  quit = True
                  bar.consumeSelection()
            elif deck == drawPile:
               deck.data[index].hide = False
               hand.addCard (deck,index)
               deck.remove (index)                     
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
                  print ( 'Illegal MTG drop' )
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
                  optionBox = OptionBox (['Cast', 'View'], x, y)
               elif deck == drawPile:
                  optionBox = OptionBox ( ['Draw'], x, y)
               else:
                  optionBox = OptionBox (['View', 'Tap'], x, y)
                  
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True
                  print ( 'quit is now: ' + str(quit) )
               elif selection == 'Cast': 
                  inplay.addCard (hand, index)
                  inplay.redeal()
                  hand.remove (index) 
                  hand.redeal()                                      
               elif selection == 'Tap': 
                  deck.tap(index,None)               
                  deck.redeal()
               elif selection == 'View':
                  name = drawPile.cardInfo.idToName (sheetIndex)
                  # name = deck.mtgNames.names[sheetIndex]
                  deck.view (sheetIndex, 'images/mtg/' + name)               
         else:
            print ( 'event: ' + typeInput)