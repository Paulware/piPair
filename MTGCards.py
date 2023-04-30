import pygame
from SubDeck      import SubDeck
from Utilities    import Utilities
from SelectButton import SelectButton 
from ViewImage    import ViewImage 
from StatusBar    import StatusBar
from Labels       import Labels 
from images.mtg.CardInfo import CardInfo 

class MTGActions(): 

   def __init__(self,utilities, cardInfo):
      self.utilities = utilities
      self.cardInfo  = cardInfo
   
   def damageOpponent (self,amount):
      print ( 'Opponent takes ' + str(amount) + ' damage' )
   
   def execute (self,mana,card,inplay,opponent):
      print ( 'card. [filename]: [' + card.filename + ']' ) 
      if card.filename == 'lands/pitOfDespair.jpg': 
         if (mana['red'] > 0) and (mana['green']  > 0):          
            optionBox = self.selectOption (['Tap For Red', 'Tap For Green', 'Force fight between 2 creatures (cost R/W)', 'Cancel'])                  
         else:
            optionBox = self.selectOption (['Tap For Red', 'Tap For Green', 'Cancel'])                  
         
         selection = optionBox.getSelection()
         if selection == 'Tap For Red': 
            mana['red'] = mana['red'] + 1
            card.tapped = True 
         elif selection == 'Tap For Green': 
            mana['green'] = mana['green'] + 1
            card.tapped = True 
         elif selection == 'Force fight between 2 creatures (cost R/W)':             
            if self.fight(inplay,opponent,mana):
               print ( 'Reduce mana by 1 red, 1 green' )
               mana['red'] = mana['red'] - 1
               mana['green'] = mana ['green'] - 1
               card.tapped = True 
            else:
               print ( 'Fight aborted' )
         elif selection == 'Cancel': 
            print ( 'Never mind') 
      else:
         print ( 'Did not find an action for: ' + filename )
         
   def fight (self,inplay,opponent,mana): 
      success = False 
      friendly = self.selectCreature(inplay)
      if friendly != -1: 
         enemy    = self.selectCreature(opponent)
         if enemy != -1:  
            print ( 'Assign damage between those creatures' )
            success = True 
         else:
            print ( 'Enemy creature aborted' )
      else:
         print ( 'Friendly creature aborted' )
      return success
      
   def selectCreature (self, deck):
      index = -1   
      ind = -1       
      self.utilities.showStatus ('Select a creature in deck: ' + deck.name)
      escape = False 
      while (ind == -1) and not escape:   
         events = utilities.readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'escape': 
               escape = True 
            elif typeInput == 'drag': 
               # Determine which subdeck the card is in. 
               ind = deck.findSprite (data)
               if ind != -1: 
                  id = deck.data[ind].sheetIndex
                  if self.cardInfo.isCreature(id): 
                     card = deck.data[ind]            
                     print ( '[deck,index]: [' + deck.name + ',' + str(ind) + ']')               
                     index = ind
                  else:
                     self.utilities.showStatus ( 'That card is not a creature aborting... ' + deck.name )
                  break
                     
      if index == -1:
         print ( 'No creature selected' )
      else:
         print ( 'Selected creature with index: ' + str(index)) 
         print ( '  Selected creature named: ' + deck.data[index].filename )
      return index 
      
   def selectOption ( self, options): 
      x = 600
      y = 100 
      optionBox = OptionBox (options, x,y, width=300)                  
      return optionBox 
