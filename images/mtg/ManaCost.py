class ManaCost ():
   def colorInMana (self,color,mana):
      exists = False 
      colors = ['colorless', 'white', 'red', 'blue', 'black', 'green']
      if color in colors: 
         if color in mana: 
            exists = True 
      else:
         exists = doubleInMana ( color, mana )         
         
      if exists:
         print ( color + ' found in ' + mana )
      else:
         print ( color + ' NOT found in ' + mana )
         
      return exists 
   
   # For land should be checking if any mana color found in self.cost[filename] 
   def colorsMatch (self,mana,filename): 
      doubles = {'grn':'green','red':'red','blu':'blue','blk':'black','wht':'white'}
      if filename.find ( 'lands') > -1: # If any land color equals any color in deck color 
         match = False 
         for color in self.cost[filename]:
            if self.cost[filename][color] > 0: 
               if self.colorInMana (color,mana):           
                  match = True 
                  break
      else:
         match = True 
         cost = self.cost[filename]
         for color in cost: 
            if color != 'colorless': # Colorless is always a match 
               if cost[color] > 0: 
                  if self.colorInMana ( color, mana ): 
                     continue
                  match = False 
                  print ( 'Could not find color: ' + color + ' in ' + str(mana) ) 
                  break
                  
      return match 
      
   def complexity (self,filename):
      baseColors = ['colorless', 'white', 'black', 'red', 'blue', 'green' ]
      cost = self.cost[filename] 
      totalComplexity = 0
      totalCost = self.totalCastingCost ( filename )
      for c in cost: 
         if cost[c] > 0:       
            if c in baseColors: 
               totalComplexity = totalComplexity + 1
            else:
               totalComplexity = totalComplexity + 0.5
         
      # Creatures bigger than 3 casting cost are more difficult to cast          
      if totalCost > 3: 
         totalComplexity = totalComplexity + (totalCost - 3)
         
      return totalComplexity
      
   def doubleInMana (self,double,mana): 
      exists = False 
      count = 0
      doubles = {'grn':'green','red':'red','blu':'blue','blk':'black','wht':'white'}
      for d in doubles: 
         if double.find (d) > -1: 
            color = doubles[d]
            if color in mana: 
               exists = True 
               break
         
      if exists: 
         print ( double + ' found in ' + str(mana) ) 
      else:
         print ( double + ' not found in ' + str(mana) )       
         
      return exists
         
   def doubleToList (self,color):
      values = {'red':'red','white':'white','blue':'blue','black':'black','green':'green','wht':'white','blk':'black','blu':'blue','grn':'green'}
      manaList = []
      for value in values: 
         if color.find (value) > -1: 
            manaList.append (values[value])
      return manaList
      
   def enoughMana (self,mana,filename):
      manaCopy = mana.copy()
      doubles = ['blkred', 'blured', 'grnblu', 'whtblu', 'whtblk', 'redgrn', 'redwht', 'blublk']
      enough = False
      cost = self.cost[filename]
      cost = self.removeZeroes (cost)
      print ( 'Cost: ' + str(cost) )
      print ( 'Provided mana: ' + str(mana) )
      manaTotal = self.totalMana (mana)
      costTotal = self.totalMana (cost)
      if manaTotal < costTotal:
         print ( 'You do not have enough total mana to handle this cost: ' + str(self.totalMana (cost)) )
      else: # There is sufficient total mana, and enough colorless
         enough = True 
         for color in cost:
            if cost[color] > 0:
               if not color in mana: 
                  if color in doubles: 
                     print ( 'This is a double: ' + color )
                     (success,mana) = self.removeDouble (mana, color, cost[color]) 
                     if not success: 
                        enough = False 
                        break
                  else:
                     print ( 'This color is missing from provided mana: ' + color )               
               elif (mana[color] < cost [color]) and (color != 'colorless'):
                  print ( 'Not enough ' + color )
                  enough = False 
                  break
      if not enough:      
         print ( 'Cannot cast: ' + filename )
         mana = manaCopy.copy()
      return (enough,mana) 
      
   
   def idToInfo (self,id): 
      return list(self.cost)[id]
   
   def isBasicLand (self,filename): 
      isBasic = False 

      for land in ['forest', 'Island', 'mountain','plains','swamp']:
         if filename.find (land) > -1: 
            isBasic = True
            print ( filename + ' is a basic land' )
            break     
      return isBasic
      
   def matchCards (self,mana,howComplex,number,searchString):
      print ( 'match ' + str(number) + ' cards with complexity <= ' + str(howComplex) )    
      creatures = []
      count = 0 
      lastCount = 0 
      while len(creatures) < number: 
         for filename in self.cost: 
            if filename.find ( searchString ) > -1: 
               if self.colorsMatch (mana, filename): 
                  complexity = self.complexity (filename)
                  # 6 = maximum complexity specified
                  if howComplex == self.MAXIMUM_COMPLEXITY:
                     print ( 'Ok...specified complexity is maximum: ' + str(howComplex) + ' for: ' + filename )
                     if count < number: 
                        if (creatures.count (filename) < 4) or self.isBasicLand (filename): 
                           count = count + 1                           
                           creatures.append (list(self.cost.keys()).index(filename)) # load the sheetIndex 
                        else:
                           print ( 'Cannot add ' + filename + ' because there are already 4 in the deck' )
                  elif (complexity <= howComplex) : 
                     print ( 'Ok...specified complexity: ' + str(howComplex) + ' > ' + str(complexity) + ' for: ' + filename )
                     if count < number: 
                        if (creatures.count(filename) < 4) or self.isBasicLand (filename): 
                           count = count + 1
                           creatures.append (list(self.cost.keys()).index(filename))
                        else:
                           print ( 'Cannot add ' + filename + ' because there are already 4 in the deck' )
                  else:
                     print ( 'Complexity of ' + filename + ':' + str(complexity) + ' > specified complexity: ' + str(howComplex) ) 
            if len(creatures) == number:
               break
         if lastCount == count: 
            print ( 'No progress on count: ' + str(count) ) 
            exit()
         lastCount = count
         
      print ( str(len(creatures)) + ' ' + searchString + ' matched: ' + str(creatures)) 
      return creatures       
               
   def getTypes ( self, typeName ): 
      types = {} 
      print ( 'getTypes [' + typeName + ']' )
      for c in self.cost: 
         if c.find (typeName) > -1: 
            types[c] = self.cost[c]         
      print ( 'Found ' + str(len(types)) + ' ' + typeName + ' in manacost' ) 
      return types
      
   def payMana (self, manaLevel, requiredMana): 
      print ( 'ManaCost.payMana, requiredMana: ' + str(requiredMana) )
      for color in requiredMana: # Do none-colorless first
         if color in ['red','blue','white','green','black']: 
            amount = requiredMana[color]            
            self.removeCost (manaLevel, color, requiredMana[color])
            
      self.removeCost(manaLevel, 'colorless', requiredMana['colorless']) 
      print ('ManaCost.payMana after payment: ' + str(manaLevel))
      
   def removeCost (self, pool, color, number): 
      success = False
      if number > 0: 
         success = True       
         print ( 'Take out ' + str(number) + ' of ' + color + ' from: ' + str(pool)) 
         if color in pool: 
            if pool[color] >= number:
               pool[color] = pool[color] - number
               print ( 'pool[' + color + '] is now: ' + str(pool[color]) ) 
            else:
               if color == 'colorless': 
                  print ( 'Handle colorless by pulling from other colors' ) 
                  # Remove all colorless 
                  amount = pool['colorless']
                  pool['colorless'] = 0 
                  number = number - amount
                  for color in ['red','blue','white','black','green']: 
                     amount = pool[color]
                     if amount >= 0: 
                       if number >= amount: 
                          pool[color] = 0
                          number = number - amount
                       else:
                          amount = amount - number
                          pool[color] = amount 
                          number = 0
                       if number == 0: 
                          break # done 
               else:
                  print ( '...ERR do not have enough: ' + color )
                  success = False          
      return (success,pool)      
      
   def removeDouble (self, pool, color, number): 
      startPool = pool.copy()
      success = True      
      colors = {'grn':'green','red':'red','blu':'blue','blk':'black','wht':'white'}
      print ( 'Take out ' + str(number) + ' of ' + color + ' from: ' + str(pool)) 
      for i in range(number):
         found = False 
         for colorIndex in colors: 
            if color.find (colorIndex) > -1: 
               lookupColor = colors[colorIndex]
               if pool[lookupColor] > 0: 
                  pool[lookupColor] = pool[lookupColor] - 1
                  found = True 
                  break
         if not found: 
            print ( 'removeDouble could not find ' + color + ' in ' + str(pool) )          
            success = False         
            break

      if not success: 
         pool = startPool.copy()       
      print ( 'pool after removeDouble: ' + str (pool) )       
      return (success,pool)    
 
   def removeZeroes (self,cost): 
      newCost = {}      
      for color in cost:
         if cost[color] != 0: 
            newCost[color] = cost[color]            
      return newCost
          
   def totalCastingCost (self,filename): 
      total = 0
      mana = self.cost[filename]
      for color in mana: 
         total = total + mana[color]
      return total

   def totalMana (self,mana):
      total = 0
      for color in self.colors: 
         if color in mana: 
            total = total + mana[color]
      return total 
      
   def zeroesExist (self,cost): 
      exist = False 
      for color in cost: 
         if cost[color] == 0: 
            exist = True 
            break
      return exist            
      
   def __init__(self):  
      self.MAXIMUM_COMPLEXITY = 5.95   
      self.colors = ['colorless','red','black','blue','white','green']
      self.columns = 10
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
         'creatures/agentSmith.jpg':                {'power':6, 'toughness':6, 'colorless':4, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/alGore.jpg':                    {'power':1, 'toughness':1, 'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':2},\
         'creatures/americanEagle.jpg':             {'flying':True, 'power':2, 'toughness':2,'colorless':3, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/android17.png':                 {'power':2, 'toughness':2, 'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/android18.png':                 {'power':2, 'toughness':2, 'colorless':2, 'red':1, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/annoyingOrange.jpg':            {'haste':True, 'power':1, 'toughness':1, 'colorless':0, 'red':1, 'black':0,'blue':1, 'white':0, 'green':1},\
         'creatures/arrgh.jpg':                     {'haste':True, 'power':5, 'toughness':5,'colorless':0, 'red':0, 'black':3,'blue':0, 'white':0, 'green':0},\
         'creatures/arthurKingOfTheBritains.jpg':   {'power':4, 'toughness':5,'colorless':3, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/barackHObama.jpg':              {'power':3, 'toughness':7,'power':0, 'toughness':6,'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/barackObama.jpg':               {'power':3, 'toughness':7,'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'grnblu':3, 'whtblu':3},\
         'creatures/barackObamaII.jpg':             {'power':1, 'toughness':1,'colorless':3, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/barfEagleFiveNavigator.jpg':    {'power':3, 'toughness':4,'colorless':1, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/batman.jpg':                    {'power':5, 'toughness':5,'colorless':3, 'red':0, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/batmanII.jpg':                  {'power':5, 'toughness':4,'colorless':3, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'whtblk':3},\
         'creatures/berneyStinson.jpg':             {'power':4, 'toughness':1,'colorless':0, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/bernieSanders.jpg':             {'power':5, 'toughness':8,'colorless':2, 'red':0, 'black':0,'blue':0, 'white':2, 'green':0},\
         'creatures/bernieSandersII.jpg':           {'haste':True, 'power':20, 'toughness':20,'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/bickeringGiant.jpg':            {'power':3, 'toughness':3,'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':1},\
         'creatures/biffTannen.jpg':                {'power':5, 'toughness':5,'colorless':4, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'creatures/blackKnight.jpg':               {'power':5, 'toughness':5,'colorless':1, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/borgCube.jpg':                  {'flying':True, 'power':1, 'toughness':1,'colorless':4, 'red':0, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/borgQueen.jpg':                 {'power':5, 'toughness':5,'colorless':0, 'red':0, 'black':3,'blue':3, 'white':2, 'green':0},\
         'creatures/bruceLee.jpg':                  {'power':99, 'toughness':99,'colorless':0, 'red':1, 'black':1,'blue':1, 'white':1, 'green':1},\
         'creatures/burninator.jpg':                {'power':9, 'toughness':9,'colorless':9, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/cantinaBand.jpg':               {'power':1, 'toughness':1,'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/captainAmerica.jfif':           {'power':2, 'toughness':2,'colorless':2, 'red':1, 'black':0,'blue':1, 'white':1, 'green':0},\
         'creatures/charlesXavier.jpg':             {'power':2, 'toughness':4,'colorless':2, 'red':0, 'black':0,'blue':2, 'white':1, 'green':0},\
         'creatures/cheatyFace.jpg':                {'flying':True, 'power':2, 'toughness':2, 'colorless':0, 'red':0, 'black':0,'blue':2, 'white':0, 'green':0},\
         'creatures/chivalrousChevalier.jpg':       {'flying':True, 'power':3, 'toughness':3,'colorless':4, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'creatures/chuckNorris.jpg':               {'power':99, 'toughness':99,'colorless':9, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/conanTheBarbarian.png':         {'power':3, 'toughness':3,'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/conanTheLibrarian.png':         {'power':4, 'toughness':5,'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
         'creatures/countTyroneRugen.jpg':          {'power':3, 'toughness':4,'colorless':0, 'red':1, 'black':2,'blue':0, 'white':0, 'green':0},\
         'creatures/cowardlyLion.png':              {'power':1, 'toughness':5,'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'creatures/daenerysStormborn.jpg':         {'power':2, 'toughness':2,'colorless':1, 'red':1, 'black':1,'blue':0, 'white':1, 'green':1},\
         'creatures/darkHelmet.jpg':                {'power':4, 'toughness':5,'colorless':3, 'red':0, 'black':2,'blue':1, 'white':0, 'green':0},\
         'creatures/darthSidious.jpg':              {'power':5, 'toughness':5,'colorless':4, 'red':1, 'black':1,'blue':1, 'white':0, 'green':0},\
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
         'creatures/georgeWBush.jpg':               {'colorless':0, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
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
         'lands/fireSwamp.jpg':                     {'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'lands/forest.jpg':                        {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':1},\
         'lands/mountain.jpg':                      {'colorless':0, 'red':1, 'black':0,'blue':0, 'white':0, 'green':0},\
         'lands/pitOfDespair.jpg':                  {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':0, 'green':0, 'redgrn':1},\
         'lands/plains.jpg':                        {'colorless':0, 'red':0, 'black':0,'blue':0, 'white':1, 'green':0},\
         'lands/swamp.jpg':                         {'colorless':0, 'red':0, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/Visage of the Dread Pirate.jpg':  {'colorless':0, 'red':1, 'black':1,'blue':0, 'white':0, 'green':0},\
         'sorcery/assWhuppin.png':                  {'colorless':1, 'red':0, 'black':1,'blue':0, 'white':1, 'green':0},\
         'sorcery/batheInDragonbreath.png':         {'colorless':2, 'red':2, 'black':0,'blue':0, 'white':0, 'green':0},\
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
      self.rows = int(len(self.cost) / 10) + 1
      print ( '[rows,columns.length]: [' + str(self.rows) + ',' + str(self.columns) + ',' + str(len(self.cost)) + ']' ) 
       
if __name__ == '__main__':
   manaCost = ManaCost()
   mana = {'colorless':2, 'red':4, 'black':4,'blue':2, 'white':2, 'green':2}
   (success,newMana) = manaCost.enoughMana (mana, 'creatures/barackObama.jpg')
   if success: 
      print ( 'Casting...' )
      mana = newMana         
   else:
      print ( 'Cannot cast it' )
   print ( 'Final mana: ' + str(mana))
   