import random
import copy
class cardDatabase: 
   data = { \
      'images/mtg/creatures/agentSmith.jpg':{'haste':False, 'power':6, 'toughness':6,'toCast':['4','black','black']}, \
      'images/mtg/creatures/alGore.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['green','green']}, \
      'images/mtg/creatures/americanEagle.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['3','white','blue','red']}, \
      'images/mtg/creatures/android17.png':{'haste':False, 'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/android18.png':{'haste':False, 'power':2, 'toughness':2,'toCast':['2','white','red']}, \
      'images/mtg/creatures/annoyingOrange.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/arrgh.jpg':{'haste':False, 'power':5, 'toughness':5,'toCast':['black','black','black']}, \
      'images/mtg/creatures/arthurKingOfTheBritains.jpg':{'haste':False, 'power':4, 'toughness':5,'toCast':['3','white','white']}, \
      'images/mtg/creatures/barackHObama.jpg':{'haste':False, 'power':0, 'toughness':6,'toCast':['1','red']}, \
      'images/mtg/creatures/barackObama.jpg':{'haste':False, 'power':3, 'toughness':7,'toCast':[['green','blue'],['green','blue'],['green','blue'],['white','blue'],['white','blue'],['white','blue']]}, \
      'images/mtg/creatures/barackObamaII.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['3','black']}, \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':{'haste':False, 'power':3, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/batman.jpg':{'haste':False, 'power':5, 'toughness':5,'toCast':['3','white','blue']}, \
      'images/mtg/creatures/batmanII.jpg':{'haste':False, 'power':5, 'toughness':4,'toCast':['3',['white','black'],['white','black'],['white','black']]}, \
      'images/mtg/creatures/berneyStinson.jpg':{'haste':False, 'power':4, 'toughness':1,'toCast':['red','red']}, \
      'images/mtg/creatures/bernieSanders.jpg':{'haste':False, 'power':5, 'toughness':8,'toCast':['2','white','white']}, \
      'images/mtg/creatures/bernieSandersII.jpg':{'haste':False, 'power':20, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/bickeringGiant.jpg':{'haste':False, 'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/biffTannen.jpg':{'haste':False, 'power':5, 'toughness':5,'toCast':['4','black','red']}, \
      'images/mtg/creatures/blackKnight.jpg':{'haste':False, 'power':0, 'toughness':2,'toCast':['1','black','black']}, \
      'images/mtg/creatures/borgCube.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['4','black','black']}, \
      'images/mtg/creatures/borgQueen.jpg':{'haste':False, 'power':5, 'toughness':5,'toCast':['white','white','black','black','blue','blue','blue']}, \
      'images/mtg/creatures/bruceLee.jpg':{'haste':False, 'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/burninator.jpg':{'haste':False, 'power':9, 'toughness':9,'toCast':['9','red']}, \
      'images/mtg/creatures/cantinaBand.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/captainAmerica.jfif':{'haste':False, 'power':2, 'toughness':2,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/charlesXavier.jpg':{'haste':False, 'power':2, 'toughness':4,'toCast':['2','white','blue','blue']}, \
      'images/mtg/creatures/cheatyFace.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/chivalrousChevalier.jpg':{'haste':False, 'power':3, 'toughness':3,'toCast':['4','white']}, \
      'images/mtg/creatures/chuckNorris.jpg':{'haste':False, 'power':99, 'toughness':99,'toCast':['9','green']}, \
      'images/mtg/creatures/conanTheBarbarian.png':{'haste':False, 'power':3, 'toughness':3,'toCast':['2','red','red']}, \
      'images/mtg/creatures/conanTheLibrarian.png':{'haste':False, 'power':4, 'toughness':5,'toCast':['4','red','red']}, \
      'images/mtg/creatures/countTyroneRugen.jpg':{'haste':False, 'power':3, 'toughness':4,'toCast':['black','black','red']}, \
      'images/mtg/creatures/cowardlyLion.png':{'haste':False, 'power':1, 'toughness':5,'toCast':['green']}, \
      'images/mtg/creatures/daenerysStormborn.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['1','white','black','green','red']}, \
      'images/mtg/creatures/darthSidious.jpg':{'haste':False, 'power':5, 'toughness':5,'toCast':['4','black','blue','red']}, \
      'images/mtg/creatures/darthVader.jpg':{'haste':False, 'power':13, 'toughness':13,'toCast':['5','black','black','black','black','black']}, \
      'images/mtg/creatures/darkHelmet.jpg':{'haste':False, 'power':4, 'toughness':5,'toCast':['3','black','black','blue']}, \
      'images/mtg/creatures/darylDixon.jpg':{'haste':False, 'power':6, 'toughness':6,'toCast':['red','red','red','red','red']}, \
      'images/mtg/creatures/deadPool.png':{'haste':False, 'power':10, 'toughness':10,'toCast':['2','black','red','red']}, \
      'images/mtg/creatures/deadPoolAgain.jpg':{'haste':False, 'power':3, 'toughness':3,'toCast':['3','black','red']}, \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':{'haste':False, 'power':3, 'toughness':3,'toCast':['1','black','red']}, \
      'images/mtg/creatures/deadPoolIII.png':{'haste':False, 'power':3, 'toughness':3,'toCast':['4','black','red']}, \
      'images/mtg/creatures/dickJones.png':{'haste':False, 'power':7, 'toughness':7,'toCast':['3','black','black']}, \
      'images/mtg/creatures/doctorEmmettBrown.jpg':{'haste':False, 'power':1, 'toughness':3,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/donkeyKong.png':{'haste':False, 'power':7, 'toughness':6,'toCast':['5','green','red']}, \
      'images/mtg/creatures/draxDestroyer.jpg':{'haste':False, 'power':6,'toughness':4,'toCast':['4',['black','blue'],'red']}, \
      'images/mtg/creatures/drHouse.jpg':{'haste':False, 'power':2, 'toughness':8,'toCast':['5','white','white','white']}, \
      'images/mtg/creatures/drStrange.jpg':{'haste':False, 'power':1, 'toughness':4,'toCast':['1','white','black','blue']}, \
      'images/mtg/creatures/earlOfSquirrel.jpg':{'haste':False, 'power':4, 'toughness':4,'toCast':['4','green','green']}, \
      'images/mtg/creatures/extremelySlowZombie.jpg':{'haste':False, 'power':3, 'toughness':3,'toCast':['1','black']}, \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':{'haste':False, 'power':5, 'toughness':6,'toCast':['1','white','green','red']}, \
      'images/mtg/creatures/frieza.jpg':{'haste':False, 'power':1, 'toughness':2,'toCast':['black','blue','blue']}, \
      'images/mtg/creatures/gamora.jpg':{'haste':False, 'power':3, 'toughness':2, 'toCast':['white','blue','red']}, \
      'images/mtg/creatures/gameStoreEmployee.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['blue','blue']}, \
      'images/mtg/creatures/gandalf.png':{'haste':False, 'power':2, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/generalGrievous.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['white','black','blue']}, \
      'images/mtg/creatures/georgeBushII.jpg':{'haste':False, 'power':1, 'toughness':4,'toCast':['white','blue','red']}, \
      'images/mtg/creatures/georgeMcfly.jpg':{'haste':False, 'power':1, 'toughness':2,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/georgeWBush.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['red']}, \
      'images/mtg/creatures/gilligan.png':{'haste':False, 'power':1, 'toughness':2,'toCast':['1','white']}, \
      'images/mtg/creatures/god.png':{'haste':False, 'power':11, 'toughness':11,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/godzilla.jpg':{'haste':False, 'power':7, 'toughness':6,'toCast':['5','green','blue','red']}, \
      'images/mtg/creatures/gordonRamsey.jpg':{'haste':False, 'power':3, 'toughness':2,'toCast':['3','red']}, \
      'images/mtg/creatures/groot.jpg':{'haste':False, 'power':8,'toughness':8,'toCast':['3','green','green','white']}, \
      'images/mtg/creatures/hangman.jpg':{'haste':False, 'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/hanSolo.jpg':{'haste':False, 'power':4, 'toughness':3,'toCast':['3','white']}, \
      'images/mtg/creatures/hela.png':{'haste':False, 'power':4, 'toughness':5,'toCast':['4',['black','red'],'green']}, \
      'images/mtg/creatures/hillaryClinton.jpeg':{'haste':False, 'power':4, 'toughness':3,'toCast':['2','white','red']}, \
      'images/mtg/creatures/hirohito.png':{'haste':False, 'power':4, 'toughness':3,'toCast':['3','red','white']}, \
      'images/mtg/creatures/hitler.jpg':{'haste':False, 'affects':{'cast':'destroyTarget()'}, 'power':4, 'toughness':5,'toCast':['black','black','black','black']}, \
      'images/mtg/creatures/hulk.png':{'haste':False, 'power':6, 'toughness':6,'toCast':['green','green','green','green','green','green']}, \
      'images/mtg/creatures/indianaJones.jpg':{'haste':False, 'power':1, 'toughness':3,'toCast':['1','white','blue']}, \
      'images/mtg/creatures/infinityElemental.jpg':{'haste':False, 'power':99, 'toughness':5,'toCast':['4','red','red','red']}, \
      'images/mtg/creatures/inigoMontoya.jpg':{'haste':False, 'power':4, 'toughness':4,'toCast':['2',['red','white'],['red','white']]}, \
      'images/mtg/creatures/inigoMontoyaII.jpg':{'haste':False, 'power':4, 'toughness':4,'toCast':['white','green','red']}, \
      'images/mtg/creatures/ironMan.png':{'haste':False, 'power':3, 'toughness':6,'toCast':['2','white','red','red']}, \
      'images/mtg/creatures/ironManII.jpg':{'haste':False, 'power':5, 'toughness':7,'toCast':['5','white','red']}, \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':{'haste':False, 'power':5, 'toughness':4,'toCast':['5','red']}, \
      'images/mtg/creatures/jaceTheAsshole.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['blue']}, \
      'images/mtg/creatures/jamesKirk.png':{'haste':False, 'power':3, 'toughness':5,'toCast':['1','white',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/jangoFett.jpg':{'haste':True, 'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/jeanGrey.jpg':{'haste':False, 'power':3, 'toughness':4,'toCast':['3','black','red']}, \
      'images/mtg/creatures/johnLennon.jpg':{'haste':False, 'power':7, 'toughness':7,'toCast':['3',['green','blue'],['green','blue']]}, \
      'images/mtg/creatures/johnnyCash.jpg':{'haste':False, 'power':7, 'toughness':7,'toCast':['3',['white','black'],['white','black']]}, \
      'images/mtg/creatures/johnnyCombo.png':{'haste':False, 'power':1, 'toughness':1,'toCast':['2','blue','blue']}, \
      'images/mtg/creatures/josefStalin.png':{'haste':False, 'power':2, 'toughness':8,'toCast':['8','red','red']}, \
      'images/mtg/creatures/joshLane.jpg':{'haste':False, 'power':4, 'toughness':20,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/kanyeWest.png':{'haste':False, 'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/killerBunny.jpg':{'haste':False, 'power':0, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/kingKong.jpg':{'haste':False, 'power':4, 'toughness':6,'toCast':['3','green']}, \
      'images/mtg/creatures/kittyPryde.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/koolAidMan.jpg':{'haste':False, 'power':2, 'toughness':2,'toCast':['2','red','red']}, \
      'images/mtg/creatures/krillin.jpg':{'haste':False,'power':1, 'toughness':1,'toCast':['white']}, \
      'images/mtg/creatures/libyanTerrorists.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['4','red','red']}, \
      'images/mtg/creatures/logan.jpg':{'haste':False,'power':3, 'toughness':4,'toCast':['3',['red','green'],['red','green']]}, \
      'images/mtg/creatures/lordVoldemort.jpg':{'haste':False,'power':6, 'toughness':4,'toCast':['3','black','black','black']}, \
      'images/mtg/creatures/magneto.jpg':{'haste':False,'power':4, 'toughness':4,'toCast':['3','black','blue','red']}, \
      'images/mtg/creatures/mario.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['3','red','red']}, \
      'images/mtg/creatures/masterChief.png':{'haste':False,'power':3, 'toughness':3,'toCast':['2','black','red']}, \
      'images/mtg/creatures/martyMcFly.jpg':{'haste':False,'power':3, 'toughness':4,'toCast':['2','white','red']}, \
      'images/mtg/creatures/memePirate.jpeg':{'haste':False,'power':3, 'toughness':3,'toCast':['2','blue','red']}, \
      'images/mtg/creatures/miracleMax.jpg':{'haste':False,'power':1, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/mrT.jpg':{'haste':False,'power':5, 'toughness':5,'toCast':['4','white','red']}, \
      'images/mtg/creatures/mrTII.jpg':{'haste':False,'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/mtgPlayer.png':{'haste':False,'power':2, 'toughness':2,'toCast':['2']}, \
      'images/mtg/creatures/mysterioIllusionist.png':{'haste':False,'power':1, 'toughness':3,'toCast':['blue','blue','blue']}, \
      'images/mtg/creatures/mystique.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['3','black','blue','blue']}, \
      'images/mtg/creatures/mythBusters.jpg':{'haste':False,'power':6, 'toughness':4,'toCast':['3','red','red']}, \
      'images/mtg/creatures/nerdyPlayer.jpeg':{'haste':False,'power':4, 'toughness':6,'toCast':['3','black','black']}, \
      'images/mtg/creatures/noviceBountyHunter.jpg':{'haste':False,'power':2, 'toughness':1,'toCast':['1','red']}, \
      'images/mtg/creatures/obiWanKenobi.jpg':{'haste':False,'power':5, 'toughness':5,'toCast':['2','white','green','blue']}, \
      'images/mtg/creatures/patton.png':{'haste':False,'power':2, 'toughness':2,'toCast':['2','green','green']}, \
      'images/mtg/creatures/peeweeHerman.jpg':{'haste':False,'power':1, 'toughness':4,'toCast':['1','white','red']}, \
      'images/mtg/creatures/pepe.jpg':{'haste':False,'power':0, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/pikachu.png':{'haste':False,'power':1, 'toughness':2,'toCast':[['blue','red'], ['blue','red']]}, \
      'images/mtg/creatures/pizzaTheHutt.jpg':{'haste':False,'power':3, 'toughness':5,'toCast':['3','black','green']}, \
      'images/mtg/creatures/princeHumperdinck.jpg':{'haste':False,'power':2, 'toughness':5,'toCast':['3','black','black']}, \
      'images/mtg/creatures/princessButtercup.jpg':{'haste':False,'power':2, 'toughness':6,'toCast':['white','white','green','green']}, \
      'images/mtg/creatures/princessLeia.jpg':{'haste':False,'power':2, 'toughness':2,'toCast':['3','white','green','blue']}, \
      'images/mtg/creatures/raichu.jpg':{'haste':False,'power':5, 'toughness':3,'toCast':['4','white','red']}, \
      'images/mtg/creatures/ragePlayer.jpeg':{'haste':False,'power':4, 'toughness':1,'toCast':['red','red','red']}, \
      'images/mtg/creatures/ralphNader.jpg':{'haste':False,'power':2, 'toughness':2,'toCast':['black','green']}, \
      'images/mtg/creatures/redForman.jpg':{'haste':False,'power':1, 'toughness':2,'toCast':['red','red',]}, \
      'images/mtg/creatures/rickGrimes.png':{'haste':False,'power':2, 'toughness':1,'toCast':['2','white','green']}, \
      'images/mtg/creatures/riddick.jfif':{'haste':False,'power':4, 'toughness':4,'toCast':['2','black','red']}, \
      'images/mtg/creatures/rocketRaccoon.jpg':{'haste':False,'power':2, 'toughness':2, 'toCast':['green','blue','red']}, \
      'images/mtg/creatures/robocop.jpg':{'haste':False,'power':4, 'toughness':4,'toCast':['4','white']}, \
      'images/mtg/creatures/rocketTropper.jpg':{'haste':False,'power':2, 'toughness':2,'toCast':['1','red']}, \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':{'haste':False,'power':1, 'toughness':1,'toCast':['black']}, \
      'images/mtg/creatures/samuelJackson.jpg':{'haste':False,'power':99, 'toughness':99,'toCast':['white','black','green','blue','red']}, \
      'images/mtg/creatures/santaClaus.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['2','green','green']}, \
      'images/mtg/creatures/scorpionKing.png':{'haste':False,'power':6, 'toughness':5,'toCast':['3','black','red']}, \
      'images/mtg/creatures/secretGamer.jpeg':{'haste':False,'power':3, 'toughness':3,'toCast':['white','white','white','white']}, \
      'images/mtg/creatures/seleneBloodDrainer.png':{'haste':False,'power':4, 'toughness':4,'toCast':['3','white','black','blue']}, \
      'images/mtg/creatures/shermanTank.png':{'haste':False,'power':3, 'toughness':5,'toCast':['4','blue','blue']}, \
      'images/mtg/creatures/silverSurfer.png':{'haste':False,'power':7, 'toughness':7,'toCast':['1','white','black','green','blue','red']}, \
      'images/mtg/creatures/sirBedevere.jpg':{'haste':False,'power':1, 'toughness':3,'toCast':['white','blue']}, \
      'images/mtg/creatures/sirRobin.png':{'haste':False,'power':2, 'toughness':2,'toCast':['white','blue']}, \
      'images/mtg/creatures/spaceMarineCaptain.png':{'haste':False,'power':4, 'toughness':3,'toCast':['3','white','red']}, \
      'images/mtg/creatures/spiderman.jpg':{'haste':False,'power':4, 'toughness':2,'toCast':['2',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/spidermanII.png':{'haste':False,'power':4, 'toughness':4,'toCast':['3','blue','red']}, \
      'images/mtg/creatures/spock.png':{'haste':False,'power':4, 'toughness':4,'toCast':['2','white','blue']}, \
      'images/mtg/creatures/steveAustin.png':{'haste':False,'power':5, 'toughness':6,'toCast':['1','white','black','red']}, \
      'images/mtg/creatures/stevenRogers.jpg':{'haste':False,'power':4, 'toughness':4,'toCast':['1','white','white','white']}, \
      'images/mtg/creatures/starLord.jpg':{'haste':False,'power':4, 'toughness':3, 'toCast':['2','white','red']}, \
      'images/mtg/creatures/superBattleDroid.jpg':{'haste':False,'power':4, 'toughness':5,'toCast':['5','blue']}, \
      'images/mtg/creatures/superman.gif':{'haste':False,'power':3, 'toughness':3,'toCast':['3','blue','blue']}, \
      'images/mtg/creatures/supermanII.jpg':{'haste':False,'power':6, 'toughness':6,'toCast':['2','white','white','white','white']}, \
      'images/mtg/creatures/t34Tank.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['2','red']}, \
      'images/mtg/creatures/thanos.jpg':{'haste':False,'power':9, 'toughness':9,'toCast':['5','black','black']}, \
      'images/mtg/creatures/theCollector.jpeg':{'haste':False,'power':2, 'toughness':3,'toCast':['1','green','green']}, \
      'images/mtg/creatures/theJoker.jpg':{'haste':False,'power':2, 'toughness':4,'toCast':[['black','red'],['black','red'], ['black','red'], ['black','red']]}, \
      'images/mtg/creatures/theOracle.jpg':{'haste':False,'power':0, 'toughness':3,'toCast':['1','blue','blue']}, \
      'images/mtg/creatures/theSilence.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['4','black']}, \
      'images/mtg/creatures/thor.jpg':{'haste':False,'power':6, 'toughness':6,'toCast':['2','white','blue','red']}, \
      'images/mtg/creatures/thorGodOfThunder.png':{'haste':False,'power':5, 'toughness':5,'toCast':['6',['blue','red'],['blue','red']]}, \
      'images/mtg/creatures/thorSonOfOdin.png':{'haste':False,'power':5, 'toughness':4,'toCast':['4','white','green']}, \
      'images/mtg/creatures/timmyPowerGamer.jpg':{'haste':False,'power':1, 'toughness':1,'toCast':['2','green','green']}, \
      'images/mtg/creatures/toughNerd.jpeg':{'haste':False,'power':3, 'toughness':5,'toCast':['2','red','red','red']}, \
      'images/mtg/creatures/tournamentGrinder.jpg':{'haste':False,'power':1, 'toughness':1,'toCast':['2','black','black']}, \
      'images/mtg/creatures/tribble.png':{'haste':False,'power':1, 'toughness':1,'toCast':['1','white']}, \
      'images/mtg/creatures/trooperCommander.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['2','green']}, \
      'images/mtg/creatures/trump.jpg':{'haste':False,'power':3, 'toughness':5,'toCast':['1','white','blue','red']}, \
      'images/mtg/creatures/unwillingVolunteer.jpg':{'haste':False,'power':1, 'toughness':2,'toCast':['1','green']}, \
      'images/mtg/creatures/vegeta.png':{'haste':False,'power':3, 'toughness':3,'toCast':['black','green','red']}, \
      'images/mtg/creatures/vespaDruishPrincess.jpg':{'haste':False,'power':2, 'toughness':3,'toCast':['green','green']}, \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':{'haste':False,'power':2, 'toughness':4,'toCast':['black','blue','red']}, \
      'images/mtg/creatures/wallOfTrump.png':{'haste':False,'power':0, 'toughness':6,'toCast':['white','white','blue','blue']}, \
      'images/mtg/creatures/warriorBug.png':{'haste':False,'power':1, 'toughness':1,'toCast':['1','green','red']}, \
      'images/mtg/creatures/weepingStatue.jpg':{'haste':False,'power':3, 'toughness':3,'toCast':['4']}, \
      'images/mtg/creatures/westleyMasterofEverything.jpg':{'haste':False,'power':4, 'toughness':5,'toCast':['green','blue','red']}, \
      'images/mtg/creatures/vladimirPutin.jpg':{'haste':False,'power':4,'toughness':4,'toCast':['3','green','green']}, \
      'images/mtg/creatures/youngChild.jpeg':{'haste':False,'power':1, 'toughness':1,'toCast':['white']}, \
      # Lands 
      'images/mtg/lands/red.jpg':{'haste':False,'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/white.jpg':{'haste':False,'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/black.jpg':{'haste':False,'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/blue.jpg':{'haste':False,'power':0, 'toughness':0, 'toCast':['0']}, \
      'images/mtg/lands/green.jpg':{'haste':False,'power':0, 'toughness':0, 'toCast':['0']}, \
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
           