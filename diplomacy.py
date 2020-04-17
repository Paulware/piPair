import inspect
def diplomacyPage():
   global joining 
   global move 
   global iAmHost
   global hostTurn
   global myTurn
   global statusMessage
   global selectTransport
 
   Object = type('Object', (object,), {} ) # Generic object definition

   hostTurn = True # Host gets to move first       
   myTurn = True
   state = 0
   lastStatusMessage = ''
   selectTransport = ''
   colors = {'Germany': BLACK, 'Austria': RED, 'France': LIGHTBLUE, 'Italy': GREEN, \
             'Russia':DARKGREEN, 'Turkey': YELLOW, 'England': DARKBLUE}   
   
   players = {'Germany': {'Kiel':'navy', 'Berlin':'army', 'Munich':'army'}, \
              'Austria': {'Vienna':'army', 'Budapest':'army', 'Trieste':'navy'}, \
              'France':  {'Marseilles':'army', 'Paris':'army', 'Brest':'navy'}, \
              'England': {'Liverpool':'army', 'London':'navy', 'Edinburgh':'navy'}, \
              'Italy':   {'Napoli':'navy', 'Roma':'army', 'Venezia':'navy'}, \
              'Russia':  {'St Petersburg (South Coast)': 'navy', 'Warsaw':'army', 'Moscow':'army', 'Stevastopol': 'navy'} , \
              'Turkey':  {'Constantinople': 'army', 'Ankara':'navy', 'Smyrna':'army'} \
             }
             
   locations = {'North Atlantic':(104,236), 'Norwegian Sea':(463,140), 'Barents Sea':(840,29), \
                'Norway': (546,284), 'Sweden': (604,318), 'Gulf of Bothnia': (666,283), 'Finland': (747,242), 'St Petersburg (North Coast)': (853,212), 'St Petersburg (South Coast)': (795,324), \
                'Clyde': (318,360), 'Edinburgh': (340,366), 'North Sea': (433,385), 'Skagerrak': (537,350), 'Denmark': (533,410), 'Baltic Sea': (624,427), 'Livonia': (744,418), 'Moscow': (920,395), \
                'Irish Sea': (239,467), 'Wales': (320,460), 'Liverpool': (330,431), 'Yorkshire': (356,434), 'London': (350,480), 'Helgeland Bight': (470,444), 'Kiel': (500,485), 'Berlin': (565,510), 'Prussia': (630,484), 'Warsaw': (686,526), \
                'Mid Atlantic': (85,580), 'English Channel': (310,517), 'Belgium': (406,523), 'Holland': (439,505), 'Ruhr': (473,543), 'Munich': (522,591), 'Bohemia': (574,573), 'Silesia': (606,533), 'Galicia': (727,580), 'Ukraine': (826,550), 'Stevastopol': (1000,570), \
                'Brest': (288,563), 'Paris': (370,580), 'Picardy': (374,545), 'Burgundy': (400,600), 'Tyrolia': (540,648), 'Vienna': (620,625), 'Budapest': (672,642), 'Rumania': (797,702), 'Black Sea': (936,719), \
                'Gascony': (322,677), 'Marseilles': (400,700), 'Piemonte': (467,684), 'Venezia': (535,676), 'Trieste': (601,692), 'Serbia': (683,729), \
                'Portugal': (118,744), 'Spain (North Coast)': (240,691), 'Spain (South Coast)': (254,806), 'Gulf of Lyon': (404,771), 'Tuscany': (512,736), 'Roma': (542,782), 'Apulia': (586,792), 'Napoli': (570,809), 'Adriatic Sea': (593,756), 'Albania': (675,796), 'Bulgaria (East Coast)': (810,738), 'Bulgaria (South Coast)': (776,799), 'Constantinople': (839,795), 'Ankara': (936,800), 'Armenia': (1102,798), \
                'North Africa': (145,913), 'West Mediterranean': (316,850), 'Tunisia': (459,920), 'Tyrhennian Sea': (504,841), 'Ionian Sea': (626,930), 'Greece': (720,854), 'Aegean Sea': (785,883), 'Smyrna': (932,863), 'East Mediterranean': (873,938), 'Syria': (1082,896) }
             
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
                 'Trieste':['Tyrolia','Vienna','Budapest','Serbia','Albania','Adriatic Sea'], \
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
      global selectTransport
      background = pygame.image.load ('images/diplomacy.gif')
      # background = pygame.transform.scale(background, (DISPLAYWIDTH, DISPLAYHEIGHT)) 
               
      def getButtons (state,myTurn): 
         if myTurn:
            pygame.display.set_caption('Click on card to perform action')         
         else:
            pygame.display.set_caption('Waiting for opponent to move')
         
         if myTurn:
            if state == 0: 
               buttons = ['quit']
            elif state == 1:
               buttons = ['quit']
            elif state == 2: 
               buttons =  ['turndone','quit']
         else:
            buttons = ['quit']
         print ( '[state,myTurn]:[' + str(state) + ',' + str(myTurn) + '] buttons: ' + \
                 str(buttons) ) 
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
               
      def showPiece (imgPos): 
         global selectTransport
         print ( 'showPiece, imgPos: ' + str(imgPos)) 
         (player,city,unit) = findPiece (imgPos)
         if player != '':
            pygame.display.set_caption('Select action for the ' + player + ' ' + unit + ' stationed at ' + city)
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
                        selectTransport = city
                        quit = True
                     else:
                        if action == 'transport':
                           if selectTransport == '':
                              drawStatus ( 'First select an army unit for transport')
                           elif selectedTown == '':
                              drawStatus ( 'Select a destination town')
                           else:
                              if isAdjacent (selectTransport, city):
                                 drawStatus ( selectTransport + ' will be transported to: ' + selectedTown)
                                 orders.append (['transport',selectTranport,selectedTown])
                              else:
                                 drawStatus ( 'Navy unit at: ' + city + ' cannot transport a unit located from ' + selectTransport + ' (it is too far away).')
                        elif selectedTown == '':
                           drawStatus ('Select a town first (for ' + action + ')')
                        else:
                           print ( action + ' ' + selectedTown )
                           orders.append ([action,selectedTown])
                           quit = True
                  
               # Check if a town was clicked on       
               sprite = getSpriteClick (eventType, data, cities ) 
               if sprite != -1:
                  selectedTown = cityList [sprite]            
                  drawStatus ( 'You have selected: ' + selectedTown)
                  
      def showPieces (imgPos): 
         for player in players:
            color = colors[player]
            positions = players[player]
            for town in positions:
               unit = positions[town]
               x = locations[town][0] + imgPos[0]
               y = locations[town][1] + imgPos[1]
               # print ( 'player: ' + player + ' has a ' + unit + ' in ' + town + 'located at [' + str(x) + ',' + str(y) + ']' )
               if unit == 'navy': 
                  drawNavy ((x,y),color)
               else:
                  drawArmy ((x,y),color)                  
                  
               
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
      buttons = getButtons (state,myTurn)
      buttonSprites = showBoard(buttons,imgPos)

      quit = False      
      selected = None
      drag = None
      lastCity = ''
      lastPosition = (0,0)
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
               showPiece (lastPosition)
            drag = None

         showBoard (buttons,imgPos) 
                
         # Handle button press
         sprite = getSpriteClick (eventType, data, buttonSprites ) 
         if sprite > -1:
            action = buttons[sprite]
            
            if action == 'quit':
               quit = True
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