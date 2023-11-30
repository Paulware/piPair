import pygame
from SubDeck                  import SubDeck
from Utilities                import Utilities
from SelectButton             import SelectButton 
from ViewImage                import ViewImage 
from StatusBar                import StatusBar
from Labels                   import Labels
from images.mtg.CardInfo      import CardInfo  
from images.mtg.Counter       import Counter
from images.mtg.DamageCounter import DamageCounter
from Globals                  import * 
from OptionBox                import OptionBox

def exit1 ():
   print ( 'exit1, terminate the program....' )
   comm.disconnect()
   exit()
   
       
def topToDeck (deckSource,deckTarget,reveal=False): 
   index = len(deckSource.data)-1  
   ind = deckTarget.addCardToDeck (deckSource.data[index])
   deckSource.remove (index)      
   if reveal: 
      deckTarget.revealTopCard()
   

def selectCard (decks, title, isCreature, isLand, isWall):
   index = -1   
   ind = -1       
   escape = False 
   name = ''
   globalDictionary['utilities'].showStatus (title)
   while (ind == -1) and not escape:   
      events = globalDictionary['utilities'].readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'escape': 
            escape = True 
         elif typeInput == 'drag': 
            escape = True # Got a click          
            # Determine which subdeck the card is in. 
            for deckName in decks:
               deck = globalDictionary[deckName] 
               # globalDictionary['utilities'].showStatus ('check if selection is from deck: ' + deck.name)
               (ind,eInd) = deck.findSprite (data)
               if ind != -1: 
                  id = deck.data[ind].sheetIndex
                  if (isCreature and deck.data[ind].behavior.isCreature) or \
                     (isLand and deck.data[ind].behavior.isLand) or \
                     (isWall and deck.data[ind].behavior.isWall):
                     card = deck.data[ind]            
                     print ( '[deck,index]: [' + deck.name + ',' + str(ind) + ']')               
                     name = deck.name 
                     index = ind
                  break                  
   if index == -1:
      print ( 'No creature selected' )
   else:
      print ( 'Selected creature with index: ' + str(index)) 
      print ( '  Selected creature named: ' + deck.data[index].name )
   return (name,index) 
def selectCreature (decks, title='Select a creature in play (press esc to skip)'):
   return selectCard (decks, title, True, False, False )   
def selectLand (decks):
   return selectCard (decks,'Select a land in play', False, True, False)   
def selectPermanent (decks):
   return selectCard (decks,'Select a land or creature in play', True, True, False)
def selectWall (decks,title):
   return selectCard (decks,title, False, False, True)
 
class MTGUtilities: 
   def killAllCreatures(self):
      print ( 'MTGUtilitites.kill all creatures in play' )  
      exit1()      
 
#from MTGUtilities           import MTGUtilities   
class MTGCardBase: # (Behavior)
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
      self.isEquipment           = False  
      self.isWall                = False  
      self.tapEffects            = False   
      self.haste                 = False   
      self.flying                = False 
      self.offsetPower           = 0
      self.offsetToughness       = 0
      self.flanking              = False    # Used by the T34 tank 
     
      # Special Effects are not effects you tap for, they can happen anytime...
      self.specialEffects        = []
      self.counters              = []
   
   def addDamage (self,damage): 
      print ( '\n***' );
      print ( 'add damage: ' + str(damage) )
      if not hasattr (self,"damageCounter"): 
         print ( 'creating self.damageCounter ' )
         self.damageCounter = DamageCounter ()
      print ( 'Now addDamage...' )
      self.damageCounter.addDamage (damage)
   
   def addIntCounter (self):
      x = 110
      y = (len(self.counters) * 35 ) + 110
      counter = Counter (x,y)
      self.counters.append (counter)
      return counter
         
   def addTextCounter (self,text):
      x = 100
      y = (len(self.counters) * 35 ) + 110
      counter = Counter (x,y,text)
      self.counters.append (counter)
      return counter
   
   def attack (self):
      print ( self.container.name + ' is attacking...' )
      self.container.tapped = True 
   
   def castEnchantment (self,deckName,ind): 
      creature = globalDictionary[deckName].data[ind]            
      #print ( 'Add ' + self.container.name + ' to: ' + deckName + ', card: ' + creature.name )       
      creature.enchantments.append (self.container)
      
      self.container.x = creature.x 
      self.container.y = creature.y + 30
      
      #print ( creature.name + ' now has ' + str(len(creature.enchantments)) + ' enchantments' ) 
      globalDictionary[deckName].redeal()
      globalDictionary[deckName].draw()
      
      # Remove enchantment from the hand
      index = globalDictionary['hand'].findCard (self.container.name)
      globalDictionary['hand'].remove (index, True ) 
      globalDictionary['hand'].redeal()         

   # Return True if the provided mana is enough to cast the creature      
   def canCast (self,mana):
      print ( 'Check if ' + str(mana) + ' is sufficient to handle casting cost: ' + str(self.manaCost) ) 
      return True  
      
   # move card from hand to inplay 
   def cast (self):
      print ( 'MTGCardBase, cast of ' + self.name )
      index = globalDictionary['hand'].findCard (self.container.name)      
      ind = globalDictionary['inplay'].addCardToDeck (globalDictionary['hand'].data[index]) 
      globalDictionary['hand'].remove (index)

      card = globalDictionary['inplay'].data[ind]
      card.hide = False
      globalDictionary['inplay'].redeal()
      globalDictionary['drawPile'].checkY()
      globalDictionary['manaBar'].payMana (self.container.sheetIndex)  
      self.summoningSickness = not self.haste
      print ( 'Summoning sickness for: ' + self.name + ' : ' + str(self.summoningSickness))
      
   def reset (self):
      self.offsetPower     = 0
      self.offsetToughness = 0 
      self.damage          = 0
   def tap (self):
      card = self.container 
      print ('MTGCardBase, tap of: ' + self.name) 
      card.tapped = True
      if hasattr (card, "enchantments"): 
         if len(card.enchantments) > 0: 
            print ( 'Draw all enchantments for: ' + card.name )
            count = 0
            for enchantment in card.enchantments:
               enchantment.tapped = True 
               count = count + 1
               print ( 'tap enchantment[' + str(count) + '] ' + enchantment.name )
                   
               # Enchantment tap must return True for card to tap?!
               if not enchantment.behavior.tap():
                  card.tapped = False 
                  break 
      return True                  
   def equip (self):
      print ( 'MTGCardBase, Equip a creature.' )
