import pygame
from SubDeck             import SubDeck
from Utilities           import Utilities
from SelectButton        import SelectButton 
from ViewImage           import ViewImage 
from StatusBar           import StatusBar
from Labels              import Labels 
from images.mtg.CardInfo import CardInfo 
from images.mtg.Counter  import Counter
from images.mtg.Globals  import * 

      
class MTGActions():   
   def __init__ (self):
      self.phase = TextBox ('Upkeep', 500, 755)

   def addEnchantment (self, card):
      print ('addEnchantment' )
      
   # Card is cast from hand deck to inplay deck    
   def cast (self,sourceDeck,index):         
      if card.name == 'enchantments/redRibbonArmy.png':                      
         card = globalDictionary['inplay'].addCard (sourceDeck,index)           
         ind = globalDictionary['inplay'].length()-1
         card.counter = Counter ( card.x + 10, card.y + 10)
      elif card.name == 'enchantments/lethalResponse.png': 
         ind = self.selectPermanent()
         if ind == -1: 
            print ( 'Casting cancelled')
         else:
            card = sourceDeck.data[index]
            self.addEnchantment(card):
            print ( 'Casting completed' )
      else:
         card = globalDictionary['inplay'].addCard (sourceDeck,index)  
      
      print ( 'Card cast: [' + card.name + ']' )

   def damageOpponent (self,amount):
      print ( 'Opponent takes ' + str(amount) + ' damage' )

   def executePhase (self,deck,phase): 
      print ( 'Execute ' + phase + ' for all cards' )
      for card in deck.data:
         if phase == "Upkeep":
            print ( 'Execute Upkeep phase for : ' + card.name )
            if card.name == 'enchantments/redRibbonArmy.png':
               print ( 'Increment counter for redRibbonArmy' )
               if card.counter is None:
                  raise Exception("Red Ribbon Army has no counter?!")
               else:
                  card.counter.increment()
                  for i in range (card.counter.value):
                     globalDictionary['inplay'].addCoverCard('1/1 Army')
                     
   def fight (self,mana): 
      success = False 
      friendly = self.selectCreature(globalDictionary['inplay'])
      if friendly != -1: 
         enemy    = self.selectCreature(globalDictionary['opponent'])
         if enemy != -1:  
            print ( 'Assign damage between those creatures' )
            success = True 
         else:
            print ( 'Enemy creature aborted' )
      else:
         print ( 'Friendly creature aborted' )
      return success
      
   def nextPhase(self):     
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
         while globalDictionary['hand'].length() > 7: 
            ind = self.selectCardToDiscard(globalDictionary['hand'])
            print ( 'delete card [' + str(ind) + '] from hand' )
            globalDictionary['hand'].discard (ind) 
            globalDictionary['hand'].redeal()
      elif self.phase.text == 'End Turn':
         self.phase.text = 'Upkeep'  
      print ( 'new phase.text: [' + self.phase.text + ']' )
         
   def selectCardFromDeck (self, deck, prompt):
      index = -1   
      ind   = -1       
      globalDictionary['utilities'].showStatus (prompt)
      escape = False 
      while (ind == -1) and not escape:   
         events = globalDictionary['utilities'].readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'escape': 
               escape = True 
            elif typeInput == 'drag': 
               ind = deck.findSprite (data)
               if ind != -1: 
                  index = ind 
                  break
                     
      if index == -1:
         print ( 'No card selected' )
      else:
         print ( 'Selected card with index: ' + str(index)) 
         print ( '  Selected card with name : ' + deck.data[index].name )
      globalDictionary['utilities'].clearStatus()
      return index
      
   def selectCardToDiscard (self, deck):
      return self.selectCardFromDeck (deck, 'Select a card from your hand to discard: ')

   def selectPermanent (self): 
      return self.selectCardFromDeck (globalDictionary['inplay'], 'Select a permanent in play (ESC to cancel)')   
            
   def selectCreature (self, deck):
      index = -1   
      ind = -1       
      globalDictionary['utilities'].showStatus ('Select a creature in deck: ' + deck.name)
      escape = False 
      while (ind == -1) and not escape:   
         events = globalDictionary['utilities'].readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'escape': 
               escape = True 
            elif typeInput == 'drag': 
               # Determine which subdeck the card is in. 
               ind = deck.findSprite (data)
               if ind != -1: 
                  id = deck.data[ind].sheetIndex
                  if globalDictionary['cardInfo'].isCreature(id): 
                     card = deck.data[ind]            
                     print ( '[deck,index]: [' + deck.name + ',' + str(ind) + ']')               
                     index = ind
                  else:
                     globalDictionary['utilities'].showStatus ( 'That card is not a creature aborting... ' + deck.name )
                  break
                     
      if index == -1:
         print ( 'No creature selected' )
      else:
         print ( 'Selected creature with index: ' + str(index)) 
         print ( '  Selected creature named: ' + deck.data[index].name )
      return index
              
   def tap (self,mana,card):
      print ( 'tap [mana,card]: [' + str(mana) + ',' + card.name + ']' )
      name = card.name 
      print ( 'tap: card. [name]: [' + name + ']' ) 
      if name == 'lands/fireSwamp.jpg':
         options = ['Tap For Red', 'Tap For Black']
         if mana['red'] > 0:
            options.append ( 'Damage target player (cost R)' )
         if mana['black'] > 0:
            options.append ( 'Target creature reduced 1/1 (cost B)' )
         options.append ( 'Cancel' )
         optionBox = globalDictionary['utilities'].selectOption (options)
         selection = optionBox.getSelection()
         if selection == 'Tap For Red':
            mana['red'] = mana['red'] + 1
            card.tapped = True
         elif selection == 'Tap For Black':
            mana['black'] = mana['black'] + 1
            card.tapped = True
         elif selection == 'Damage target player (cost R)':
            print ( 'Deal 1 point damage to target player' ) # Todo select which player?
         elif selection == 'Target creature reduced 1/1 (cost B)':
            print ('TODO ')
         elif selection == 'Cancel':
            print ('Never mind') 
      elif name == 'lands/pitOfDespair.jpg': 
         options = ['Tap For Red', 'Tap For Green']
         if (mana['red'] > 0) and (mana['green']  > 0) and (globalDictionary['inplay'].countType ('creatures') > 0):
            options.append ( 'Force fight between 2 creatures (cost R/W)' )         
         options.append ( 'Cancel' )
         optionBox = globalDictionary['utilities'].selectOption (options)
         
         selection = optionBox.getSelection()
         if selection == 'Tap For Red': 
            mana['red'] = mana['red'] + 1
            card.tapped = True 
         elif selection == 'Tap For Green': 
            mana['green'] = mana['green'] + 1
            card.tapped = True 
         elif selection == 'Force fight between 2 creatures (cost R/W)':             
            if self.fight(mana):
               print ( 'Reduce mana by 1 red, 1 green' )
               mana['red'] = mana['red'] - 1
               mana['green'] = mana ['green'] - 1
               card.tapped = True 
            else:
               print ( 'Fight aborted' )
         elif selection == 'Cancel': 
            print ( 'Never mind') 
      elif globalDictionary['inplay'].isLand (card.sheetIndex):
         globalDictionary['manaBar'].addLand (card.name)                     
      else:
         print ( 'Did not find an action for: ' + card.name )
         card.tapped = True 
         
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
      self.manaLevel = {'red':4, 'black':0, 'green':0, 'white':0, 'blue':0, 'colorless': 0}
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
               self.change (color, value)
      
      print ( 'Added this mana to pool: ' + str(mana) )    

   def canCast (self, sheetIndex): 
      name = globalDictionary['cardInfo'].idToName (sheetIndex)       
      requiredMana = globalDictionary['cardInfo'].cards[name]
      (ok,mana) = self.manaCost.enoughMana ( self.manaLevel, name )
      return ok            
      
   def change (self,color,delta):
      self.manaLevel[color] = self.manaLevel[color] + delta 
      
   def draw(self):
      self.mana.text = 'Mana: ' + str(self.manaLevel)
      self.mana.draw()
      
   def payMana (self, sheetIndex):     
      name = globalDictionary['cardInfo'].idToName (sheetIndex)       
      requiredMana = globalDictionary['cardInfo'].cards[name]
      self.manaCost.payMana (self.manaLevel, requiredMana)
                
