import random
import copy
class castingCost: 
   cost = { \
      'images/mtg/creatures/agentSmith.jpg':{'power':6, 'toughness':6,'toCast':['4','black','black']}, \
      'images/mtg/creatures/alGore.jpg':{'power':1, 'toughness':1,'toCast':['green','green']}, \
      'images/mtg/creatures/americanEagle.jpg':{'power':2, 'toughness':2,'toCast':['3','white','blue','red']}, \
      'images/mtg/creatures/android17.png':{'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/android18.png':{'power':2, 'toughness':2,'toCast':['2','white','red']}, \
      'images/mtg/creatures/annoyingOrange.jpg':{'power':1, 'toughness':1,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/arrgh.jpg':{'power':5, 'toughness':5,'toCast':['black','black','black']}, \
      'images/mtg/creatures/arthurKingOfTheBritains.jpg':{'power':4, 'toughness':5,'toCast':['3','white','white']}, \
      'images/mtg/creatures/barackHObama.jpg':{'power':0, 'toughness':6,'toCast':['1','red']}, \
      'images/mtg/creatures/barackObama.jpg':{'power':3, 'toughness':7,'toCast':[['green','blue'],['green','blue'],['green','blue'],['white','blue'],['white','blue'],['white','blue']]}, \
      'images/mtg/creatures/barackObamaII.jpg':{'power':1, 'toughness':1,'toCast':['3','black']}, \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':{'power':3, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/batman.jpg':{'power':5, 'toughness':5,'toCast':['3','white','blue']}, \
      'images/mtg/creatures/batmanII.jpg':{'power':5, 'toughness':4,'toCast':['3',['white','black'],['white','black'],['white','black']]}, \
      'images/mtg/creatures/berneyStinson.jpg':{'power':4, 'toughness':1,'toCast':['red','red']}, \
      'images/mtg/creatures/bernieSanders.jpg':{'power':5, 'toughness':8,'toCast':['2','white','white']}, \
      'images/mtg/creatures/bernieSandersII.jpg':{'power':20, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/bickeringGiant.jpg':{'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/biffTannen.jpg':{'power':5, 'toughness':5,'toCast':['4','black','red']}, \
      'images/mtg/creatures/blackKnight.jpg':{'power':0, 'toughness':2,'toCast':['1','black','black']}, \
      'images/mtg/creatures/borgCube.jpg':{'power':1, 'toughness':1,'toCast':['4','black','black']}, \
      'images/mtg/creatures/borgQueen.jpg':{'power':5, 'toughness':5,'toCast':['white','white','black','black','blue','blue','blue']}, \
      'images/mtg/creatures/bruceLee.jpg':{'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/burninator.jpg':{'power':9, 'toughness':9,'toCast':['9','red']}, \
      'images/mtg/creatures/cantinaBand.jpg':{'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/captainAmerica.jfif':{'power':2, 'toughness':2,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/charlesXavier.jpg':{'power':2, 'toughness':4,'toCast':['2','white','blue','blue']}, \
      'images/mtg/creatures/cheatyFace.jpg':{'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/chivalrousChevalier.jpg':{'power':3, 'toughness':3,'toCast':['4','white']}, \
      'images/mtg/creatures/chuckNorris.jpg':{'power':99, 'toughness':99,'toCast':['9','green']}, \
      'images/mtg/creatures/conanTheBarbarian.png':{'power':3, 'toughness':3,'toCast':['2','red','red']}, \
      'images/mtg/creatures/conanTheLibrarian.png':{'power':4, 'toughness':5,'toCast':['4','red','red']}, \
      'images/mtg/creatures/countTyroneRugen.jpg':{'power':3, 'toughness':4,'toCast':['black','black','red']}, \
      'images/mtg/creatures/cowardlyLion.png':{'power':1, 'toughness':5,'toCast':['green']}, \
      'images/mtg/creatures/daenerysStormborn.jpg':{'power':2, 'toughness':2,'toCast':['1','white','black','green','red']}, \
      'images/mtg/creatures/darthSidious.jpg':{'power':5, 'toughness':5,'toCast':['4','black','blue','red']}, \
      'images/mtg/creatures/darthVader.jpg':{'power':13, 'toughness':13,'toCast':['5','black','black','black','black','black']}, \
      'images/mtg/creatures/darkHelmet.jpg':{'power':4, 'toughness':5,'toCast':['3','black','black','blue']}, \
      'images/mtg/creatures/darylDixon.jpg':{'power':6, 'toughness':6,'toCast':['red','red','red','red','red']}, \
      'images/mtg/creatures/deadPool.png':{'power':3, 'toughness':3,'toCast':['2','black','red','red']}, \
      'images/mtg/creatures/deadPoolAgain.jpg':{'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':{'power':3, 'toughness':3,'toCast':['1','black','red']}, \
      'images/mtg/creatures/deadPoolIII.png':{'power':3, 'toughness':3,'toCast':['4','black','red']}, \
      'images/mtg/creatures/dickJones.png':{'power':3, 'toughness':3,'toCast':['3','black','black']}, \
      'images/mtg/creatures/doctorEmmettBrown.jpg':{'power':3, 'toughness':3,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/doge.jpg':{'power':3, 'toughness':3,'toCast':['1']}, \
      'images/mtg/creatures/donkeyKong.png':{'power':3, 'toughness':3,'toCast':['5','green','red']}, \
      'images/mtg/creatures/drHouse.jpg':{'power':3, 'toughness':3,'toCast':['5','white','white','white']}, \
      'images/mtg/creatures/drStrange.jpg':{'power':3, 'toughness':3,'toCast':['1','white','black','blue']}, \
      'images/mtg/creatures/earlOfSquirrel.jpg':{'power':3, 'toughness':3,'toCast':['4','green','green']}, \
      'images/mtg/creatures/extremelySlowZombie.jpg':{'power':3, 'toughness':3,'toCast':['1','black']}, \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':{'power':3, 'toughness':3,'toCast':['1','white','green','red']}, \
      'images/mtg/creatures/frieza.jpg':{'power':3, 'toughness':3,'toCast':['black','blue','blue']}, \
      'images/mtg/creatures/galactus.jpg':{'power':3, 'toughness':3,'toCast':['10']}, \
      'images/mtg/creatures/gameStoreEmployee.jpg':{'power':3, 'toughness':3,'toCast':['blue','blue']}, \
      'images/mtg/creatures/gandalf.png':{'power':3, 'toughness':3,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/generalGrievous.jpg':{'power':3, 'toughness':3,'toCast':['white','black','blue']}, \
      'images/mtg/creatures/georgeBushII.jpg':{'power':3, 'toughness':3,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/georgeMcfly.jpg':{'power':3, 'toughness':3,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/georgeWBush.jpg':{'power':3, 'toughness':3,'toCast':['red']}, \
      'images/mtg/creatures/god.png':{'power':3, 'toughness':3,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/godzilla.jpg':{'power':3, 'toughness':3,'toCast':['5','green','blue','red']}, \
      'images/mtg/creatures/gordonRamsey.jpg':{'power':3, 'toughness':3,'toCast':['3','red']}, \
      'images/mtg/creatures/hangman.jpg':{'power':3, 'toughness':3,'toCast':['black']}, \
      'images/mtg/creatures/hanSolo.jpg':{'power':3, 'toughness':3,'toCast':['3','white']}, \
      'images/mtg/creatures/hela.png':{'power':3, 'toughness':3,'toCast':['4',['black','red'],'green']}, \
      'images/mtg/creatures/hillaryClinton.jpeg':{'power':3, 'toughness':3,'toCast':['2','white','red']}, \
      'images/mtg/creatures/hirohito.png':{'power':3, 'toughness':3,'toCast':['3','red','white']}, \
      'images/mtg/creatures/hitler.jpg':{'power':3, 'toughness':3,'toCast':['black','black','black','black']}, \
      'images/mtg/creatures/hulk.png':{'power':3, 'toughness':3,'toCast':['green','green','green','green','green','green']}, \
      'images/mtg/creatures/iKnowKungFu.jpg':{'power':3, 'toughness':3,'toCast':['3','green']}, \
      'images/mtg/creatures/indianaJones.jpg':{'power':3, 'toughness':3,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/infinityElemental.jpg':{'power':3, 'toughness':3,'toCast':['4','red','red','red']}, \
      'images/mtg/creatures/inigoMontoya.jpg':{'power':3, 'toughness':3,'toCast':['2',['red','white'],['red','white']]}, \
      'images/mtg/creatures/inigoMontoyaII.jpg':{'power':3, 'toughness':3,'toCast':['white','green','red']}, \
      'images/mtg/creatures/ironMan.png':{'power':3, 'toughness':3,'toCast':['2','white','red','red']}, \
      'images/mtg/creatures/ironManII.jpg':{'power':3, 'toughness':3,'toCast':['5','white','red']}, \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':{'power':3, 'toughness':3,'toCast':['5','red']}, \
      'images/mtg/creatures/jaceTheAsshole.jpg':{'power':3, 'toughness':3,'toCast':['blue']}, \
      'images/mtg/creatures/jamesKirk.png':{'power':3, 'toughness':3,'toCast':['1','white',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/jangoFett.jpg':{'power':3, 'toughness':3,'toCast':['2','red','red']}, \
      'images/mtg/creatures/jeanGrey.jpg':{'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/johnLennon.jpg':{'power':3, 'toughness':3,'toCast':['3',['green','blue'],['green','blue']]}, \
      'images/mtg/creatures/johnnyCash.jpg':{'power':3, 'toughness':3,'toCast':['3',['white','black'],['white','black']]}, \
      'images/mtg/creatures/johnnyCombo.png':{'power':3, 'toughness':3,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/josefStalin.png':{'power':3, 'toughness':3,'toCast':['8','red','red']}, \
      'images/mtg/creatures/joshLane.jpg':{'power':3, 'toughness':3,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/kanyeWest.png':{'power':3, 'toughness':3,'toCast':['black']}, \
      'images/mtg/creatures/killerBunny.jpg':{'power':3, 'toughness':3,'toCast':['white']}, \
      'images/mtg/creatures/kingKong.jpg':{'power':3, 'toughness':3,'toCast':['3','green']}, \
      'images/mtg/creatures/kittyPryde.jpg':{'power':3, 'toughness':3,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/koolAidMan.jpg':{'power':3, 'toughness':3,'toCast':['2','red','red']}, \
      'images/mtg/creatures/krillin.jpg':{'power':0, 'toughness':3,'toCast':['white']}, \
      'images/mtg/creatures/libyanTerrorists.jpg':{'power':3, 'toughness':3,'toCast':['4','red','red']}, \
      'images/mtg/creatures/logan.jpg':{'power':3, 'toughness':3,'toCast':['3',['red','green'],['red','green']]}, \
      'images/mtg/creatures/lordVoldemort.jpg':{'power':3, 'toughness':3,'toCast':['3','black','black','black']}, \
      'images/mtg/creatures/magneto.jpg':{'power':3, 'toughness':3,'toCast':['3','black','blue','red']}, \
      'images/mtg/creatures/mario.jpg':{'power':3, 'toughness':3,'toCast':['3','red','red']}, \
      'images/mtg/creatures/masterChief.png':{'power':3, 'toughness':3,'toCast':['2','black','red']}, \
      'images/mtg/creatures/martyMcFly.jpg':{'power':3, 'toughness':3,'toCast':['2','white','red']}, \
      'images/mtg/creatures/memePirate.jpeg':{'power':3, 'toughness':3,'toCast':['2','blue','red']}, \
      'images/mtg/creatures/miracleMax.jpg':{'power':3, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/mrT.jpg':{'power':3, 'toughness':3,'toCast':['4','white','red']}, \
      'images/mtg/creatures/mrTII.jpg':{'power':3, 'toughness':3,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/mtgPlayer.png':{'power':3, 'toughness':3,'toCast':['2']}, \
      'images/mtg/creatures/mysterioIllusionist.png':{'power':3, 'toughness':3,'toCast':['blue','blue','blue']}, \
      'images/mtg/creatures/mystique.jpg':{'power':3, 'toughness':3,'toCast':['3','black','blue','blue']}, \
      'images/mtg/creatures/mythBusters.jpg':{'power':3, 'toughness':3,'toCast':['3','red','red']}, \
      'images/mtg/creatures/nerdyPlayer.jpeg':{'power':3, 'toughness':3,'toCast':['3','black','black']}, \
      'images/mtg/creatures/noviceBountyHunter.jpg':{'power':3, 'toughness':3,'toCast':['1','red']}, \
      'images/mtg/creatures/obiWanKenobi.jpg':{'power':3, 'toughness':3,'toCast':['2','white','green','blue']}, \
      'images/mtg/creatures/patton.png':{'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/peasants.png':{'power':3, 'toughness':3,'toCast':['1','white','green']}, \
      'images/mtg/creatures/peeweeHerman.jpg':{'power':3, 'toughness':3,'toCast':['1','white','red']}, \
      'images/mtg/creatures/pepe.jpg':{'power':3, 'toughness':3,'toCast':['black']}, \
      'images/mtg/creatures/pikachu.png':{'power':3, 'toughness':3,'toCast':[['blue','red'], ['blue','red']]}, \
      'images/mtg/creatures/pizzaTheHutt.jpg':{'power':3, 'toughness':3,'toCast':['3','black','green']}, \
      'images/mtg/creatures/princeHumperdinck.jpg':{'power':3, 'toughness':3,'toCast':['3','black','black']}, \
      'images/mtg/creatures/princessButtercup.jpg':{'power':3, 'toughness':3,'toCast':['white','white','green','green']}, \
      'images/mtg/creatures/princessLeia.jpg':{'power':3, 'toughness':3,'toCast':['3','white','green','blue']}, \
      'images/mtg/creatures/raichu.jpg':{'power':3, 'toughness':3,'toCast':['4','white','red']}, \
      'images/mtg/creatures/ragePlayer.jpeg':{'power':3, 'toughness':3,'toCast':['red','red','red']}, \
      'images/mtg/creatures/ralphNader.jpg':{'power':3, 'toughness':3,'toCast':['black','green']}, \
      'images/mtg/creatures/redForman.jpg':{'power':3, 'toughness':3,'toCast':['red','red',]}, \
      'images/mtg/creatures/rickGrimes.png':{'power':3, 'toughness':3,'toCast':['2','white','green']}, \
      'images/mtg/creatures/riddick.jfif':{'power':3, 'toughness':3,'toCast':['2','black','red']}, \
      'images/mtg/creatures/robocop.jpg':{'power':3, 'toughness':3,'toCast':['4','white']}, \
      'images/mtg/creatures/rocketTropper.jpg':{'power':3, 'toughness':3,'toCast':['1','red']}, \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':{'power':3, 'toughness':3,'toCast':['black']}, \
      'images/mtg/creatures/samuelJackson.jpg':{'power':3, 'toughness':3,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/santaClaus.jpg':{'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/scorpionKing.png':{'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/secretGamer.jpeg':{'power':3, 'toughness':3,'toCast':['white','white','white','white']}, \
      'images/mtg/creatures/seleneBloodDrainer.png':{'power':3, 'toughness':3,'toCast':['3','white','black','blue']}, \
      'images/mtg/creatures/shermanTank.png':{'power':3, 'toughness':3,'toCast':['4','blue','blue']}, \
      'images/mtg/creatures/silverSurfer.png':{'power':3, 'toughness':3,'toCast':['1','white','black','green','blue','red']}, \
      'images/mtg/creatures/sirBedevere.jpg':{'power':3, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/sirRobin.png':{'power':3, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/spaceMarineCaptain.png':{'power':3, 'toughness':3,'toCast':['3','white','red']}, \
      'images/mtg/creatures/spiderman.jpg':{'power':3, 'toughness':3,'toCast':['2',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/spidermanII.png':{'power':3, 'toughness':3,'toCast':['3','blue','red']}, \
      'images/mtg/creatures/spock.png':{'power':3, 'toughness':3,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/steveAustin.png':{'power':3, 'toughness':3,'toCast':['1','white','black','red']}, \
      'images/mtg/creatures/stevenRogers.jpg':{'power':3, 'toughness':3,'toCast':['1','white','white','white']}, \
      'images/mtg/creatures/superBattleDroid.jpg':{'power':3, 'toughness':3,'toCast':['5','blue']}, \
      'images/mtg/creatures/superman.gif':{'power':3, 'toughness':3,'toCast':['3','blue','blue']}, \
      'images/mtg/creatures/supermanII.jpg':{'power':3, 'toughness':3,'toCast':['2','white','white','white','white']}, \
      'images/mtg/creatures/t34Tank.jpg':{'power':3, 'toughness':3,'toCast':['2','red']}, \
      'images/mtg/creatures/thanos.jpg':{'power':3, 'toughness':3,'toCast':['5','black','black']}, \
      'images/mtg/creatures/theCollector.jpeg':{'power':3, 'toughness':3,'toCast':['1','green','green']}, \
      'images/mtg/creatures/theJoker.jpg':{'power':3, 'toughness':3,'toCast':[['black','red'],['black','red'], ['black','red'], ['black','red']]}, \
      'images/mtg/creatures/theOracle.jpg':{'power':3, 'toughness':3,'toCast':['1','blue','blue']}, \
      'images/mtg/creatures/theSilence.jpg':{'power':3, 'toughness':3,'toCast':['4','black']}, \
      'images/mtg/creatures/thor.jpg':{'power':3, 'toughness':3,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/thorGodOfThunder.png':{'power':3, 'toughness':3,'toCast':['6',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/thorSonOfOdin.png':{'power':3, 'toughness':3,'toCast':['4','white','green']}, \
      'images/mtg/creatures/timmyPowerGamer.jpg':{'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/tigerTank.png':{'power':3, 'toughness':3,'toCast':['8']}, \
      'images/mtg/creatures/tinman.png':{'power':3, 'toughness':3,'toCast':['3']}, \
      'images/mtg/creatures/toughNerd.jpeg':{'power':3, 'toughness':3,'toCast':['2','red','red','red']}, \
      'images/mtg/creatures/tournamentGrinder.jpg':{'power':3, 'toughness':3,'toCast':['2','black','black']}, \
      'images/mtg/creatures/tribble.png':{'power':3, 'toughness':3,'toCast':['1','white']}, \
      'images/mtg/creatures/trooperCommander.jpg':{'power':3, 'toughness':3,'toCast':['2','green']}, \
      'images/mtg/creatures/trump.jpg':{'power':3, 'toughness':3,'toCast':['1','white','blue','red']}, \
      'images/mtg/creatures/unwillingVolunteer.jpg':{'power':3, 'toughness':3,'toCast':['1','green']}, \
      'images/mtg/creatures/vegeta.png':{'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/vespaDruishPrincess.jpg':{'power':3, 'toughness':3,'toCast':['green','green']}, \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':{'power':3, 'toughness':3,'toCast':['black','blue','red']}, \
      'images/mtg/creatures/wallOfTrump.png':{'power':3, 'toughness':3,'toCast':['white','white','blue','blue']}, \
      'images/mtg/creatures/warriorBug.png':{'power':3, 'toughness':3,'toCast':['1','green','red']}, \
      'images/mtg/creatures/weepingStatue.jpg':{'power':3, 'toughness':3,'toCast':['4']}, \
      'images/mtg/creatures/westleyMasterofEverything.jpg':{'power':3, 'toughness':3,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/youngChild.jpeg':{'power':3, 'toughness':3,'toCast':['white']} \
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
         power = self.cost[key]['power']
         toughness = self.cost[key]['toughness']
         cards.append ( {'index':count,'iOwnIt':True, 'filename':key, \
                         'location':'library', 'tapped':False, \
                         'summoned':False, 'power':power, \
                         'toughness':toughness} )
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

         

      