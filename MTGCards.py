import pygame
from SubDeck      import SubDeck
from Utilities    import Utilities
from SelectButton import SelectButton 
from ViewImage    import ViewImage 
from StatusBar    import StatusBar
from Labels       import Labels 
from images.mtg.CardInfo import CardInfo 
from images.mtg.Counter  import Counter

class MTGPhases (): 
   def __init__ (self,inplay,hand): 
      self.phase = TextBox ('Upkeep', 500, 755)       
      self.manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0}
      self.inplay = inplay
      self.hand = hand
      
   def next(self):
      
      if self.phase.text == 'Upkeep':
         self.phase.text = 'Draw'
      elif self.phase.text == 'Draw':
         self.phase.text = 'Cast'
      elif self.phase.text == 'Cast':
         self.phase.text = 'Attack'
      elif self.phase.text == 'Attack':
         self.phase.text = 'Assign Damage'
      elif self.phase.text == 'Assign Damage':
         self.phase.text = 'End Turn'
         while self.hand.length() > 7: 
            ind = self.hand.action.selectCardToDiscard(self.hand)
            print ( 'delete card [' + str(ind) + '] from hand' )
            self.hand.discard (ind) 
            self.hand.redeal()
      elif self.phase.text == 'End Turn':
         self.phase.text = 'Upkeep'
         print ( 'Handle those Upkeep items...' ) 
         for card in self.inplay.data: 
            name = self.inplay.getName (card) 
            print ( 'Upkeep, card in play: ' + name )
            if name == 'enchantments/redRibbonArmy.png': 
               print ( 'Place a red ribbon army token in play' )
            
      print ( 'new phase.text: [' + self.phase.text + ']' )
   
   def text(self):
      return self.phase.text
      
   def draw(self):
      self.phase.draw()
      
class MTGAction ():
   def __init__(self,card,cardInfo): 
      self.card = card 
      self.name = cardInfo.idToName (card.sheetIndex)  
      print ( "Action created for : " + self.name )      
   def executePhase (self,phase):
      if phase == "Upkeep": 
         if self.name == 'enchantments/redRibbonArmy.png':
            print ( 'Increment counter for redRibbonArmy' )
            card.counter.increment()
   
class MTGActions(): 
   def __init__(self,utilities, cardInfo):
      self.utilities = utilities
      self.cardInfo  = cardInfo
   
   def damageOpponent (self,amount):
      print ( 'Opponent takes ' + str(amount) + ' damage' )
   
   def tap (self,mana,card,inplay,opponent):
      print ( 'tap: card. [filename]: [' + card.filename + ']' ) 
      if card.filename == 'lands/pitOfDespair.jpg': 
         if (mana['red'] > 0) and (mana['green']  > 0) and (inplay.countType ('creatures') > 0):          
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
         card.tapped = True 
         
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
      
   def selectCardToDiscard (self, deck):
      index = -1   
      ind = -1       
      deck.utilities.showStatus ('Select a card from your hand to discard: ')
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
                  index = ind 
                  break
                     
      if index == -1:
         print ( 'No card selected' )
      else:
         print ( 'Selected card with index: ' + str(index)) 
         print ( '  Selected card with name : ' + deck.data[index].name )
      deck.utilities.clearStatus()
      return index 
      
      
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

class HealthBar(): 
   def __init__ (self): 
      self.health = 20
      self.bar = TextBox ('Health:' + str(self.health), 250, 5)             
   def draw(self):
      self.bar.text = 'Health: ' + str(self.health)
      self.bar.draw()

from images.mtg.CardInfo import CardInfo  
from images.mtg.ManaCost import ManaCost
class ManaBar (): 
   def __init__ (self): 
      self.manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0, 'colorless': 0}
      self.mana = TextBox ('Mana:' + str(self.manaLevel), 400, 5)             
      self.cardInfo = CardInfo()
      self.manaCost = ManaCost()
      
   def addLand (self,name):
      colors = ['colorless', 'white', 'red', 'blue', 'black', 'green']   
      if name == '': 
         pass 
      else:
         mana = self.cardInfo.cards[name]   
         for color in colors: 
            if color in mana:
               value = mana[color]
               print ( 'Got a value of: ' + str(value) )                
               self.change (color, value)
      
      print ( 'Added this mana to pool: ' + str(mana) )    

   def canCast (self, deck, sheetIndex): 
      name = deck.cardInfo.idToName (sheetIndex)       
      requiredMana = self.cardInfo.cards[name]
      (ok,mana) = self.manaCost.enoughMana ( self.manaLevel, name )
      return ok            
      
   def change (self,color,delta):
      self.manaLevel[color] = self.manaLevel[color] + delta 
      
   def draw(self):
      self.mana.text = 'Mana: ' + str(self.manaLevel)
      self.mana.draw()
      
   def payMana (self, deck, sheetIndex):     
      name = deck.cardInfo.idToName (sheetIndex)       
      requiredMana = self.cardInfo.cards[name]
      self.manaCost.payMana (self.manaLevel, requiredMana)
                
