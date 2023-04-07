class ManaCost (): 
   def totalMana (self,mana):
      total = 0
      for color in self.colors: 
         total = total + mana[color]
      return total 
      
   def enoughMana (self,mana,filename):
      enough = False
      cost = self.cost[filename]
      if self.totalMana (mana) < self.totalMana (cost): 
         print ( 'You do not have enough total mana to handle this cost: ' + str(self.totalMana (cost)) )
      else: # This is sufficient total mana....
         if mana['colorless'] >= cost ['colorless']: 
            if mana['red'] >= cost ['red']:
               if mana ['black'] >= cost ['black']:
                  if mana ['blue'] >= cost ['blue']:
                     if mana ['white'] >= cost ['white']:
                        if mana ['green'] >= cost ['green']:
                           enough = True
                        else:
                           print ( 'Not enough green' )
                     else:
                        print ( 'Not enough white' )
                  else:
                     print ( 'Not enough blue' )
               else:
                  print ( 'Not enough black' )
            else:
               print ( 'Not enough red' )
         else:
            print ( 'Not enough colorless' )
            
      if not enough:
         print ( 'Cannot cast: ' + filename )
      return enough 
      
   def __init__(self):    
      self.colors = ['colorless','red','black','blue','white','green']
      self.cost = {\
         'artifacts/The Machine.jpg':               {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/ak47.png':                      {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/beeBeeBun.jpg':                 {'colorless':6, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/bfg.jpg':                       {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/blackerLotus.jpg':              {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/blurryBeeble.jpg':              {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'artifacts/captainAmericasShield.png':     {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/chaosConfetti.jpg':             {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/doItYourselfSeraph.png':        {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'artifacts/doge.jpg':                      {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/dragonBalls.jpg':               {'colorless':7, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/eagleFiveWinnebago.jpg':        {'colorless':6, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/fluxCapacitor.jpg':             {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/fodderCannon.jpg':              {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/galactus.jpg':                  {'colorless':10, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/gatlingGun.png':                {'kick':1,'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/infinityGauntlet.png':          {'colorless':6, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/letterBomb.jpg':                {'colorless':6, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/limbReplacement.png':           {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/m1911.png':                     {'colorless':9, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/molotov.png':                   {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/nullRod.jpg':                   {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/peeweesBike.jpg':               {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/predatorTech.jpg':              {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/psychicPaper.jpg':              {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/ratchetBomb.jpg':               {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/sonicScrewdriver.jpg':          {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/staffofdomination.jpg':         {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/swordOfDungeonsAndDragons.jpg': {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/tardis.jpg':                    {'colorless':0, 'red':0, 'black':0,'blue':6, 'white':0, 'green':0},\
         'artifacts/tesseract.png':                 {'colorless':3, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'artifacts/thatAss.jpg':                   {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/tigerTank.png':                 {'colorless':8, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/tinman.png':                    {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'artifacts/urzasContactLenses.jpg':        {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/agentSmith.jpg':                {'colorless':4, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/alGore.jpg':                    {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/americanEagle.jpg':             {'colorless':3, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/android17.png':                 {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/android18.png':                 {'colorless':2, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/annoyingOrange.jpg':            {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':0, 'green':1},\
         'creatures/arrgh.jpg':                     {'colorless':0, 'red':0, 'black':3,'blue':0, 'white':0, 'green':0},\
         'creatures/arthurKingOfTheBritains.jpg':   {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/barackHObama.jpg':              {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/barackObama.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'grnblu':3, 'whtblu':3},\
         'creatures/barackObamaII.jpg':             {'colorless':3, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/barfEagleFiveNavigator.jpg':    {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/batman.jpg':                    {'colorless':3, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/batmanII.jpg':                  {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'whtblk':3},\
         'creatures/berneyStinson.jpg':             {'colorless':0, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/bernieSanders.jpg':             {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/bernieSandersII.jpg':           {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/bickeringGiant.jpg':            {'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':1},\
         'creatures/biffTannen.jpg':                {'colorless':4, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/blackKnight.jpg':               {'colorless':1, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/borgCube.jpg':                  {'colorless':4, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/borgQueen.jpg':                 {'colorless':0, 'red':0, 'black':3,'blue':3, 'white':2, 'green':0},\
         'creatures/bruceLee.jpg':                  {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/burninator.jpg':                {'colorless':9, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/cantinaBand.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/captainAmerica.jfif':           {'colorless':2, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/charlesXavier.jpg':             {'colorless':2, 'red':0, 'black':0,'blue':2, 'white':1, 'green':0},\
         'creatures/cheatyFace.jpg':                {'colorless':0, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/chivalrousChevalier.jpg':       {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/chuckNorris.jpg':               {'colorless':9, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/conanTheBarbarian.png':         {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/conanTheLibrarian.png':         {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/countTyroneRugen.jpg':          {'colorless':0, 'red':1, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/cowardlyLion.png':              {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/daenerysStormborn.jpg':         {'colorless':1, 'red':1, 'black':1,'blue':0, 'white':1, 'green':1},\
         'creatures/darkHelmet.jpg':                {'colorless':3, 'red':0, 'black':2,'blue':1, 'white':0, 'green':0},\
         'creatures/darthSidious.jpg':              {'colorless':4, 'red':1, 'black':1,'blue':1, 'white':0, 'green':0},\
         'creatures/darthVader.jpg':                {'colorless':5, 'red':0, 'black':5,'blue':0, 'white':0, 'green':0},\
         'creatures/darylDixon.jpg':                {'colorless':0, 'red':5, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/deadPool.png':                  {'colorless':2, 'red':2, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/deadPoolAgain.jpg':             {'colorless':3, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/deadPoolIII.png':               {'colorless':4, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/deadpoolFairyPrincess.jpg':     {'colorless':1, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/dickJones.png':                 {'colorless':3, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/doctorEmmettBrown.jpg':         {'colorless':2, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/donkeyKong.png':                {'colorless':5, 'red':1, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/drHouse.jpg':                   {'colorless':5, 'red':0, 'black':0,'blue':0, 'white':3, 'green':0},\
         'creatures/drStrange.jpg':                 {'colorless':1, 'red':0, 'black':1,'blue':1, 'white':1, 'green':0},\
         'creatures/draxDestroyer.jpg':             {'colorless':4, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0, 'blublk':1},\
         'creatures/earlOfSquirrel.jpg':            {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/extremelySlowZombie.jpg':       {'colorless':1, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/fezzikTheKindlyGiant.jpg':      {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':1, 'green':1},\
         'creatures/frieza.jpg':                    {'colorless':0, 'red':0, 'black':2,'blue':1, 'white':0, 'green':0},\
         'creatures/gameStoreEmployee.jpg':         {'colorless':0, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/gamora.jpg':                    {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/gandalf.png':                   {'colorless':2, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/generalGrievous.jpg':           {'colorless':0, 'red':0, 'black':1,'blue':1, 'white':1, 'green':0},\
         'creatures/georgeBushII.jpg':              {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/georgeMcfly.jpg':               {'colorless':1, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/georgeWBush.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/gilligan.png':                  {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/god.png':                       {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/godzilla.jpg':                  {'colorless':5, 'red':1, 'black':0,'blue':1, 'white':0, 'green':1},\
         'creatures/gordonRamsey.jpg':              {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/groot.jpg':                     {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':1, 'green':2},\
         'creatures/hanSolo.jpg':                   {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/hangman.jpg':                   {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/hela.png':                      {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1, 'blkred':1},\
         'creatures/hillaryClinton.jpeg':           {'colorless':2, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/hirohito.png':                  {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/hitler.jpg':                    {'colorless':0, 'red':0, 'black':4,'blue':0, 'white':0, 'green':0},\
         'creatures/hulk.png':                      {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':6},\
         'creatures/indianaJones.jpg':              {'colorless':1, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/infinityElemental.jpg':         {'colorless':4, 'red':3, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/inigoMontoya.jpg':              {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'redwht':2},\
         'creatures/inigoMontoyaII.jpg':            {'colorless':0, 'red':1, 'black':0,'blue':0, 'white':1, 'green':1},\
         'creatures/ironMan.png':                   {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/ironManII.jpg':                 {'colorless':5, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/itThatGetsLeftHanging.jpg':     {'colorless':5, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/jaceTheAsshole.jpg':            {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'creatures/jamesKirk.png':                 {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0, 'blured':2},\
         'creatures/jangoFett.jpg':                 {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/jeanGrey.jpg':                  {'colorless':3, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/johnLennon.jpg':                {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'grnblu':2},\
         'creatures/johnnyCash.jpg':                {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'whtblk':2},\
         'creatures/johnnyCombo.png':               {'colorless':2, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/josefStalin.png':               {'colorless':8, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/joshLane.jpg':                  {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/kanyeWest.png':                 {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/killerBunny.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/kingKong.jpg':                  {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/kittyPryde.jpg':                {'colorless':2, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/koolAidMan.jpg':                {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/krillin.jpg':                   {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/libyanTerrorists.jpg':          {'colorless':4, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/logan.jpg':                     {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'redgrn':2},\
         'creatures/lordVoldemort.jpg':             {'colorless':3, 'red':0, 'black':3,'blue':0, 'white':0, 'green':0},\
         'creatures/magneto.jpg':                   {'colorless':3, 'red':1, 'black':1,'blue':1, 'white':0, 'green':0},\
         'creatures/mario.jpg':                     {'colorless':3, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/martyMcFly.jpg':                {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/masterChief.png':               {'colorless':2, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/memePirate.jpeg':               {'colorless':2, 'red':1, 'black':0,'blue':1, 'white':0, 'green':0},\
         'creatures/miracleMax.jpg':                {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/mrT.jpg':                       {'colorless':4, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/mrTII.jpg':                     {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/mtgPlayer.png':                 {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/mysterioIllusionist.png':       {'colorless':0, 'red':0, 'black':0,'blue':3, 'white':0, 'green':0},\
         'creatures/mystique.jpg':                  {'colorless':3, 'red':0, 'black':1,'blue':2, 'white':0, 'green':0},\
         'creatures/mythBusters.jpg':               {'colorless':3, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/nerdyPlayer.jpeg':              {'colorless':3, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/noviceBountyHunter.jpg':        {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/obiWanKenobi.jpg':              {'colorless':2, 'red':0, 'black':0,'blue':1, 'white':1, 'green':1},\
         'creatures/oldGuard.jpg':                  {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/patton.png':                    {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/peeweeHerman.jpg':              {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/pepe.jpg':                      {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/pikachu.png':                   {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'blured':2},\
         'creatures/pizzaTheHutt.jpg':              {'colorless':3, 'red':0, 'black':1,'blue':0, 'white':0, 'green':1},\
         'creatures/predator.png':                  {'colorless':4, 'red':1, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/princeHumperdinck.jpg':         {'colorless':3, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/princessButtercup.jpg':         {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':2, 'green':2},\
         'creatures/princessLeia.jpg':              {'colorless':3, 'red':0, 'black':0,'blue':1, 'white':1, 'green':1},\
         'creatures/ragePlayer.jpeg':               {'colorless':0, 'red':3, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/raichu.jpg':                    {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/ralphNader.jpg':                {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':1},\
         'creatures/redForman.jpg':                 {'colorless':0, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/rickGrimes.png':                {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':1, 'green':1},\
         'creatures/riddick.jfif':                  {'colorless':2, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/robocop.jpg':                   {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/rocketRaccoon.jpg':             {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':0, 'green':1},\
         'creatures/rocketTropper.jpg':             {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/rodentOfUnusualSize.jpg':       {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/samuelJackson.jpg':             {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/santaClaus.jpg':                {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/scorpionKing.png':              {'colorless':3, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/secretGamer.jpeg':              {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':4, 'green':0},\
         'creatures/seleneBloodDrainer.png':        {'colorless':3, 'red':0, 'black':1,'blue':1, 'white':1, 'green':0},\
         'creatures/shermanTank.png':               {'colorless':4, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/silverSurfer.png':              {'colorless':1, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/sirBedevere.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/sirRobin.png':                  {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/spaceMarineCaptain.png':        {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/spiderman.jpg':                 {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'blured':2},\
         'creatures/spidermanII.png':               {'colorless':3, 'red':1, 'black':0,'blue':1, 'white':0, 'green':0},\
         'creatures/spock.png':                     {'colorless':2, 'red':2, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/starLord.jpg':                  {'colorless':2, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/steveAustin.png':               {'kick':1, 'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/stevenRogers.jpg':              {'colorless':1, 'red':0, 'black':1,'blue':0, 'white':3, 'green':0},\
         'creatures/superBattleDroid.jpg':          {'colorless':5, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'creatures/superman.jpg':                  {'colorless':3, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/supermanII.jpg':                {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':4, 'green':0},\
         'creatures/supermanIII.png':               {'colorless':5, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/t34Tank.jpg':                   {'colorless':2, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/thanos.jpg':                    {'colorless':5, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/theCollector.jpeg':             {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/theJoker.jpg':                  {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'blkred':4},\
         'creatures/theOracle.jpg':                 {'colorless':1, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/theSilence.jpg':                {'colorless':4, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/thor.jpg':                      {'colorless':2, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/thorGodOfThunder.png':          {'colorless':6, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'blured':2},\
         'creatures/thorSonOfOdin.png':             {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':1, 'green':1},\
         'creatures/timmyPowerGamer.jpg':           {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/toughNerd.jpeg':                {'colorless':2, 'red':3, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/tournamentGrinder.jpg':         {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'spike':2},\
         'creatures/tribble.png':                   {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/trooperCommander.jpg':          {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/trump.jpg':                     {'colorless':1, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/unwillingVolunteer.jpg':        {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/vegeta.png':                    {'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':1},\
         'creatures/vespaDruishPrincess.jpg':       {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/vizziniSicilianMastermind.jpg': {'colorless':0, 'red':1, 'black':1,'blue':1, 'white':0, 'green':0},\
         'creatures/vladimirPutin.jpg':             {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/wallOfTrump.png':               {'colorless':0, 'red':0, 'black':0,'blue':2, 'white':2, 'green':0},\
         'creatures/warriorBug.png':                {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/weepingStatue.jpg':             {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/westleyMasterofEverything.jpg': {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':0, 'green':1},\
         'creatures/youngChild.jpeg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'enchantments/achHansRun.jpg':             {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':2},\
         'enchantments/animateLibrary.jpg':         {'colorless':4, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'enchantments/blitzkrieg.jpg':             {'colorless':0, 'red':2, 'black':2,'blue':0, 'white':0, 'green':0},\
         'enchantments/charmSchool.jpg':            {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'enchantments/curseOfTheFirePenguin.jpg':  {'colorless':4, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'enchantments/executiveOversight.png':     {'colorless':4, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'enchantments/forceMastery.jpg':           {'colorless':3, 'red':2, 'black':0,'blue':1, 'white':1, 'green':1},\
         'enchantments/hiddenProtocol.png':         {'colorless':1, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'enchantments/imposingVisage.jpg':         {'colorless':0, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'enchantments/jediMindTrick.png':          {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'enchantments/lethalResponse.png':         {'colorless':1, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'enchantments/looseLips.jpg':              {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'enchantments/nameDropping.jpg':           {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'enchantments/oprahsKindness.jpg':         {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'enchantments/privateContract.jpg':        {'colorless':1, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'enchantments/redRibbonArmy.png':          {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'enchantments/stricklandsDiscipline.jpg':  {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'enchantments/theCheeseStandsAlone.jpg':   {'colorless':4, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'enchantments/totalBodyProsthesis.png':    {'colorless':8, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/Race.jpg':                       {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'whtblk':1},\
         'instants/aestheticConsultation.jpg':      {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'instants/capitolOffense.png':             {'colorless':2, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'instants/counterSpell.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'instants/curseOfTheRetarded.jpg':         {'colorless':2, 'red':0, 'black':2,'blue':1, 'white':0, 'green':0},\
         'instants/darkRitual.jpg':                 {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'instants/duh.jpg':                        {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'instants/enchantmentUndertheSea.jpg':     {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':1, 'green':1},\
         'instants/forcePush.jpg':                  {'colorless':3, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'instants/gameOver.jpg':                   {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/getALife.jpg':                   {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'instants/gigawattBolt.jpg':               {'colorless':2, 'red':3, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/holyHandgrenade.jpg':            {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'instants/iocanePowder.jpg':               {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'instants/jediReflex.jpg':                 {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'instants/justDesserts.jpg':               {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/kanyeInterrup.jpg':              {'colorless':0, 'red':0, 'black':1,'blue':1, 'white':0, 'green':0},\
         'instants/molotov.png':                    {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/moreOrLess.png':                 {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'instants/notToday.jpg':                   {'colorless':0, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'instants/rickRoll.jpg':                   {'colorless':1, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'instants/shotInTheArm.jpg':               {'colorless':0, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'instants/subtleInnuendo.jpg':             {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'instants/sugarRush.png':                  {'colorless':3, 'red':1, 'black':0,'blue':0, 'white':0, 'green':1},\
         'instants/swiftDeath.jpg':                 {'colorless':1, 'red':0, 'black':1,'blue':1, 'white':0, 'green':0},\
         'instants/unplug.jpg':                     {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'instants/veryCrypticCommand.jpg':         {'colorless':1, 'red':0, 'black':0,'blue':3, 'white':0, 'green':0},\
         'lands/Island.jpg':                        {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0,},\
         'lands/cliffsOfInsanity.jpg':              {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'redwht':1},\
         'lands/deathStar.jpg':                     {'chargeCounter':1, 'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
         'lands/fireSwamp.jpg':                     {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'blkred':1},\
         'lands/forest.jpg':                        {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'lands/mountain.jpg':                      {'colorless':0, 'red':1, 'black':0,'blue':1, 'white':0, 'green':0},\
         'lands/pitOfDespair.jpg':                  {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'redgrn':1},\
         'lands/plains.jpg':                        {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'lands/swamp.jpg':                         {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/Visage of the Dread Pirate.jpg':  {'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/assWhuppin.png':                  {'colorless':1, 'red':0, 'black':1,'blue':0, 'white':1, 'green':0},\
         'sorcery/combTheDesert.jpg':               {'colorless':2, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/damnation.jpg':                   {'colorless':2, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'sorcery/fiveFingerDiscount.jpg':          {'colorless':4, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'sorcery/hotFix.png':                      {'colorless':4, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'sorcery/iKnowKungFu.jpg':                 {'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'sorcery/inspirationalHeadBump.jpg':       {'colorless':1, 'red':1, 'black':0,'blue':1, 'white':0, 'green':0},\
         'sorcery/lastOneStanding.jpg':             {'colorless':1, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/ludicrousSpeed.jpg':              {'colorless':1, 'red':1, 'black':0,'blue':1, 'white':0, 'green':0},\
         'sorcery/manureDump.jpg':                  {'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':1},\
         'sorcery/michaelBay.jpg':                  {'colorless':1, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'sorcery/naturalSpring.jpg':               {'colorless':3, 'red':1, 'black':0,'blue':1, 'white':0, 'green':2},\
         'sorcery/order66.jpg':                     {'colorless':7, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'sorcery/organHarvest.png':                {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/peasants.png':                    {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':1, 'green':1},\
         'sorcery/ponder.jpg':                      {'colorless':0, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'sorcery/powerNap.jpg':                    {'colorless':0, 'red':0, 'black':0,'blue':3, 'white':0, 'green':0},\
         'sorcery/reallyEpicPunch.jpg':             {'colorless':1, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'sorcery/riseOfTheDarkRealms.jpg':         {'colorless':7, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'sorcery/scoutThePerimeter.jpg':           {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'sorcery/timeWalk.jpg':                    {'colorless':1, 'red':0, 'black':0,'blue':1, 'white':0, 'green':0},\
         'mtg.jpg':                                 {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0},\
       }
       
if __name__ == '__main__':  
   manaCost = ManaCost()
   if manaCost.enoughMana ( {'colorless':2, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0}, 'creatures/cowardlyLion.png'):
      print ( 'Cast it' )
   else:
      print ( 'Cannot cast it' )