import inspect
def diplomacyPage():
   global joining 
   global move 
   global iAmHost
   global hostTurn
   global myTurn
   global statusMessage
 
   Object = type('Object', (object,), {} ) # Generic object definition
   showStatus ( 'iAmHost: ' + str(iAmHost) )    

   hostTurn = True # Host gets to move first       
   myTurn = True
   state = 0
   lastStatusMessage = ''
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
                'Clyde': (318,360), 'Edinburgh': (340,366), 'North Sea': (433,385), 'Skagerrak Sea': (537,350), 'Denmark': (533,410), 'Baltic Sea': (624,427), 'Livonia': (744,418), 'Moscow': (920,395), \
                'Irish Sea': (239,467), 'Wales': (320,460), 'Liverpool': (330,431), 'Yorkshire': (356,434), 'London': (350,480), 'Helgeland Bight': (470,444), 'Kiel': (500,485), 'Berlin': (565,510), 'Prussia': (630,484), 'Warsaw': (686,526), \
                'Mid Atlantic': (85,580), 'English Channel': (310,517), 'Belgium': (406,523), 'Holland': (439,505), 'Ruhr': (473,543), 'Munich': (522,591), 'Bohemia': (574,573), 'Silesia': (606,533), 'Galicia': (727,580), 'Ukraine': (826,550), 'Stevastopol': (1000,570), \
                'Brest': (288,563), 'Paris': (370,580), 'Picardy': (374,545), 'Burgundy': (400,600), 'Tyrolia': (540,648), 'Vienna': (600,615), 'Budapest': (672,642), 'Rumania': (797,702), 'Black Sea': (936,719), \
                'Gascony': (322,677), 'Marseilles': (400,700), 'Piemonte': (467,684), 'Venezia': (535,676), 'Trieste': (601,692), 'Serbia': (683,729), 'Rumania': (795,700), \
                'Portugal': (118,744), 'Spain (North Coast)': (240,691), 'Spain (South Coast)': (254,806), 'Gulf of Lyon': (404,771), 'Tuscany': (512,736), 'Roma': (542,782), 'Apulia': (586,792), 'Napoli': (570,809), 'Adriatic Sea': (593,756), 'Albania': (675,796), 'Bulgaria (East Coast)': (810,738), 'Bulgaria (South Coast)': (776,799), 'Constantinople': (839,795), 'Ankara': (936,800), 'Armenia': (1102,798), \
                'North Africa': (145,913), 'West Mediterranean': (316,850), 'Tunisia': (459,920), 'Tyrhennian Sea': (504,841), 'Ionian Sea': (626,930), 'Greece': (720,854), 'Aegean Sea': (785,883), 'Smyrna': (932,863), 'East Mediterranean': (873,938), 'Syria': (1082,896) }
             
   
   def drawBoard():
      global myTurn
      global lastStatusMessage
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
           
      def showStatusMessage():
         global lastStatusMessage
         if statusMessage != "":
            lastStatusMessage = statusMessage
            # print ( 'Show status: ' + statusMessage )
            height = DISPLAYHEIGHT - 23
            pygame.draw.rect(DISPLAYSURF, BLACK, (0,height+2,DISPLAYWIDTH,25))    
            showLine (statusMessage, 1, height+4) # Show status message
            # print ('Done showing Status: ' + statusMessage)
            
      def findLocation(pos):
         city = ''
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
         player = None
         unit = None
         for player_ in players:
            positions = players[player_]
            for town in positions:
               if town == city: 
                  unit = positions[town] 
                  player = player_
                  break
            if unit != None:
               break
         return (player,unit) 
      
      def showArmy (pos,color):
         x = pos[0]
         y = pos[1]         
         pygame.draw.circle(DISPLAYSURF, color, (x, y), 10, 10)  
         pygame.draw.rect  (DISPLAYSURF, color, (x-20,y-10,20,10))         
         pygame.draw.line  (DISPLAYSURF, color, (x+6, y+4), (x+13, y+10))
         
      def showNavy (pos,color):
         x = pos[0] - 20
         y = pos[1]
         points = [(x,y), (x+40,y), (x+30,y+7), (x+10,y+7)]
         pygame.draw.polygon (DISPLAYSURF, color, points, 0)
         points = [(x+40,y-3), (x+20,y-23), (x+20, y-3)]         
         pygame.draw.polygon (DISPLAYSURF, color, points, 0)         
         

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
                  showNavy ((x,y),color)
               else:
                  showArmy ((x,y),color)
         
      def showBoard (actions,imgPos): 
         DISPLAYSURF.fill((WHITE))
         DISPLAYSURF.blit (background,imgPos)    
         # print ( "show board at: [" + str(imgPos[0]) + "," + str(imgPos[1]) + "]" )          
         (filenames,locations) = actionsToIcons (actions) 
         (images,buttonSprites) = showImages (filenames, locations )      
         showStatusMessage()         
         showPieces (imgPos) 
         pygame.display.update() 
         return buttonSprites   
         
      imgPos = (0,0)   
      buttons = getButtons (state,myTurn)
      buttonSprites = showBoard(buttons,imgPos)

      quit = False      
      selected = None
      drag = None
      lastCity = ''
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
            
            if (city != '') and (city != lastCity):
               showStatus (city)
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
               city = findLocation (pos)
               (player,unit) = findPiece (pos)
               print ( 'You have selected [player,unit,city] : [' + player + ',' + unit + ',' + city + ']') 
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
  
   showStatus ( "First select a country" )

   pygame.display.set_caption('Play diplomacy yo')
      
   drawBoard() # Also give options for play
        
DIPLOMACY=inspect.getsource(diplomacyPage)