'''
   MTGCards is based on SubDeck but customized to an MTG deck   
'''
class MTGCards (SubDeck):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, empty=False, name=''):
      numCards = 0
      self.name = name 
      
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
         card.name = globalDictionary['cardInfo'].idToName (card.sheetIndex)
         print ( 'name set to: ' + card.name )
      
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__')

   def cardName (self, sheetIndex):
      name = globalDictionary['cardInfo'].idToName (sheetIndex)
      print ( 'cardName returning: [' + name + ']' )
      return name
      
   # return the number of creatures in this deck.      
   def countType (self,typeName):
      count = 0 
      for card in self.data: # Set the width/height of each image 
         sheetIndex = card.sheetIndex
         name = globalDictionary['cardInfo'].idToName (sheetIndex)            
         if name.find ( typeName ) > -1: 
            count = count + 1
      print ( 'The number of ' + typeName + ' type cards in ' + self.name + ' = ' + str(count)) 
      return count
      
   def draw (self, debugIt=False):
      SubDeck.draw (self)
      
      for card in self.data:  
         sheetIndex = card.sheetIndex
         name = globalDictionary['cardInfo'].idToName (sheetIndex)  
         if name == 'enchantments/redRibbonArmy.png':         
            if hasattr (card, "counter"):  # Counter appears after being cast
               card.counter.draw()
                   
   def getName (self, data):
      return self.cardName (data.sheetIndex)       
      
   def isCreature (self,sheetIndex):
      return globalDictionary['cardInfo'].isCreature (sheetIndex)
        
   def isLand (self,sheetIndex):
      return globalDictionary['cardInfo'].isLand (sheetIndex)
      
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))  

   def redeal (self, debugIt=False):              
      SubDeck.redeal(self,debugIt)        
      for card in self.data:
         if hasattr (card,"counter"):       
            card.counter.move (card.x+10, card.y+10 )         
         
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def untap (self):
      print ( 'Untap all cards in deck: ' + self.name )
      for d in self.data: 
         d.tapped = False
         
 
    