'''
   MTGCards is based on SubDeck but customized to an MTG deck   
'''
class MTGCards (SubDeck):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, empty=False, name='', utils=None):
      numCards = 0
      self.cardInfo = CardInfo()
      self.utilities = utils
      assert not utils is None, 'MTGCards for [' + name + '], utils is None' 
      self.action  = MTGActions(self.utilities, self.cardInfo)
      self.name = name 
      self.counter = None
      
      cards = []
      if str(filename).isnumeric():  
         print ( 'ERR MTGCards, filename has been passed as a number: ' + str(filename) ) 
         exit ()
      elif filename != '': 
         print ( 'open [filename]: [' + str(filename) + ']' )
         f = open ( filename, 'r' )
         line = f.readline()
         f.close 
         data = line.split ( ',' ) # Array of numeric strings
         numCards = len(data)
         print ( 'Got ' + str(numCards) + ' of cards read' )         
         
         # Convert array of string to array of integers 
         cards = [] 
         for d in data: 
            cards.append (int(d)) 
            
      print ( 'MTGCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier, cards=cards, empty=empty, name=name)
      
      for card in self.data:  
         card.counter = None
         card.name = self.cardInfo.idToName (card.sheetIndex)            
         card.action = MTGAction (card, self.cardInfo)
      
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__') 

   def cardName (self, sheetIndex):
      name = drawPile.cardInfo.idToName (sheetIndex)
      print ( 'cardName returning: [' + name + ']' )
      return name

   # return the number of creatures in this deck.      
   def countType (self,typeName):
      count = 0 
      for card in self.data: # Set the width/height of each image 
         sheetIndex = card.sheetIndex
         name = self.cardInfo.idToName (sheetIndex)            
         if name.find ( typeName ) > -1: 
            count = count + 1
      print ( 'The number of ' + typeName + ' type cards in ' + self.name + ' = ' + str(count)) 
      return count
      
   def executePhase (self,phase): 
      for card in self.data:  
         sheetIndex = card.sheetIndex
         name = self.cardInfo.idToName (sheetIndex)            
         print ( '[phase,name]: [' + phase + ',' + name + ']' )
         card.action.executePhase (phase)
   
      
   def draw (self, debugIt=False):
      SubDeck.draw (self)
      
      for card in self.data:  
         sheetIndex = card.sheetIndex
         name = self.cardInfo.idToName (sheetIndex)  
         if name == 'enchantments/redRibbonArmy.png':         
            if not card.counter is None:             
               card.counter.draw()
            
   def getName (self, data):
      return self.cardName (data.sheetIndex)       
      
   def isCreature (self,sheetIndex):
      return self.cardInfo.isCreature (sheetIndex)
        
   def isLand (self,sheetIndex):
      return self.cardInfo.isLand (sheetIndex)
      
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))  

   def redeal (self, debugIt=False):              
      SubDeck.redeal(self,debugIt)        
      for card in self.data: 
         if not card.counter == None:  
            card.counter.move (card.x+10, card.y+10 )         
         
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def untap (self):
      print ( 'Untap all cards in deck: ' + self.name )
      for d in self.data: 
         d.tapped = False
         
 
    
