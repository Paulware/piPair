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


def exit1 ():
   comm.disconnect()
   exit()
 
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
   def cast (self):
      print ( 'MTGCardBase, casting of ' + self.name )
      sourceDeck = globalDictionary['hand']
      card = globalDictionary['inplay'].addData (self.container)
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
      self.specialEffects        = []
      
   def selectCreature (self, decks):
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
               for deck in decks:
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
                    
   def selectPermanent (self): 
      return self.selectCardFromDeck (globalDictionary['inplay'], 'Select a permanent in play (ESC to cancel)')   
   def tap (self):
      print ( 'MTGCardBase, tap of: ' + self.name )
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
   def tap (self):
      print ( 'Add the default color to your mana pool' )
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
   def cast (self):
      print ( 'BathInDragonBreath, deal 3 damage to target creature' )      
class BlackerLotus (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/blackerLotus.jpg')  
   def cast (self):
      print ( 'BlackerLotus add 4 mana of any color' ) 
      print ( 'Remove card from the game' )      
class CaptainAmericasShield (ArtifactCard):
   def __init__ (self): 
      ArtifactCard.__init__(self,'artifacts/captainAmericasShield.png')  
   def cast (self):
      print ( 'CaptainAmericasShield, equipped player gets +1/+4' )
class CliffsOfInsanity (LandCard): 
   def __init__ (self): 
      LandCard.__init__(self,'/lands/cliffsOfInsanity.jpg')  
   def tap (self):
      print ( 'CliffsOfInsanity, choose white or red' )   
class DarylDixon (CreatureCard):
   def __init__ (self): 
      CreatureCard.__init__(self,'creatures/darylDixon.jpg')  
   def tap (self):
      print ( 'Tapping DarylDixon yo' )
class GameOver (InstantCard):
   def __init__ (self):
      InstantCard.__init__(self,'instants/gameOver.jpg')
   def cast (self):
      print ( 'GameOver, Game is a draw yo' )
class GeorgeWBush (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'/creatures/georgeWBush.jpg')          
   def tap(self):
      print ( 'George W Bush, tap, discard a card' )      
class GordonRamsey (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'/creatures/georgeWBush.jpg')          
   def attack(self):
      print ( 'First strike and combat damage' )      
class ImposingVisage (MTGCardBase): 
   def __init__ (self):         
      MTGCardBase.__init__(self,'enchantments/imposingVisage.jpg',12)    
      self.minimumNumberBlockers = 2 
      self.creatureEnchantment = True 
   def cast (self): 
      ind = self.selectCreature([globalDictionary['inplay'],globalDictionary['opponent']])
      if ind == -1: 
         print ( 'Casting/Selection cancelled')
         wasCast = False
      else:
         permanent   = globalDictionary['inplay'].data[ind]
         enchantment = self.container 
         if hasattr (permanent,"enchantments"): 
            enchantment.x = permanent.x
            enchantment.y = permanent.y + 30         
            permanent.enchantments.append (enchantment) 
            print ( 'Added ' + self.name + ' to enchantments for: ' + permanent.name )
         else:
            print ( 'Could not find enchantments for: ' + permanent.name )
            exit1()
         print ( 'Casting completed' ) 
class InigoMontoya (CreatureCard): 
   def __init__ (self): 
      CreatureCard.__init__(self,'/creatures/inigoMontoya.jpg')          
   def cast(self):
      print ( 'Inigo Montoya, place father killer counter on target creature' )   
class JangoFett (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/creatures/jangoFett.jpg')          
   def attack(self):
      print ( 'JengoFett, place bounty counter on target creature' )   
class JustDesserts (InstantCard):
   def __init__ (self):
      InstantCard.__init__(self,'instants/justDesserts.jpg')
   def cast (self):
      print ( 'Just Desserts, deal 3 damage to target creature' )
class KoolAidMan (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/creatures/koolAidMan.jpg')          
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
         print ( 'Casting completed' )  
class MichaelBay (SorceryCard):
   def __init__ (self): 
      SorceryCard.__init__(self,'sorcery/michaelBay.jpg')  
   def cast (self):
      print ( 'MichaelBay, destroy target land' )               
class Molotov (InstantCard):
   def __init__ (self):
      InstantCard.__init__(self,'instants/molotov.png')
   def cast (self):
      print ( 'Molotov, 2 damage to target creature, 1 damage to adjacent?!' )         
class Mountain (LandCard): 
   def __init__ (self): 
      LandCard.__init__(self,'/lands/mountain.jpg')          
class NoviceBountyHunter (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/creatures/noviceBountyHunter.jpg')          
   def cast(self):
      print ( 'NoviceBountyHunter, place bounty counter on target creature' )   
class Pikachu (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/creatures/pikachu.jpg')          
   def cast(self):
      print ( 'Pikachu cast, 1 direct damage or +1/+1' )   
class PitOfDespair (LandCard):       
   def __init__ (self):
      LandCard.__init__(self,'/lands/pitOfDespair.jpg') 
      self.specialEffects.append ( ('fight', 'red,green,tap','You and Opponent, random creature fight' ) )
   def tap (self):
      print ( 'PitOfDespair, choose red or Green' )        
class RedRibbonArmy (MTGCardBase): 
   def __init__ (self):         
      MTGCardBase.__init__(self,'enchantments/redRibbonArmy.png',12)      
   # Actions that take place when the card is cast 
   def cast (self): 
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
      CreatureCard.__init__(self,'/creatures/rocketTropper.jpg')          
   def cast(self):
      print ( 'Rocket Trooper cast, 1 direct damage' )                   
class SpiderMan (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/creatures/rocketTropper.jpg')
      self.specialEffects.append ( ('spray web', 'red,blue','target creature cannot untap' ) )
      self.specialEffects.append ( ('spidey sense', 'red,red', 'first strike' ) ) 
   def cast(self):
      print ( 'SpiderMan, all rogues get minus 1' )   
class ShotInTheArm (InstantCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/instants/shotInTheArm.jpg')
   def cast(self):
      print ( 'ShotInTheArm, target creature gets +4/+4' ) 
class TheFireSwamp (LandCard): 
   def __init__ (self): 
      LandCard.__init__(self,'/lands/fireSwamp.jpg') 
      self.specialEffects.append ( ('plague', 'black,tap','target creature gets -1/-1' ) )
      self.specialEffects.append ( ('poke', 'red,tap', 'target creature gets 1 damage' ) )       
   def tap (self):
      print ( 'CliffsOfInsanity, choose black or red' )        
class TheMachine (CreatureCard):       
   def __init__ (self):
      CreatureCard.__init__(self,'/artifacts/The Machine.jpg')
   def tap(self):
      print ( 'The Machine, suck life out of creatures' )   

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
      card = sourceDeck.data[index].behavior.cast()
      ''' 
      if card.name == 'enchantments/imposingVisage.jpg': 
         ind = self.selectCreature([globalDictionary['inplay'],globalDictionary['opponent']])
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
      friendly = self.selectCreature([globalDictionary['inplay']])
      if friendly != -1: 
         enemy    = self.selectCreature([globalDictionary['opponent']])
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
            
   def selectCreature (self, decks):
      index = -1   
      ind = -1       
      escape = False 
      while (ind == -1) and not escape:   
         events = globalDictionary['utilities'].readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'escape': 
               escape = True 
            elif typeInput == 'drag': 
               # Determine which subdeck the card is in. 
               for deck in decks:
                  globalDictionary['utilities'].showStatus ('check if selection is from deck: ' + deck.name)
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
         card.isEnchantment = False 
         card.isCreature    = False
         if card.name.find ( 'enchantment' ) > -1:
            card.isEnchantment = True 
         if card.name in behaviors: 
            card.behavior = behaviors[card.name]
            card.behavior.container = card 
         else:
            print ( card.name + ' needs a behavior' )
            exit1()
         
      
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
         if hasattr (card, "counter"):  # Counter appears after being cast
            card.counter.draw()
         if hasattr (card, "enchantments"): 
            # print ( 'Draw all enchantments for: ' + card.name )
            for c in card.enchantments:
               image = self.getImage (c)
               self.displaySurface.blit (image, (c.x,c.y))             
   
   def getName (self, data):
      return self.cardName (data.sheetIndex)       
      
   def isCreature (self,sheetIndex):
      return globalDictionary['cardInfo'].isCreature (sheetIndex)
        
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))  

   def redeal (self, debugIt=False):
      print ( 'redeal' )
            
      SubDeck.redeal(self,debugIt)        
      for card in self.data:
         if hasattr (card,"counter"):       
            card.counter.move (card.x+10, card.y+10 )         
         if hasattr (card,"enchantments"): 
            for enchantment in card.enchantments:
               enchantment.x = card.x            
         if hasattr (card,'label'):
            card.label.move (card.x+5, card.y+30)
            
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
   
   comm = MTGCommunications ();
   comm.sendDeck (hand, 'opponent' ) 
   
   # Move Daryl Dixon from drawPile to Inplay (Test purposes only)
   ind = drawPile.findCard ( 'creatures/darylDixon.jpg')
   print ( 'Found draylDixon: ' + str(ind) ) 
   drawPile.data[ind].behavior = behaviors['creatures/darylDixon.jpg']
   drawPile.moveToDeck ( globalDictionary['inplay'],ind,True)
      
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
            card = findEnchantment (data)
            if card is None: 
               (deck,index) = decks.findSprite (data) 
               try:
                  if index != -1: 
                     card = deck.data[index]                             
               except Exception as ex:
                  print ( 'Exception : ' + str(ex)) 
               
            if not card is None: # A card was clicked on 
               print ( 'card.name: ' + card.name )
               x = card.x
               y = card.y
               sheetIndex = card.sheetIndex                        

               optionBox = OptionBox ( ['Unknown'] )
               if deck == globalDictionary['hand']: 
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
                  if card.tapped: 
                     optionBox = globalDictionary['utilities'].selectOption (['View', 'Untap', 'Cancel'])
                  else:
                     if (globalDictionary['inplay'].isCreature (sheetIndex)) and (actions.phase.text == 'Attack') and \
                        (not card.tapped):                  
                        optionBox = globalDictionary['utilities'].selectOption (['View', 'Attack', 'Cancel'])
                     else:
                        if card.isEnchantment:                     
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Cancel'])
                        else:                        
                           optionBox = globalDictionary['utilities'].selectOption (['View', 'Tap', 'Cancel'])
                                 
               # Handle user action selection 
               selection = optionBox.getSelection()
               print ( '[selection]: [' + selection + ']' ) 
               if selection == 'Attack':
                  card.tapped = True
               elif selection == 'Cast':
                  if actions.cast (globalDictionary['hand'], index): # Can cast the card 
                     if not card.behavior.isLand:
                        manaBar.payMana (sheetIndex) 
                        
                     # Add behavior to last item cast 
                     behavior = returnBehavior ( card.name )                      
                        
                     globalDictionary['inplay'].redeal()
                     globalDictionary['hand'].remove (index) 
                     globalDictionary['hand'].redeal()                           
                     if card.behavior.isLand:
                        haveCastLand = True                                 
                     if card.behavior.isCreature:
                        globalDictionary['hand'].data[index].tapped = True # TODO: should not tap, just has summoning sickness so can't attack                
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + card.name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  globalDictionary['inplay'].redeal()                  
                  for enchantment in card.enchantments:
                     enchantment.tapped = False
               elif selection == 'Tap':                  
                  actions.tap (manaBar.manaLevel,card)               
                  for enchantment in card.enchantments:
                     actions.tap (manaBar.manaLevel,enchantment)
   
         else:
            print ( 'event: ' + typeInput)
            
print ( 'All done doing a disconnect...' )
comm.disconnect()