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
                         
   locations = {'North Atlantic':[104,236,None,'sea'], 'Norwegian Sea':[463,140,None,'sea'], 'Barents Sea':[840,29,None,'sea'], \
                'Norway': [546,284,None,'coast'], 'Sweden': [604,318,None,'land'], 'Gulf of Bothnia': [666,283,None,'sea'], 'Finland': [747,242,None,'coast'], 'St Petersburg [North Coast]': [853,212,None,'coast'], 'St Petersburg [South Coast]': [795,324,None,'coast'], \
                'Clyde': [318,360,None,'coast'], 'Edinburgh': [340,366,None,'coast'], 'North Sea': [433,385,None,'sea'], 'Skagerrak': [537,350,None,'sea'], 'Denmark': [533,410,None,'coast'], 'Baltic Sea': [624,427,None,'sea'], 'Livonia': [744,418,None,'coast'], 'Moscow': [920,395,None,'land'], \
                'Irish Sea': [239,467,None,'sea'], 'Wales': [320,460,None,'coast'], 'Liverpool': [330,431,None,'coast'], 'Yorkshire': [356,434,None,'coast'], 'London': [350,480,None,'coast'], 'Helgeland Bight': [470,444,None,'sea'], 'Kiel': [500,485,None,'coast'], 'Berlin': [565,510,None,'coast'], 'Prussia': [630,484,'Germany','coast'], 'Warsaw': [686,526,None,'land'], \
                'Mid Atlantic': [85,580,None,'sea'], 'English Channel': [310,517,None,'sea'], 'Belgium': [406,523,None,'coast'], 'Holland': [439,505,None,'coast'], 'Ruhr': [473,543,None,'land'], 'Munich': [522,591,None,'land'], 'Bohemia': [574,573,None,'land'], 'Silesia': [606,533,None,'land'], 'Galicia': [727,580,None,'land'], 'Ukraine': [826,550,None,'land'], 'Stevastopol': [1000,570,None,'coast'], \
                'Brest': [288,563,None,'coast'], 'Paris': [370,580,None,'land'], 'Picardy': [374,545,None,'coast'], 'Burgundy': [400,600,None,'land'], 'Tyrolia': [540,648,None,'land'], 'Vienna': [620,625,None,'land'], 'Budapest': [672,642,None,'land'], 'Rumania': [797,702,None,'coast'], 'Black Sea': [936,719,None,'sea'], \
                'Gascony': [322,677,None,'coast'], 'Marseilles': [400,700,None,'coast'], 'Piemonte': [467,684,None,'coast'], 'Venezia': [535,676,None,'coast'], 'Trieste': [601,692,None,'coast'], 'Serbia': [683,729,None,'land'], \
                'Portugal': [118,744,None,'coast'], 'Spain [North Coast]': [240,691,None,'coast'], 'Spain [South Coast]': [254,806,None,'coast'], 'Gulf of Lyon': [404,771,None,'sea'], 'Tuscany': [512,736,None,'coast'], 'Roma': [542,782,None,'coast'], 'Apulia': [586,792,None,'coast'], 'Napoli': [570,809,None,'coast'], 'Adriatic Sea': [593,756,None,'sea'], 'Albania': [675,796,None,'coast'], 'Bulgaria [East Coast]': [810,738,None,'coast'], 'Bulgaria [South Coast]': [776,799,None,'coast'], 'Constantinople': [839,795,None,'coast'], 'Ankara': [936,800,None,'coast'], 'Armenia': [1102,798,None,'coast'], \
                'North Africa': [145,913,None,'coast'], 'West Mediterranean': [316,850,None,'sea'], 'Tunisia': [459,920,None,'coast'], 'Tyrhennian Sea': [504,841,None,'sea'], 'Ionian Sea': [626,930,None,'sea'], 'Greece': [720,854,None,'coast'], 'Aegean Sea': [785,883,None,'sea'], 'Smyrna': [932,863,None,'coast'], 'East Mediterranean': [873,938,None,'sea'], 'Syria': [1082,896,None,'coast'] }
             
   adjacents = { \
                 'North Atlantic':['Norwegian Sea','Irish Sea','Mid Atlantic'], \
                 'Norwegian Sea':['Barents Sea','North Sea'], \
                 'Barents Sea':['Norwegian Sea'], \
                 'Norway':['Norwegian Sea', 'Barents Sea', 'Sweden', 'Finland', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)'], \
                 'Sweden':['Norway', 'Finland', 'Gulf of Bothnia', 'Baltic Sea', 'Skagerrak'], \
                 'Gulf of Bothnia':['Sweden','Finland','Livonia','St Petersburg (South Coast)'], \
                 'Finland':['Gulf of Bothnia','Norway', 'Sweden', 'St Petersburg (South Coast)','St Petersburg (North Coast)'], \
                 'St Petersburg (North Coast)':['Barents Sea','Finland', 'Moscow'], \
                 'St Petersburg (South Coast)':['Gulf of Bothnia','Finland','Moscow','Livonia'], \
                 'Clyde':['Edinburgh','Liverpool','North Atlantic'], \
                 'Edinburgh':['Clyde','Yorkshire','Liverpool','North Sea','Norwegian Sea'], \
                 'North Sea':['Edinburgh','Yorkshire','London','Belgium','Holland','Denmark','Norway','English Channel','Helgeland','Skagerrak','Norwegian Sea'], \
                 'Skagerrak':['Norway','Sweden','Denmark','North Sea','Baltic Sea'], \
                 'Denmark':['Kiel','Helgeland Bight','North Sea','Baltic Sea','Skagerrak'], \
                 'Baltic Sea':['Skagerrak','Gulf of Bothnia','Denmark','Sweden','Livonia','Prussia','Berlin','Kiel'], \
                 'Livonia':['Moscow','Prussia','Warsaw','St Petersburg (North Coast)', 'St Petersburg (South Coast)','Gulf of Bothnia','Baltic Sea'], \
                 'Moscow':['Livonia','Warsaw','Ukraine','St Petersburg (North Coast)', 'St Petersburg (South Coast)','Stevastopol'], \
                 'Irish Sea':['North Atlantic','Mid Atlantic','English Channel','Liverpool','Wales'], \
                 'Wales':['Liverpool','Yorkshire','London','Irish Sea','English Channel'], \
                 'Liverpool':['Clyde','Edinburgh','Yorkshire','London','Wales','North Atlantic','Irish Sea'], \
                 'Yorkshire':['Edinburgh','Liverpool','London','Wales','North Sea'], \
                 'London':['Yorkshire','Wales','North Sea','English Channel'], \
                 'Helgeland Bight':['Denmark','Kiel','Holland','North Sea'], \
                 'Kiel':['Denmark','Berlin','Munich','Ruhr','Holland','Helgeland Bight','Baltic Sea'], \
                 'Berlin':['Prussia','Silesia','Munich','Kiel','Baltic Sea'], \
                 'Prussia':['Livonia','Silesia','Warsaw','Berlin','Baltic Sea'], \
                 'Warsaw':['Prussia','Livonia','Moscow','Ukraine','Silesia','Galicia'], \
                 'Mid Atlantic':['North Atlantic','Irish Sea','English Channel','West Mediterranean','Brest','Gascony','Spain','Portugal','North Africa'], \
                 'English Channel':['Irish Sea','Mid Atlantic','North Sea'], \
                 'Belgium':['English Channel','North Sea','Holland','Ruhr','Burgundy','Picardy'], \
                 'Holland':['Kiel','Ruhr','Belgium','Helgeland Bight','North Sea'], \
                 'Ruhr':['Kiel','Munich','Burgundy','Belgium','Holland'], \
                 'Munich':['Burgundy','Ruhr','Kiel','Berlin','Silesia','Bohemia','Tyrolia'], \
                 'Bohemia':['Silesia','Galicia','Vienna','Tyrolia','Munich'], \
                 'Silesia':['Berlin','Prussia','Warsaw','Galicia','Bohemia','Munich'], \
                 'Galicia':['Warsaw','Ukraine','Rumania','Budapest','Vienna','Bohemia','Silesia'], \
                 'Ukraine':['Moscow','Stevastopol','Rumania','Galicia','Warsaw'], \
                 'Stevastopol':['Moscow','Ukraine','Armenia','Rumania','Black Sea'], \
                 'Brest':['Picardy','Paris','Gascony','English Channel','Mid Atlantic'], \
                 'Paris':['Picardy','Burgundy','Gascony','Brest'], \
                 'Picardy':['Belgium','Burgundy','Paris','Bret','English Channel'], \
                 'Burgundy':['Belgium','Ruhr','Munich','Marseilles','Gascony','Paris','Picardy'], \
                 'Tyrolia':['Munich','Bohemia','Venezia','Piemonte','Trieste'], \
                 'Vienna':['Bohemia','Galicia','Budapest','Trieste','Tyrolia'], \
                 'Budapest':['Galicia','Rumania','Serbia','Trieste','Vienna'], \
                 'Gascony':['Brest','Paris','Burgundy','Spain','Marseilles','Mid Atlantic'], \
                 'Marseilles':['Burgundy','Piemonte','Gascony','Spain','Gulf of Lyon'], \
                 'Piemonte':['Tyrolia','Venezia','Tuscany','Marseilles','Gulf of Lyon'], \
                 'Venezia':['Tyrolia','Trieste','Piemonte','Tuscany','Roma','Apulia'], \
                 'Trieste':['Tyrolia','Vienna','Budapest','Serbia','Albania','Adriatic Sea','Venezia'], \
                 'Serbia':['Budapest','Bulgaria','Rumania','Greece','Albania','Trieste'], \
                 'Rumania':['Ukraine','Stevastopol','Black Sea','Bulgaria (South Coast)','Bulgaria (East Coast)','Serbia','Galicia'], \
                 'Black Sea':['Stevastopol','Armenia','Ankara','Constantinople','Bulgaria (South Coast)','Bulgaria (East Coast)','Rumania'], \
                 'Portugal':['Spain','Mid Atlantic'], \
                 'Spain (North Coast)':['Portugal','Gascony','Marseilles','Mid Atlantic','Gulf of Lyon','West Mediterranean'], \
                 'Spain (South Coast)':['Portugal','Gascony','Marseilles','Mid Atlantic','Gulf of Lyon','West Mediterranean'], \
                 'Gulf of Lyon':['Spain (South Coast)','Marseilles','Piemonte','Tuscany','Tyrhennian Sea','West Mediterranean'], \
                 'Tuscany':['Piemonte','Venezia','Roma','Gulf of Lyon','Tyrhennian Sea'], \
                 'Roma':['Tuscany','Venezia','Apulia','Napoli','Tyrhennian Sea'], \
                 'Apulia':['Venezia','Napoli','Roma','Adriatic Sea', 'Ionian Sea'], \
                 'Napoli':['Roma','Apulia','Tyrhennian Sea','Ionian Sea'], \
                 'Adriatic Sea':['Venezia','Trieste','Albania','Apulia','Ionian Sea'], \
                 'Albania':['Trieste','Serbia','Greece','Adriatic Sea','Ionian Sea'], \
                 'Bulgaria (East Coast)':['Rumania','Constantinople','Serbia','Greece','Black Sea'], \
                 'Bulgaria (South Coast)':['Rumania','Constantinople','Serbia','Greece','Aegean Sea'], \
                 'Constantinople':['Bulgaria (South Coast)','Bulgaria (East Coast)','Ankara','Smyrna','Black Sea','Aegean Sea'], \
                 'Ankara':['Armenia','Smyrna','Constantinople','Black Sea'], \
                 'Armenia':['Stevastopol','Syria','Ankara','Smyrna','Black Sea'], \
                 'North Africa':['Tunisia','Mid Atlantic','West Mediterranean'], \
                 'West Mediterranean':['Spain','North Africa','Tunisia','Mid Atlantic'], \
                 'Tunisia':['North Africa', 'West Mediterranean', 'Tyrhennian Sea', 'Ionian Sea'], \
                 'Tyrhennian Sea':['Tuscany','Roma','Napoli','Tunisia','Gulf of Lyon','West Mediterranean','Ionian Sea'], \
                 'Ionian Sea':['Napoli','Apulia','Greece','Tunisia','Tyrhennian Sea', 'Adriatic Sea', 'Aegean Sea'], \
                 'Greece':['Albania','Serbia','Bulgaria (South Coast)','Bulgaria (East Coast)','Aegean Sea','Ionian Sea','Adriatic Sea'], \
                 'Aegean Sea':['Greece','Bulgaria (South Coast)','Constantinople','Smyrna','East Mediterranean','Ionian Sea'], \
                 'Smyrna':['Constantinople','Ankara','Armenia','Syria','East Mediterranean','Aegean Sea'], \
                 'East Mediterranean':['Smyrna','Syria','Aegean Sea','Ionian Sea'], \
                 'Syria':['Armenia','Smyrna','East Mediterranean'] \
               }
               
   orders = []
   
   def isAdjacent (city1,city2): 
      adjacent = False
      adjacentCities = adjacents[city1]
      for city in adjacentCities:
         if city == city2:
            adjacent = True
            break
      return adjacent
   
   def drawBoard():
      global myTurn
      global lastStatusMessage
      global fromCity
      background = pygame.image.load ('images/diplomacy.gif')
      # background = pygame.transform.scale(background, (DISPLAYWIDTH, DISPLAYHEIGHT)) 
               
      def getButtons (state=0,myTurn=True): 
         if myTurn:
            pygame.display.set_caption('Click on card to perform action')         
         else:
            pygame.display.set_caption('Waiting for opponent to move')
         
         if myTurn:
            if state == 0: 
               buttons = ['viewOrders','turnDone','quit']
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
            pos = locations[key]
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
         for city in adjacents[city]:
            info = locations[city]
            landType = info[3]
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
         for city in adjacents[city]:
            info = locations[city]
            landType = info[3]
            if (landType == 'coast') or (landType == 'land'): 
               cityList.append (city)   
         print ('cityList: ' + str(cityList))                
         return cityList
         
      def convoyToList (city):
         print ( 'convoyTotList (' + city + ')' )
         cityList = []
         for city in adjacents[city]:
            info = locations[city]
            landType = info[3]
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
            print ( 'locations[' + destinationCity + '] : ' + str(locations[destinationCity]))
            destinationType = locations[destinationCity][3]
            print ( 'locations[' + fromCity + '] : ' + str(locations[fromCity]))
            fromType = locations[fromCity][3]
            print ( 'convoy, [fromType,destinationType], [' + fromType + ',' + destinationCity + ']')
            if isAdjacent (fromCity, city):
               drawStatus ( fromCity + ' will be transported to: ' + destinationCity)
               orders.append ([city,'convoy',fromCity,destinationCity])
            elif destinationType != 'coast': 
               drawStatus ('Err, destination must be a coastal location' )                              
            else:
               drawStatus ( 'Navy unit at: ' + city + ' cannot transport a unit located from ' + fromCity + ' (it is too far away).')
               
      def showPiece (imgPos,orders):
         action = ''
         destination = ''
         cities = []
         fromCity = ''
         toCity = ''
         print ( 'showPiece, imgPos: ' + str(imgPos)) 
         (player,city,unit) = findPiece (imgPos)
         if player == iAmPlayer:
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
                        print ( 'suport yo')
                        cityList = moveAdjacentList (city,unit)
                        cities = showList (cityList)                                                       
                     elif action == 'hold':
                        print ( 'hold yo')
                        quit = True
                     else:
                        print ( 'did not handle action: ' + action)
                  
               # Check if a town was clicked on       
               sprite = getSpriteClick (eventType, data, cities ) 
               if sprite != -1:
                  print ( 'sprite: ' + str(sprite) + ' cities: ' + str(cityList)) 
                  destinationCity = cityList [sprite]            
                  drawStatus ( 'You have selected: ' + destinationCity)
                  if action != '': 
                     if action == 'move':
                        orders.append ([city,action,selectedTown,destinationCity])
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
                        orders.append ([city,action,selectedTown])
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
            #if player == 'Austria': 
            #   print ( 'Austrias positions: ' + str(positions)) 
            for town in positions:
               unit = positions[town]
               x = locations[town][0] + imgPos[0]
               y = locations[town][1] + imgPos[1]
               # print ( 'player: ' + player + ' has a ' + unit + ' in ' + town + 'located at [' + str(x) + ',' + str(y) + ']' )
               if unit == 'navy': 
                  drawNavy ((x,y),color)
               else:
                  drawArmy ((x,y),color)
 
               locations [town][2] = player
                  
         for location in locations: 
            # print( 'Got a location of: ' + str(location))
            owner = locations[location][2]
            if owner != None:
               x = locations[location][0] + imgPos[0]
               y = locations[location][1] + imgPos[1]
               # print ( 'Get the color for : ' + owner )
               color = colors[owner]
               if not townOccupied (location):
                  drawFlag ( (x,y), color)             
                  
      def executeOrders(orders):
         global locations
         global players
         for order in orders:
            fromTown = order[0]
            toTown = order[2]
            player = locations[fromTown][2]
            print ( 'execute this order: for ' + player + ':' + str(order)) 
            # update locations
            locations[toTown][2] = player
            print ( 'locations[Galicia]:' + str(locations['Galicia']) )
            print ( 'try again: ' + str(locations['Galicia']))
            
            # update players 
            playerUnits = players[player]
            print ( 'playerUnits before update: ' + str(playerUnits))
            unit = playerUnits[fromTown]
            print ( 'Delete ' + fromTown + ' from playerUnits' )
            del playerUnits[fromTown]
            print ( 'Add ' + toTown + ' to playerUnits' )
            playerUnits[toTown] = unit # add back the unit
            print ( 'playerUnits after update: ' + str(playerUnits))
            players[player] = playerUnits
                            
         orders = []   
         # return orders         
               
      def showBoard (actions,imgPos): 
         DISPLAYSURF.fill((WHITE))
         DISPLAYSURF.blit (background,imgPos)    
         # print ( "show board at: [" + str(imgPos[0]) + "," + str(imgPos[1]) + "]" )          
         (filenames,locations) = actionsToIcons (actions) 
         showPieces (imgPos) 
         (images,buttonSprites) = showImages (filenames, locations )      
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
               drawStatus (city)
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
            elif action == 'turnDone':
               executeOrders(orders)
               showBoard (['viewOrders','turnDone','quit'],imgPos)

            else: 
               print ( 'action: [' + action + ']')
               
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