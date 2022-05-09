import random
import copy
class cardDatabase: 
   data = { \
      'images/mtg/creatures/agentSmith.jpg':{'power':6, 'toughness':6,'toCast':['4','black','black']}, \
      'images/mtg/creatures/alGore.jpg':{'power':1, 'toughness':1,'toCast':['green','green']}, \
      'images/mtg/creatures/americanEagle.jpg':{'flying':True, 'power':2, 'toughness':2,'toCast':['3','white','blue','red']}, \
      'images/mtg/creatures/android17.png':{'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/android18.png':{'power':2, 'toughness':2,'toCast':['2','white','red']}, \
      'images/mtg/creatures/annoyingOrange.jpg':{'haste':True, 'power':1, 'toughness':1,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/arrgh.jpg':{'haste':True, 'power':5, 'toughness':5,'toCast':['black','black','black']}, \
      'images/mtg/creatures/arthurKingOfTheBritains.jpg':{'power':4, 'toughness':5,'toCast':['3','white','white']}, \
      'images/mtg/creatures/barackHObama.jpg':{'power':0, 'toughness':6,'toCast':['1','red']}, \
      'images/mtg/creatures/barackObama.jpg':{'power':3, 'toughness':7,'toCast':[['green','blue'],['green','blue'],['green','blue'],['white','blue'],['white','blue'],['white','blue']]}, \
      'images/mtg/creatures/barackObamaII.jpg':{'power':1, 'toughness':1,'toCast':['3','black']}, \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':{'power':3, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/batman.jpg':{'power':5, 'toughness':5,'toCast':['3','white','blue']}, \
      'images/mtg/creatures/batmanII.jpg':{'power':5, 'toughness':4,'toCast':['3',['white','black'],['white','black'],['white','black']]}, \
      'images/mtg/creatures/berneyStinson.jpg':{'power':4, 'toughness':1,'toCast':['red','red']}, \
      'images/mtg/creatures/bernieSanders.jpg':{'power':5, 'toughness':8,'toCast':['2','white','white']}, \
      'images/mtg/creatures/bernieSandersII.jpg':{'haste':True, 'power':20, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/bickeringGiant.jpg':{'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/biffTannen.jpg':{'power':5, 'toughness':5,'toCast':['4','black','red']}, \
      'images/mtg/creatures/blackKnight.jpg':{'power':0, 'toughness':2,'toCast':['1','black','black']}, \
      'images/mtg/creatures/borgCube.jpg':{'flying':True, 'power':1, 'toughness':1,'toCast':['4','black','black']}, \
      'images/mtg/creatures/borgQueen.jpg':{'power':5, 'toughness':5,'toCast':['white','white','black','black','blue','blue','blue']}, \
      'images/mtg/creatures/bruceLee.jpg':{'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/burninator.jpg':{'power':9, 'toughness':9,'toCast':['9','red']}, \
      'images/mtg/creatures/cantinaBand.jpg':{'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/captainAmerica.jfif':{'power':2, 'toughness':2,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/charlesXavier.jpg':{'power':2, 'toughness':4,'toCast':['2','white','blue','blue']}, \
      'images/mtg/creatures/cheatyFace.jpg':{'flying':True, 'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/chivalrousChevalier.jpg':{'flying':True, 'power':3, 'toughness':3,'toCast':['4','white']}, \
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
      'images/mtg/creatures/deadPool.png':{'haste':True, 'power':10, 'toughness':10,'toCast':['2','black','red','red']}, \
      'images/mtg/creatures/deadPoolAgain.jpg':{'haste':True, 'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':{'power':3, 'toughness':3,'toCast':['1','black','red']}, \
      'images/mtg/creatures/deadPoolIII.png':{'power':3, 'toughness':3,'toCast':['4','black','red']}, \
      'images/mtg/creatures/dickJones.png':{'power':7, 'toughness':7,'toCast':['3','black','black']}, \
      'images/mtg/creatures/doctorEmmettBrown.jpg':{'power':1, 'toughness':3,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/donkeyKong.png':{'power':7, 'toughness':6,'toCast':['5','green','red']}, \
      'images/mtg/creatures/draxDestroyer.jpg':{'power':6,'toughness':4,'toCast':['4',['black','blue'],'red']}, \
      'images/mtg/creatures/drHouse.jpg':{'power':2, 'toughness':8,'toCast':['5','white','white','white']}, \
      'images/mtg/creatures/drStrange.jpg':{'flying':True, 'power':1, 'toughness':4,'toCast':['1','white','black','blue']}, \
      'images/mtg/creatures/earlOfSquirrel.jpg':{'power':4, 'toughness':4,'toCast':['4','green','green']}, \
      'images/mtg/creatures/extremelySlowZombie.jpg':{'power':3, 'toughness':3,'toCast':['1','black']}, \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':{'power':5, 'toughness':6,'toCast':['1','white','green','red']}, \
      'images/mtg/creatures/frieza.jpg':{'flying':True, 'power':1, 'toughness':2,'toCast':['black','blue','blue']}, \
      'images/mtg/creatures/gamora.jpg':{'power':3, 'toughness':2, 'toCast':['white','blue','red']}, \
      'images/mtg/creatures/gameStoreEmployee.jpg':{'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/gandalf.png':{'power':2, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/generalGrievous.jpg':{'power':2, 'toughness':2,'toCast':['white','black','blue']}, \
      'images/mtg/creatures/georgeBushII.jpg':{'power':1, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/georgeMcfly.jpg':{'power':1, 'toughness':2,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/georgeWBush.jpg':{'power':1, 'toughness':1,'toCast':['red']}, \
      'images/mtg/creatures/gilligan.png':{'power':1, 'toughness':2,'toCast':['1','white']}, \
      'images/mtg/creatures/god.png':{'flying':True, 'power':11, 'toughness':11,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/godzilla.jpg':{'power':7, 'toughness':6,'toCast':['5','green','blue','red']}, \
      'images/mtg/creatures/gordonRamsey.jpg':{'power':3, 'toughness':2,'toCast':['3','red']}, \
      'images/mtg/creatures/groot.jpg':{'power':8,'toughness':8,'toCast':['3','green','green','white']}, \
      'images/mtg/creatures/hangman.jpg':{'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/hanSolo.jpg':{'power':4, 'toughness':3,'toCast':['3','white']}, \
      'images/mtg/creatures/hela.png':{'power':4, 'toughness':5,'toCast':['4',['black','red'],'green']}, \
      'images/mtg/creatures/hillaryClinton.jpeg':{'power':4, 'toughness':3,'toCast':['2','white','red']}, \
      'images/mtg/creatures/hirohito.png':{'power':4, 'toughness':3,'toCast':['3','red','white']}, \
      'images/mtg/creatures/hitler.jpg':{'affects':{'cast':'destroyTarget()'}, 'power':4, 'toughness':5,'toCast':['black','black','black','black']}, \
      'images/mtg/creatures/hulk.png':{'power':6, 'toughness':6,'toCast':['green','green','green','green','green','green']}, \
      'images/mtg/creatures/indianaJones.jpg':{'power':1, 'toughness':3,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/infinityElemental.jpg':{'power':99, 'toughness':5,'toCast':['4','red','red','red']}, \
      'images/mtg/creatures/inigoMontoya.jpg':{'power':4, 'toughness':4,'toCast':['2',['red','white'],['red','white']]}, \
      'images/mtg/creatures/inigoMontoyaII.jpg':{'power':4, 'toughness':4,'toCast':['white','green','red']}, \
      'images/mtg/creatures/ironMan.png':{'flying':True, 'power':3, 'toughness':6,'toCast':['2','white','red','red']}, \
      'images/mtg/creatures/ironManII.jpg':{'flying':True, 'power':5, 'toughness':7,'toCast':['5','white','red']}, \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':{'power':5, 'toughness':4,'toCast':['5','red']}, \
      'images/mtg/creatures/jaceTheAsshole.jpg':{'power':2, 'toughness':2,'toCast':['blue']}, \
      'images/mtg/creatures/jamesKirk.png':{'power':3, 'toughness':5,'toCast':['1','white',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/jangoFett.jpg':{'flying':True, 'haste':True, 'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/jeanGrey.jpg':{'power':3, 'toughness':4,'toCast':['3','black','red']}, \
      'images/mtg/creatures/johnLennon.jpg':{'power':7, 'toughness':7,'toCast':['3',['green','blue'],['green','blue']]}, \
      'images/mtg/creatures/johnnyCash.jpg':{'power':7, 'toughness':7,'toCast':['3',['white','black'],['white','black']]}, \
      'images/mtg/creatures/johnnyCombo.png':{'power':1, 'toughness':1,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/josefStalin.png':{'power':2, 'toughness':8,'toCast':['8','red','red']}, \
      'images/mtg/creatures/joshLane.jpg':{'power':4, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/kanyeWest.png':{'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/killerBunny.jpg':{'power':0, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/kingKong.jpg':{'haste':True, 'power':4, 'toughness':6,'toCast':['3','green']}, \
      'images/mtg/creatures/kittyPryde.jpg':{'power':2, 'toughness':2,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/koolAidMan.jpg':{'haste':True, 'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/krillin.jpg':{'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/libyanTerrorists.jpg':{'power':3, 'toughness':3,'toCast':['4','red','red']}, \
      'images/mtg/creatures/logan.jpg':{'power':3, 'toughness':4,'toCast':['3',['red','green'],['red','green']]}, \
      'images/mtg/creatures/lordVoldemort.jpg':{'flying':True, 'power':6, 'toughness':4,'toCast':['3','black','black','black']}, \
      'images/mtg/creatures/magneto.jpg':{'power':4, 'toughness':4,'toCast':['3','black','blue','red']}, \
      'images/mtg/creatures/mario.jpg':{'power':3, 'toughness':3,'toCast':['3','red','red']}, \
      'images/mtg/creatures/masterChief.png':{'haste':True, 'power':3, 'toughness':3,'toCast':['2','black','red']}, \
      'images/mtg/creatures/martyMcFly.jpg':{'haste':True, 'power':3, 'toughness':4,'toCast':['2','white','red']}, \
      'images/mtg/creatures/memePirate.jpeg':{'power':3, 'toughness':3,'toCast':['2','blue','red']}, \
      'images/mtg/creatures/miracleMax.jpg':{'power':1, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/mrT.jpg':{'power':5, 'toughness':5,'toCast':['4','white','red']}, \
      'images/mtg/creatures/mrTII.jpg':{'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/mtgPlayer.png':{'power':2, 'toughness':2,'toCast':['2']}, \
      'images/mtg/creatures/mysterioIllusionist.png':{'power':1, 'toughness':3,'toCast':['blue','blue','blue']}, \
      'images/mtg/creatures/mystique.jpg':{'power':3, 'toughness':3,'toCast':['3','black','blue','blue']}, \
      'images/mtg/creatures/mythBusters.jpg':{'power':6, 'toughness':4,'toCast':['3','red','red']}, \
      'images/mtg/creatures/nerdyPlayer.jpeg':{'power':4, 'toughness':6,'toCast':['3','black','black']}, \
      'images/mtg/creatures/noviceBountyHunter.jpg':{'power':2, 'toughness':1,'toCast':['1','red']}, \
      'images/mtg/creatures/obiWanKenobi.jpg':{'power':5, 'toughness':5,'toCast':['2','white','green','blue']}, \
      'images/mtg/creatures/patton.png':{'power':2, 'toughness':2,'toCast':['2','green','green']}, \
      'images/mtg/creatures/peeweeHerman.jpg':{'power':1, 'toughness':4,'toCast':['1','white','red']}, \
      'images/mtg/creatures/pepe.jpg':{'power':0, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/pikachu.png':{'power':1, 'toughness':2,'toCast':[['blue','red'], ['blue','red']]}, \
      'images/mtg/creatures/pizzaTheHutt.jpg':{'power':3, 'toughness':5,'toCast':['3','black','green']}, \
      'images/mtg/creatures/princeHumperdinck.jpg':{'power':2, 'toughness':5,'toCast':['3','black','black']}, \
      'images/mtg/creatures/princessButtercup.jpg':{'power':2, 'toughness':6,'toCast':['white','white','green','green']}, \
      'images/mtg/creatures/princessLeia.jpg':{'power':2, 'toughness':2,'toCast':['3','white','green','blue']}, \
      'images/mtg/creatures/raichu.jpg':{'haste':True, 'power':5, 'toughness':3,'toCast':['4','white','red']}, \
      'images/mtg/creatures/ragePlayer.jpeg':{'power':4, 'toughness':1,'toCast':['red','red','red']}, \
      'images/mtg/creatures/ralphNader.jpg':{'power':2, 'toughness':2,'toCast':['black','green']}, \
      'images/mtg/creatures/redForman.jpg':{'power':1, 'toughness':2,'toCast':['red','red',]}, \
      'images/mtg/creatures/rickGrimes.png':{'power':2, 'toughness':1,'toCast':['2','white','green']}, \
      'images/mtg/creatures/riddick.jfif':{'power':4, 'toughness':4,'toCast':['2','black','red']}, \
      'images/mtg/creatures/rocketRaccoon.jpg':{'power':2, 'toughness':2, 'toCast':['green','blue','red']}, \
      'images/mtg/creatures/robocop.jpg':{'power':4, 'toughness':4,'toCast':['4','white']}, \
      'images/mtg/creatures/rocketTropper.jpg':{'power':2, 'toughness':2,'toCast':['1','red']}, \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':{'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/samuelJackson.jpg':{'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/santaClaus.jpg':{'flying':True, 'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/scorpionKing.png':{'power':6, 'toughness':5,'toCast':['3','black','red']}, \
      'images/mtg/creatures/secretGamer.jpeg':{'power':3, 'toughness':3,'toCast':['white','white','white','white']}, \
      'images/mtg/creatures/seleneBloodDrainer.png':{'flying':True, 'power':4, 'toughness':4,'toCast':['3','white','black','blue']}, \
      'images/mtg/creatures/shermanTank.png':{'power':3, 'toughness':5,'toCast':['4','blue','blue']}, \
      'images/mtg/creatures/silverSurfer.png':{'flying':True, 'power':7, 'toughness':7,'toCast':['1','white','black','green','blue','red']}, \
      'images/mtg/creatures/sirBedevere.jpg':{'power':1, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/sirRobin.png':{'power':2, 'toughness':2,'toCast':['white','blue']}, \
      'images/mtg/creatures/spaceMarineCaptain.png':{'power':4, 'toughness':3,'toCast':['3','white','red']}, \
      'images/mtg/creatures/spiderman.jpg':{'power':4, 'toughness':2,'toCast':['2',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/spidermanIII.png':{'flying':True, 'haste':True, 'power':4, 'toughness':4,'toCast':['3','blue','red']}, \
      'images/mtg/creatures/spock.png':{'power':4, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/steveAustin.png':{'haste':True, 'power':5, 'toughness':6,'toCast':['1','white','black','red']}, \
      'images/mtg/creatures/stevenRogers.jpg':{'power':4, 'toughness':4,'toCast':['1','white','white','white']}, \
      'images/mtg/creatures/starLord.jpg':{'power':4, 'toughness':3, 'toCast':['2','white','red']}, \
      'images/mtg/creatures/superBattleDroid.jpg':{'power':4, 'toughness':5,'toCast':['5','blue']}, \
      'images/mtg/creatures/superman.gif':{'power':3, 'toughness':3,'toCast':['3','blue','blue']}, \
      'images/mtg/creatures/supermanII.jpg':{'flying':True, 'haste':True, 'power':6, 'toughness':6,'toCast':['2','white','white','white','white']}, \
      'images/mtg/creatures/t34Tank.jpg':{'power':3, 'toughness':3,'toCast':['2','red']}, \
      'images/mtg/creatures/thanos.jpg':{'power':9, 'toughness':9,'toCast':['5','black','black']}, \
      'images/mtg/creatures/theCollector.jpeg':{'power':2, 'toughness':3,'toCast':['1','green','green']}, \
      'images/mtg/creatures/theJoker.jpg':{'power':2, 'toughness':4,'toCast':[['black','red'],['black','red'], ['black','red'], ['black','red']]}, \
      'images/mtg/creatures/theOracle.jpg':{'power':0, 'toughness':3,'toCast':['1','blue','blue']}, \
      'images/mtg/creatures/theSilence.jpg':{'power':3, 'toughness':3,'toCast':['4','black']}, \
      'images/mtg/creatures/thor.jpg':{'flying':True, 'power':6, 'toughness':6,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/thorGodOfThunder.png':{'flying': True, 'power':5, 'toughness':5,'toCast':['6',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/thorSonOfOdin.png':{'power':5, 'toughness':4,'toCast':['4','white','green']}, \
      'images/mtg/creatures/timmyPowerGamer.jpg':{'power':1, 'toughness':1,'toCast':['2','green','green']}, \
      'images/mtg/creatures/toughNerd.jpeg':{'power':3, 'toughness':5,'toCast':['2','red','red','red']}, \
      'images/mtg/creatures/tournamentGrinder.jpg':{'power':1, 'toughness':1,'toCast':['2','black','black']}, \
      'images/mtg/creatures/tribble.png':{'power':1, 'toughness':1,'toCast':['1','white']}, \
      'images/mtg/creatures/trooperCommander.jpg':{'power':3, 'toughness':3,'toCast':['2','green']}, \
      'images/mtg/creatures/trump.jpg':{'power':3, 'toughness':5,'toCast':['1','white','blue','red']}, \
      'images/mtg/creatures/unwillingVolunteer.jpg':{'power':1, 'toughness':2,'toCast':['1','green']}, \
      'images/mtg/creatures/vegeta.png':{'haste:':True, 'flying':True, 'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/vespaDruishPrincess.jpg':{'power':2, 'toughness':3,'toCast':['green','green']}, \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':{'power':2, 'toughness':4,'toCast':['black','blue','red']}, \
      'images/mtg/creatures/wallOfTrump.png':{'power':0, 'toughness':6,'toCast':['white','white','blue','blue']}, \
      'images/mtg/creatures/warriorBug.png':{'power':1, 'toughness':1,'toCast':['1','green','red']}, \
      'images/mtg/creatures/weepingStatue.jpg':{'power':3, 'toughness':3,'toCast':['4']}, \
      'images/mtg/creatures/westleyMasterofEverything.jpg':{'power':4, 'toughness':5,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/vladimirPutin.jpg':{'power':4,'toughness':4,'toCast':['3','green','green']}, \
      'images/mtg/creatures/youngChild.jpeg':{'power':1, 'toughness':1,'toCast':['white']}, \
      # Lands 
      'images/mtg/lands/red.jpg':{'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/white.jpg':{'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/black.jpg':{'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/blue.jpg':{'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/green.jpg':{'power':0, 'toughness':0, 'toCast':['0']}, \
   }
   
   reverse = []
   
   def __init__(self):
      count = 0
      for filename in self.data:
         info = self.data[filename]
         info['index'] = count
         count = count + 1
    
   def indexToInfo (self, index):
      return list(self.data)[index]
    
   def indexToFilename ( self, index ):
      return list(self.data)[index]

   def filenameToInfo (self, filename ):
      return self.data[filename]
           
   def filenameToIndex (self, filename):
      return self.data [filename]['index']
            
   def getRandomInfo (self):
      num = int ( random.random() * len(self.data))
      return self.indexToInfo (num)
      
   def filenamesToIndexes (self,filenames): 
      try:
         indexList = []         
         for filename in filenames:
            indexList.append (self. filenameToIndex (filename)) 
      except Exception as ex:
         assert False, 'Trouble in filenamesToIndexes,problem: ' + str(ex)
         
      return indexList
      
   def indexesToFilenames (self,indexes): 
      filenames = []
      try: 
         for index in indexes:
            filenames.append (self.indexToFilename(index))
      except Exception as ex:
         assert False, 'toFilenames, indexes list: ' + str(list)
         
      return filenames      
   
   def actualCost (self,filename):
      return self.data[filename]['toCast']      
      
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

      return sufficient                           
     
           
   def baseCost ( self, filename ):
      base = []
      casting = self.actualCost(filename)
      for color in casting: 
         if isinstance(color, list):
            # print ( "This is a list: " + str(color) )
            for c in color:
               # print ( 'c: ' + c )
               if c not in base: 
                  base.append(c)                 
         else:
            if not color.isnumeric(): 
               if color not in base:             
                  base.append(color)
      base.sort()            
      return base
   
   # Return a list of filenames 
   def matchingCards (self,filename):    
      matches = []
      casting = self.baseCost(filename)
      casting.sort()
      print ( 'casting for ' + filename + ' is: ' + str( casting ))
      #check all Creature Cards 
      for key in self.data:
         if self.baseCost(key) == casting: 
            matches.append (key) 
         else:
            #Check if match on single color
            for mono in casting: 
               if self.baseCost(key) == [mono]:
                  matches.append (key)
                  break

      return matches
      
   # List of filenames    
   def cardList (self): 
      listCards = [] 
      for key in self.data: 
         listCards.append (key) 
      return listCards
        
   def buildDeck (self,filename): 
      print ( 'cardDatabase, Building a deck list based on ' + filename )
      indexList = [] 
      creatures = self.matchingCards (filename)
      colors = self.baseCost(filename)
      print ( 'colors: ' + str(colors) ) 
      print ( 'matching creatures: ' + str(creatures )) 
      maxCreatures = 30
      count = 0
      while len(indexList) < maxCreatures: 
         index = count % len(creatures)
         filename = creatures[index]         
         indexList.append (self.filenameToIndex (filename))
         count = count + 1
            
      # Add Lands      
      maxLands = 20 
      while len (indexList) < (maxCreatures + maxLands):
         for color in colors: 
            land = 'images/mtg/lands/' + color + '.jpg'
            index = self.filenameToIndex(land)
            indexList.append (index)
            count = count + 1
            if count == (maxCreatures + maxLands): 
               break
            
      # TODO: Add instants/sorceries/artifacts               
      return indexList
      
            
if __name__ == '__main__':
    try:
       db = cardDatabase()
       print ( str(db.cardList()) )
       filename = db.indexToFilename (0)
       print ( 'Got filename: ' + filename )
       index = db.filenameToIndex ('images/mtg/creatures/nerdyPlayer.jpeg')       
       print ( 'Got index for nerdy Player: ' + str(index) )
       filenames = db.indexesToFilenames ( [ 0, 4, 9 ] ) 
       print ( str (filenames ) ) 
       indexes = db.filenamesToIndexes ( ['images/mtg/creatures/agentSmith.jpg', \
                                          'images/mtg/creatures/android18.png', \
                                          'images/mtg/creatures/barackObama.jpg'] )
       print ( str (indexes ) ) 
       indexes = db.buildDeck (filename)
       
       print ( 'Built the deck: ' + str(indexes ) )
    except Exception as ex:
       print ( "Got exception: " + str(ex)) 
    finally:
       print ( 'finally' )
           