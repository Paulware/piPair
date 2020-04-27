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
      'images/mtg/creatures/deadPool.png':{'power':10, 'toughness':10,'toCast':['2','black','red','red']}, \
      'images/mtg/creatures/deadPoolAgain.jpg':{'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':{'power':3, 'toughness':3,'toCast':['1','black','red']}, \
      'images/mtg/creatures/deadPoolIII.png':{'power':3, 'toughness':3,'toCast':['4','black','red']}, \
      'images/mtg/creatures/dickJones.png':{'power':7, 'toughness':7,'toCast':['3','black','black']}, \
      'images/mtg/creatures/doctorEmmettBrown.jpg':{'power':1, 'toughness':3,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/donkeyKong.png':{'power':7, 'toughness':6,'toCast':['5','green','red']}, \
      'images/mtg/creatures/draxDestroyer.jpg':{'power':6,'toughness':4,'toCast':['4',['black','blue'],'red']}, \
      'images/mtg/creatures/drHouse.jpg':{'power':2, 'toughness':8,'toCast':['5','white','white','white']}, \
      'images/mtg/creatures/drStrange.jpg':{'power':1, 'toughness':4,'toCast':['1','white','black','blue']}, \
      'images/mtg/creatures/earlOfSquirrel.jpg':{'power':4, 'toughness':4,'toCast':['4','green','green']}, \
      'images/mtg/creatures/extremelySlowZombie.jpg':{'power':3, 'toughness':3,'toCast':['1','black']}, \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':{'power':5, 'toughness':6,'toCast':['1','white','green','red']}, \
      'images/mtg/creatures/frieza.jpg':{'power':1, 'toughness':2,'toCast':['black','blue','blue']}, \
      'images/mtg/creatures/gamora.jpg':{'power':3, 'toughness':2, 'toCast':['white','blue','red']}, \
      'images/mtg/creatures/gameStoreEmployee.jpg':{'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/gandalf.png':{'power':2, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/generalGrievous.jpg':{'power':2, 'toughness':2,'toCast':['white','black','blue']}, \
      'images/mtg/creatures/georgeBushII.jpg':{'power':1, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/georgeMcfly.jpg':{'power':1, 'toughness':2,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/georgeWBush.jpg':{'power':1, 'toughness':1,'toCast':['red']}, \
      'images/mtg/creatures/gilligan.png':{'power':1, 'toughness':2,'toCast':['1','white']}, \
      'images/mtg/creatures/god.png':{'power':11, 'toughness':11,'toCast':['white','black','green','blue','red']}, \
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
      'images/mtg/creatures/ironMan.png':{'power':3, 'toughness':6,'toCast':['2','white','red','red']}, \
      'images/mtg/creatures/ironManII.jpg':{'power':5, 'toughness':7,'toCast':['5','white','red']}, \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':{'power':5, 'toughness':4,'toCast':['5','red']}, \
      'images/mtg/creatures/jaceTheAsshole.jpg':{'power':2, 'toughness':2,'toCast':['blue']}, \
      'images/mtg/creatures/jamesKirk.png':{'power':3, 'toughness':5,'toCast':['1','white',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/jangoFett.jpg':{'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/jeanGrey.jpg':{'power':3, 'toughness':4,'toCast':['3','black','red']}, \
      'images/mtg/creatures/johnLennon.jpg':{'power':7, 'toughness':7,'toCast':['3',['green','blue'],['green','blue']]}, \
      'images/mtg/creatures/johnnyCash.jpg':{'power':7, 'toughness':7,'toCast':['3',['white','black'],['white','black']]}, \
      'images/mtg/creatures/johnnyCombo.png':{'power':1, 'toughness':1,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/josefStalin.png':{'power':2, 'toughness':8,'toCast':['8','red','red']}, \
      'images/mtg/creatures/joshLane.jpg':{'power':4, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/kanyeWest.png':{'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/killerBunny.jpg':{'power':0, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/kingKong.jpg':{'power':4, 'toughness':6,'toCast':['3','green']}, \
      'images/mtg/creatures/kittyPryde.jpg':{'power':2, 'toughness':2,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/koolAidMan.jpg':{'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/krillin.jpg':{'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/libyanTerrorists.jpg':{'power':3, 'toughness':3,'toCast':['4','red','red']}, \
      'images/mtg/creatures/logan.jpg':{'power':3, 'toughness':4,'toCast':['3',['red','green'],['red','green']]}, \
      'images/mtg/creatures/lordVoldemort.jpg':{'power':6, 'toughness':4,'toCast':['3','black','black','black']}, \
      'images/mtg/creatures/magneto.jpg':{'power':4, 'toughness':4,'toCast':['3','black','blue','red']}, \
      'images/mtg/creatures/mario.jpg':{'power':3, 'toughness':3,'toCast':['3','red','red']}, \
      'images/mtg/creatures/masterChief.png':{'power':3, 'toughness':3,'toCast':['2','black','red']}, \
      'images/mtg/creatures/martyMcFly.jpg':{'power':3, 'toughness':4,'toCast':['2','white','red']}, \
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
      'images/mtg/creatures/raichu.jpg':{'power':5, 'toughness':3,'toCast':['4','white','red']}, \
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
      'images/mtg/creatures/santaClaus.jpg':{'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/scorpionKing.png':{'power':6, 'toughness':5,'toCast':['3','black','red']}, \
      'images/mtg/creatures/secretGamer.jpeg':{'power':3, 'toughness':3,'toCast':['white','white','white','white']}, \
      'images/mtg/creatures/seleneBloodDrainer.png':{'power':4, 'toughness':4,'toCast':['3','white','black','blue']}, \
      'images/mtg/creatures/shermanTank.png':{'power':3, 'toughness':5,'toCast':['4','blue','blue']}, \
      'images/mtg/creatures/silverSurfer.png':{'power':7, 'toughness':7,'toCast':['1','white','black','green','blue','red']}, \
      'images/mtg/creatures/sirBedevere.jpg':{'power':1, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/sirRobin.png':{'power':2, 'toughness':2,'toCast':['white','blue']}, \
      'images/mtg/creatures/spaceMarineCaptain.png':{'power':4, 'toughness':3,'toCast':['3','white','red']}, \
      'images/mtg/creatures/spiderman.jpg':{'power':4, 'toughness':2,'toCast':['2',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/spidermanII.png':{'power':4, 'toughness':4,'toCast':['3','blue','red']}, \
      'images/mtg/creatures/spock.png':{'power':4, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/steveAustin.png':{'power':5, 'toughness':6,'toCast':['1','white','black','red']}, \
      'images/mtg/creatures/stevenRogers.jpg':{'power':4, 'toughness':4,'toCast':['1','white','white','white']}, \
      'images/mtg/creatures/starLord.jpg':{'power':4, 'toughness':3, 'toCast':['2','white','red']}, \
      'images/mtg/creatures/superBattleDroid.jpg':{'power':4, 'toughness':5,'toCast':['5','blue']}, \
      'images/mtg/creatures/superman.gif':{'power':3, 'toughness':3,'toCast':['3','blue','blue']}, \
      'images/mtg/creatures/supermanII.jpg':{'power':6, 'toughness':6,'toCast':['2','white','white','white','white']}, \
      'images/mtg/creatures/t34Tank.jpg':{'power':3, 'toughness':3,'toCast':['2','red']}, \
      'images/mtg/creatures/thanos.jpg':{'power':9, 'toughness':9,'toCast':['5','black','black']}, \
      'images/mtg/creatures/theCollector.jpeg':{'power':2, 'toughness':3,'toCast':['1','green','green']}, \
      'images/mtg/creatures/theJoker.jpg':{'power':2, 'toughness':4,'toCast':[['black','red'],['black','red'], ['black','red'], ['black','red']]}, \
      'images/mtg/creatures/theOracle.jpg':{'power':0, 'toughness':3,'toCast':['1','blue','blue']}, \
      'images/mtg/creatures/theSilence.jpg':{'power':3, 'toughness':3,'toCast':['4','black']}, \
      'images/mtg/creatures/thor.jpg':{'power':6, 'toughness':6,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/thorGodOfThunder.png':{'power':5, 'toughness':5,'toCast':['6',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/thorSonOfOdin.png':{'power':5, 'toughness':4,'toCast':['4','white','green']}, \
      'images/mtg/creatures/timmyPowerGamer.jpg':{'power':1, 'toughness':1,'toCast':['2','green','green']}, \
      'images/mtg/creatures/toughNerd.jpeg':{'power':3, 'toughness':5,'toCast':['2','red','red','red']}, \
      'images/mtg/creatures/tournamentGrinder.jpg':{'power':1, 'toughness':1,'toCast':['2','black','black']}, \
      'images/mtg/creatures/tribble.png':{'power':1, 'toughness':1,'toCast':['1','white']}, \
      'images/mtg/creatures/trooperCommander.jpg':{'power':3, 'toughness':3,'toCast':['2','green']}, \
      'images/mtg/creatures/trump.jpg':{'power':3, 'toughness':5,'toCast':['1','white','blue','red']}, \
      'images/mtg/creatures/unwillingVolunteer.jpg':{'power':1, 'toughness':2,'toCast':['1','green']}, \
      'images/mtg/creatures/vegeta.png':{'power':3, 'toughness':3,'toCast':['black','green','red']}, \
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
   
   def defaultRecord (self,filename):
      info = {'host':False,'filename':filename,'power':0,'toughness':0, \
              'toCast':0,'tapped':False,'location':'library','affects':''}
      return info
   
   def oneRecord (self,filename): 
      info = self.cost [filename]
      data = { 'filename':filename,'power':info['power'], 'toughness':info['toughness'], \
               'toCast':info['toCast'], 'tapped':False, 'location':'library', 'affects':'', \
               'host':False}
      return data 
      
   def toIndexes (self,list): 
      try:
         indexList = []
         
         for item in list:
            info = list[item]
            index = info['index']
            indexList.append (index) 
      except Exception as ex:
         assert False, 'Trouble in toIndexes,problem: ' + str(ex)
         
      return indexList
      
   def toFilenames (self,list,infoList): 
      filenames = []
      try: 
         for index in list:
            info = infoList[index]
            print ( 'Got info: ' + str(info ) ) 
            filename = info['filename']
            filenames.append (filename)
      except Exception as ex:
         assert False, 'toFilenames, indexes list: ' + str(list)
         
      return filenames
      
   
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

      return sufficient                           
     
   def allCards(self): # Used to select card for basis of deck
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
      deck = {}
      creatures = self.matchingCards (filename)
      colors = self.baseCost(filename)
      maxCreatures = 30
      print ( 'len(creatures): ' + str(len(creatures)) )
      count = 0
      while len(deck) < maxCreatures: 
         index = count % len(creatures)
         creature = creatures [index]
         aRecord = self.oneRecord (creature)
         aRecord['index'] = index         
         deck[count] = aRecord 
         filename = str(aRecord['filename'])
         if str.isnumeric (filename): 
            assert False, 'buildDeck, aRecord bad filename value: ' + filename 
         # For each creature 
         count = count + 1
            
      # Add Lands      
      maxLands = 20 
      while len (deck) < (maxCreatures + maxLands):
         for color in colors: 
            land = 'images/mtg/lands/' + color + '.jpg'
            index = self.getIndex (land)
            deck[count] = self.defaultRecord (land)
            deck[count]['index'] = index
            filename = str(deck[count]['filename'])
            if str.isnumeric (filename): 
               assert False, 'buildDeck, land, bad filename value: ' + filename             
            
            count = count + 1
            if count == (maxCreatures + maxLands): 
               break
               
      # Add instants/sorceries/artifacts               
      filename = str(deck[0]['filename'])
      if str.isnumeric (filename): 
         assert False, 'buildDeck, deck[0][filename], bad filename value: ' + filename             
      
      return deck
      
   def getIndex ( self, filename ): 
      count = 0
      found = False 
      for card in self.cost: 
         if card == filename: 
            found = True
            break
         count = count + 1
      print ( 'filename: ' + str(filename) )
      assert found, 'getIndex could not find filename: ' + str(filename) 
      return count
      
   def indexToFilename ( self, index ):
      count = 0
      filename = ''
      for card in self.cost: 
         if count == index:
            filename = card
            break
         count = count + 1
      assert filename != '', 'indexToFilename could not find index: ' + str(index) 
      return filename
   
   def buildDecksMessage (self,allDecks): 
      message = '['
      for card in allDecks: 
         info = allDecks[card]
         index = info['index']
         if message != '[': 
            message = message + ','
         message = message + str(index)
      message = message + ']'
      print ( 'buildDecksMessage created the message: [' + message + ']' )
      return message
      
   def validateAllDecks (self,deck): 
      assert len(deck) > 0, 'Err built an empty deck'      
      
      try: 
         affects = deck[0]['affects']
      except Exception as ex:
         assert False, 'After building decks, allDecks[0][affects] does not exist yo'
         
      filename = str(deck[0]['filename'])
      if str.isnumeric(filename):
         assert False, 'After building decks, allDecks 0 filename is bad: ' + filename
      print ( 'allDecks[0] after buildDecks: ' + str(deck[0]))             
   
      
   def buildDecks (self,hostFilename,opponentFilename):
      allDecks = {}
      # Add host cards
      deck = self.buildDeck (hostFilename)
      count = 0
      for card in deck: 
        info = deck[card]
        filename = info['filename']
        allDecks[count] = {'summoned':False, 'index':info['index'], 'filename':filename, \
                           'affects':'', 'location':'library', 'tapped':False, 'host':True } 
        count = count + 1

      # Add opponent Cards        
      deck = self.buildDeck (opponentFilename)
      for card in deck:
        info = deck[card]
        filename = info['filename']
        allDecks[count] = {'summoned':False, 'index':info['index'], 'filename':filename, \
                           'location':'library', 'tapped':False, 'host':False, 'affects':'' } 
        count = count + 1
      
      self.validateAllDecks (allDecks) 
      return allDecks
      
   def getRandomItem (self,list):
      item = None
      assert len(list) > 0, 'Cannot get random item, list is empty' 
      print ( 'getRandomItem, list has (' + str(len(list)) + ' elements' )
      num = int ( random.random() * len(list))
      item = list[num]
      print (str(list[0])) 
      print ( 'Got randomitem: ' + str(item) )
      assert item != None, 'getRandomItem returning None'
      return item

   def extractLocation (self, list, host, location):
      indexes = [] 
      data = {} 
      count = 0
      print ( 'extractLocation, len(list): ' + str(len(list)) + ', location: ' + location )
      for card in list: 
         info = list[card] # card == count.  TODO: confirm
         if info['location'] != location: 
            pass # print ( 'extractLocation, (info[location] != location): ([' +  info['location'] + ']!= [' + location + '])')
         elif info['host'] != host:
            pass # print ( 'info[host] !=' + str(host)) 
         else:
            index = info['index']
            indexes.append (index) # list of indexes 
            data[count] = info            
            count = count + 1
      print ( 'extractLocation len(indexes): ' + str(len(indexes)) + ', len(data): ' + str(len(data)) ) 
      return indexes,data
      
   # allDecks[index]['location'] = 'inhand'      
   def dealCard (self,list,host): 
      info = None
      assert len(list) > 0, "dealCard list is empty" 
      indexes,infoList = self.extractLocation (list, host, 'library')
      assert len(infoList) > 0, 'Why is library list empty? Big list:' + str(list) 
      info = self.getRandomItem (infoList)
      card = info['index']
      list[card]['location'] = 'inhand'
      print ( 'dealCard got card: ' + str (info) )
      return info
      
   def dealHand (self,list,host):
      infoList = []
      assert len(list) > 0, 'Cannot deal a hand from an empty list'
      for i in range(7):
         info = self.dealCard (list,host)
         infoList.append ( info['index'] ) 
      print ( 'I was dealt this hand: ' + str(infoList)) 
      return infoList