'''
   Type cards 
'''         
class ArtifactCard (MTGCardBase): 
   def __init__ (self,name): 
      super().__init__(name,0)  
      self.isArtifact = True       
class CreatureCard (MTGCardBase): 
   def __init__ (self,name): 
      super().__init__(name,0)  
      self.isCreature = True 

class EnchantmentCard (MTGCardBase):
   def __init__ (self,name): 
      super().__init__(name,0)  
      self.isEnchantment = True 
   def cast (self): 
      (deckName,ind) = selectCreature(['inplay','opponent'])
      if ind == -1: 
         print ( 'Casting/Selection cancelled')
      else:
         self.castEnchantment (deckName,ind)     
class InstantCard (MTGCardBase): 
   def __init__ (self,name): 
      super().__init__(name,0)  
      self.isInstant = True 
   def cast (self): 
      print ( 'MTGCardBase, cast of ' + self.name + ', remove from hand' )
      index = globalDictionary['hand'].findCard (self.container.name)
      globalDictionary['hand'].remove (index,True)  
      globalDictionary['manaBar'].payMana (self.container.sheetIndex)  
class LandCard (MTGCardBase): 
   def __init__ (self,name): 
      super().__init__(name,0)       
      self.isLand = True 
   def tap (self): 
      globalDictionary['manaBar'].addLand (self.name)
      super().tap()      
class SorceryCard (MTGCardBase): 
   def __init__ (self,name): 
      super().__init__(name,0)  
      self.isSorcery = True       
'''
   Specific cards 
'''   
class AK47 (ArtifactCard):
   def __init__ (self): 
      super().__init__('artifacts/ak47.png')  
      self.isEquipment = True 
   def attack (self):
      print ( 'AK47 add +2/+0, and remove an ammo counter' )     
   def cast (self):
      # Place 3 counters on AK47
      counter = self.addIntCounter ()
      for I in range(3):
         counter.increment()
   def equip (self):
      print ( 'Equip an AK47 on a creature' )   
class BFG (ArtifactCard):
   def __init__ (self): 
      super().__init__('artifacts/bfg.jpg')  
   def attack (self):
      print ( 'BFG add +8/+8' )      
class BatheInDragonBreath (SorceryCard):
   def __init__ (self): 
      super().__init__('sorcery/batheInDragonbreath.png')  
   def cast (self):
      print ( 'BathInDragonBreath, deal 3 damage to target creature' )      
      (deck,ind) = selectCreature(['inplay','opponent'])
      if ind == -1: 
         print ( 'Casting/Selection cancelled')
         wasCast = False
      else:
         creature = globalDictionary[deck].data[ind]            
         creature.damage = creature.damage + 3
         index = globalDictionary['hand'].findCard (self.container.name)
         globalDictionary['hand'].remove (index, True )     
