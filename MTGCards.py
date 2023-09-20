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
from OptionBox           import OptionBox

def exit1 ():
   comm.disconnect()
   exit()
 
def selectCreature (decks):
   index = -1   
   ind = -1       
   escape = False 
   globalDictionary['utilities'].showStatus ('Select a creature in play')
   while (ind == -1) and not escape:   
      events = globalDictionary['utilities'].readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'escape': 
            escape = True 
         elif typeInput == 'drag': 
            # Determine which subdeck the card is in. 
            for deckName in decks:
               deck = globalDictionary[deckName] 
               globalDictionary['utilities'].showStatus ('check if selection is from deck: ' + deck.name)
               ind = deck.findSprite (data)
               if ind != -1: 
                  id = deck.data[ind].sheetIndex
                  if deck.data[ind].behavior.isCreature:
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
         
def selectLand (decks):
   index = -1  
   name = ''   
   ind = -1       
   escape = False 
   globalDictionary['utilities'].showStatus ('Select a land in play')
   while (ind == -1) and not escape:   
      events = globalDictionary['utilities'].readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'escape': 
            escape = True 
         elif typeInput == 'drag': 
            # Determine which subdeck the card is in. 
            for deckName in decks:
               deck = globalDictionary[deckName] 
               globalDictionary['utilities'].showStatus ('check if selection is from deck: ' + deck.name)
               ind = deck.findSprite (data)
               if ind != -1: 
                  id = deck.data[ind].sheetIndex
                  if deck.data[ind].behavior.isLand:
                     card = deck.data[ind]            
                     print ( '[deck,index]: [' + deck.name + ',' + str(ind) + ']')  
                     name = deck.name                      
                     index = ind
                  else:
                     globalDictionary['utilities'].showStatus ( 'That card is not a land aborting... ' + deck.name )
                  break
                  
   if index == -1:
      print ( 'No land selected' )
   else:
      print ( 'Selected land with index: ' + str(index)) 
      print ( '  Selected land named: ' + deck.data[index].name )
   return (name,index)
 
class MTGUtilities: 
   def killAllCreatures(self):
      print ( 'MTGUtilitites.kill all creatures in play' )  
      exit1()      
 
#from MTGUtilities           import MTGUtilities   
class MTGCardBase: 
   # Return True if the provided mana is enough to cast the creature      
   def canCast (self,mana):
      print ( 'Check if ' + str(mana) + ' is sufficient to handle casting cost: ' + str(self.manaCost) ) 
      return True  
   def cast (self,container):
      print ( 'MTGCardBase, cast of ' + self.name )
      card = globalDictionary['hand'].moveDataToDeck ( globalDictionary['inplay'],container,True)
      #remove card from 'hand'
      index = globalDictionary['hand'].findCard ( container.name )
      globalDictionary['hand'].remove (index,True)     
   def __init__ (self,name,manaCost): 
      print ( 'Base Card initialization [name,manaCost]: [' + name + ',' + str(manaCost) + ']' )
      self.name                  = name  
      self.manaCost              = manaCost 
      self.minimumNumberBlockers = 1 
      self.creatureEnchantment   = False     
      self.isLand                = False
      self.isArtifact            = False 
      self.isInstant             = False
      self.isSorcery             = False 
      self.isCreature            = False      
      self.isEnchantment         = False 
      self.tapped                = False       
      self.specialEffects        = []                 
   def selectPermanent (self): 
      return self.selectCardFromDeck (globalDictionary['inplay'], 'Select a permanent in play (ESC to cancel)')   
   def tap (self):
      print ( 'MTGCardBase, tap of: ' + self.name ) 
      return True 
'''
   Type cards 
'''         
class ArtifactCard (MTGCardBase): 
   def __init__ (self,name): 
      MTGCardBase.__init__(self,name,0)  
      self.isArtifact = True       
class CreatureCard (MTGCardBase): 
   def __init__ (self,name): 
      MTGCardBase.__init__(self,name,0)  
      self.isCreature = True   
class InstantCard (MTGCardBase): 
   def __init__ (self,name): 
      MTGCardBase.__init__(self,name,0)  
      self.isInstant = True        
