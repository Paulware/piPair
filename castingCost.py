import random
class castingCost: 
   cost = { \
      'images/mtg/creatures/agentSmith.jpg':['4','black','black'], \
      'images/mtg/creatures/alGore.jpg':['green','green'], \
      'images/mtg/creatures/americanEagle.jpg':['3','white','blue','red'], \
      'images/mtg/creatures/annoyingOrange.jpg':['green','blue','red'], \
      'images/mtg/creatures/arbalestElite.jpg':['2','white','white'], \
      'images/mtg/creatures/arrgh.jpg':['black','black','black'], \
      'images/mtg/creatures/barackHObama.jpg':['1','red'], \
      'images/mtg/creatures/barackObama.jpg':[['green','blue'],['green','blue'],['green','blue'],['white','blue'],['white','blue'],['white','blue']], \
      'images/mtg/creatures/barackObamaII.jpg':['3','black'], \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':['white','blue','red'], \
      'images/mtg/creatures/batman.jpg':['3','white','blue'], \
      'images/mtg/creatures/batmanII.jpg':['3',['white','black'],['white','black'],['white','black']], \
      'images/mtg/creatures/berneyStinson.jpg':['red','red'], \
      'images/mtg/creatures/bernieSanders.jpg':['2','white','white'], \
      'images/mtg/creatures/bernieSandersII.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/bickeringGiant.jpg':['black','green','red'], \
      'images/mtg/creatures/biffTannen.jpg':['4','black','red'], \
      'images/mtg/creatures/blackKnight.jpg':['1','black','black'], \
      'images/mtg/creatures/borgCube.jpg':['4','black','black'], \
      'images/mtg/creatures/borgQueen.jpg':['white','white','black','black','blue','blue','blue'], \
      'images/mtg/creatures/bruceLee.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/burninator.jpg':['9','red'], \
      'images/mtg/creatures/cantinaBand.jpg':['white'], \
      'images/mtg/creatures/charlesXavier.jpg':['2','white','blue','blue'], \
      'images/mtg/creatures/cheatyFace.jpg':['blue','blue'], \
      'images/mtg/creatures/chivalrousChevalier.jpg':['4','white'], \
      'images/mtg/creatures/chuckNorris.jpg':['9','green'], \
      'images/mtg/creatures/conanTheBarbarian.png':['2','red','red'], \
      'images/mtg/creatures/conanTheLibrarian.png':['4','red','red'], \
      'images/mtg/creatures/countTyroneRugen.jpg':['black','black','red'], \
      'images/mtg/creatures/daenerysStormborn.jpg':['1','white','black','green','red'], \
      'images/mtg/creatures/darthSidious.jpg':['4','black','blue','red'], \
      'images/mtg/creatures/darthVader.jpg':['5','black','black','black','black','black'], \
      'images/mtg/creatures/darkHelmet.jpg':['3','black','black','blue'], \
      'images/mtg/creatures/darylDixon.jpg':['red','red','red','red','red'], \
      'images/mtg/creatures/deadPool.png':['2','black','red','red'], \
      'images/mtg/creatures/deadPoolAgain.jpg':['3','black','red'], \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':['1','black','red'], \
      'images/mtg/creatures/deadPoolIII.png':['4','black','red'], \
      'images/mtg/creatures/dickJones.png':['3','black','black'],
      'images/mtg/creatures/doctorEmmettBrown.jpg':['2','blue','blue'], \
      'images/mtg/creatures/doge.jpg':['1'], \
      'images/mtg/creatures/drHouse.jpg':['5','white','white','white'], \
      'images/mtg/creatures/drStrange.jpg':['1','white','black','blue'], \
      'images/mtg/creatures/earlOfSquirrel.jpg':['4','green','green'], \
      'images/mtg/creatures/extremelySlowZombie.jpg':['1','black'], \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':['1','white','green','red'], \
      'images/mtg/creatures/galactus.jpg':['10'], \
      'images/mtg/creatures/gameStoreEmployee.jpg':['blue','blue'], \
      'images/mtg/creatures/gandalf.png':['2','white','blue'], \
      'images/mtg/creatures/generalGrievous.jpg':['white','black','blue'], \
      'images/mtg/creatures/georgeBushII.jpg':['white','blue','red'], \
      'images/mtg/creatures/georgeMcfly.jpg':['1','white','blue'], \
      'images/mtg/creatures/georgeWBush.jpg':['red'], \
      'images/mtg/creatures/god.png':['white','black','green','blue','red'], \
      'images/mtg/creatures/gordonRamsey.jpg':['3','red'], \
      'images/mtg/creatures/hangman.jpg':['black'], \
      'images/mtg/creatures/hanSolo.jpg':['3','white'], \
      'images/mtg/creatures/hela.png':['4',['black','red'],'green'], \
      'images/mtg/creatures/hillaryClinton.jpeg':['2','white','red'], \
      'images/mtg/creatures/hitler.jpg':['black'], \
      'images/mtg/creatures/hulk.png':['green','green','green','green','green','green'], \
      'images/mtg/creatures/iKnowKungFu.jpg':['3','green'], \
      'images/mtg/creatures/indianaJones.jpg':['1','white','blue'], \
      'images/mtg/creatures/infinityElemental.jpg':['4','red','red','red'], \
      'images/mtg/creatures/inigoMontoya.jpg':['2',['red','white'],['red','white']], \
      'images/mtg/creatures/inigoMontoyaII.jpg':['white','green','red'], \
      'images/mtg/creatures/ironMan.png':['2','white','red','red'], \
      'images/mtg/creatures/ironManII.jpg':['5','white','red'], \
      'images/mtg/creatures/itThatGetsLeftHanging.jpg':['5','red'], \
      'images/mtg/creatures/jaceTheAsshole.jpg':['blue'], \
      'images/mtg/creatures/jamesKirk.png':['1','white',['blue','red'],['blue','red']], \
      'images/mtg/creatures/jangoFett.jpg':['2','red','red'], \
      'images/mtg/creatures/jeanGrey.jpg':['3','black','red'], \
      'images/mtg/creatures/johnLennon.jpg':['3',['green','blue'],['green','blue']], \
      'images/mtg/creatures/johnnyCash.jpg':['3',['white','black'],['white','black']], \
      'images/mtg/creatures/johnnyCombo.png':['2','blue','blue'], \
      'images/mtg/creatures/josefStalin.png':['8','red','red'], \
      'images/mtg/creatures/joshLane.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/kanyeWest.png':['black'], \
      'images/mtg/creatures/killerBunny.jpg':['white'], \
      'images/mtg/creatures/kittyPryde.jpg':['2','white','blue'], \
      'images/mtg/creatures/koolAidMan.jpg':['2','red','red'], \
      'images/mtg/creatures/krillin.jpg':['white'], \
      'images/mtg/creatures/libyanTerrorists.jpg':['4','red','red'], \
      'images/mtg/creatures/logan.jpg':['3',['red','green'],['red','green']], \
      'images/mtg/creatures/lordVoldemort.jpg':['3','black','black','black'], \
      'images/mtg/creatures/magneto.jpg':['3','black','blue','red'], \
      'images/mtg/creatures/mario.jpg':['3','red','red'], \
      'images/mtg/creatures/martyMcFly.jpg':['2','white','red'], \
      'images/mtg/creatures/memePirate.jpeg':['2','blue','red'], \
      'images/mtg/creatures/miracleMax.jpg':['white','blue'], \
      'images/mtg/creatures/mrT.jpg':['4','white','red'], \
      'images/mtg/creatures/mrTII.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/mtgPlayer.png':['2'], \
      'images/mtg/creatures/mysterioIllusionist.png':['blue','blue','blue'], \
      'images/mtg/creatures/mystique.jpg':['3','black','blue','blue'], \
      'images/mtg/creatures/mythBusters.jpg':['3','red','red'], \
      'images/mtg/creatures/nerdyPlayer.jpeg':['3','black','black'], \
      'images/mtg/creatures/noviceBountyHunter.jpg':['1','red'], \
      'images/mtg/creatures/obiWanKenobi.jpg':['2','white','green','blue'], \
      'images/mtg/creatures/patton.png':['2','green','green'], \
      'images/mtg/creatures/peasants.png':['1','white','green'], \
      'images/mtg/creatures/peeweeHerman.jpg':['1','white','red'], \
      'images/mtg/creatures/pepe.jpg':['black'], \
      'images/mtg/creatures/pizzaTheHutt.jpg':['3','black','green'], \
      'images/mtg/creatures/princeHumperdinck.jpg':['3','black','black'], \
      'images/mtg/creatures/princessButtercup.jpg':['white','white','green','green'], \
      'images/mtg/creatures/princessLeia.jpg':['3','white','green','blue'], \
      'images/mtg/creatures/ragePlayer.jpeg':['red','red','red'], \
      'images/mtg/creatures/ralphNader.jpg':['black','green'], \
      'images/mtg/creatures/redForman.jpg':['red','red',], \
      'images/mtg/creatures/rickGrimes.png':['2','white','green'], \
      'images/mtg/creatures/riddick.jfif':['2','black','red'], \
      'images/mtg/creatures/robocop.jpg':['4','white'], \
      'images/mtg/creatures/rocketTropper.jpg':['1','red'], \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':['black'], \
      'images/mtg/creatures/samuelJackson.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/santaClaus.jpg':['2','green','green'], \
      'images/mtg/creatures/scorpionKing.png':['3','black','red'], \
      'images/mtg/creatures/secretGamer.jpeg':['white','white','white','white'], \
      'images/mtg/creatures/seleneBloodDrainer.png':['3','white','black','blue'], \
      'images/mtg/creatures/shermanTank.png':['4','blue','blue'], \
      'images/mtg/creatures/silverSurfer.png':['1','white','black','green','blue','red'], \
      'images/mtg/creatures/sirBedevere.jpg':['white','blue'], \
      'images/mtg/creatures/sirRobin.png':['white','blue'], \
      'images/mtg/creatures/spiderman.jpg':['2',['blue','red'],['blue','red']], \
      'images/mtg/creatures/spidermanII.png':['3','blue','red'], \
      'images/mtg/creatures/spock.png':['2','white','blue'], \
      'images/mtg/creatures/steveAustin.png':['1','white','black','red'], \
      'images/mtg/creatures/superBattleDroid.jpg':['5','blue'], \
      'images/mtg/creatures/superman.gif':['3','blue','blue'], \
      'images/mtg/creatures/supermanII.jpg':['2','white','white','white','white'], \
      'images/mtg/creatures/t34Tank.jpg':['2','red'], \
      'images/mtg/creatures/theCollector.jpeg':['1','green','green'], \
      'images/mtg/creatures/theJoker.jpg':[['black','red'],['black','red'], ['black','red'], ['black','red']], \
      'images/mtg/creatures/theOracle.jpg':['1','blue','blue'], \
      'images/mtg/creatures/theSilence.jpg':['4','black'], \
      'images/mtg/creatures/thor.jpg':['2','white','blue','red'], \
      'images/mtg/creatures/thorGodOfThunder.png':['6',['blue','red'],['blue','red']], \
      'images/mtg/creatures/thorSonOfOdin.png':['4','white','green'], \
      'images/mtg/creatures/timmyPowerGamer.jpg':['2','green','green'], \
      'images/mtg/creatures/tigerTank.png':['8'], \
      'images/mtg/creatures/toughNerd.jpeg':['2','red','red','red'], \
      'images/mtg/creatures/tournamentGrinder.jpg':['2','black','black'], \
      'images/mtg/creatures/tribble.png':['1','white'], \
      'images/mtg/creatures/trooperCommander.jpg':['2','green'], \
      'images/mtg/creatures/trump.jpg':['1','white','blue','red'], \
      'images/mtg/creatures/unwillingVolunteer.jpg':['1','green'], \
      'images/mtg/creatures/vespaDruishPrincess.jpg':['green','green'], \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':['black','blue','red'], \
      'images/mtg/creatures/wallOfTrump.png':['white','white','blue','blue'], \
      'images/mtg/creatures/weepingStatue.jpg':['4'], \
      'images/mtg/creatures/westleyMasterofEverything.jpg':['green','blue','red'], \
      'images/mtg/creatures/youngChild.jpeg':['white'] \
   }
   def __init__(self):
      pass
      
   def totalManaCost(self,filename): 
      list = self.cost[filename]
      total = 1
      if list[0].isnumeric():
         total = int(list[0])
         
      total = total + len(list) - 1
      return total
      
   def allCards(self):
      cards = []
      indexes = []
      count = 0      
      for key in self.cost:
         cards.append ( {'index':count,'iOwnIt':True, 'filename':key, 'location':'library', 'tapped':False } )
         indexes.append (count)
         count = count + 1
      return (cards,indexes)
      
   def matchingColor (self, color):
      matches = []
      for key in self.cost: 
         if self.cost[key] == [color]:
            matches.append (key)               
      return matches
      
   def baseCost ( self, filename ):
      base = []
      casting = self.cost[filename]
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
         if count == len(creatures):
            count = 0
            
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

      