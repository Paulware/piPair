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
   
   def drawBoard():
      global myTurn
      background = pygame.image.load ('images/diplomacy.jpg')
      background = pygame.transform.scale(background, (DISPLAYWIDTH, DISPLAYHEIGHT)) 
      
      def findCountry (countryColors): 
         countries = {# Germany \
                      'kiel':[207,187,162], 'ruhr':[217,197,172], 'munich':[197,177,152], \
                      'berlin':[227,207,182], 'silesia':[187,167,142], 'prussia':[237,187,192], \
                      # Russia \
                      'warsaw':[140,240,140], 'livonia':[130,245,130]}

         country = ''
         for key in countries:
            total = 0
            colors = countries[key]
            count = 0
            for color in colors: 
               total = total + abs (color - countryColors[count]) 
               count = count + 1
            # print ( 'Got a total of : ' + str(total) + ' for: ' + key )
            if total < 10: 
               country = key 
               break               
         return country  
         
      def getButtons (state,myTurn): 
         if myTurn:
            pygame.display.set_caption('Click on card to perform action')         
         else:
            pygame.display.set_caption('Waiting for opponent to move')
         
         if myTurn:
            if state == 0: 
               buttons = ['untap', 'quit']
            elif state == 1:
               buttons = ['draw', 'quit']
            elif state == 2: 
               buttons =  ['turndone','quit']
         else:
            buttons = ['quit']
         print ( '[state,myTurn]:[' + str(state) + ',' + str(myTurn) + '] buttons: ' + \
                 str(buttons) ) 
         return buttons
               
      def showStatusMessage():
         if statusMessage != "":
            print ( 'Show status: ' + statusMessage )
            height = DISPLAYHEIGHT - 23
            pygame.draw.line(DISPLAYSURF, RED, (0, height), (DISPLAYWIDTH, height)) #status line
            pygame.draw.rect(DISPLAYSURF, BLACK, (0,height+2,DISPLAYWIDTH,25))    
            showLine (statusMessage, 1, height+4) # Show status message
            print ('Done showing Status: ' + statusMessage)
               
      def showBoard (actions): 
         DISPLAYSURF.fill((WHITE))
         DISPLAYSURF.blit (background,(0,0))         
         (filenames,locations) = actionsToIcons (actions) 
         (images,buttonSprites) = showImages (filenames, locations )      
         showStatusMessage()         
         pygame.display.update() 
         return buttonSprites
         
      buttons = getButtons (state,myTurn)
      buttonSprites = showBoard(buttons)

      quit = False      
      while not quit:            
         myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)       
         (eventType,data,addr) = getKeyOrUdp()         
          
         if eventType == pygame.MOUSEBUTTONDOWN:
            pos = data
            color = DISPLAYSURF.get_at(data)[:3]
            print ( 'Color at mouse down: ' + str(color))
            country = findCountry (color)
            if country != "": 
                print ( "Found country: " + country ) 
                        
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