class BlackerLotus (ArtifactCard):
   def __init__ (self): 
      super().__init__('artifacts/blackerLotus.jpg')  
      self.tapEffects = True      
   def tap():
      cancelTap = False 
      print ( 'BlackerLotus add 4 mana of any color' ) 
      options = ['receive 4 red mana', 'receive 4 black mana', 'receive 4 white mana', 'receive 4 blue mana', 'receive 4 green mana', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'receive 4 red mana': 
         for I in range (4):
            globalDictionary['manaBar'].addLand ('lands/mountain.jpg')
      elif result == 'receive 4 black mana':
         for I in range (4):
            globalDictionary['manaBar'].addLand ('lands/swamp.jpg')
      elif result == 'receive 4 white mana':
         for I in range (4):
            globalDictionary['manaBar'].addLand ('lands/plains.jpg')
      elif result == 'receive 4 blue mana':
         for I in range (4):
            globalDictionary['manaBar'].addLand ('lands/island.jpg')
      elif result == 'receive 4 green mana':
         for I in range (4):
            globalDictionary['manaBar'].addLand ('lands/forest.jpg')
      else:
         cancelTap = True 
         
      if not cancelTap: # Remove the card from the game 
         index = globalDictionary['inplay'].findCard (self.container.name)
         globalDictionary['inplay'].remove (index,True)  
                           
class CaptainAmericasShield (ArtifactCard):
   def __init__ (self): 
      super().__init__('artifacts/captainAmericasShield.png')  
   def cast (self):
      print ( 'CaptainAmericasShield, equipped player gets +1/+4' )
class CliffsOfInsanity (LandCard): 
   def __init__ (self): 
      super().__init__('lands/cliffsOfInsanity.jpg')
   def tap (self):
      print ( 'CliffsOfInsanity, choose white or red' )   
      options = ['1 red mana', '1 white mana', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         super().tap()  
         if result == '1 red mana':
            globalDictionary['manaBar'].addLand ('lands/mountain.jpg')         
         else:
            globalDictionary['manaBar'].addLand ('lands/plains.jpg')
class DarylDixon (CreatureCard):
   def __init__ (self): 
      super().__init__('creatures/darylDixon.jpg')  
class GameOver (InstantCard):
   def __init__ (self):
      super().__init__('instants/gameOver.jpg')
   def cast (self):
      print ( 'GameOver, Game is a draw yo' )
      # globalDictionary['inplay'].addData (self.container)
      exit1()
class GeorgeWBush (CreatureCard): 
   def __init__ (self): 
      super().__init__('creatures/georgeWBush.jpg') 
      self.tapEffects = True       
   def tap(self):
      print ( 'GeorgeWBush, tap to discard a card' )   
      options = ['attack', 'discard a card', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         super().tap()  
         if result == 'discard a card':
            print ( 'Select a card from hand to discard' )
class GordonRamsey (CreatureCard): 
   def __init__ (self): 
      super().__init__('creatures/georgeWBush.jpg')          
   def attack(self):
      print ( 'First strike and combat damage' )      
class ImposingVisage (EnchantmentCard): 
   def __init__ (self):         
      super().__init__('enchantments/imposingVisage.jpg')    
      self.minimumNumberBlockers = 2 
      self.creatureEnchantment = True 
class InigoMontoya (CreatureCard): 
   def __init__ (self): 
      super().__init__('creatures/inigoMontoya.jpg')          
   def cast(self):
      print ( 'Inigo Montoya, place father killer counter on target creature' )   
      (deckName,ind) = selectCreature(['opponent'],'Select the creature that killed Inigo\'s father')
      if ind != -1:
         creature = globalDictionary['opponent'].data[ind]
         # creature.counter = Counter ( creature.x,creature.y+10,'father killer')
         counter = self.addTextCounter ( 'father killer' )
      super().cast()
class JangoFett (CreatureCard):       
   def __init__ (self):
      super().__init__('creatures/jangoFett.jpg')  
      self.haste  = True
      self.flying = True       
   def attack(self):
      print ( 'JengoFett, place bounty counter on target creature' )   
      super().attack()
class JustDesserts (InstantCard):
   def __init__ (self):
      super().__init__('instants/justDesserts.jpg')
   def cast (self):
      print ( 'Just Desserts, deal 3 damage to target creature' )
      (deckName,ind) = selectCreature(['opponent'],'Select the creature that killed Inigo\'s father')
      if ind != -1:
         creature = globalDictionary['opponent'].data[ind]
         creature.damage = creature.damage + 3
      super().cast()
class KoolAidMan (CreatureCard):       
   def __init__ (self):
      super().__init__('creatures/koolAidMan.jpg')   
      self.tapEffects = True   
      self.haste = True      
   def tap(self):
      print ( 'KoolAidMan, destroy target wall on tap' )   
      (deckName,ind) = selectWall(['inplay','opponent'],'Select a wall that will be destroyed')
      if ind != -1:
         globalDictionary[deckName].remove (ind)      
class LethalResponse (EnchantmentCard): 
   def __init__ (self):         
      super().__init__('enchantments/lethalResponse.png')    
   def tap (self): 
      print ( 'LethalResponse will destroy a creature on tap' )
      (deckName,ind) = selectCreature(['inplay','opponent'],'Select a creature that will be destroyed')
      if ind != -1:
         globalDictionary[deckName].remove (ind)      
      return True          
   def cast (self):
      (deckName,ind) = selectPermanent(['inplay'])
      if ind == -1:
         print ( 'Casting/Selection cancelled')
      else:
         self.castEnchantment (deckName,ind)
class MichaelBay (SorceryCard):
   def __init__ (self): 
      super().__init__('sorcery/michaelBay.jpg')  
   def cast (self):
      print ( 'MichaelBay, destroy target land' )  
      (deck,ind) = selectLand(['opponent','inplay']) 
      if deck != '': 
         print ( 'Remove land with index: ' + str(ind) + ' from deck: ' + deck )               
      super().cast()
class Molotov (InstantCard):
   def __init__ (self):
      super().__init__('instants/molotov.png')
   def cast (self):
      print ( 'Molotov, 2 damage to target creature, 1 damage to adjacent?!' )   
      (deck,index) = selectCreature ( ['inplay','opponent'],'Select creature to receive 2 damage' )
      if index != -1:
         target = globalDictionary[deck].data[index]     
         target.damage = target.damage + 2
         target.behavior.addDamage(2)
         
         print ( 'Creature ' + globalDictionary[deck].data[index].name + '.damage is now set = ' + \
                 str(globalDictionary[deck].data[index].damage) )
         #TODO: Add/Remove counter based on list of counters.... or do this on view?
         globalDictionary[deck].data[index].behavior.addTextCounter ( 'Damage: ' + str(globalDictionary[deck].data[index].damage) )
         super().cast() # Remove from hand 
class Mountain (LandCard): 
   def __init__ (self): 
      super().__init__('lands/mountain.jpg')          
class NoviceBountyHunter (CreatureCard):       
   def __init__ (self):
      super().__init__('creatures/noviceBountyHunter.jpg')          
   def cast(self):
      print ( 'NoviceBountyHunter, place bounty counter on target creature' )   
class Pikachu (CreatureCard):       
   def __init__ (self):
      super().__init__('creatures/pikachu.jpg')     
      self.specialEffects = ['Evolve']      
   def cast(self):
      print ( 'Pikachu cast, 1 direct damage any target or +1/+1 with haste until end of turn' )   
      options = ['1 damage to opponent', '1 damage to any creature', 'haste and +1/+1 until end of turn', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()             
      if result == '1 damage to opponent':
         print ( 'Damage opponent by 1') 
      elif result == '1 damage to any creature':
         (deckName,ind) = selectCreature(['inplay','opponent'],'Select a creature that will receive 1 damage')
         if ind != -1:
            damage = globalDictionary[deckName].data[ind].damage
            globalDictionary[deckName].data[ind].damage = damage + 1
      elif result == 'haste and +1/+1 until end of turn':
         self.haste = True 
         self.offsetPower = 1
         self.offsetToughness = 1
      else:
         print ( 'No cast action taken' )
      super().cast()  
        
class PitOfDespair (LandCard):       
   def __init__ (self):
      super().__init__('lands/pitOfDespair.jpg') 
      # self.specialEffects.append ( ('fight', 'red,green,tap','You and Opponent, random creature fight' ) )
   def tap (self):
      print ( 'Tap of PitOfDespair...behavior being called') 
      super().tap()   
      print ( 'PitOfDespair, choose red or Green' )        
      
      # TODO: only present the 3rd option if rw is in the mana pool.      
      options = ['1 white mana', '1 red mana', 'cost:rw, fight creatures', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run () 
            
      if result == 'cancel': 
         print ( 'Do not tap yo' )
         tapped = False
      else:
         tapped = True 
         super().tap()  
         if result == '1 white mana':
            globalDictionary['manaBar'].addLand ('lands/plains.jpg')         
         elif result == '1 red mana':
            globalDictionary['manaBar'].addLand ('lands/mountain.jpg')
         else:
            print ( '2 Creature fight' )
      return tapped       
class RedRibbonArmy (MTGCardBase): 
   def __init__ (self):         
      super().__init__('enchantments/redRibbonArmy.png',12)      
   # Actions that take place when the card is cast 
   def cast (self): 
      globalDictionary['mtgUtilities'].killAllCreatures()
      count = addIntCounter ()
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
      super().__init__('creatures/rocketTropper.jpg')          
   def cast(self):
      print ( 'Rocket Trooper cast, 1 direct damage' )  
      options = ['1 damage to player', '1 damage to creature', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == '1 damage to player': 
         print ( 'Player damaged by 1' )
      else:
         (deck,ind) = selectCreature(['inplay','opponent'])
         if ind == -1: 
            print ( 'Casting/Selection cancelled')
            wasCast = False
         else:
            creature = globalDictionary[deck].data[ind]            
            creature.damage = creature.damage + 1
            index = globalDictionary['hand'].findCard (container.name)
            globalDictionary['hand'].remove (index, True )     
class SirRobin (CreatureCard):
   def __init__ (self): 
      super().__init__('creatures/sirRobin.png')             
class SpiderMan (CreatureCard):       
   def __init__ (self):
      super().__init__('creatures/rocketTropper.jpg')
      #self.specialEffects.append ( ('spray web', 'red,blue','target creature cannot untap' ) )
      #self.specialEffects.append ( ('spidey sense', 'red,red', 'first strike' ) ) 
   def cast(self):
      print ( 'SpiderMan, all rogues get minus 1' )   
class ShotInTheArm (InstantCard):       
   def __init__ (self):
      super().__init__('instants/shotInTheArm.jpg')
   def cast(self):
      print ( 'ShotInTheArm, target creature gets +4/+4' ) 
      self.offsetPower = 4
      self.offsetToughness = 4

class TheFireSwamp (LandCard): 
   def __init__ (self): 
      super().__init__('lands/fireSwamp.jpg')   
    
   def tap (self):
      print ( 'TheFireSwamp, choose black or red' )  
      tapped = False 
      options = ['1 black mana', '1 red mana', 'cancel']
      comboBox = OptionBox(options)
      result = comboBox.run ()      
      if result == 'cancel': 
         print ( 'Do not tap yo' )
      else:
         self.container.tapped = True 
         if result == '1 red mana':
            print ( 'Add 1 red mana to your mana pool' )
            globalDictionary['manaBar'].addLand ('lands/mountain.jpg')
         else:
            print ( 'Add 1 black mana to your mana pool' )
            globalDictionary['manaBar'].addLand ('lands/swamp.jpg')
            
      return tapped          
     
class TheMachine (CreatureCard):       
   def __init__ (self):
      super().__init__('artifacts/The Machine.jpg')
   def tap(self):
      print ( 'The Machine, suck life out of creatures' )
      return True
class T34 (CreatureCard):
   def __init__ (self):
      super().__init__('creatures/t34Tank.jpg')
      self.flanking = True
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
   def __init__ (self,iAmHost):
        
      if iAmHost:
         broker = 'localhost'
         myName = 'host'
         target = 'player'
      else: # Windows computer 
         broker = 'localhost'
         myName = 'player'
         target = 'host'
      topic = 'messages'
      
      print ( '[broker,myName,target]: [' + broker + ',' + myName + ',' + target + ']')
      super().__init__(topic,broker,myName)
      
      '''
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
      '''
      
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
      (name,friendly) = selectCreature(['inplay'])
      if friendly != -1: 
         (name,enemy) = selectCreature(['opponent'])
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
               (ind,eInd) = deck.findSprite (data)
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
      self.manaLevel = {'red':14, 'black':10, 'green':0, 'white':0, 'blue':0, 'colorless': 0}
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
    
   # When you cast a creature you should call this procedure     
   def payMana (self, sheetIndex):     
      name = globalDictionary['cardInfo'].idToName (sheetIndex)       
      requiredMana = globalDictionary['cardInfo'].cards[name]
      self.manaCost.payMana (self.manaLevel, requiredMana)

from SubDecks import SubDecks 
class MTGDecks (SubDecks):
   #TODO: favor the enchantment over the creature and the last enchantment encountered.
   def findSprite (self,pos): 
      print ( 'MTGDecks.findSprite (' + str(pos) + ')' )
      found = ('',-1,-1)
      for deck in self.decks:           
         (index,enchantmentIndex) = deck.findSprite (pos)
         if index > -1:
            found = (deck,index,enchantmentIndex)
            break
            
      if found == ('',-1,-1):
         print ( 'No deck found with sprite associated with this position: ' + str(pos) ) 
      else:
         print ( 'SubDecks.findSprite, found: ' + str(found) ) 
         print ( 'SubDecks.findSprite, found a match at position: ' + str(pos) + ', found: ' + str(found)) 
         
      return found
   def reset (self):
      for deck in self.decks:           
         deck.reset()
   
'''
   MTGCards is based on SubDeck but customized to an MTG deck   
'''
class MTGCards (SubDeck):  
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, empty=False, name=''):
      numCards  = 0
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
      
         card.name              = globalDictionary['cardInfo'].idToName (card.sheetIndex)
         cardsInfo              = globalDictionary['cardInfo'].cards[card.name]
         card.toughness         = 0
         if 'toughness' in cardsInfo: 
            card.toughness      = cardsInfo['toughness']
            # print ( '[name,toughness]: [' + card.name + ',' + str(card.toughness) + ']')
         card.enchantments      = []
         card.damage            = 0
         if card.name in behaviors: 
            card.behavior = behaviors[card.name]
            card.behavior.container = card 
         else:
            print ( card.name + ' needs a behavior' )
            exit1()
               
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__')

   def addCardToDeck (self,card): 
      index = super().addCardToDeck (card)
      self.data[index].tapped       = card.tapped
      self.data[index].behavior     = card.behavior
      self.data[index].enchantments = card.enchantments
      self.data[index].toughness    = card.toughness
      self.data[index].damage       = card.damage
      self.data[index].name         = card.name 
      
      return index 
      
   def addCoverCard (self, labelText, name='cover.jpg'): 
      obj = super().addCoverCard (labelText, name)
      obj.tapped = False 
      
   def addData (self,d): 
      obj = super().addData(d)
      if hasattr (d,'tapped'): 
         obj.tapped = d.tapped 
      else:
         obj.tapped = False
      return obj
      
   def assignDamage (self):
      count = -1
      for card in self.data: 
         count = count + 1
         if card.damage != 0: 
            print ( card.name + ' has ' + str(card.damage) + ' it can handle: ' + str(card.toughness) + ' damage')          
            if card.damage >= card.toughness: 
               self.remove (count, True) # kill the creature and redeal 
               
   def cardName (self, sheetIndex):
      name = globalDictionary['cardInfo'].idToName (sheetIndex)
      print ( 'cardName returning: [' + name + ']' )
      return name
      
   def checkY (self):
      count = 0
      for card in self.data:       
         if count == 0: 
            y = card.y
         elif y != card.y: 
            print ( '\n***Got a mismatch! [y,card.y,count]: [' + str(y) + ',' + str(card.y) + ',' + str(count) + ']' )
            self.showInfo()
            count = count + 1
            raise Exception ( 'mismatch exception' )
         
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
      
   # This is probably only used by deck: drawPile    
   def dealCard (self,name): 
      if name == '':       
         topToDeck (globalDictionary['drawPile'], globalDictionary['hand'] )
      else:
         ind  = globalDictionary['drawPile'].findCard (name)
         if ind == -1: 
            print ( name + ' not found in drawPile!' )
         else:
            index = globalDictionary['hand'].addCardToDeck (globalDictionary['drawPile'].data[ind])
            globalDictionary['drawPile'].remove (ind) 
            
   def draw (self, debugIt=False):
      ind = -1 
      count = -1
      SubDeck.draw (self)
      
      
      for card in self.data:  
         count = count + 1
         sheetIndex = card.sheetIndex
         name = globalDictionary['cardInfo'].idToName (sheetIndex)  
         if hasattr (card, "counter"):  # Counter appears after being cast
            card.counter.draw()
         if hasattr (card, "enchantments"): 
            if len(card.enchantments) > 0: 
               # print ( 'Draw all enchantments for: ' + card.name )
               count = 0
               for c in card.enchantments:
                  count = count + 1
                  # print ( 'draw enchantment[' + str(count) + '] ' + c.name )
                  image = self.getImage (c)
                  self.displaySurface.blit (image, (c.x,c.y))             
         if hasattr (card.behavior,"damageCounter"): 
            card.behavior.damageCounter.draw(card.x,card.y)
            ind = count
      if debugIt: 
         if ind != -1:
             print ( 'The deck: [' + self.name + '] has a damage counter at index: ' + str(ind) + \
                     ' the name of the card is: ' + self.data[ind].name )
             self.showInfo()
             exit1()
                     
   def findSprite (self,pos,debugIt=False): 
      enchantmentIndex = -1
      found = (-1,-1)
      print ( 'Could not find it, so now check enchantments' )         
      x = pos[0]
      y = pos[1]
      index = -1
      for c in self.data:
         index = index + 1
         if hasattr (c,"enchantments"):
            enchantmentIndex = -1
            for card in c.enchantments:
               enchantmentIndex = enchantmentIndex + 1
               width  = card.width
               height = card.height
               rect = pygame.Rect (card.x, card.y, width,height)
               if rect.collidepoint (pos):
                  print ( 'FindSprite enchantment rect.collidepoint(pos): ' + str(rect) + '.collidepoint(' + str(pos) + ')' )                
                  print ( 'Found sprite at index: ' + str(index) + ' pos: ' + str(pos) + ' rect: ' + str(rect))
                  found = (index,enchantmentIndex)
       
      if found == (-1,-1):        
         index = super().findSprite (pos,debugIt)
         if index != -1:
            found = (index,-1)
                     
      return found
      
   def getImage (self,sprite):
      image = super().getImage (sprite)
      if sprite.tapped:          
         image = self.rotate (image,90) 
      sprite.width  = image.get_width()
      sprite.height = image.get_height()      
      return image                
   
   def getName (self, data):
      return self.cardName (data.sheetIndex)  

   def monitor (self):
      if not hasattr (self,"numDamages"):
         self.numDamages = 0

      count = 0 
      for card in self.data:
         if hasattr (card.behavior,"damageCounter"):
            count = count + 1
      if self.numDamages != count: 
         print ( '/n**** ' + self.name + ' has ' + str(count) + ' damaged cards' )
         exit1()
      self.numDamages = count
    
       
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
            
      print ( '\nMTGCards.redeal ***Show deck (' + self.name + ') after redeal' )       
      self.showInfo()
   
   def reset (self):
      for card in self.data:
         card.behavior.reset()      
                                    
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
          
   # untap all cards in the deck 
   def untap (self):
      print ( 'Untap all cards in deck: ' + self.name )
      for d in self.data: 
         d.tapped = False
         for enchantment in d.enchantments:
            enchantment.tapped = False 
         
   def summoned (self):
      print ( 'Untap all cards in deck: ' + self.name )
      for d in self.data: 
         d.behavior.summoningSickness = False
         
             
if __name__ == '__main__':
   from Deck               import Deck
   from Utilities          import Utilities
   from OptionBox          import OptionBox
   #from MTGDecks           import MTGDecks  defined above
   from TextBox            import TextBox
   from MTGSetup           import MTGSetup
   from Communications     import Communications
   import os
   import time  

   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 780))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   
   globalDictionary['mtgUtilities'] = MTGUtilities()
   globalDictionary['utilities']    = Utilities (displaySurface, BIGFONT)
   globalDictionary['cardInfo']     = CardInfo()

   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = 'images/mtg/redDeck.txt' # MTGSetup().chooseDeckFilename('redDeck.txt')
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
         
   drawPile.dealCard ('creatures/inigoMontoya.jpg'     )
   drawPile.dealCard ('enchantments/imposingVisage.jpg')
   drawPile.dealCard ('instants/molotov.png'           )   
   drawPile.dealCard ('creatures/pikachu.png'          )
   drawPile.dealCard ('creatures/pikachu.png'          )
   drawPile.dealCard ('creatures/jangoFett.jpg'        )

   while len(globalDictionary['hand'].data) < 7:    
      drawPile.dealCard ( '' )   
   
   globalDictionary['hand'].showAll() 
   globalDictionary['hand'].redeal(True)    
   
   cards=[]
   cards.append (drawPile)   
   
   cards.append (discardDeck)
   cards.append (globalDictionary['hand'])
   cards.append (globalDictionary['inplay'])
   cards.append (globalDictionary['opponent'])
   decks = MTGDecks (cards)    
   
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
   
   options        = ['host', 'player']
   comboBox       = OptionBox(options)
   result         = comboBox.run ()
   
   iAmHost = result == 'host'
   if iAmHost:
      globalDictionary['utilities'].setTitle ( 'You are host and move first' )
   else:
      globalDictionary['utilities'].setTitle ( 'You are player and move second' )
   comm = MTGCommunications (iAmHost)
   comm.sendDeck (hand, 'opponent' )
      
   # Move Daryl Dixon from drawPile to hand, and then cast it
   ind  = drawPile.findCard ( 'creatures/darylDixon.jpg')
   # card = drawPile.data[ind]
   print ( '\n***\nbefore moveToDeck, drawPile to hand...')
   drawPile.showInfo()
   print ('Before move, drawPile card located at [ind]: [' + str(ind) + ']' )
   print( drawPile.data[ind].name )
   if ind == -1: 
      print ( 'Daryl Dixon not found in drawPile!' )
      exit1()
   
   index = globalDictionary['inplay'].addCardToDeck (globalDictionary['drawPile'].retrieveCard(ind))
   globalDictionary['inplay'].data[index].hide = False 
   
   print ( 'index before remove: ' + str(index) )
   globalDictionary['drawPile'].remove (ind)
   print ( 'index after remove: ' + str(index) )
   drawPile.draw (True)
   
   print ( '\n***\nafter moveToDeck, drawPile to hand...' )
   drawPile.showInfo()
   drawPile.draw (True)
   drawPile.showInfo()
   drawPile.draw (True)
   print ( '\n***Check drawPile after moving darylDixon, ind:' + str(ind) )
   drawPile.checkY()
      
   print ( '\n***check hand early' )
   hand.redeal()
   hand.checkY()
   drawPile.draw (True)
      
   # Move rocket Tropper from drawPile to Inplay (Test purposes only)
   ind  = drawPile.findCard ( 'creatures/rocketTropper.jpg')
   if ind == -1: 
      print ( 'Could not find rocketTropper.jpg, TBD: pick another card' )
   else:   
   
      index = globalDictionary['opponent'].addCardToDeck (globalDictionary['drawPile'].retrieveCard(ind))
      globalDictionary['opponent'].data[index].hide = False 
      globalDictionary['opponent'].redeal()
      globalDictionary['drawPile'].remove (ind) 
      print ( '\n***Trooper moved to opponent deck' )      
   
   lastPhase = ''   
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      labels.show ()   
      actions.phase.draw()
      manaBar.draw()
      health.draw()
      decks.draw() # Show and set their x/y locations
      globalDictionary['drawPile'].monitor()
      
      globalDictionary['utilities'].showLastStatus()
      bar.show (['Quit', 'Message', 'Next Phase','Inplay'] )
      pygame.display.update() 
      if actions.phase.text == 'Draw': #Draw a card 
         topToDeck (globalDictionary['drawPile'], globalDictionary['hand'], reveal=True)
         globalDictionary['hand'].redeal() 
         actions.nextPhase()       
      elif actions.phase.text == 'Upkeep': 
         manaLevel = {'red':0, 'black':0, 'green':0, 'white':0, 'blue':0} # Reset mana level          
         decks.reset() # Reset all turn based values
         globalDictionary['inplay'].untap()
         globalDictionary['inplay'].summoned()
         globalDictionary['inplay'].redeal(True)
         actions.executePhase (globalDictionary['inplay'], 'Upkeep')      
         actions.nextPhase()
         print ( 'phase.text is now: ' + actions.phase.text )
         haveCastLand = False 
      elif (actions.phase.text == 'Assign Damage') and (lastPhase != 'Assign Damage'): 
         print ( 'Go through and assign damage' )
         globalDictionary['inplay'].assignDamage()
      lastPhase = actions.phase.text         
      
      events = globalDictionary['utilities'].readOne()
      for event in events:
         options = [] 
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
               elif bar.selection == 'Inplay':
                  globalDictionary['inplay'].showInfo()
               else:
                  print ( 'bar.selection not handled: [' + bar.selection + ']' )
               bar.selection = ''
            else: 
               (deck,index,eIndex) = decks.findSprite (data) # Returns index in list                         
               if deck == drawPile:
                  if actions.phase.text == 'Draw':               
                     deck.data[index].hide = False
                     card = globalDictionary['hand'].addCard (deck,index)
                     globalDictionary['hand'].redeal() 
                     deck.remove (index)
                     globalDictionary['hand'].revealTopCard()
                     actions.nextPhase()
                  else:
                     globalDictionary['utilities'].showStatus ( 'You can only draw in draw phase')                  
        
         elif typeInput == 'select': 
            # Determine which subdeck the card is in. 

            (deck,index,eIndex) = decks.findSprite (data) 
            try:
               if index == -1: 
                  print ( 'Could not find a deck for selection' )
               else:
                  card = deck.data[index]                             
                  if eIndex != -1:
                     card = card.enchantments[eIndex]
            except Exception as ex:
               print ( 'Exception : ' + str(ex)) 
               
            if index != -1: # A card was clicked on 
               print ( 'card.name: ' + card.name )
               x = card.x
               y = card.y
               sheetIndex = card.sheetIndex                        

               optionBox = OptionBox ( ['Unknown'] )
               print ( 'Deck selected: ' + deck.name )
               if deck.name == 'hand': 
                  print ( card.name + ' isLand: ' + str(card.behavior.isLand) )  
                  options = [] 
                  # options = card.behavior.specialEffects, not sure why this doesn't work
                  for effect in card.behavior.specialEffects:
                     options.append (effect)
                  options.append ( 'View' )
                  if card.behavior.isLand:  
                     if haveCastLand: 
                        print ( 'Already cast a land this turn' )                           
                     else: 
                        options.append ( 'Cast' )
                  elif manaBar.canCast (sheetIndex) or card.behavior.isLand: 
                     if globalDictionary['cardInfo'].isEnchantCreature (sheetIndex):
                        if (globalDictionary['inplay'].countType ('creatures') > 0) or \
                           (globalDictionary['opponent'].countType ('creatures') > 0): 
                           options.append ('Cast')
                     elif globalDictionary['cardInfo'].isEnchantPermanent(sheetIndex):
                        if globalDictionary['inplay'].length() > 0: 
                           options.append ( 'Cast' )
                     else:
                        options.append ( 'Cast' )
                  options.append ( 'Cancel') 
                  optionBox = globalDictionary['utilities'].selectOption (options)   
               elif deck == globalDictionary['inplay']: 
                  print ( 'Clicked on a card in play' )
                  if card.tapped: 
                     optionBox = globalDictionary['utilities'].selectOption (['View', 'Untap', 'Cancel'])
                  else:
                     options = ['View']
                     if card.behavior.tapEffects:   
                        options.append ( 'Tap' )
                     if card.behavior.isCreature:    
                        if not card.behavior.summoningSickness:                         
                           options.append ( 'Attack' ) 
                        options.append ( 'Block' )
                     options.append ( 'Cancel' )
                     optionBox = globalDictionary['utilities'].selectOption (options)
               # Handle user action selection 
               selection = optionBox.getSelection()
               print ( '[selection]: [' + selection + ']' ) 
               if selection == 'Attack':
                  card.behavior.attack()
                  globalDictionary['inplay'].redeal()                  
               elif selection == 'Cast':                            
                  if card.behavior.isLand: 
                     haveCastLand = True 
                  card.behavior.cast()   
               elif selection == 'View':                 
                  deck.view (sheetIndex, 'images/mtg/' + card.name)               
               elif selection == 'Untap': 
                  card.tapped = False 
                  globalDictionary['inplay'].redeal()                  
                  for enchantment in card.enchantments:
                     enchantment.tapped = False
               elif selection == 'Tap':  
                  card.behavior.tap()
                  # deck.tap (index, True) # Call to MTGCards
                  deck.redeal()                     
         else:
            print ( 'event: ' + typeInput)
            
print ( 'All done doing a disconnect...' )
comm.disconnect()