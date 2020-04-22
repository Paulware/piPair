import inspect
def diplomacyPage(numPlayers=2):
   global joining 
   global move 
   global iAmHost
   global hostTurn
   global myTurn
   global statusMessage
   global fromCity
   global locations
   global players
   global remindTimeout
   
   remindTimeout = 0
    
   Object = type('Object', (object,), {} ) # Generic object definition

   hostTurn = True # Host gets to move first       
   myTurn = True
   state = 0
   lastStatusMessage = ''
   fromCity = ''
   colors = {'Germany': BLACK, 'Austria': RED, 'France': LIGHTBLUE, 'Italy': GREEN, \
             'Russia':DARKGREEN, 'Turkey': YELLOW, 'England': DARKBLUE}   
   if numPlayers == 2: 
      players = {'Austria': {'Vienna':'army', 'Budapest':'army', 'Trieste':'navy'}, \
                 'France':  {'Marseilles':'army', 'Paris':'army', 'Brest':'navy'}, \
                 }   
   else:
      players = {'Germany': {'Kiel':'navy', 'Berlin':'army', 'Munich':'army'}, \
                 'Austria': {'Vienna':'army', 'Budapest':'army', 'Trieste':'navy'}, \
                 'France':  {'Marseilles':'army', 'Paris':'army', 'Brest':'navy'}, \
                 'England': {'Liverpool':'army', 'London':'navy', 'Edinburgh':'navy'}, \
                 'Italy':   {'Napoli':'navy', 'Roma':'army', 'Venezia':'navy'}, \
                 'Russia':  {'St Petersburg (South Coast)': 'navy', 'Warsaw':'army', 'Moscow':'army', 'Stevastopol': 'navy'} , \
                 'Turkey':  {'Constantinople': 'army', 'Ankara':'navy', 'Smyrna':'army'} \
                }

   locations = { \
      'North Atlantic':{'adjacents':['Norwegian Sea', 'Irish Sea', 'Mid Atlantic'],'x':104,'y':236, 'owner':None,'landType':'sea','occupied':False}, \
      'Norwegian Sea':{'adjacents':['Barents Sea', 'North Sea'],'x':463,'y':140, 'owner':None,'landType':'sea','occupied':False}, \
      'Barents Sea':{'adjacents':['Norwegian Sea'],'x':840,'y':29, 'owner':None,'landType':'sea','occupied':False}, \
      'Norway':{'adjacents':['Norwegian Sea', 'Barents Sea', 'Sweden', 'Finland', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)'],'x':546,'y':284, 'owner':None,'landType':'coast','occupied':False}, \
      'Sweden':{'adjacents':['Norway', 'Finland', 'Gulf of Bothnia', 'Baltic Sea', 'Skagerrak'],'x':604,'y':318, 'owner':None,'landType':'land','occupied':False}, \
      'Gulf of Bothnia':{'adjacents':['Sweden', 'Finland', 'Livonia', 'St Petersburg (South Coast)'],'x':666,'y':283, 'owner':None,'landType':'sea','occupied':False}, \
      'Finland':{'adjacents':['Gulf of Bothnia', 'Norway', 'Sweden', 'St Petersburg (South Coast)', 'St Petersburg (North Coast)'],'x':747,'y':242, 'owner':None,'landType':'coast','occupied':False}, \
      'St Petersburg (North Coast)':{'adjacents':['Barents Sea', 'Finland', 'Moscow'],'x':853,'y':212, 'owner':None,'landType':'coast','occupied':False}, \
      'St Petersburg (South Coast)':{'adjacents':['Gulf of Bothnia', 'Finland', 'Moscow', 'Livonia'],'x':795,'y':324, 'owner':None,'landType':'coast','occupied':False}, \
      'Clyde':{'adjacents':['Edinburgh', 'Liverpool', 'North Atlantic'],'x':318,'y':360, 'owner':None,'landType':'coast','occupied':False}, \
      'Edinburgh':{'adjacents':['Clyde', 'Yorkshire', 'Liverpool', 'North Sea', 'Norwegian Sea'],'x':340,'y':366, 'owner':None,'landType':'coast','occupied':False}, \
      'North Sea':{'adjacents':['Edinburgh', 'Yorkshire', 'London', 'Belgium', 'Holland', 'Denmark', 'Norway', 'English Channel', 'Helgeland', 'Skagerrak', 'Norwegian Sea'],'x':433,'y':385, 'owner':None,'landType':'sea','occupied':False}, \
      'Skagerrak':{'adjacents':['Norway', 'Sweden', 'Denmark', 'North Sea', 'Baltic Sea'],'x':537,'y':350, 'owner':None,'landType':'sea','occupied':False}, \
      'Denmark':{'adjacents':['Kiel', 'Helgeland Bight', 'North Sea', 'Baltic Sea', 'Skagerrak'],'x':533,'y':410, 'owner':None,'landType':'coast','occupied':False}, \
      'Baltic Sea':{'adjacents':['Skagerrak', 'Gulf of Bothnia', 'Denmark', 'Sweden', 'Livonia', 'Prussia', 'Berlin', 'Kiel'],'x':624,'y':427, 'owner':None,'landType':'sea','occupied':False}, \
      'Livonia':{'adjacents':['Moscow', 'Prussia', 'Warsaw', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)', 'Gulf of Bothnia', 'Baltic Sea'],'x':744,'y':418, 'owner':None,'landType':'coast','occupied':False}, \
      'Moscow':{'adjacents':['Livonia', 'Warsaw', 'Ukraine', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)', 'Stevastopol'],'x':920,'y':395, 'owner':None,'landType':'land','occupied':False}, \
      'Irish Sea':{'adjacents':['North Atlantic', 'Mid Atlantic', 'English Channel', 'Liverpool', 'Wales'],'x':239,'y':467, 'owner':None,'landType':'sea','occupied':False}, \
      'Wales':{'adjacents':['Liverpool', 'Yorkshire', 'London', 'Irish Sea', 'English Channel'],'x':320,'y':460, 'owner':None,'landType':'coast','occupied':False}, \
      'Liverpool':{'adjacents':['Clyde', 'Edinburgh', 'Yorkshire', 'London', 'Wales', 'North Atlantic', 'Irish Sea'],'x':330,'y':431, 'owner':None,'landType':'coast','occupied':False}, \
      'Yorkshire':{'adjacents':['Edinburgh', 'Liverpool', 'London', 'Wales', 'North Sea'],'x':356,'y':434, 'owner':None,'landType':'coast','occupied':False}, \
      'London':{'adjacents':['Yorkshire', 'Wales', 'North Sea', 'English Channel'],'x':350,'y':480, 'owner':None,'landType':'coast','occupied':False}, \
      'Helgeland Bight':{'adjacents':['Denmark', 'Kiel', 'Holland', 'North Sea'],'x':470,'y':444, 'owner':None,'landType':'sea','occupied':False}, \
      'Kiel':{'adjacents':['Denmark', 'Berlin', 'Munich', 'Ruhr', 'Holland', 'Helgeland Bight', 'Baltic Sea'],'x':500,'y':485, 'owner':None,'landType':'coast','occupied':False}, \
      'Berlin':{'adjacents':['Prussia', 'Silesia', 'Munich', 'Kiel', 'Baltic Sea'],'x':565,'y':510, 'owner':None,'landType':'coast','occupied':False}, \
      'Prussia':{'adjacents':['Livonia', 'Silesia', 'Warsaw', 'Berlin', 'Baltic Sea'],'x':630,'y':484, 'owner':'Germany','landType':'coast','occupied':False}, \
      'Warsaw':{'adjacents':['Prussia', 'Livonia', 'Moscow', 'Ukraine', 'Silesia', 'Galicia'],'x':686,'y':526, 'owner':None,'landType':'land','occupied':False}, \
      'Mid Atlantic':{'adjacents':['North Atlantic', 'Irish Sea', 'English Channel', 'West Mediterranean', 'Brest', 'Gascony', 'Spain', 'Portugal', 'North Africa'],'x':85,'y':580, 'owner':None,'landType':'sea','occupied':False}, \
      'English Channel':{'adjacents':['Irish Sea', 'Mid Atlantic', 'North Sea'],'x':310,'y':517, 'owner':None,'landType':'sea','occupied':False}, \
      'Belgium':{'adjacents':['English Channel', 'North Sea', 'Holland', 'Ruhr', 'Burgundy', 'Picardy'],'x':406,'y':523, 'owner':None,'landType':'coast','occupied':False}, \
      'Holland':{'adjacents':['Kiel', 'Ruhr', 'Belgium', 'Helgeland Bight', 'North Sea'],'x':439,'y':505, 'owner':None,'landType':'coast','occupied':False}, \
      'Ruhr':{'adjacents':['Kiel', 'Munich', 'Burgundy', 'Belgium', 'Holland'],'x':473,'y':543, 'owner':None,'landType':'land','occupied':False}, \
      'Munich':{'adjacents':['Burgundy', 'Ruhr', 'Kiel', 'Berlin', 'Silesia', 'Bohemia', 'Tyrolia'],'x':522,'y':591, 'owner':None,'landType':'land','occupied':False}, \
      'Bohemia':{'adjacents':['Silesia', 'Galicia', 'Vienna', 'Tyrolia', 'Munich'],'x':574,'y':573, 'owner':None,'landType':'land','occupied':False}, \
      'Silesia':{'adjacents':['Berlin', 'Prussia', 'Warsaw', 'Galicia', 'Bohemia', 'Munich'],'x':606,'y':533, 'owner':None,'landType':'land','occupied':False}, \
      'Galicia':{'adjacents':['Warsaw', 'Ukraine', 'Rumania', 'Budapest', 'Vienna', 'Bohemia', 'Silesia'],'x':727,'y':580, 'owner':None,'landType':'land','occupied':False}, \
      'Ukraine':{'adjacents':['Moscow', 'Stevastopol', 'Rumania', 'Galicia', 'Warsaw'],'x':826,'y':550, 'owner':None,'landType':'land','occupied':False}, \
      'Stevastopol':{'adjacents':['Moscow', 'Ukraine', 'Armenia', 'Rumania', 'Black Sea'],'x':1000,'y':570, 'owner':None,'landType':'coast','occupied':False}, \
      'Brest':{'adjacents':['Picardy', 'Paris', 'Gascony', 'English Channel', 'Mid Atlantic'],'x':288,'y':563, 'owner':'France','landType':'coast','occupied':True}, \
      'Paris':{'adjacents':['Picardy', 'Burgundy', 'Gascony', 'Brest'],'x':370,'y':580, 'owner':'France','landType':'land','occupied':True}, \
      'Picardy':{'adjacents':['Belgium', 'Burgundy', 'Paris', 'Bret', 'English Channel'],'x':374,'y':545, 'owner':None,'landType':'coast','occupied':False}, \
      'Burgundy':{'adjacents':['Belgium', 'Ruhr', 'Munich', 'Marseilles', 'Gascony', 'Paris', 'Picardy'],'x':400,'y':600, 'owner':None,'landType':'land','occupied':False}, \
      'Tyrolia':{'adjacents':['Munich', 'Bohemia', 'Venezia', 'Piemonte', 'Trieste'],'x':540,'y':648, 'owner':None,'landType':'land','occupied':False}, \
      'Vienna':{'adjacents':['Bohemia', 'Galicia', 'Budapest', 'Trieste', 'Tyrolia'],'x':620,'y':625, 'owner':'Austria','landType':'land','occupied':True}, \
      'Budapest':{'adjacents':['Galicia', 'Rumania', 'Serbia', 'Trieste', 'Vienna'],'x':672,'y':642, 'owner':'Austria','landType':'land','occupied':True}, \
      'Rumania':{'adjacents':['Ukraine', 'Stevastopol', 'Black Sea', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Serbia', 'Galicia'],'x':797,'y':702, 'owner':None,'landType':'coast','occupied':False}, \
      'Black Sea':{'adjacents':['Stevastopol', 'Armenia', 'Ankara', 'Constantinople', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Rumania'],'x':936,'y':719, 'owner':None,'landType':'sea','occupied':False}, \
      'Gascony':{'adjacents':['Brest', 'Paris', 'Burgundy', 'Spain', 'Marseilles', 'Mid Atlantic'],'x':322,'y':677, 'owner':None,'landType':'coast','occupied':False}, \
      'Marseilles':{'adjacents':['Burgundy', 'Piemonte', 'Gascony', 'Spain', 'Gulf of Lyon'],'x':400,'y':700, 'owner':'France','landType':'coast','occupied':True}, \
      'Piemonte':{'adjacents':['Tyrolia', 'Venezia', 'Tuscany', 'Marseilles', 'Gulf of Lyon'],'x':467,'y':684, 'owner':None,'landType':'coast','occupied':False}, \
      'Venezia':{'adjacents':['Tyrolia', 'Trieste', 'Piemonte', 'Tuscany', 'Roma', 'Apulia'],'x':535,'y':676, 'owner':None,'landType':'coast','occupied':False}, \
      'Trieste':{'adjacents':['Tyrolia', 'Vienna', 'Budapest', 'Serbia', 'Albania', 'Adriatic Sea', 'Venezia'],'x':601,'y':692, 'owner':'Austria','landType':'coast','occupied':True}, \
      'Serbia':{'adjacents':['Budapest', 'Bulgaria', 'Rumania', 'Greece', 'Albania', 'Trieste'],'x':683,'y':729, 'owner':None,'landType':'land','occupied':False}, \
      'Portugal':{'adjacents':['Spain', 'Mid Atlantic'],'x':118,'y':744, 'owner':None,'landType':'coast','occupied':False}, \
      'Spain (North Coast)':{'adjacents':['Portugal', 'Gascony', 'Marseilles', 'Mid Atlantic', 'Gulf of Lyon', 'West Mediterranean'],'x':240,'y':691, 'owner':None,'landType':'coast','occupied':False}, \
      'Spain (South Coast)':{'adjacents':['Portugal', 'Gascony', 'Marseilles', 'Mid Atlantic', 'Gulf of Lyon', 'West Mediterranean'],'x':254,'y':806, 'owner':None,'landType':'coast','occupied':False}, \
      'Gulf of Lyon':{'adjacents':['Spain (South Coast)', 'Marseilles', 'Piemonte', 'Tuscany', 'Tyrhennian Sea', 'West Mediterranean'],'x':404,'y':771, 'owner':None,'landType':'sea','occupied':False}, \
      'Tuscany':{'adjacents':['Piemonte', 'Venezia', 'Roma', 'Gulf of Lyon', 'Tyrhennian Sea'],'x':512,'y':736, 'owner':None,'landType':'coast','occupied':False}, \
      'Roma':{'adjacents':['Tuscany', 'Venezia', 'Apulia', 'Napoli', 'Tyrhennian Sea'],'x':542,'y':782, 'owner':None,'landType':'coast','occupied':False}, \
      'Apulia':{'adjacents':['Venezia', 'Napoli', 'Roma', 'Adriatic Sea', 'Ionian Sea'],'x':586,'y':792, 'owner':None,'landType':'coast','occupied':False}, \
      'Napoli':{'adjacents':['Roma', 'Apulia', 'Tyrhennian Sea', 'Ionian Sea'],'x':570,'y':809, 'owner':None,'landType':'coast','occupied':False}, \
      'Adriatic Sea':{'adjacents':['Venezia', 'Trieste', 'Albania', 'Apulia', 'Ionian Sea'],'x':593,'y':756, 'owner':None,'landType':'sea','occupied':False}, \
      'Albania':{'adjacents':['Trieste', 'Serbia', 'Greece', 'Adriatic Sea', 'Ionian Sea'],'x':675,'y':796, 'owner':None,'landType':'coast','occupied':False}, \
      'Bulgaria (East Coast)':{'adjacents':['Rumania', 'Constantinople', 'Serbia', 'Greece', 'Black Sea'],'x':810,'y':738, 'owner':None,'landType':'coast','occupied':False}, \
      'Bulgaria (South Coast)':{'adjacents':['Rumania', 'Constantinople', 'Serbia', 'Greece', 'Aegean Sea'],'x':776,'y':799, 'owner':None,'landType':'coast','occupied':False}, \
      'Constantinople':{'adjacents':['Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Ankara', 'Smyrna', 'Black Sea', 'Aegean Sea'],'x':839,'y':795, 'owner':None,'landType':'coast','occupied':False}, \
      'Ankara':{'adjacents':['Armenia', 'Smyrna', 'Constantinople', 'Black Sea'],'x':936,'y':800, 'owner':None,'landType':'coast','occupied':False}, \
      'Armenia':{'adjacents':['Stevastopol', 'Syria', 'Ankara', 'Smyrna', 'Black Sea'],'x':1102,'y':798, 'owner':None,'landType':'coast','occupied':False}, \
      'North Africa':{'adjacents':['Tunisia', 'Mid Atlantic', 'West Mediterranean'],'x':145,'y':913, 'owner':None,'landType':'coast','occupied':False}, \
      'West Mediterranean':{'adjacents':['Spain', 'North Africa', 'Tunisia', 'Mid Atlantic'],'x':316,'y':850, 'owner':None,'landType':'sea','occupied':False}, \
      'Tunisia':{'adjacents':['North Africa', 'West Mediterranean', 'Tyrhennian Sea', 'Ionian Sea'],'x':459,'y':920, 'owner':None,'landType':'coast','occupied':False}, \
      'Tyrhennian Sea':{'adjacents':['Tuscany', 'Roma', 'Napoli', 'Tunisia', 'Gulf of Lyon', 'West Mediterranean', 'Ionian Sea'],'x':504,'y':841, 'owner':None,'landType':'sea','occupied':False}, \
      'Ionian Sea':{'adjacents':['Napoli', 'Apulia', 'Greece', 'Tunisia', 'Tyrhennian Sea', 'Adriatic Sea', 'Aegean Sea'],'x':626,'y':930, 'owner':None,'landType':'sea','occupied':False}, \
      'Greece':{'adjacents':['Albania', 'Serbia', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Aegean Sea', 'Ionian Sea', 'Adriatic Sea'],'x':720,'y':854, 'owner':None,'landType':'coast','occupied':False}, \
      'Aegean Sea':{'adjacents':['Greece', 'Bulgaria (South Coast)', 'Constantinople', 'Smyrna', 'East Mediterranean', 'Ionian Sea'],'x':785,'y':883, 'owner':None,'landType':'sea','occupied':False}, \
      'Smyrna':{'adjacents':['Constantinople', 'Ankara', 'Armenia', 'Syria', 'East Mediterranean', 'Aegean Sea'],'x':932,'y':863, 'owner':None,'landType':'coast','occupied':False}, \
      'East Mediterranean':{'adjacents':['Smyrna', 'Syria', 'Aegean Sea', 'Ionian Sea'],'x':873,'y':938, 'owner':None,'landType':'sea','occupied':False}, \
      'Syria':{'adjacents':['Armenia', 'Smyrna', 'East Mediterranean'],'x':1082,'y':896, 'owner':None,'landType':'coast','occupied':False}, \
   }
                   
   for player in players:
      cities = players[player]
      for city in cities:
         print ( player + ' occupies city: ' + city )
         locations[city][4] = True # occupied
         locations[city][2] = player # Set owner         
                
   if iAmHost: 
      for player in players:
         iAmPlayer = player 
         break
   else:
      iAmPlayer = ''
      for player in players:
         if iAmPlayer != '':
            break  # Take the seoond player
         iAmPlayer = player
                                           
   orders = []
   
   def ordersAppend (order,orders):  
     print ( 'Add order: ' + str(order) + ' to orders: ' + str(orders))    
     message = ','.join (order)
     udpBroadcast ( message ) # send order to other player 
     orders.append (order)
     
   def isAdjacent (city1,city2): 
      adjacent = False
      adjacentCities = locations[city1]['adjacents'] # adjacents[city1]
      for city in adjacentCities:
         if city == city2:
            adjacent = True
            break
      return adjacent
   
   def drawBoard():
      global myTurn
      global lastStatusMessage
      global fromCity
      global remindTimeout
      
      background = pygame.image.load ('images/diplomacy.gif')
      # background = pygame.transform.scale(background, (DISPLAYWIDTH, DISPLAYHEIGHT)) 
               
      def getButtons (state=0,myTurn=True): 
         if myTurn:
            pygame.display.set_caption('Click on card to perform action')         
         else:
            pygame.display.set_caption('Waiting for opponent to move')
         
         if myTurn:
            if state == 0: 
               buttons = ['viewOrders','quit']
         else:
            buttons = ['quit']
         # print ( '[state,myTurn]:[' + str(state) + ',' + str(myTurn) + '] buttons: ' + str(buttons) ) 
         return buttons
                       
      def findLocation(pos):
         city = ''
         x = pos[0]
         y = pos[1]
         minDistance = 1000
         for key in locations:
            pos = (locations[key]['x'], locations[key]['y'])
            difference = abs ( x - pos[0]) + abs (y - pos[1])
            if difference < minDistance:                
               if ((key != 'Portugal') or (x < 156)) and \
                  ((key != 'West Mediterranean') or (y < 876)) and \
                  ((key != 'Spain (South Coast)') or (y < 848 )) and \
                  ((key != 'North Africa') or (y > 886)) and \
                  ((key != 'Portugal') or (y < 807)) and \
                  ((key != 'Tuscany') or (y > 708)):                  
                  city = key
                  minDistance = difference
         return city
         
      def findPiece (pos): 
         city = findLocation (pos)
         player = ''
         unit = ''
         for player_ in players:
            positions = players[player_]
            for town in positions:
               if town == city: 
                  unit = positions[town] 
                  player = player_
                  break
            if unit != '':
               break
         print ( 'findPiece got (player,city,unit): (' + str(player) + ',' + str(city) + ',' + str(unit) + ')' )
         return (player,city,unit) 
         
      def moveAdjacentList (city,unit):
         print ( 'moveAdjacentList (' + city + ',' + unit + ')' )
         cityList = []
         adjacents = locations [city]['adjacents']
         for city in adjacents:
            landType = locations[city]['landType']
            if unit == 'navy':
               if (landType == 'sea') or (landType == 'coast'): 
                  cityList.append (city)               
            else: 
               if (landType == 'coast') or (landType == 'land'):
                  cityList.append (city)
         print ('cityList: ' + str(cityList))                   
         return cityList
         
      def convoyFromList (city):
         print ( 'convoyFromList (' + city + ')' )
         cityList = []
         adjacents = locations [city]['adjacents']         
         for city in adjacents:
            landType = locations[city]['landType']
            occupied = locations[city]['occupied']
            if (landType == 'coast') or (landType == 'land'):
               print ( city + ' occupied: ?' + str(occupied)) 
               if occupied:                
                  cityList.append (city)   
            else:
               print ( city + ' ignored because it is of type: ' + landType)
         print ('cityList: ' + str(cityList))                
         return cityList
         
      def convoyToList (city):
         print ( 'convoyTotList (' + city + ')' )
         cityList = []
         adjacents = locations [city]['adjacents']          
         for city in adjacents:
            landType = locations[city]['landType']
            if (landType == 'coast'): 
               cityList.append (city)   
         print ('cityList: ' + str(cityList))                
         return cityList
               
      def drawArmy (pos,color):
         x = pos[0]
         y = pos[1]         
         pygame.draw.circle(DISPLAYSURF, color, (x, y), 10, 10)  
         pygame.draw.rect  (DISPLAYSURF, color, (x-20,y-10,20,10))         
         pygame.draw.line  (DISPLAYSURF, color, (x+6, y+4), (x+13, y+10))
         
      def drawNavy (pos,color):
         x = pos[0] - 20
         y = pos[1]
         points = [(x,y), (x+40,y), (x+30,y+7), (x+10,y+7)]
         pygame.draw.polygon (DISPLAYSURF, color, points, 0)
         points = [(x+40,y-3), (x+20,y-23), (x+20, y-3)]         
         pygame.draw.polygon (DISPLAYSURF, color, points, 0)         
         
      def drawFlag (pos,color):
         # print ( 'Draw a flag at ' + str(pos)) 
         x = pos[0] - 20
         y = pos[1]
         points = [(x+25,y-3), (x+35,y-15), (x+35, y+7), (x+33,y+7), (x+33,y-3)]         
         pygame.draw.polygon (DISPLAYSURF, color, points, 0)         
         
      def validateConvoyOrder(orders,convoyCity,fromCity,destinationCity):
         print ( 'Do a convoy yo [convoyCity,fromCity,destinationCity]: [' + convoyCity + ',' + fromCity + ',' + destinationCity + ']' )
         if convoyCity == '':
            drawStatus ( 'convoy city not specified yo')
         elif fromCity == '':
            drawStatus ( 'First select an army unit for transport')
         elif destinationCity == '':
            drawStatus ( 'Select a destination town')
         elif destinationCity == fromCity: 
            drawStatus ( 'Cannot transport unit from ' + fromCity + ' to ' + destinationCity + ' (pick different destination)')
         else:
            # print ( 'locations[' + destinationCity + '] : ' + str(locations[destinationCity]))
            destinationType = locations[destinationCity]['landType']
            # print ( 'locations[' + fromCity + '] : ' + str(locations[fromCity]))
            fromType = locations[fromCity]['landType']
            print ( 'convoy, [fromType,destinationType], [' + fromType + ',' + destinationCity + ']')
            if isAdjacent (fromCity, city):
               drawStatus ( fromCity + ' will be transported to: ' + destinationCity)
               ordersAppend ([city,'convoy',fromCity,destinationCity],orders)
            elif destinationType != 'coast': 
               drawStatus ('Err, destination must be a coastal location' )                              
            else:
               drawStatus ( 'Navy unit at: ' + city + ' cannot transport a unit located from ' + fromCity + ' (it is too far away).')

                     
      def waitingOn ( player): 
         # players = {'Austria': {'Vienna':'army', 'Budapest':'army', 'Trieste':'navy'}, \
         #            'France':  {'Marseilles':'army', 'Paris':'army', 'Brest':'navy'}, \   
         units = players[player]
         waiting = False          
         for city in units:
            found = False
            for order in orders:
               if order[0] == city:
                  found = True 
                  break
            if not found:
               drawStatus ( city + ' has not been assigned an order yet')
               waiting = True
               break               
         return waiting
       
      def showPiece (imgPos,orders):
         action = ''
         destination = ''
         cities = []
         fromCity = ''
         toCity = ''
         print ( 'showPiece, imgPos: ' + str(imgPos)) 
         (player,city,unit) = findPiece (imgPos)
         if player != iAmPlayer:
            print ( 'You do not own this piece [player,iAmPlayer] :[' + player + ',' + \
                    iAmPlayer + ', no action required')
         else:
            msg = 'Select action for the ' + player + ' ' + unit + ' stationed at ' + city
            pygame.display.set_caption(msg)
            print (msg)
            DISPLAYSURF.fill((WHITE))
            if unit == 'navy':
               drawNavy ((100,100), colors[player])   
               actions = ['convoy','move','support','hold','ok']
            else:        
               drawArmy ((100,100), colors[player])  
               actions = ['move','support','hold','ok']
                      
            (filenames,buttons) = actionsToIcons (actions) 
            (images,buttonSprites) = showImages (filenames, buttons)      
            pygame.display.update() 
            quit = False
            selectedTown = ''
            while not quit:
               (eventType,data,addr) = getKeyOrUdp()                  
               
               # Check for click on action 
               sprite = getSpriteClick (eventType, data, buttonSprites ) 
               if sprite != -1:  
                  print ( 'actions: ' + str(actions) + ' sprite: ' + str(sprite))
                  action = actions[sprite]        
                  if action == 'ok': 
                     quit = True
                  else:
                     if action == 'convoy':
                        pygame.display.set_caption('Select From Town')                     
                        cityList = convoyFromList (city)
                        cities = showList (cityList)                            
                     elif action == 'move': 
                        cityList = moveAdjacentList (city,unit)
                        cities = showList (cityList)                            
                     elif action == 'support':
                        cityList = moveAdjacentList (city,unit)
                        cities = showList (cityList)                                                       
                     elif action == 'hold':                      
                        ordersAppend([city,'hold',''],orders)                     
                        quit = True
                     else:
                        print ( 'did not handle action: ' + action)
                  
               # Check if a town was clicked on       
               sprite = getSpriteClick (eventType, data, cities ) 
               if sprite != -1:
                  print ( 'sprite: ' + str(sprite) + ' cities: ' + str(cityList)) 
                  if action != '': 
                     if (action == 'hold'): 
                        ordersAppend ([city,'hold'],orders)
                        quit = True
                     else: 
                        destinationCity = cityList [sprite]            
                        drawStatus ( 'You have selected: ' + destinationCity)

                        if (action == 'move') or (action == 'support'):
                           ordersAppend ([city,action,destinationCity],orders)
                           quit = True
                        elif action == 'convoy':
                           if fromCity == '':                       
                              fromCity = cityList[sprite]
                              pygame.display.set_caption('Select destination city')
                              cityList = convoyToList (city)
                              DISPLAYSURF.fill((WHITE))                            
                              drawNavy ((100,100), colors[player])   
                              actions = ['ok']                      
                              (filenames,buttons) = actionsToIcons (actions) 
                              (images,buttonSprites) = showImages (filenames, buttons)      
                              pygame.display.update() 
                              cities = showList (cityList)                            
                           else:
                              toCity = cityList[sprite]                           
                              convoyCity = city
                              validateConvoyOrder (orders,convoyCity,fromCity,toCity)
                              quit = True
                        else:
                           print ( 'Can add order? [city,action,selectedTown]:[' + city + ',' + action + ',' + selectedTown + ']' )
                           ordersAppend ([city,action,selectedTown],orders)
                           quit = True
                     
      def showOrders(orders):
         DISPLAYSURF.fill((BLACK))     
         drawStatus ( "View the " + str(len(orders)) + " orders yo")
         count = 0
         myOrders = []
         for order in orders:
            msg = 'order [' + str(count) + ']: ' + str(order)
            print (msg)
            myOrders.append (msg)
            count = count + 1
         
         labels = showList(myOrders)      
         (images,buttonSprites) = showImages (['images/ok.jpg'], [(400,400)] )
         pygame.display.update()
         
         quit = False      
         while not quit: 
            (eventType,data,addr) = getKeyOrUdp()         
            sprite = getSpriteClick (eventType, data, buttonSprites ) 
            if sprite > -1:
               quit = True            
                                      
      def townOccupied(town):
         occupied = False
         for player in players:
            positions = players[player]
            for city in positions:
               if city == town:
                  #print ( town + ' occupied, by ' + player + ' based on players position')
                  occupied = True 
                  break                  
            if occupied: 
               break
               
         return occupied 
         
      def showPieces (imgPos):
         #print ( 'showPieces: locations[Galicia]:' + str(locations['Galicia']) )     
         #print ( 'showPieces: players:' + str (players))          
         for player in players:
            color = colors[player]
            positions = players[player]
            for town in positions:
               unit = positions[town]
               
               x = locations[town]['x'] + imgPos[0]
               y = locations[town]['y'] + imgPos[1]
               if unit == 'navy': 
                  drawNavy ((x,y),color)
               else:
                  drawArmy ((x,y),color)
               # locations [town]['owner'] = player
                  
         for location in locations: 
            # print( 'Got a location of: ' + str(location))
            owner = locations[location]['owner']
            if owner != None:
               x = locations[location]['x'] + imgPos[0]
               y = locations[location]['y'] + imgPos[1]
               # print ( 'Get the color for : ' + owner )
               color = colors[owner]
               if not townOccupied (location):
                  drawFlag ( (x,y), color)             
      def allOrdersIn():
         return False      
 
      def executeOrders(orders):
         global locations
         global players
         print ( 'Execute all orders yo' )
         for order in orders:
            fromTown = order[0]
            toTown = order[2]
            player = locations[fromTown]['owner']
            #print ( 'execute this order: for ' + player + ':' + str(order)) 
            # update locations
            locations[toTown]['owner'] = player
            #print ( 'locations[Galicia]:' + str(locations['Galicia']) )
            #print ( 'try again: ' + str(locations['Galicia']))
            
            # update players 
            playerUnits = players[player]
            #print ( 'playerUnits before update: ' + str(playerUnits))
            unit = playerUnits[fromTown]
            #print ( 'Delete ' + fromTown + ' from playerUnits' )
            del playerUnits[fromTown]
            #print ( 'Add ' + toTown + ' to playerUnits' )
            playerUnits[toTown] = unit # add back the unit
            #print ( 'playerUnits after update: ' + str(playerUnits))
            players[player] = playerUnits
                            
         orders = []   
         # return orders         
               
      def showBoard (actions,imgPos): 
         DISPLAYSURF.fill((WHITE))
         DISPLAYSURF.blit (background,imgPos)    
         # print ( "show board at: [" + str(imgPos[0]) + "," + str(imgPos[1]) + "]" )          
         (filenames,rectangles) = actionsToIcons (actions) 
         showPieces (imgPos) 
         (images,buttonSprites) = showImages (filenames,rectangles)      
         showLastStatus()
         pygame.display.update() 
         return buttonSprites   
         
      imgPos = (0,0)   
      buttons = getButtons ()
      buttonSprites = showBoard(buttons,imgPos)

      quit = False      
      selected = None
      drag = None
      lastCity = ''
      lastPosition = (0,0)
      orders = []
      while not quit:            
         myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)       
         (eventType,data,addr) = getKeyOrUdp()         
         
         if time.time() > remindTimeout:
            remindTimeout = time.time() + 10 # Remind every 10 seconds 
            if waitingOn(iAmPlayer):
               drawStatus ("Waiting on you to finish orders")
            elif allOrdersIn (): 
               executeOrders(orders)
            else:
               drawStatus ("Waiting on others to finish orders" )
          
         if eventType == pygame.MOUSEBUTTONDOWN:
            pos = data
            color = DISPLAYSURF.get_at(data)[:3]
            x = pos[0] - imgPos[0]
            y = pos[1] - imgPos[1]
            selected = pos
            drag = pos
            rel = pygame.mouse.get_rel()
         elif eventType == pygame.MOUSEMOTION:
            pos = data
            x = pos[0] - imgPos[0]
            y = pos[1] - imgPos[1]
            #print ( '[' + str(x) + ',' + str(y) + ']' )
            city = findLocation ((x,y))
            
            lastPosition = (x,y)
            
            if (city != '') and (city != lastCity):
               #drawStatus (city)
               lastCity = city
               
            if drag != None:
               rel = pygame.mouse.get_rel()
               x = imgPos[0]
               y = imgPos[1]
               x += rel[0]
               y += rel[1]
               imgPos = (x,y)
         elif eventType == pygame.MOUSEBUTTONUP:
            if data == selected: 
               showPiece (lastPosition,orders)
            drag = None

         # Handle button press
         sprite = getSpriteClick (eventType, data, buttonSprites ) 
         if sprite > -1:
            action = buttons[sprite]          
            if action == 'quit':
               quit = True
            elif action == 'viewOrders':
               showOrders(orders)
            #elif action == 'turnDone':
            #   executeOrders(orders)
            #   showBoard (['viewOrders','turnDone','quit'],imgPos)

            else: 
               print ( 'action: [' + action + ']')
               
         if (eventType != pygame.MOUSEMOTION) or (drag != None):      
            showBoard (buttons,imgPos) 
                
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'Diplomacy\']')
      myTurn = True 
   else:
      udpBroadcast ( 'exec:joining=\'Diplomacy\'')
      joining = 'Diplomacy' # Opponent should be waiting
      myTurn = False
  

   pygame.display.set_caption('Play diplomacy yo')
      
   drawBoard() # Also give options for play
        
DIPLOMACY=inspect.getsource(diplomacyPage)