'''
   MTGCards is based on SubDeck but customized to an MTG deck   
   Wherever SubDeck is used, MTGCards can be used instead.  
'''
class MTGCards (SubDeck):  

   def cardName (self, sheetIndex):
      name = drawPile.cardInfo.idToName (sheetIndex)
      print ( 'cardName returning: [' + name + ']' )
      return name
      
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[], empty=False, \
                 name='', utils=None):
      data = []
      numCards = 0
      self.cardInfo = CardInfo()
      self.utilities = utils
      self.action  = MTGActions(self.utilities, self.cardInfo)
      
      if str(filename).isnumeric():  
         print ( 'ERR MTGCards, filename has been passed as a number: ' + str(filename) ) 
         exit ()
      elif filename != '': 
         print ( 'open [filename]: [' + str(filename) + ']' )
         f = open ( filename, 'r' )
         line = f.readline()
         f.close 
         data = line.split ( ',' )
         numCards = len(data)
         print ( 'Got ' + str(numCards) + ' of cards read' )         
         
      cards = [] 
      for d in data: 
         cards.append ( int(d)) 
         
      print ( 'MTGCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier, cards=cards, empty=empty, name=name)
                        
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__') 
    
    
      
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      
              
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
    
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
   drawPile     = MTGCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, \
                  yMultiplier=0.0, name='drawPile')   
   drawPile.hideAll()
   opponent     = MTGCards (deck, empty=True, startXY=(100, 30), xMultiplier=1.0, yMultiplier=0.0, \
                             displaySurface=displaySurface, name='opponent')
   hand         = MTGCards (deck, empty=True, startXY=(100,600), xMultiplier=1.0, yMultiplier=0.0, displaySurface=displaySurface, name='hand')
   inplay       = MTGCards (deck, empty=True, startXY=(100,400), displaySurface=displaySurface, \
                   xMultiplier=1.0, yMultiplier=0.0, name='inplay', utils=utilities)   
   discardPile  = MTGCards (deck, empty=True, startXY=(100,200), displaySurface=displaySurface, xMultiplier=0.0, yMultiplier=0.0, name='discardPile')
   for i in range (5):
      drawPile.topToDeck (hand, reveal=True)
    
   hand.showAll() 
   hand.redeal(True)    
   hand.draw(True)
   
   cards=[]
   cards.append (drawPile)   
   cards.append (discardPile)
   cards.append (hand)
   cards.append (inplay)
   cards.append (opponent)
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
               hand.redeal() 
               deck.remove (index)                     
            else: 
               if dragCard is None:
                  dragCard = hand.findSprite (data) 
                  print ( 'dragCard: ' + str(dragCard) ) 
                  if dragCard > -1:
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
            card = deck.data[index]
            
            print ( '[deck,index]: [' + deck.name + ',' + str(index) + ']')             
            if index != -1: 
               x = deck.data[index].x
               y = deck.data[index].y
               sheetIndex = deck.data[index].sheetIndex
               name = deck.cardInfo.idToName (sheetIndex)            
               deck.data[index].filename = name # Set the filename of the card                
               card = deck.data[index]
               
               optionBox = OptionBox ( ['Unknown'] )
               if deck == hand: 
                  optionBox = hand.action.selectOption (['View', 'Cast'])
               elif deck == inplay: 
                  if card.tapped: 
                     optionBox = hand.action.selectOption (['View', 'Untap'])
                  else:
                     optionBox = hand.action.selectOption (['View', 'Tap'])
               elif deck == drawPile:
                  optionBox = hand.action.selectOption  ( ['Draw'])
                  
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'Cancel': 
                  quit = True
                  print ( 'quit is now: ' + str(quit) )
               elif selection == 'Cast': 
                  hand.data[index].tapped = True 
                  inplay.addCard (hand, index)
                  inplay.redeal()
                  hand.remove (index) 
                  hand.redeal()                                  
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  utilities.showStatus ( 'Card is untapped' )
               elif selection == 'Tap':
                  name = drawPile.cardInfo.idToName (sheetIndex)
                  mana = {'red':1, 'green':2}
                  print ( 'Mana before execution: ' + str(mana) ) 
                  inplay.action.execute (mana,card,inplay,opponent)               
                  print ( 'Mana is now: ' + str(mana) ) 
         else:
            print ( 'event: ' + typeInput)