if __name__ == '__main__':
   from Deck      import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   from SubDecks  import SubDecks
   from TextBox   import TextBox
   from MTGSetup  import MTGSetup
   import time   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 780))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = MTGSetup(utilities).chooseDeckFilename('redDeck.txt')   
   drawPile     = MTGCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, \
                  yMultiplier=0.0, name='drawPile',utils=utilities)   
   drawPile.hideAll()
   opponent     = MTGCards (deck, empty=True, startXY=(100, 30), xMultiplier=1.0, yMultiplier=0.0, \
                             displaySurface=displaySurface, name='opponent', utils=utilities)
   hand         = MTGCards (deck, empty=True, startXY=(100,600), xMultiplier=1.0, yMultiplier=0.0, \
                             displaySurface=displaySurface, name='hand', utils=utilities)
   inplay       = MTGCards (deck, empty=True, startXY=(100,400), displaySurface=displaySurface, \
                             xMultiplier=1.0, yMultiplier=0.0, utils=utilities, name='inplay')   
   discardPile  = MTGCards (deck, empty=True, startXY=(100,200), displaySurface=displaySurface, \
                             xMultiplier=0.0, yMultiplier=0.0, name='discardPile', utils=utilities)
   for i in range (7):
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
   
   window   = pygame.display.get_surface()
   quit     = False
   dragCard = None   
   bar      = StatusBar ()
   manaBar  = ManaBar()
   health   = HealthBar()
  
   labels = Labels()
   labels.addLabel ('Opponent', 100, 5)
   labels.addLabel ('Discard' , 100, 175)
   labels.addLabel ('Draw'    , 310, 175)
   labels.addLabel ('In Play' , 100, 375)
   labels.addLabel ('Hand'    , 100, 575)
   phase = MTGPhases (inplay,hand)
   
   haveCastLand = False 
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      labels.show ()   
      phase.draw()
      manaBar.draw()
      health.draw()
      decks.draw() # Show and set their x/y locations
      utilities.showLastStatus()
      bar.show (['Quit', 'Message', 'Next Phase'] )
      pygame.display.update() 
      
      if phase.text() == 'Upkeep': 
         manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0} # Reset mana level          
         inplay.untap()
         inplay.redeal(True)
         inplay.executePhase('Upkeep')      
         phase.next()
         print ( 'phase.text is now: ' + phase.text() )
         haveCastLand = False 
      elif phase.text() == 'Draw':
         drawPile.topToDeck (hand, reveal=True)
         hand.redeal() 
         phase.next()       
      
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
               elif bar.selection == 'Next Phase': 
                  phase.next()
               else:
                  print ( 'bar.selection not handled: [' + bar.selection + ']' )
               bar.selection = ''
            else: 
               (deck,index) = decks.findSprite (data) # Returns index in list                         
               if deck == drawPile:
                  if phase.text() == 'Draw':               
                     deck.data[index].hide = False
                     hand.addCard (deck,index)
                     hand.redeal() 
                     deck.remove (index)
                     phase.next()
                  else:
                     utilities.showStatus ( 'You can only draw in draw phase')                  
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
            try:
               card = deck.data[index]            
               print ( '[deck,index]: [' + deck.name + ',' + str(index) + ']')             
            except Exception as ex:
               print ( 'Exception : ' + str(ex)) 
               index = -1
               
            if index != -1: 
               x = deck.data[index].x
               y = deck.data[index].y
               sheetIndex = deck.data[index].sheetIndex
               name = deck.cardInfo.idToName (sheetIndex)            
               deck.data[index].filename = name # Set the filename of the card                
               card = deck.data[index]
               
               optionBox = OptionBox ( ['Unknown'] )
               if deck == hand: 
                  if phase.text() == 'Cast': 
                     if hand.isLand(sheetIndex): 
                        if haveCastLand: 
                           print ( 'Already cast a land this turn' )
                           optionBox = hand.action.selectOption (['View', 'Cancel'])
                        else: 
                           optionBox = hand.action.selectOption (['View', 'Cast', 'Cancel'])
                     elif manaBar.canCast (hand,sheetIndex): 
                        if hand.cardInfo.isEnchantCreature (sheetIndex):
                           if (inplay.countType ('creatures') > 0) or (opponent.countType ('creatures') > 0): 
                              optionBox = hand.action.selectOption (['View', 'Cast', 'Cancel'])
                           else:
                              optionBox = hand.action.selectOption (['View', 'Cancel'])
                        elif hand.cardInfo.isEnchantPermanent(sheetIndex):
                           if inplay.length() > 0: 
                              optionBox = hand.action.selectOption (['View', 'Cast', 'Cancel'])
                           else:
                              optionBox = hand.action.selectOption (['View', 'Cancel'])
                           
                        else:
                           optionBox = hand.action.selectOption (['View', 'Cast', 'Cancel'])
                     else:
                        optionBox = hand.action.selectOption (['View', 'Cancel'])
                  else:
                     optionBox = hand.action.selectOption (['View', 'Cancel'] ) 
               elif deck == inplay: 
                  if card.tapped: 
                     optionBox = inplay.action.selectOption (['View', 'Untap', 'Cancel'])
                  else:
                     if (inplay.isCreature (sheetIndex)) and (phase.text() == 'Attack'):                  
                        optionBox = inplay.action.selectOption (['View', 'Attack', 'Cancel'])
                     else:                     
                        optionBox = inplay.action.selectOption (['View', 'Tap', 'Cancel'])
                  
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               name = inplay.cardInfo.idToName (sheetIndex)
               if selection == 'Cast': 
                  if not hand.isLand(sheetIndex): 
                     manaBar.payMana (hand, sheetIndex) 
                  if hand.isCreature(sheetIndex): # Summoning sickness...
                     hand.data[index].tapped = True 
                  inplay.addCard (hand, index)
                  inplay.redeal()
                  hand.remove (index) 
                  hand.redeal()                           
                  if hand.isLand (sheetIndex):                   
                     haveCastLand = True                   
                  if name == 'enchantments/redRibbonArmy.png': 
                     card.counter = Counter ( card.x + 10, card.y + 10)
                                         
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  utilities.showStatus ( 'Card is untapped' )
               elif selection == 'Tap':
                  if inplay.isLand (sheetIndex):
                     manaBar.addLand (name)                     
                  
                  print ( 'Mana before execution: ' + str(manaBar.manaLevel) ) 
                  inplay.action.tap (manaBar.manaLevel,card,inplay,opponent)               
                  print ( 'Mana is now: ' + str(manaBar.manaLevel) ) 
         else:
            print ( 'event: ' + typeInput)