if __name__ == '__main__':
   from Deck               import Deck
   from Utilities          import Utilities
   from OptionBox          import OptionBox
   from SubDecks           import SubDecks
   from TextBox            import TextBox
   from MTGSetup           import MTGSetup

   import time   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 780))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   
   globalDictionary['utilities'] = Utilities (displaySurface, BIGFONT)   
   globalDictionary['cardInfo']  = CardInfo()
    
   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = MTGSetup().chooseDeckFilename('redDeck.txt')   
   drawPile     = MTGCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, \
                  yMultiplier=0.0, name='drawPile')                     
   drawPile.hideAll()
   
   opponentDeck = MTGCards (deck, empty=True, startXY=(100, 30), xMultiplier=1.0, yMultiplier=0.0, \
                             displaySurface=displaySurface, name='opponent')
   hand         = MTGCards (deck, empty=True, startXY=(100,600), xMultiplier=1.0, yMultiplier=0.0, \
                             displaySurface=displaySurface, name='hand')
   inplay       = MTGCards (deck, empty=True, startXY=(100,400), displaySurface=displaySurface, \
                             xMultiplier=1.0, yMultiplier=0.0, name='inplay')   
   discardDeck  = MTGCards (deck, empty=True, startXY=(100,200), displaySurface=displaySurface, \
                             xMultiplier=0.0, yMultiplier=0.0, name='discardPile')
      
   globalDictionary['inplay']      = inplay
   globalDictionary['opponent']    = opponentDeck
   globalDictionary['hand']        = hand
   globalDictionary['discardPile'] = discardDeck
   globalDictionary['drawPile']    = drawPile
   manaBar                         = ManaBar()
   globalDictionary['manaBar']     = manaBar   
   actions                         = MTGActions()
   
   for i in range (7):
      drawPile.topToDeck (globalDictionary['hand'], reveal=True)
    
   globalDictionary['hand'].showAll() 
   globalDictionary['hand'].redeal(True)    
   globalDictionary['hand'].draw(True)
   
   cards=[]
   cards.append (drawPile)   
   cards.append (discardDeck)
   cards.append (globalDictionary['hand'])
   cards.append (globalDictionary['inplay'])
   cards.append (opponentDeck)
   decks = SubDecks (cards)    
   
   window   = pygame.display.get_surface()
   quit     = False
   dragCard = None   
   bar      = StatusBar ()
   health   = HealthBar()
  
   labels = Labels()
   labels.addLabel ('Opponent', 100, 5)
   labels.addLabel ('Discard' , 100, 175)
   labels.addLabel ('Draw'    , 310, 175)
   labels.addLabel ('In Play' , 100, 375)
   labels.addLabel ('Hand'    , 100, 575)
   
   haveCastLand = False 
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      labels.show ()   
      actions.phase.draw()
      manaBar.draw()
      health.draw()
      decks.draw() # Show and set their x/y locations
      globalDictionary['utilities'].showLastStatus()
      bar.show (['Quit', 'Message', 'Next Phase'] )
      pygame.display.update() 
      
      if actions.phase.text == 'Upkeep': 
         manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0} # Reset mana level          
         globalDictionary['inplay'].untap()
         globalDictionary['inplay'].redeal(True)
         actions.executePhase (globalDictionary['inplay'], 'Upkeep')      
         actions.nextPhase()
         print ( 'phase.text is now: ' + actions.phase.text )
         haveCastLand = False 
      elif actions.phase.text == 'Draw':
         drawPile.topToDeck (globalDictionary['hand'], reveal=True)
         globalDictionary['hand'].redeal() 
         actions.nextPhase()       
      
      events = globalDictionary['utilities'].readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'move':
            if not dragCard is None:
               x = data[0]
               y = data[1]
               print ( 'Moving...' + str(dragCard) + ' to [' + str(x) + ',' + str(y) + ']')
               globalDictionary['hand'].move (dragCard,data)
                  
         elif typeInput == 'drag':
            bar.update (data) 
            if bar.selection != '':
               if bar.selection == 'Quit': 
                  quit = True
                  bar.consumeSelection()
               elif bar.selection == 'Next Phase': 
                  actions.nextPhase()
               else:
                  print ( 'bar.selection not handled: [' + bar.selection + ']' )
               bar.selection = ''
            else: 
               (deck,index) = decks.findSprite (data) # Returns index in list                         
               if deck == drawPile:
                  if actionsphase.text == 'Draw':               
                     deck.data[index].hide = False
                     globalDictionary['hand'].addCard (deck,index)
                     globalDictionary['hand'].redeal() 
                     deck.remove (index)
                     actions.nextPhase()
                  else:
                     globalDictionary['utilities'].showStatus ( 'You can only draw in draw phase')                  
               else: 
                  if dragCard is None:
                     dragCard = globalDictionary['hand'].findSprite (data) 
                     print ( 'dragCard: ' + str(dragCard) ) 
                     if dragCard > -1:
                        sheetIndex = globalDictionary['hand'].data[dragCard].sheetIndex
                        globalDictionary['hand'].data[dragCard].drag = True 
                        print ( '\n\n***DRAG*** ' + globalDictionary['hand'].cardName(sheetIndex) + '\n\n' )
                     
         elif typeInput == 'drop':
            (deck,index) = decks.findSprite (data) # Where are we dropping                                  
            if deck == globalDictionary['discardPile']: 
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
               card = deck.data[index]

               optionBox = OptionBox ( ['Unknown'] )
               if deck == globalDictionary['hand']: 
                  if actions.phase.text == 'Cast': 
                     if globalDictionary['hand'].isLand(sheetIndex): 
                        if haveCastLand: 
                           print ( 'Already cast a land this turn' )
                           
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                        else: 
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Cast', 'Cancel'])
                     elif manaBar.canCast (sheetIndex): 
                        if globalDictionary['cardInfo'].isEnchantCreature (sheetIndex):
                           if (globalDictionary['inplay'].countType ('creatures') > 0) or \
                              (globalDictionary['opponent'].countType ('creatures') > 0): 
                              optionBox = globalDictionary['utilities'].selectOption (['View', 'Cast', 'Cancel'])
                           else:
                              optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                        elif globalDictionary['cardInfo'].isEnchantPermanent(sheetIndex):
                           if globalDictionary['inplay'].length() > 0: 
                              optionBox = globalDictionary['utilities'].selectOption (['View', 'Cast', 'Cancel'])
                           else:
                              optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                           
                        else:
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Cast', 'Cancel'])
                     else:
                        optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                  else:
                     optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'] ) 
               elif deck == globalDictionary['inplay']: 
                  if card.tapped: 
                     optionBox = globalDictionary['utilities'].selectOption (['View', 'Untap', 'Cancel'])
                  else:
                     if (globalDictionary['inplay'].isCreature (sheetIndex)) and (actions.phase.text == 'Attack'):                  
                        optionBox = globalDictionary['utilities'].selectOption (['View', 'Attack', 'Cancel'])
                     else:                     
                        optionBox = globalDictionary['utilities'].selectOption (['View', 'Tap', 'Cancel'])
                  
               selection = optionBox.getSelection()
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               # name = globalDictionary['cardInfo'].idToName (sheetIndex)
               if selection == 'Cast': 
                  if not globalDictionary['hand'].isLand(sheetIndex): 
                     manaBar.payMana (sheetIndex) 
                  if globalDictionary['hand'].isCreature(sheetIndex): # Summoning sickness...
                     globalDictionary['hand'].data[index].tapped = True # TODO: should not tap, just has summoning sickness so can't attack
                     
                  actions.cast (globalDictionary['hand'], index)
                  globalDictionary['inplay'].redeal()
                  globalDictionary['hand'].remove (index) 
                  globalDictionary['hand'].redeal()                           
                  if globalDictionary['hand'].isLand (sheetIndex):                   
                     haveCastLand = True                                 
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + card.name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  globalDictionary['utilities'].showStatus ( 'Card is untapped' )
               elif selection == 'Tap':                  
                  print ( 'Mana before execution: ' + str(manaBar.manaLevel) ) 
                  actions.tap (manaBar.manaLevel,card)               
                  print ( 'Mana is now: ' + str(manaBar.manaLevel) ) 
         else:
            print ( 'event: ' + typeInput)