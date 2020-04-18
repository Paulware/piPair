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
             
   locations = {'North Atlantic':(104,236,None), 'Norwegian Sea':(463,140,None), 'Barents Sea':(840,29,None), \
                'Norway': (546,284,None), 'Sweden': (604,318,None), 'Gulf of Bothnia': (666,283,None), 'Finland': (747,242,None), 'St Petersburg (North Coast)': (853,212,None), 'St Petersburg (South Coast)': (795,324,None), \
                'Clyde': (318,360,None), 'Edinburgh': (340,366,None), 'North Sea': (433,385,None), 'Skagerrak': (537,350,None), 'Denmark': (533,410,None), 'Baltic Sea': (624,427,None), 'Livonia': (744,418,None), 'Moscow': (920,395,None), \
                'Irish Sea': (239,467,None), 'Wales': (320,460,None), 'Liverpool': (330,431,None), 'Yorkshire': (356,434,None), 'London': (350,480,None), 'Helgeland Bight': (470,444,None), 'Kiel': (500,485,None), 'Berlin': (565,510,None), 'Prussia': (630,484,'Germany'), 'Warsaw': (686,526,None), \
                'Mid Atlantic': (85,580,None), 'English Channel': (310,517,None), 'Belgium': (406,523,None), 'Holland': (439,505,None), 'Ruhr': (473,543,None), 'Munich': (522,591,None), 'Bohemia': (574,573,None), 'Silesia': (606,533,None), 'Galicia': (727,580,None), 'Ukraine': (826,550,None), 'Stevastopol': (1000,570,None), \
                'Brest': (288,563,None), 'Paris': (370,580,None), 'Picardy': (374,545,None), 'Burgundy': (400,600,None), 'Tyrolia': (540,648,None), 'Vienna': (620,625,None), 'Budapest': (672,642,None), 'Rumania': (797,702,None), 'Black Sea': (936,719,None), \
                'Gascony': (322,677,None), 'Marseilles': (400,700,None), 'Piemonte': (467,684,None), 'Venezia': (535,676,None), 'Trieste': (601,692,None), 'Serbia': (683,729,None), \
                'Portugal': (118,744,None), 'Spain (North Coast)': (240,691,None), 'Spain (South Coast)': (254,806,None), 'Gulf of Lyon': (404,771,None), 'Tuscany': (512,736,None), 'Roma': (542,782,None), 'Apulia': (586,792,None), 'Napoli': (570,809,None), 'Adriatic Sea': (593,756,None), 'Albania': (675,796,None), 'Bulgaria (East Coast)': (810,738,None), 'Bulgaria (South Coast)': (776,799,None), 'Constantinople': (839,795,None), 'Ankara': (936,800,None), 'Armenia': (1102,798,None), \
                'North Africa': (145,913,None), 'West Mediterranean': (316,850,None), 'Tunisia': (459,920,None), 'Tyrhennian Sea': (504,841,None), 'Ionian Sea': (626,930,None), 'Greece': (720,854,None), 'Aegean Sea': (785,883,None), 'Smyrna': (932,863,None), 'East Mediterranean': (873,938,None), 'Syria': (1082,896,None) }
             
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
               
      def showPiece (imgPos,orders):
         global fromCity
         action = ''
         destination = ''
         print ( 'showPiece, imgPos: ' + str(imgPos)) 
         (player,city,unit) = findPiece (imgPos)
         if player != '':
            msg = 'Select action for the ' + player + ' ' + unit + ' stationed at ' + city
            pygame.display.set_caption(msg)
            print (msg)
            DISPLAYSURF.fill((WHITE))         
            if unit == 'navy': 
               drawNavy ((100,100), colors[player])   
               actions = ['transport','attack','support','ok']
            else:        
               drawArmy ((100,100), colors[player])  
               actions = ['selectTransport', 'attack','support','ok']
                      
            (filenames,locations) = actionsToIcons (actions) 
            (images,buttonSprites) = showImages (filenames, locations )      
            cityList = adjacents[city]         
            cities = showList (cityList)          
            pygame.display.update() 
            quit = False
            selectedTown = ''
            while not quit:
               (eventType,data,addr) = getKeyOrUdp()                  
               sprite = getSpriteClick (eventType, data, buttonSprites ) 
               if sprite != -1:  
                  print ( 'actions: ' + str(actions) + ' sprite: ' + str(sprite))             
                  action = actions[sprite]        
                  if action == 'ok': 
                     quit = True
                  else:
                     if action == 'selectTransport':
                        fromCity = city
                        quit = True
                     else:
                        if action == 'transport':
                           if fromCity == '':
                              drawStatus ( 'First select an army unit for transport')
                           elif selectedTown == '':
                              drawStatus ( 'Select a destination town')
                           else:
                              if isAdjacent (fromCity, city):
                                 drawStatus ( fromCity + ' will be transported to: ' + selectedTown)
                                 orders.append ([city,'transport',fromCity,selectedTown])
                              else:
                                 drawStatus ( 'Navy unit at: ' + city + ' cannot transport a unit located from ' + fromCity + ' (it is too far away).')
                        elif selectedTown == '':
                           drawStatus ('Select a town first (for ' + action + ')')
                        else:
                           print ( action + ' ' + selectedTown )
                           orders.append ([city,action,selectedTown,destination])
                           quit = True
                  
               # Check if a town was clicked on       
               sprite = getSpriteClick (eventType, data, cities ) 
               if sprite != -1:
                  selectedTown = cityList [sprite]            
                  drawStatus ( 'You have selected: ' + selectedTown)
                  if action != '': 
                     if action == 'transport':
                        if isAdjacent (fromCity, city):
                           drawStatus ( fromCity + ' will be transported to: ' + selectedTown)
                           orders.append ([city,'transport',fromCity,selectedTown])
                        else:
                           drawStatus ( 'Navy unit at: ' + city + ' cannot transport a unit located from ' + fromCity + ' (it is too far away).')
                     else:
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
 
               x = locations[town][0]
               y = locations[town][1]
               locations [town] = (x,y,player) 
                  
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
            x = locations[toTown][0]
            y = locations[toTown][1]
            locations[toTown] = (x,y,player)
            print ( 'locations[Galicia]:' + str(locations['Galicia']) )
            
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
         return orders         
               
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
               orders = executeOrders(orders)
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