class LandCard (MTGCardBase): 
   def __init__ (self,name): 
      MTGCardBase.__init__(self,name,0)  
      self.isLand = True       
class SorceryCard (MTGCardBase): 
   def __init__ (self,name): 
      MTGCardBase.__init__(self,name,0)  
      self.isSorcery = True       
'''
   Specific cards 
'''   
class AK47 (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/ak47.png')  
   def attack (self):
      print ( 'AK47 add +2/+0, and remove an ammo counter' )      
class BFG (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/bfg.jpg')  
   def attack (self):
      print ( 'BFG add +8/+8' )      
class BatheInDragonBreath (SorceryCard):
   def __init__ (self): 
      SorceryCard.__init__(self,'sorcery/batheInDragonbreath.png')  
   def cast (self,container):
      print ( 'BathInDragonBreath, deal 3 damage to target creature' )      
class BlackerLotus (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/blackerLotus.jpg')  
   def cast (self,container):
      print ( 'BlackerLotus add 4 mana of any color' ) 
      print ( 'Remove card from the game' )      
class CaptainAmericasShield (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/captainAmericasShield.png')  
   def cast (self,container):
      print ( 'CaptainAmericasShield, equipped player gets +1/+4' )
class CliffsOfInsanity (LandCard): 
   def __init__ (self): 
      super().__init__('lands/cliffsOfInsanity.jpg')  
   def tap (self):
      tapped = False 
      print ( 'CliffsOfInsanity, choose white or red' )   
      options = ['1 red mana', '1 white mana', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         tapped = True 
         super().tap()  
         if result == '1 red mana':
            print ( 'Add 1 red mana to your mana pool' )
         else:
            print ( 'Add 1 white mana to your mana pool' )
      return tapped       
class DarylDixon (CreatureCard):
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/darylDixon.jpg')  
   def tap (self):
      super().tap()      
      print ( 'Tapping DarylDixon yo' )
      return True      
class GameOver (InstantCard):
   def __init__ (self):
      super().__init__('instants/gameOver.jpg')
   def cast (self,container):
      print ( 'GameOver, Game is a draw yo' )
      # globalDictionary['inplay'].addData (self.container)
      exit1()
class GeorgeWBush (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/georgeWBush.jpg')          
   def tap(self):
      print ( 'George W Bush, tap, discard a card' )      
class GordonRamsey (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/georgeWBush.jpg')          
   def attack(self):
      print ( 'First strike and combat damage' )      
class ImposingVisage (MTGCardBase): 
   def __init__ (self):         
      MTGCardBase.__init__(self,'enchantments/imposingVisage.jpg',12)    
      self.minimumNumberBlockers = 2 
      self.creatureEnchantment = True 
   def cast (self,container): 
      ind = selectCreature(['inplay','opponent'])
      if ind == -1: 
         print ( 'Casting/Selection cancelled')
         wasCast = False
      else:
         creature = globalDictionary['inplay'].data[ind]
         creature.enchantments.append (container)
         index = globalDictionary['hand'].findCard (creature.name)
         globalDictionary['hand'].remove (index, True )
         
class InigoMontoya (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/inigoMontoya.jpg')          
   def cast(self,container):
      print ( 'Inigo Montoya, place father killer counter on target creature' )   
class JangoFett (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/jangoFett.jpg')          
   def attack(self):
      print ( 'JengoFett, place bounty counter on target creature' )   
class JustDesserts (InstantCard):
   def __init__ (self):
      InstantCard.__init__(self,'instants/justDesserts.jpg')
   def cast (self,container):
      print ( 'Just Desserts, deal 3 damage to target creature' )
class KoolAidMan (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/koolAidMan.jpg')          
   def tap(self):
      print ( 'KoolAidMan, destroy target wall' )   
class LethalResponse (MTGCardBase): 
   def __init__ (self):         
      MTGCardBase.__init__(self,'enchantments/lethalResponse.png',12)    
   def tap (self): 
      print ( 'Destroy a creature' )
      ind = self.selectPermanent()
      if ind == -1: 
         print ( 'Selection cancelled')
      else:
         permanent = globalDictionary['inplay'].data[ind]
      return True  
class MichaelBay (SorceryCard):
   def __init__ (self): 
      SorceryCard.__init__(self,'sorcery/michaelBay.jpg')  
   def cast (self,container):
      print ( 'MichaelBay, destroy target land' )  
      (deck,ind) = selectLand(['opponent','inplay']) 
      if deck != '': 
         print ( 'Remove land with index: ' + str(ind) + ' from deck: ' + deck )
               
class Molotov (InstantCard):
   def __init__ (self):
      InstantCard.__init__(self,'instants/molotov.png')
   def cast (self,container):
      print ( 'Molotov, 2 damage to target creature, 1 damage to adjacent?!' )         
class Mountain (LandCard): 
   def __init__ (self): 
      super().__init__('lands/mountain.jpg')          
class NoviceBountyHunter (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/noviceBountyHunter.jpg')          
   def cast(self):
      print ( 'NoviceBountyHunter, place bounty counter on target creature' )   
class Pikachu (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/pikachu.jpg')          
   def cast(self):
      print ( 'Pikachu cast, 1 direct damage or +1/+1' )   
class PitOfDespair (LandCard):       
   def __init__ (self):
      super().__init__('lands/pitOfDespair.jpg') 
      self.specialEffects.append ( ('fight', 'red,green,tap','You and Opponent, random creature fight' ) )
   def tap (self):
      super().tap()   
      print ( 'PitOfDespair, choose red or Green' )        
      
      # TODO: only present the 3rd option if rw is in the mana pool.      
      options = ['1 white mana', '1 red mana', 'cost:rw, fight creatures', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         tapped = True 
         super().tap()  
         if result == '1 white mana':
            print ( 'Add 1 white mana to your mana pool' )
         elif result == '1 red mana':
            print ( 'Add 1 red mana to your mana pool' )
         else:
            print ( '2 Creature fight' )
      return tapped       
class RedRibbonArmy (MTGCardBase): 
   def __init__ (self):         
      MTGCardBase.__init__(self,'enchantments/redRibbonArmy.png',12)      
   # Actions that take place when the card is cast 
   def cast (self,container): 
      globalDictionary['mtgUtilities'].killAllCreatures()
      self.counter = Counter (110,110)            
   def upkeep (self):
      print ( 'Execute Upkeep phase for : ' + self.name )
      print ( 'Increment counter for redRibbonArmy' )
      if not hasattr(self,"counter"):          
         raise Exception("Red Ribbon Army has no counter?!")
      else:
         self.counter.increment()
         for i in range (self.counter.value):
            globalDictionary['inplay'].addCoverCard('1/1 Army')               
class RocketTrooper (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/rocketTropper.jpg')          
   def cast(self,container):
      print ( 'Rocket Trooper cast, 1 direct damage' )  
class SirRobin (CreatureCard):
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/sirRobin.png')  
   def tap (self):
      super().tap()      
      print ( 'Tapping Sir Robin yo' )
      return True            
class SpiderMan (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'creatures/rocketTropper.jpg')
      self.specialEffects.append ( ('spray web', 'red,blue','target creature cannot untap' ) )
      self.specialEffects.append ( ('spidey sense', 'red,red', 'first strike' ) ) 
   def cast(self,container):
      print ( 'SpiderMan, all rogues get minus 1' )   
class ShotInTheArm (InstantCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'instants/shotInTheArm.jpg')
   def cast(self,container):
      print ( 'ShotInTheArm, target creature gets +4/+4' ) 
class TheFireSwamp (LandCard): 
   def __init__ (self): 
      LandCard.__init__(self,'lands/fireSwamp.jpg') 
      self.specialEffects.append ( ('plague', 'black,tap','target creature gets -1/-1' ) )
      self.specialEffects.append ( ('poke', 'red,tap', 'target creature gets 1 damage' ) )       
   def tap (self):
      print ( 'TheFireSwamp, choose black or red' )  
      tapped = False 
      options = ['1 black mana', '1 red mana', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         tapped = True 
         super().tap()  
         if result == '1 red mana':
            print ( 'Add 1 red mana to your mana pool' )
         else:
            print ( 'Add 1 white mana to your mana pool' )
      return tapped       
class TheMachine (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'artifacts/The Machine.jpg')
   def tap(self):
      print ( 'The Machine, suck life out of creatures' )   
      return True 
behaviors = {}
behaviors['artifacts/ak47.png']                  = AK47                  ()
behaviors['artifacts/bfg.jpg']                   = BFG                   ()
behaviors['artifacts/blackerLotus.jpg']          = BlackerLotus          ()
behaviors['artifacts/captainAmericasShield.png'] = CaptainAmericasShield ()
behaviors['artifacts/The Machine.jpg']           = TheMachine            ()
behaviors['creatures/darylDixon.jpg']            = DarylDixon            ()
behaviors['creatures/georgeWBush.jpg']           = GeorgeWBush           () 
behaviors['creatures/gordonRamsey.jpg']          = GordonRamsey          () 
behaviors['creatures/inigoMontoya.jpg']          = InigoMontoya          ()
behaviors['creatures/jangoFett.jpg']             = JangoFett             ()
behaviors['creatures/koolAidMan.jpg']            = KoolAidMan            () 
behaviors['creatures/logan.jpg']                 = CreatureCard          ('creatures/logan.jpg')
behaviors['creatures/mtgPlayer.png']             = CreatureCard          ('creatures/mtgPlayer.png')
behaviors['creatures/noviceBountyHunter.jpg']    = CreatureCard          ('creatures/noviceBountyHunter.jpg')
behaviors['creatures/pikachu.png']               = Pikachu               ()
behaviors['creatures/rocketTropper.jpg']         = RocketTrooper         ()
behaviors['creatures/ragePlayer.jpeg']           = CreatureCard          ('creatures/ragePlayer.jpeg')
behaviors['creatures/redForman.jpg']             = CreatureCard          ('creatures/redForman.jpg')
behaviors['creatures/sirRobin.png']              = SirRobin              ()
behaviors['creatures/spiderman.jpg']             = SpiderMan             ()
behaviors['creatures/t34Tank.jpg']               = CreatureCard          ('creatures/t34Tank.jpg')
behaviors['creatures/theJoker.jpg']              = CreatureCard          ('creatures/theJoker.jpg')
behaviors['creatures/weepingStatue.jpg']         = CreatureCard          ('creatures/weepingStatue.jpg')
behaviors['enchantments/redRibbonArmy.png']      = RedRibbonArmy         ()
behaviors['enchantments/imposingVisage.jpg']     = ImposingVisage        ()
behaviors['enchantments/lethalResponse.png']     = LethalResponse        ()
behaviors['instants/gameOver.jpg']               = GameOver              ()
behaviors['instants/justDesserts.jpg']           = JustDesserts          ()
behaviors['instants/molotov.png']                = Molotov               ()
behaviors['instants/shotInTheArm.jpg']           = ShotInTheArm          ()
behaviors['lands/cliffsOfInsanity.jpg']          = CliffsOfInsanity      ()
behaviors['lands/fireSwamp.jpg']                 = TheFireSwamp          ()
behaviors['lands/mountain.jpg']                  = Mountain              ()
behaviors['lands/pitOfDespair.jpg']              = PitOfDespair          ()
behaviors['sorcery/batheInDragonbreath.png']     = BatheInDragonBreath   ()
behaviors['sorcery/michaelBay.jpg']              = MichaelBay            ()

def returnBehavior ( name ): 
   if name in behaviors: 
      behavior = behaviors[name]
   else:
      raise Exception ( 'Could not find behavior for: ' + name )
   return behavior


import os
from Communications      import Communications
class MTGCommunications (Communications):
   # data is a list of objects that have an image and index attribute
   def __init__ (self):
      if os.name == 'posix':
         broker = 'localhost'
         myName = 'pi7'
         target = 'laptop'
      else: # Windows computer 
         broker = '192.168.4.1'
         myName = 'laptop'
         target = 'pi7'
         broker = 'testServer' # pi not required to be in loop 
      topic = 'messages'
      
      print ( '[broker,myName,target]: [' + broker + ',' + myName + ',' + target + ']')
      Communications.__init__(self,topic,broker,myName)
      self.callback = self.callbackProcedure
      if self.connectBroker():
         self.setTarget (target)
      else:
         raise Exception ( 'Could not connect to broker: ' + broker )

   def moveCard ( self, card, sourceDeck, destinationDeck): 
      self.send ( 'move ' + str(card.index) + sourceDeck + ' ' + destinationDeck )
  
   def addCard ( self, deckName, card):
      print ( 'Add ' + card.name + ' to ' + deckName )
  
   def callbackProcedure (self, msg ):
      data = msg.split ( ' ' )
      print ( 'callbackProcedure got the message: ' + str(data) )  
      if data[0] == 'move': 
         index = int(data[1]) 
         sourceDeck = data[2]
         destinationDeck = data[3]
         print ( 'Move card ' + str(index) + ' from ' + sourceDeck + ' to: ' + destinationDeck)            
         source = globalDictionary[sourceDeck]
         card = globalDictionary[destinationDeck].addCard (source,index)              
  
   def sendDeck ( self, deck, deckName ): 
      self.send ( 'deck init ' + deckName )
      for card in deck.data: 
         self.addCard (deckName, card)   
                   
class MTGActions():   
   def __init__ (self):
      self.phase = TextBox ('Upkeep', 500, 755)

   def addEnchantment (self, permanent, enchantment):
      print ('addEnchantment' )
      # permanent.enchantments = []
      # Move card from hand to inplay 
      enchantment.x = permanent.x
      enchantment.y = permanent.y + 30
      print ( 'card [x,y]: [' + str(card.x) + ',' + str(card.y) + ']' )
      permanent.enchantments.append (enchantment) 
            
   # Card is cast from hand deck to inplay deck    
   def cast (self,sourceDeck,index):  
      wasCast = True   
      #card = sourceDeck.data[index]
      #card.behavior.cast(card)
 
      # card = globalDictionary['inplay'].addCard (sourceDeck,index)  
      ''' 
      if card.name == 'enchantments/imposingVisage.jpg': 
         ind = selectCreature(['inplay','opponent'])
         if ind == -1: 
            print ( 'Casting/Selection cancelled')
            wasCast = False
         else:
            permanent = globalDictionary['inplay'].data[ind]
            self.addEnchantment (permanent,card)
            print ( 'Casting completed' )    
            
      elif card.name == 'enchantments/lethalResponse.png': 
         ind = self.selectPermanent()
         if ind == -1: 
            print ( 'Casting/Selection cancelled')
            wasCast = False
         else:
            permanent = globalDictionary['inplay'].data[ind]
            self.addEnchantment (permanent,card)
            print ( 'Casting completed' )
            
      elif card.name == 'enchantments/redRibbonArmy.png':                      
         card = globalDictionary['inplay'].addCard (sourceDeck,index)           
         ind = globalDictionary['inplay'].length()-1
         card.counter = Counter ( card.x + 10, card.y + 10)
      else:
         card = globalDictionary['inplay'].addCard (sourceDeck,index)  
      
      if wasCast:
         print ( 'Card cast: [' + card.name + ']' )
      else:
         print ( 'This card was NOT cast: ' + card.name )
      '''   
      return wasCast 
      
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
      friendly = selectCreature(['inplay'])
      if friendly != -1: 
         enemy    = selectCreature(['opponent'])
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
   
   def tap (self,mana,card):
      print ( 'Mana before execution: ' + str(mana) ) 
      if not hasattr (card, 'behavior'):
         print ( 'Missing behavior for this card: ' + card.name ) 
         exit1()
         
      print ( 'tap [mana,card]: [' + str(mana) + ',' + card.name + ']' )
      name = card.name 
      print ( 'tap: card. [name]: [' + name + ']' ) 
      '''
      if name == 'lands/cliffsOfInsanity.jpg':
         options = ['Tap For Red', 'Tap For White','Cancel']
         optionBox = globalDictionary['utilities'].selectOption (options)
         selection = optionBox.getSelection()
         if selection == 'Tap For Red':
            mana['red'] = mana['red'] + 1
            card.tapped = True
         elif selection == 'Tap For White':
            mana['white'] = mana['white'] + 1
            card.tapped = True      
      elif name == 'lands/fireSwamp.jpg':
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
         card.tapped = True 
      else:
         print ( 'Did not find an action for: ' + card.name )
         card.tapped = True 
      '''   
      card.tapped = True 
      globalDictionary['inplay'].redeal()
      print ( 'Mana is now: ' + str(mana) ) 
      
      
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
         exit1()
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
      
      # Add attributes which are specific to MTG cards 
      for card in self.data:  
         card.name = globalDictionary['cardInfo'].idToName (card.sheetIndex)
         card.enchantments  = []
         if card.name in behaviors: 
            card.behavior = behaviors[card.name]
         else:
            print ( card.name + ' needs a behavior' )
            exit1()
         
      
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__')

   def addCoverCard (self, labelText, name='cover.jpg'): 
      obj = super().addCoverCard (labelText, name)
      obj.tapped = False 

   def cardName (self, sheetIndex):
      name = globalDictionary['cardInfo'].idToName (sheetIndex)
      print ( 'cardName returning: [' + name + ']' )
      return name
      
   def cast (self,index):  
      card.behavior.cast (card) # Use the behavior to cast this is because some cards are cast differently (like enchantments)
      self.redeal()
        
      # TODO: Behavior will dictate if cast was completed properly or aborted
      
      #if card.behavior.isCreature:
      #   globalDictionary['hand'].data[index].tapped = True # TODO: should not tap, just has summoning sickness so can't attack      
      globalDictionary['inplay'].redeal(True)

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
         if hasattr (card, "counter"):  # Counter appears after being cast
            card.counter.draw()
         if hasattr (card, "enchantments"): 
            # print ( 'Draw all enchantments for: ' + card.name )
            for c in card.enchantments:
               image = self.getImage (c)
               self.displaySurface.blit (image, (c.x,c.y))             
               
   def getImage (self,sprite):
      image = super().getImage (sprite)
      if sprite.tapped:          
         image = self.rotate (image,90) 
      sprite.width  = image.get_width()
      sprite.height = image.get_height()      
      return image                
   
   def getName (self, data):
      return self.cardName (data.sheetIndex)       

   def moveToDeck (self,destinationDeck,index,reveal=False): 
      card = super().moveToDeck (destinationDeck,index,reveal)
      card.behavior = behaviors[card.name]
      destinationDeck.redeal()
      card.x = destinationDeck.nextX
      card.y = destinationDeck.nextY
      return card 
       
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))  

   # set the x location of cards
   def redeal (self, debugIt=False):  
      yOffset = self.yMultiplier * self.height  
      x = self.startX
      y = self.startY           
      cnt = 0    
      for card in self.data: # Set the width/height of each image 
         ind = cnt         
         self.data[ind].x = x
         self.data[ind].y = y
         card.x = x
         card.y = y 
         if card.tapped: 
            xOffset = self.height * self.xMultiplier
         else:
            xOffset = self.width * self.xMultiplier
         c = self.data[ind]
         x = x + xOffset
         y = y + yOffset    
         cnt = cnt + 1
         if hasattr (card,"counter"):       
            card.counter.move (card.x+10, card.y+10 )         
         if hasattr (card,"enchantments"): 
            for enchantment in card.enchantments:
               enchantment.x = card.x            
         if hasattr (card,'label'):
            card.label.move (card.x+5, card.y+30)
                                    
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   # Note: Tap should be just for the MTG game for a specific game.   
   def tap (self,index,value): 
      print ( 'self.data[' + str(index) + '].tapped = ' + str(value))
      card = self.data[index]
      
      if value: 
         val = card.behavior.tap()
         if val: 
            card.tapped = True 
            for enchantment in card.enchantments:
               enchantment.behavior.tap()
         self.redeal()      
      else:
         card.tapped = False

          
   # untap all cards in the deck 
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
   from Communications     import Communications
   import os

   import time  

   def findEnchantment (pos):
      print ( 'MTGUtility? findEnchantment' )      
      found = None 
      for card in globalDictionary['inplay'].data: 
         if hasattr (card, 'enchantments'): 
            for enchantment in card.enchantments:          
               width  = enchantment.width
               height = enchantment.height
               rect   = pygame.Rect (enchantment.x, enchantment.y, width,height)               
               if rect.collidepoint (pos): 
                  print ( 'Found enchantment sprite at pos: ' + str(pos))
                  found = enchantment  
      if not found is None: 
         print ( found.name + '.findSprite found at [' + str(found.x) + ',' + str(found.y) + ']' ) 
         
      return found   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 780))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   
   globalDictionary['mtgUtilities'] = MTGUtilities()
   globalDictionary['utilities']    = Utilities (displaySurface, BIGFONT)   
   globalDictionary['cardInfo']     = CardInfo()

   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = MTGSetup().chooseDeckFilename('redDeck.txt')   
   drawPile     = MTGCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=0.0, \
                  yMultiplier=0.0, name='drawPile')                     
   drawPile.hideAll()
   drawPile.shuffle()
   
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
   cards.append (globalDictionary['opponent'])
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
   
   comm = MTGCommunications ();
   comm.sendDeck (hand, 'opponent' ) 
   
   # Move Daryl Dixon from drawPile to Inplay (Test purposes only)
   ind  = drawPile.findCard ( 'creatures/darylDixon.jpg')
   card = drawPile.moveToDeck ( globalDictionary['inplay'],ind,True)
   
   # Move rocket Tropper from drawPile to Inplay (Test purposes only)
   ind  = drawPile.findCard ( 'creatures/rocketTropper.jpg')
   card = drawPile.moveToDeck ( globalDictionary['opponent'],ind,True)      
         
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

      if actions.phase.text == 'Draw': #Draw a card 
         drawPile.topToDeck (globalDictionary['hand'], reveal=True)
         globalDictionary['hand'].redeal() 
         actions.nextPhase()       
      elif actions.phase.text == 'Upkeep': 
         manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0} # Reset mana level          
         globalDictionary['inplay'].untap()
         globalDictionary['inplay'].redeal(True)
         actions.executePhase (globalDictionary['inplay'], 'Upkeep')      
         actions.nextPhase()
         print ( 'phase.text is now: ' + actions.phase.text )
         haveCastLand = False 
      
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
                  if actions.phase.text == 'Draw':               
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
            #card = findEnchantment (data)
            if True: #if card is None: 
               (deck,index) = decks.findSprite (data) 
               try:
                  if index == -1: 
                     print ( 'Could not find a deck for selection' )
                     exit1()
                  else:
                     card = deck.data[index]                             
               except Exception as ex:
                  print ( 'Exception : ' + str(ex)) 
               
            if not card is None: # A card was clicked on 
               print ( 'card.name: ' + card.name )
               x = card.x
               y = card.y
               sheetIndex = card.sheetIndex                        

               optionBox = OptionBox ( ['Unknown'] )
               print ( 'Deck selected: ' + deck.name )
               if deck.name == 'hand': 
                  if actions.phase.text == 'Cast': 
                     if card.behavior.isLand:  
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
                  print ( 'Clicked on a card in play' )
                  if card.tapped: 
                     optionBox = globalDictionary['utilities'].selectOption (['View', 'Untap', 'Cancel'])
                  else:
                     #TODO: Attack if it is my turn, block if it is opponents turn
                     if card.behavior.isCreature and not card.tapped:                  
                        optionBox = globalDictionary['utilities'].selectOption (['View', 'Attack', 'Block', 'Cancel'])
                     else:
                        if card.behavior.isEnchantment:                     
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                        else:                        
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Tap', 'Cancel'])
                                 
               # Handle user action selection 
               selection = optionBox.getSelection()
               print ( '[selection]: [' + selection + ']' ) 
               if selection == 'Attack':
                  globalDictionary['inplay'].tap (index,True)
               elif selection == 'Cast':                            
                  if card.behavior.isLand: 
                     haveCastLand = True 
                  globalDictionary['hand'].cast ( index )
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + card.name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  globalDictionary['inplay'].redeal()                  
                  for enchantment in card.enchantments:
                     enchantment.tapped = False
               elif selection == 'Tap':  
                  deck.tap (index, True)  
                  deck.redeal()                  
   
         else:
            print ( 'event: ' + typeInput)
            
print ( 'All done doing a disconnect...' )
comm.disconnect()