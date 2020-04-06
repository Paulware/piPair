import random
class castingCost: 
   cost = { \
      'images/mtg/creatures/agentSmith.jpg':['black'], \
      'images/mtg/creatures/alGore.jpg':['green'], \
      'images/mtg/creatures/americanEagle.jpg':['white','blue','red'], \
      'images/mtg/creatures/annoyingOrange.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/arbalestElite.jfif':['white'], \
      'images/mtg/creatures/arrgh.jpg':['black'], \
      'images/mtg/creatures/averageAmerican.jpg':['red'], \
      'images/mtg/creatures/barackHObama.jpg':['red'], \
      'images/mtg/creatures/barackObama.jpg':['white','green','blue'], \
      'images/mtg/creatures/barackObamaII.jpg':['green'], \
      'images/mtg/creatures/barfEagleFiveNavigator.jpg':['white','blue','red'], \
      'images/mtg/creatures/batman.jpg':['white','blue'], \
      'images/mtg/creatures/batmanII.jpg':['white','black'], \
      'images/mtg/creatures/berneyStinson.jpg':['red'], \
      'images/mtg/creatures/bernieSanders.jpg':['white'], \
      'images/mtg/creatures/bernieSandersII.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/bickeringGiant.jpg':['black','green','red'], \
      'images/mtg/creatures/biffTannen.jpg':['black','red'], \
      'images/mtg/creatures/blackKnight.jpg':['black'], \
      'images/mtg/creatures/bruceLee.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/burninator.jpg':['red'], \
      'images/mtg/creatures/cantinaBand.jpg':['white'], \
      'images/mtg/creatures/charlesXavier.jpg':['white','blue'], \
      'images/mtg/creatures/cheatyFace.jpg':['blue'], \
      'images/mtg/creatures/chivalrousChevalier.jpg':['white'], \
      'images/mtg/creatures/chuckNorris.jpg':['green'], \
      'images/mtg/creatures/countTyroneRugen.jpg':['black','red'], \
      'images/mtg/creatures/daenerysStormborn.jpg':['white','black','green','red'], \
      'images/mtg/creatures/daringSaboteur.jpg':['blue'], \
      'images/mtg/creatures/darthSidious.jpg':['black','blue','red'], \
      'images/mtg/creatures/darthVader.jpg':['black'], \
      'images/mtg/creatures/darkHelmet.jpg':['black','blue'], \
      'images/mtg/creatures/darylDixon.jpg':['red'], \
      'images/mtg/creatures/deadPool.png':['black','red'], \
      'images/mtg/creatures/deadPoolAgain.jpg':['black','red'], \
      'images/mtg/creatures/deadpoolFairyPrincess.jpg':['black','red'], \
      'images/mtg/creatures/deadPoolIII.png':['black','red'], \
      'images/mtg/creatures/doge.jpg':['white'], \
      'images/mtg/creatures/doctorEmmettBrown.jpg':['blue'], \
      'images/mtg/creatures/drHouse.jpg':['white'], \
      'images/mtg/creatures/drStrange.jpg':['white','black','blue'], \
      'images/mtg/creatures/earlOfSquirrel.jpg':['green'], \
      'images/mtg/creatures/extremelySlowZombie.jpg':['black'], \
      # Add tap, creature gains flying and is destroyed at end of turn (Fezzik)
      'images/mtg/creatures/fezzikTheKindlyGiant.jpg':['white','green','red'], \
      'images/mtg/creatures/gameStoreEmployee.jpg':['blue'], \
      'images/mtg/creatures/generalGrievous.jpg':['white','black','blue'], \
      'images/mtg/creatures/georgeBushII.jpg':['white','blue','red'], \
      'images/mtg/creatures/georgeMcfly.jpg':['white','blue'], \
      'images/mtg/creatures/georgeWBush.jpg':['red'], \
      'images/mtg/creatures/god.png':['white','black','green','blue','red'], \
      'images/mtg/creatures/gordonRamsey.jpg':['red'], \
      'images/mtg/creatures/groundPounder.jpg':['green'], \
      'images/mtg/creatures/hangman.jpg':['black'], \
      'images/mtg/creatures/hanSolo.jpg':['white'], \
      'images/mtg/creatures/hillaryClinton.jpeg':['white','red'], \
      'images/mtg/creatures/ifThatGetsLeftHanging.jpg':['red'], \
      'images/mtg/creatures/iKnowKungFu.jpg':['green'], \
      'images/mtg/creatures/infinityElemental.jpg':['red'], \
      'images/mtg/creatures/inigoMontoya.jpg':['white','red'], \
      'images/mtg/creatures/inigoMontoyaII.jpg':['white','green','red'], \
      'images/mtg/creatures/ironMan.png':['white','red'], \
      'images/mtg/creatures/ironManII.jpg':['white','red'], \
      'images/mtg/creatures/jaceTheAsshole.jpg':['blue'], \
      'images/mtg/creatures/jangoFett.jpg':['red'], \
      'images/mtg/creatures/jeanGrey.jpg':['black','red'], \
      'images/mtg/creatures/johnLennon.jpg':['green','blue'], \
      'images/mtg/creatures/johnnyCash.jpg':['white','black'], \
      'images/mtg/creatures/johnnyCombo.png':['blue'], \
      'images/mtg/creatures/joshLane.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/kanyeWest.png':['black'], \
      'images/mtg/creatures/killerBunny.jpg':['white'], \
      'images/mtg/creatures/kittyPryde.jpg':['white','blue'], \
      'images/mtg/creatures/koolAidMan.jpg':['red'], \
      'images/mtg/creatures/krillin.jpg':['white'], \
      'images/mtg/creatures/libyanTerrorists.jpg':['red'], \
      'images/mtg/creatures/logan.jpg':['green','red'], \
      'images/mtg/creatures/lordVoldemort.jpg':['black'], \
      'images/mtg/creatures/magneto.jpg':['black','blue','red'], \
      'images/mtg/creatures/mario.jpg':['red'], \
      'images/mtg/creatures/martyMcFly.jpg':['white','red'], \
      'images/mtg/creatures/masterfulNinja.jpg':['black'], \
      'images/mtg/creatures/memePirate.jpeg':['blue','red'], \
      'images/mtg/creatures/miracleMax.jpg':['white','blue'], \
      'images/mtg/creatures/mrT.jpg':['white','red'], \
      'images/mtg/creatures/mrTII.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/mtgPlayer.png':['white'], \
      'images/mtg/creatures/mysterioIllusionist.png':['blue'], \
      'images/mtg/creatures/mystique.jpg':['black','blue'], \
      'images/mtg/creatures/mythBusters.jpg':['red'], \
      'images/mtg/creatures/nerdyPlayer.jpeg':['black'], \
      'images/mtg/creatures/noviceBountyHunter.jpg':['red'], \
      'images/mtg/creatures/obiWanKenobi.jpg':['white','green','blue'], \
      'images/mtg/creatures/oliviaVampire.jpg':['black','red'], \
      'images/mtg/creatures/painiac.jpg':['red'], \
      'images/mtg/creatures/partycrasher.jpg':['red'], \
      'images/mtg/creatures/peasants.png':['white','green'], \
      'images/mtg/creatures/peeweeHerman.jpg':['white','red'], \
      'images/mtg/creatures/pepe.jpg':['black'], \
      'images/mtg/creatures/phoebeHeadOfSneak.jpg':['black','blue'], \
      'images/mtg/creatures/pizzaTheHutt.jpg':['black','green'], \
      'images/mtg/creatures/princeHumperdinck.jpg':['black'], \
      'images/mtg/creatures/princessButtercup.jpg':['white','green'], \
      'images/mtg/creatures/princessLeia.jpg':['white','green','blue'], \
      'images/mtg/creatures/ragePlayer.jpeg':['red'], \
      'images/mtg/creatures/ralphNader.jpg':['black','green'], \
      'images/mtg/creatures/redForman.jpg':['red'], \
      'images/mtg/creatures/rickGrimes.png':['white','green'], \
      'images/mtg/creatures/riddick.jfif':['black','red'], \
      'images/mtg/creatures/robocop.jpg':['white'], \
      'images/mtg/creatures/rocketTropper.jpg':['red'], \
      'images/mtg/creatures/rodentOfUnusualSize.jpg':['black'], \
      'images/mtg/creatures/samuelJackson.jpg':['white','black','green','blue','red'], \
      'images/mtg/creatures/santaClaus.jpg':['green'], \
      'images/mtg/creatures/scorpionKing.png':['black','red'], \
      'images/mtg/creatures/secretGamer.jpeg':['white'], \
      'images/mtg/creatures/sirBedevere.jpg':['white','blue'], \
      'images/mtg/creatures/sirRobin.png':['white','blue'], \
      'images/mtg/creatures/skinShifter.jpg':['green'], \
      'images/mtg/creatures/skullSaucer.jpg':['black'], \
      'images/mtg/creatures/sneakDispatcher.png':['blue'], \
      'images/mtg/creatures/spiderman.jpg':['blue','red'], \
      'images/mtg/creatures/spidermanII.png':['blue','red'], \
      'images/mtg/creatures/spyEye.png':['blue'], \
      'images/mtg/creatures/stoneColdBasilisk.jpg':['green'], \
      'images/mtg/creatures/superBattleDroid.jpg':['blue'], \
      'images/mtg/creatures/superman.gif':['blue'], \
      'images/mtg/creatures/supermanII.jpg':['white'], \
      'images/mtg/creatures/supermanIII.png':['white','blue','red'], \
      'images/mtg/creatures/surgeonCommander.png':['green'], \
      'images/mtg/creatures/theCollector.jpeg':['green'], \
      'images/mtg/creatures/theJoker.jpg':['black','red'], \
      'images/mtg/creatures/theOracle.jpg':['blue'], \
      'images/mtg/creatures/theSilence.jpg':['black'], \
      'images/mtg/creatures/timmyPowerGamer.jpg':['green'], \
      'images/mtg/creatures/toughNerd.jpeg':['red'], \
      'images/mtg/creatures/tournamentGrinder.jpg':['black'], \
      'images/mtg/creatures/trooperCommander.jpg':['green'], \
      'images/mtg/creatures/trump.jpg':['white','blue','red'], \
      'images/mtg/creatures/unwillingVolunteer.jpg':['green'], \
      'images/mtg/creatures/vespaDruishPrincess.jpg':['green'], \
      'images/mtg/creatures/vizziniSicilianMastermind.jpg':['black','blue','red'], \
      'images/mtg/creatures/wallOfTrump.png':['white','blue'], \
      'images/mtg/creatures/weepingStatue.jpg':['white'], \
      'images/mtg/creatures/westleyMasterofEverything.jpg':['green','blue','red'], \
      'images/mtg/creatures/wharfinfiltrator.jpg':['blue'], \
      'images/mtg/creatures/youngChild.jpeg':['white'] \
   }
   def __init__(self):
      pass
      
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
      
   def matchingCards (self,filename):    
      matches = []
      casting = self.cost[filename]
      for key in self.cost:
         if self.cost[key] == casting: 
            matches.append (key) 

      print ( "Got a casting cost of: " + str(casting) )
      return matches
      
   def buildDeck (self,filename): 
      deck = []
      count = 0
      creatures = self.matchingCards (filename)
      colors = self.cost[filename]
      maxCreatures = 30
      # continue until you have enough creatures
      while len(deck) < maxCreatures: 
         # For each creature 
         for key in self.cost:
            if self.cost[key] == colors: # Check if casting matches
               deck.append (key) 
            else: # check if mono color matches
               for color in colors:
                  if self.cost[key] == [color]: 
                     deck.append (key)
                     break
              
            if len(deck) == maxCreatures:
               break            
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

      