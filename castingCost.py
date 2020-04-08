import random
import copy
class castingCost: 
   cost = { \
      'images/mtg/creatures/agentSmith.jpg':{'toCast':['4','black','black']}, \
      'images/mtg/creatures/alGore.jpg':{'toCast':['green','green']}, \
      'images/mtg/creatures/americanEagle.jpg':{'toCast':['3','white','blue','red']}, \
      'images/mtg/creatures/android17.png':{'toCast':['2','red','red']}, \
      'images/mtg/creatures/android18.png':{'toCast':['2','white','red']}, \
      'images/mtg/creatures/annoyingOrange.jpg':{'toCast':['green','blue','red']}, \
      'images/mtg/creatures/arbalestElite.jpg':{'toCast':['2','white','white']}, \
      'images/mtg/creatures/arrgh.jpg':{'toCast':['black','black','black']}, \
      'images/mtg/creatures/arthurKingOfTheBritains.jpg':{'toCast':['3','white','white']}, \
      'images/mtg/creatures/barackHObama.jpg':{'toCast':['1','red']}, \
      'images/mtg/creatures/barackObama.jpg':{'toCast':[['green','blue'],['green','blue'],['green','blue'],['white','blue'],['white','blue'],['white','blue']]}, \
      'images/mtg/creatures/barackObamaII.jpg':{'toCast':['3','black']}, \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':{'toCast':['white','blue','red']}, \
      'images/mtg/creatures/batman.jpg':{'toCast':['3','white','blue']}, \
      'images/mtg/creatures/batmanII.jpg':{'toCast':['3',['white','black'],['white','black'],['white','black']]}, \
      'images/mtg/creatures/berneyStinson.jpg':{'toCast':['red','red']}, \
      'images/mtg/creatures/bernieSanders.jpg':{'toCast':['2','white','white']}, \
      'images/mtg/creatures/bernieSandersII.jpg':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/bickeringGiant.jpg':{'toCast':['black','green','red']}, \
      'images/mtg/creatures/biffTannen.jpg':{'toCast':['4','black','red']}, \
      'images/mtg/creatures/blackKnight.jpg':{'toCast':['1','black','black']}, \
      'images/mtg/creatures/borgCube.jpg':{'toCast':['4','black','black']}, \
      'images/mtg/creatures/borgQueen.jpg':{'toCast':['white','white','black','black','blue','blue','blue']}, \
      'images/mtg/creatures/bruceLee.jpg':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/burninator.jpg':{'toCast':['9','red']}, \
      'images/mtg/creatures/cantinaBand.jpg':{'toCast':['white']}, \
      'images/mtg/creatures/captainAmerica.jfif':{'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/charlesXavier.jpg':{'toCast':['2','white','blue','blue']}, \
      'images/mtg/creatures/cheatyFace.jpg':{'toCast':['blue','blue']}, \
      'images/mtg/creatures/chivalrousChevalier.jpg':{'toCast':['4','white']}, \
      'images/mtg/creatures/chuckNorris.jpg':{'toCast':['9','green']}, \
      'images/mtg/creatures/conanTheBarbarian.png':{'toCast':['2','red','red']}, \
      'images/mtg/creatures/conanTheLibrarian.png':{'toCast':['4','red','red']}, \
      'images/mtg/creatures/countTyroneRugen.jpg':{'toCast':['black','black','red']}, \
      'images/mtg/creatures/cowardlyLion.png':{'toCast':['green']}, \
      'images/mtg/creatures/daenerysStormborn.jpg':{'toCast':['1','white','black','green','red']}, \
      'images/mtg/creatures/darthSidious.jpg':{'toCast':['4','black','blue','red']}, \
      'images/mtg/creatures/darthVader.jpg':{'toCast':['5','black','black','black','black','black']}, \
      'images/mtg/creatures/darkHelmet.jpg':{'toCast':['3','black','black','blue']}, \
      'images/mtg/creatures/darylDixon.jpg':{'toCast':['red','red','red','red','red']}, \
      'images/mtg/creatures/deadPool.png':{'toCast':['2','black','red','red']}, \
      'images/mtg/creatures/deadPoolAgain.jpg':{'toCast':['3','black','red']}, \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':{'toCast':['1','black','red']}, \
      'images/mtg/creatures/deadPoolIII.png':{'toCast':['4','black','red']}, \
      'images/mtg/creatures/dickJones.png':{'toCast':['3','black','black']}, \
      'images/mtg/creatures/doctorEmmettBrown.jpg':{'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/doge.jpg':{'toCast':['1']}, \
      'images/mtg/creatures/donkeyKong.png':{'toCast':['5','green','red']}, \
      'images/mtg/creatures/drHouse.jpg':{'toCast':['5','white','white','white']}, \
      'images/mtg/creatures/drStrange.jpg':{'toCast':['1','white','black','blue']}, \
      'images/mtg/creatures/earlOfSquirrel.jpg':{'toCast':['4','green','green']}, \
      'images/mtg/creatures/extremelySlowZombie.jpg':{'toCast':['1','black']}, \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':{'toCast':['1','white','green','red']}, \
      'images/mtg/creatures/frieza.jpg':{'toCast':['black','blue','blue']}, \
      'images/mtg/creatures/galactus.jpg':{'toCast':['10']}, \
      'images/mtg/creatures/gameStoreEmployee.jpg':{'toCast':['blue','blue']}, \
      'images/mtg/creatures/gandalf.png':{'toCast':['2','white','blue']}, \
      'images/mtg/creatures/generalGrievous.jpg':{'toCast':['white','black','blue']}, \
      'images/mtg/creatures/georgeBushII.jpg':{'toCast':['white','blue','red']}, \
      'images/mtg/creatures/georgeMcfly.jpg':{'toCast':['1','white','blue']}, \
      'images/mtg/creatures/georgeWBush.jpg':{'toCast':['red']}, \
      'images/mtg/creatures/god.png':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/godzilla.jpg':{'toCast':['5','green','blue','red']}, \
      'images/mtg/creatures/gordonRamsey.jpg':{'toCast':['3','red']}, \
      'images/mtg/creatures/hangman.jpg':{'toCast':['black']}, \
      'images/mtg/creatures/hanSolo.jpg':{'toCast':['3','white']}, \
      'images/mtg/creatures/hela.png':{'toCast':['4',['black','red'],'green']}, \
      'images/mtg/creatures/hillaryClinton.jpeg':{'toCast':['2','white','red']}, \
      'images/mtg/creatures/hirohito.png':{'toCast':['3','red','white']}, \
      'images/mtg/creatures/hitler.jpg':{'toCast':['black','black','black','black']}, \
      'images/mtg/creatures/hulk.png':{'toCast':['green','green','green','green','green','green']}, \
      'images/mtg/creatures/iKnowKungFu.jpg':{'toCast':['3','green']}, \
      'images/mtg/creatures/indianaJones.jpg':{'toCast':['1','white','blue']}, \
      'images/mtg/creatures/infinityElemental.jpg':{'toCast':['4','red','red','red']}, \
      'images/mtg/creatures/inigoMontoya.jpg':{'toCast':['2',['red','white'],['red','white']]}, \
      'images/mtg/creatures/inigoMontoyaII.jpg':{'toCast':['white','green','red']}, \
      'images/mtg/creatures/ironMan.png':{'toCast':['2','white','red','red']}, \
      'images/mtg/creatures/ironManII.jpg':{'toCast':['5','white','red']}, \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':{'toCast':['5','red']}, \
      'images/mtg/creatures/jaceTheAsshole.jpg':{'toCast':['blue']}, \
      'images/mtg/creatures/jamesKirk.png':{'toCast':['1','white',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/jangoFett.jpg':{'toCast':['2','red','red']}, \
      'images/mtg/creatures/jeanGrey.jpg':{'toCast':['3','black','red']}, \
      'images/mtg/creatures/johnLennon.jpg':{'toCast':['3',['green','blue'],['green','blue']]}, \
      'images/mtg/creatures/johnnyCash.jpg':{'toCast':['3',['white','black'],['white','black']]}, \
      'images/mtg/creatures/johnnyCombo.png':{'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/josefStalin.png':{'toCast':['8','red','red']}, \
      'images/mtg/creatures/joshLane.jpg':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/kanyeWest.png':{'toCast':['black']}, \
      'images/mtg/creatures/killerBunny.jpg':{'toCast':['white']}, \
      'images/mtg/creatures/kingKong.jpg':{'toCast':['3','green']}, \
      'images/mtg/creatures/kittyPryde.jpg':{'toCast':['2','white','blue']}, \
      'images/mtg/creatures/koolAidMan.jpg':{'toCast':['2','red','red']}, \
      'images/mtg/creatures/krillin.jpg':{'toCast':['white']}, \
      'images/mtg/creatures/libyanTerrorists.jpg':{'toCast':['4','red','red']}, \
      'images/mtg/creatures/logan.jpg':{'toCast':['3',['red','green'],['red','green']]}, \
      'images/mtg/creatures/lordVoldemort.jpg':{'toCast':['3','black','black','black']}, \
      'images/mtg/creatures/magneto.jpg':{'toCast':['3','black','blue','red']}, \
      'images/mtg/creatures/mario.jpg':{'toCast':['3','red','red']}, \
      'images/mtg/creatures/masterChief.png':{'toCast':['2','black','red']}, \
      'images/mtg/creatures/martyMcFly.jpg':{'toCast':['2','white','red']}, \
      'images/mtg/creatures/memePirate.jpeg':{'toCast':['2','blue','red']}, \
      'images/mtg/creatures/miracleMax.jpg':{'toCast':['white','blue']}, \
      'images/mtg/creatures/mrT.jpg':{'toCast':['4','white','red']}, \
      'images/mtg/creatures/mrTII.jpg':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/mtgPlayer.png':{'toCast':['2']}, \
      'images/mtg/creatures/mysterioIllusionist.png':{'toCast':['blue','blue','blue']}, \
      'images/mtg/creatures/mystique.jpg':{'toCast':['3','black','blue','blue']}, \
      'images/mtg/creatures/mythBusters.jpg':{'toCast':['3','red','red']}, \
      'images/mtg/creatures/nerdyPlayer.jpeg':{'toCast':['3','black','black']}, \
      'images/mtg/creatures/noviceBountyHunter.jpg':{'toCast':['1','red']}, \
      'images/mtg/creatures/obiWanKenobi.jpg':{'toCast':['2','white','green','blue']}, \
      'images/mtg/creatures/patton.png':{'toCast':['2','green','green']}, \
      'images/mtg/creatures/peasants.png':{'toCast':['1','white','green']}, \
      'images/mtg/creatures/peeweeHerman.jpg':{'toCast':['1','white','red']}, \
      'images/mtg/creatures/pepe.jpg':{'toCast':['black']}, \
      'images/mtg/creatures/pikachu.png':{'toCast':[['blue','red'], ['blue','red']]}, \
      'images/mtg/creatures/pizzaTheHutt.jpg':{'toCast':['3','black','green']}, \
      'images/mtg/creatures/princeHumperdinck.jpg':{'toCast':['3','black','black']}, \
      'images/mtg/creatures/princessButtercup.jpg':{'toCast':['white','white','green','green']}, \
      'images/mtg/creatures/princessLeia.jpg':{'toCast':['3','white','green','blue']}, \
      'images/mtg/creatures/raichu.jpg':{'toCast':['4','white','red']}, \
      'images/mtg/creatures/ragePlayer.jpeg':{'toCast':['red','red','red']}, \
      'images/mtg/creatures/ralphNader.jpg':{'toCast':['black','green']}, \
      'images/mtg/creatures/redForman.jpg':{'toCast':['red','red',]}, \
      'images/mtg/creatures/rickGrimes.png':{'toCast':['2','white','green']}, \
      'images/mtg/creatures/riddick.jfif':{'toCast':['2','black','red']}, \
      'images/mtg/creatures/robocop.jpg':{'toCast':['4','white']}, \
      'images/mtg/creatures/rocketTropper.jpg':{'toCast':['1','red']}, \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':{'toCast':['black']}, \
      'images/mtg/creatures/samuelJackson.jpg':{'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/santaClaus.jpg':{'toCast':['2','green','green']}, \
      'images/mtg/creatures/scorpionKing.png':{'toCast':['3','black','red']}, \
      'images/mtg/creatures/secretGamer.jpeg':{'toCast':['white','white','white','white']}, \
      'images/mtg/creatures/seleneBloodDrainer.png':{'toCast':['3','white','black','blue']}, \
      'images/mtg/creatures/shermanTank.png':{'toCast':['4','blue','blue']}, \
      'images/mtg/creatures/silverSurfer.png':{'toCast':['1','white','black','green','blue','red']}, \
      'images/mtg/creatures/sirBedevere.jpg':{'toCast':['white','blue']}, \
      'images/mtg/creatures/sirRobin.png':{'toCast':['white','blue']}, \
      'images/mtg/creatures/spaceMarineCaptain.png':{'toCast':['3','white','red']}, \
      'images/mtg/creatures/spiderman.jpg':{'toCast':['2',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/spidermanII.png':{'toCast':['3','blue','red']}, \
      'images/mtg/creatures/spock.png':{'toCast':['2','white','blue']}, \
      'images/mtg/creatures/steveAustin.png':{'toCast':['1','white','black','red']}, \
      'images/mtg/creatures/stevenRogers.jpg':{'toCast':['1','white','white','white']}, \
      'images/mtg/creatures/superBattleDroid.jpg':{'toCast':['5','blue']}, \
      'images/mtg/creatures/superman.gif':{'toCast':['3','blue','blue']}, \
      'images/mtg/creatures/supermanII.jpg':{'toCast':['2','white','white','white','white']}, \
      'images/mtg/creatures/t34Tank.jpg':{'toCast':['2','red']}, \
      'images/mtg/creatures/thanos.jpg':{'toCast':['5','black','black']}, \
      'images/mtg/creatures/theCollector.jpeg':{'toCast':['1','green','green']}, \
      'images/mtg/creatures/theJoker.jpg':{'toCast':[['black','red'],['black','red'], ['black','red'], ['black','red']]}, \
      'images/mtg/creatures/theOracle.jpg':{'toCast':['1','blue','blue']}, \
      'images/mtg/creatures/theSilence.jpg':{'toCast':['4','black']}, \
      'images/mtg/creatures/thor.jpg':{'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/thorGodOfThunder.png':{'toCast':['6',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/thorSonOfOdin.png':{'toCast':['4','white','green']}, \
      'images/mtg/creatures/timmyPowerGamer.jpg':{'toCast':['2','green','green']}, \
      'images/mtg/creatures/tigerTank.png':{'toCast':['8']}, \
      'images/mtg/creatures/tinman.png':{'toCast':['3']}, \
      'images/mtg/creatures/toughNerd.jpeg':{'toCast':['2','red','red','red']}, \
      'images/mtg/creatures/tournamentGrinder.jpg':{'toCast':['2','black','black']}, \
      'images/mtg/creatures/tribble.png':{'toCast':['1','white']}, \
      'images/mtg/creatures/trooperCommander.jpg':{'toCast':['2','green']}, \
      'images/mtg/creatures/trump.jpg':{'toCast':['1','white','blue','red']}, \
      'images/mtg/creatures/unwillingVolunteer.jpg':{'toCast':['1','green']}, \
      'images/mtg/creatures/vegeta.png':{'toCast':['black','green','red']}, \
      'images/mtg/creatures/vespaDruishPrincess.jpg':{'toCast':['green','green']}, \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':{'toCast':['black','blue','red']}, \
      'images/mtg/creatures/wallOfTrump.png':{'toCast':['white','white','blue','blue']}, \
      'images/mtg/creatures/warriorBug.png':{'toCast':['1','green','red']}, \
      'images/mtg/creatures/weepingStatue.jpg':{'toCast':['4']}, \
      'images/mtg/creatures/westleyMasterofEverything.jpg':{'toCast':['green','blue','red']}, \
      'images/mtg/creatures/youngChild.jpeg':{'toCast':['white']} \
   }
   def __init__(self):
      pass
      
   def actualCost (self,filename):
      return self.cost[filename]['toCast']      
      
   def totalManaCost(self,filename):
      if filename.find ( '/lands' ) > -1: 
         total = 0
      else:         
         list = self.actualCost(filename)
         total = 1
         if list[0].isnumeric():
            total = int(list[0])
            
         total = total + len(list) - 1
      return total
      
   def sufficientManaToCast ( self, manaPool, filename):
      manaList = copy.deepcopy(manaPool)
      sufficient = False
      if filename.find ( '/lands/' ) == -1: # lands are not cast just put in play
         cost = self.actualCost(filename)
         print ( 'Can i cast: ' + filename + ' with cost: ' + str(cost) + \
                 ' using: ' + str(manaList) + '?')
         numColorless = 0
         sufficient = True 
         # Check each individual required mana cost
         for mana in cost: 
            paid = False
            if isinstance(mana, list): # item could be one of two 
               for m in mana:
                  if m in manaList:
                     manaList.remove(m)
                     paid = True 
                     break
            else: 
               if mana.isnumeric():
                  numColorless = int(mana)
                  paid = True # Wait until the end 
               elif mana in manaList:
                  manaList.remove(mana)
                  paid = True
                  
            if not paid:         
               sufficient = False
               break
         if paid: 
            if len(manaList) < numColorless:
               sufficient =  False
               print ( "Not enough remaining mana " + str(manaList) + \
                       " to pay colorless: " + str(numColorless) )      
         else:
            print ( 'Did not have enough base colors to pay: ' + str(cost) )
      if sufficient: 
         print ( 'Yes most definately' )
      return sufficient                           
      
   def allCards(self):
      cards = []
      indexes = []
      count = 0      
      for key in self.cost:
         cards.append ( {'index':count,'iOwnIt':True, 'filename':key, \
                         'location':'library', 'tapped':False, \
                         'summoned':False} )
         indexes.append (count)
         count = count + 1
      return (cards,indexes)
            
   def baseCost ( self, filename ):
      base = []
      casting = self.actualCost(filename)
      for color in casting: 
         if isinstance(color, list):
            print ( "This is a list: " + str(color) )
            for c in color:
               print ( 'c: ' + c )
               if c not in base: 
                  base.append(c)                 
         else:
            if not color.isnumeric(): 
               if color not in base:             
                  base.append(color)
      base.sort()            
      return base
   
   def matchingCards (self,filename):    
      matches = []
      casting = self.baseCost(filename)
      casting.sort()
      print ( 'casting for ' + filename + ' is: ' + str( casting ))
      #check all Creature Cards 
      for key in self.cost:
         if self.baseCost(key) == casting: 
            matches.append (key) 
         else:
            #Check if match on single color
            for mono in casting: 
               if self.baseCost(key) == [mono]:
                  matches.append (key)
                  break

      return matches
      
   def buildDeck (self,filename): 
      deck = []
      creatures = self.matchingCards (filename)
      colors = self.baseCost(filename)
      maxCreatures = 30
      # continue until you have enough creatures
      count = 0
      while len(deck) < maxCreatures: 
         # For each creature 
         deck.append ( creatures[count] ) 
         count = count + 1
         count = count % len(creatures)
            
      # Add Lands      
      maxLands = 20 
      while len (deck) < (maxCreatures + maxLands):
         for color in colors: 
            deck.append ('images/mtg/lands/' + color + '.jpg') 
            if len(deck) == (maxCreatures + maxLands): 
               break

      # Add instants/sorceries/artifacts               
      print ( "Built a deck: " + str(deck) )      
      return deck 

   def getRandomIndex (self,list): 
      num = int ( random.random() * len(list))
      return num

   def dealCard (self,list): 
      card = []
      index = self.getRandomIndex (list)
      item = list[index]
      card.append (item)
      list.remove (item)    
      return (card,list)       
      
   def dealHand (self,list): 
      hand = []
      for i in range(7):
         (card,list) = self.dealCard (list)
         hand = hand + card
      return (hand,list)  

         

      