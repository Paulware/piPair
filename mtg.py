import inspect
#TODO: Each while loop has its own def 
def mtgPage():
   global joining 
   global move 
   global iAmHost
   global hostTurn
   global enemyShot
   global shot
   global explosion
   global rightClick
   global allCards
   global statusMessage
  
   CARDWIDTH = 100
   BOARDY = 50
   BOARDX = 100 
   OFFSET = 0   
   shot = None  
   enemyShot = None   
   explosion = None
   Object = type('Object', (object,), {} ) # Generic object definition
   showStatus ( 'iAmHost: ' + str(iAmHost) )    
   move = None
   lost = None
                   
   # filename is relative path to image
   # iOwnIt:True/False
   # location:'library', 'inplay','inhand','exiled','discarded'
   # tapped:True/False
   # index:0..(len(allCards)-1)
   def getAffects (data):
      affects = []
      try:
         affects = data['affects']         
      except Exception as ex:
         pass
      return affects
   def addCard (filePath,owned,location,tapped):
      power = 0
      toughness = 0
      affects = []
      if filePath.find ( '/creatures/' ) > -1:
         data = c.cost[filePath]
         affects = getAffects (data)
         if affects != []: 
            print ('\n\n' + filePath + ' has affects: ' + str(affects)) 
         power = data['power']
         toughness = data['toughness']
      ind = len(allCards)
      card = {'index':ind, 'iOwnIt':owned, 'filename':filePath, \
              'location':location, 'tapped':tapped, \
              'summoned':False, 'power':power, 'toughness':toughness, 'affects':affects }
      allCards.append (card)
      return ind

   # Modify the list of indexes related to cards in the hand   
   def drawCard(hand):
      # Make a list of all items in the draw deck (library)
      libraryList = [] 
      for card in allCards:
         location = card['location']
         if location == 'library':
            libraryList.append ( card['index'] )
      
      index = int( random.random() * len(libraryList))
      allCards[index]['location'] = 'inhand'
      hand.append (index)
      return hand
      
   c = castingCost.castingCost()
   STARTX = 50
   
   def executeAffect(index, affect):
      affects = allCards[index]['affects']
      filename = allCards[index]['filename']
      
      if affect in affects.keys():
         code = affects[affect]
         print ( 'Found a code affect for : ' + affect + '=' + code) 
         print ( 'Now apply the affect: exec(' + code + ')' )
      else: 
         print ( 'This affect: ' + affect + ' is not part of the card: ' + filename )         
   
   def indexesToFilenames (indexList): 
      # print ( 'indexesToFilenames list: ' + str(indexList) + ' len(allCards): ' + str(len(allCards))  ) 
      filenames = []
      element = None
      try:
         for index in indexList: 
            if str(index).isnumeric():   
               if int(index) <= len(allCards):  
                  element = allCards [index]               
                  filename = allCards[index]['filename']
                  filenames.append (filename)
               else:
                  print ( 'index:' + str(index) + ' is too large for len(allCards): ' + str(len(allCards)) )
            else:
               print ( 'ERR index invalid (should be a number): ' + str(index) ) 
      except Exception as ex:
         print ( 'Could not convert indexes to filenames with element: ' + str(element) + ' because: ' + str(ex)  )      

      return filenames
   
   def showCards (indexList,startLocation,width):
      filenames = indexesToFilenames(indexList)
      # print ( 'showCards (indexList: ' + str(indexList))
      #        ' startLocation: ' + str(startLocation) + ',width: ' + str(width) + ')' )
      x = startLocation [0]
      y = startLocation [1]
      height = int (width * 1.4)
      
      # Get all the images 
      images = [] 
      count = 0
      try:
         for filename in filenames:
            index = indexList[count]
            tapped = allCards[index]['tapped']
            image = pygame.image.load (filename).convert_alpha()
            image = pygame.transform.scale(image, (width, height))
            if tapped: 
               #print ( 'width before tap: ' + str(width) )            
               print ( "showCards, this card is tapped yo: " + filename ) 
               image = rotate (image, 90) 
                              
            images.append (image)     
            count = count + 1
      except Exception as ex:
         print ( 'Could not load: ' + str(filename) + ' because: ' + str(ex))

      # Place all images on the surface and get list of rectangles (sprites)
      sprites = []
      try:
         i = 0
         for image in images: 
             sprites.append (DISPLAYSURF.blit (image,(x,y)))
             width,height = image.get_size()
             
             x = x + width
             if x >= DISPLAYWIDTH:
                x = startLocation[0]
                y = y + height
             i = i + 1
         pygame.display.update()        
      except Exception as ex:
         print ( 'Show cards could not place sprite (card) on surface because: ' + str(ex))
      return (images,sprites)
                                           
   def angleXY(x,y,speed,degrees):
      degrees = degrees - 90.0# adjust for picture direction
      degrees = int(degrees) % 360
      angle_in_radians = float(degrees) / 180.0 * math.pi
      new_x = x + int(float(speed)*math.cos(angle_in_radians))
      new_y = y - int(float(speed)*math.sin(angle_in_radians))
      return new_x, new_y         
         
   def selectMainCard(creatureIndexes):   
      def drawDeckCards(): 
         global cards
         global sprites
         # Show screen
         pygame.display.set_caption('Click a card, then press select to build a deck around the selected card')  
         DISPLAYSURF.fill((WHITE)) 
         print ( 'selectMainCard.drawDeckCards' )
         (images,cards) = showCards (creatureIndexes, (0,90), 35 )
                  
      joinTimeout = 0   
      drawDeckCards()
      quit = False
      while True:  
         (eventType,data,addr) = getKeyOrUdp()
               
         if joining != 'MTG':
            if time.time() > joinTimeout: 
               joinTimeout = time.time() + 1
               udpBroadcast ( 'exec:games=[\'MTG\']') 
                                           
         card = getSpriteClick (eventType, data, cards ) 
         if card != -1:
            filename = allCards[card]['filename']
            actions = ['ok','select']            
            action = getSingleCardAction ( filename, 'View card', actions)  
            if action == 'select':                
               break
            else:                  
               drawDeckCards() # Draw deck again after viewing card              
      print ( 'card selected as basis of deck: ' + str(card))         
      return card 
      
   def showCreatedDeck(indexList,creature):
      print ( 'showCreatedDeck, my indexList ( should be all numbers ): ' + str(indexList) ) 
      deck = indexesToFilenames (indexList)
      def showDeck():
         global cards
         global sprites
         # Show the deck
         DISPLAYSURF.fill((WHITE))       
         (images,sprites) = showImages (['images/ok.jpg'], [(400,50)] ) 
         print ( 'showCreatedDeck.showDeck' )
         (images,cards) = showCards (indexList, (0,90), 35 )
         
      pygame.display.set_caption('Here is your deck based on:' + creature)
      showDeck()
      quit = False  
      joinTimeout = 0
      while not quit:  
         (eventType,data,addr) = getKeyOrUdp()
      
         if joining != 'MTG':
            if time.time() > joinTimeout: 
               joinTimeout = time.time() + 1
               udpBroadcast ( 'exec:games=[\'MTG\']')

         if eventType == pygame.MOUSEBUTTONUP:
            showDeck()
            
         card = getSpriteClick (eventType, data, cards ) 
         if card != -1: # show the card
            actions = ['ok']        
            filename = deck[card]            
            action = getSingleCardAction ( filename, 'View card', actions)          

         sprite = getSpriteClick (eventType, data, sprites ) 
         if sprite != -1: # Quit is the only other option           
            quit = True
                  
   # Get action from a single card 
   def getSingleCardAction (card,caption,actions):
      print ( 'getSingleCardAction (' + card + ',' + caption + ',' + str(actions) + ')' )   
      pygame.display.set_caption(caption)   
      DISPLAYSURF.fill((WHITE))
      
      image  = pygame.image.load (card).convert_alpha()
      width  = image.get_width()
      if width > 400: 
         width = 400
      height = int (width * 1.4)
      image = pygame.transform.scale(image, (width, height))                            
      DISPLAYSURF.blit(image, (10, 50))   
      pygame.display.update()        
      
      (filenames,locations) = actionsToIcons (actions)
      
      (images,sprites) = showImages (filenames, locations )
      list = [card]
      action = ''
      quit = False
      while not quit and (action == ''):
         (eventType,data,addr) = getKeyOrUdp()                  
         sprite = getSpriteClick (eventType, data, sprites ) 
         if sprite != -1: 
            action = actions[sprite]
      
      print ( '[' + action + ']=getSingleCardAction(' + card + ',' + caption + '), quit=' + str(quit) )       
      return action 
      
   # Draw the entire playing surface with my cards and opponents cards visible   
   def drawBoard(handIndexes, inplayIndexes): 
      global move
      global iAmHost
      global hostTurn
      global statusMessage     
      
      myHealth = 20
      manaPool = [] 
      opponentIndexes = []
      hand = []
      state = 0 
      hasPlayedLand = False
      power = 20
      
      def getButtons (state,myTurn,hand): 
         if myTurn:
            pygame.display.set_caption('Click on card to perform action')         
         else:
            pygame.display.set_caption('Waiting for opponent to move')
         
         if myTurn:
            if state == 0: 
               buttons = ['untap', 'quit']
               showStatus ( 'untap' )
            elif state == 1:
               buttons = ['draw', 'quit']
               showStatus ( 'draw a card' )
            elif state == 2:
               if len(hand) > 7:
                  showStatus ( 'play a card or discard' )
                  pygame.display.set_caption ( 'You need to discard a card' )
                  buttons = ['quit']
               else:
                  showStatus ( 'Tap a land card to play a create, instant or sorcery')
                  buttons =  ['turndone','quit']
         else:
            buttons = ['quit']
         print ( '[state,myTurn]:[' + str(state) + ',' + str(myTurn) + '] buttons: ' + \
                 str(buttons) ) 
         return buttons
               
      def showBoard (actions): 
         DISPLAYSURF.fill((WHITE))
         (filenames,locations) = actionsToIcons (actions) 
         (images,sprites) = showImages (filenames, locations )
         #print ( 'drawBoard.showBoard, draw cards in hand' )         
         (images,handSprites) = showCards (handIndexes, (0,70), 100 )
         hand = indexesToFilenames (handIndexes)
         
         print ( 'showBoard, draw cards in play' )
         (images,inplaySprites) = showCards (inplayIndexes, (0, 210), 100)  
         inplay = indexesToFilenames (inplayIndexes)
         
         #print ( 'showBoard opponentCards: ' + str(opponentCards))
         (images,opponentSprites) = showCards (opponentIndexes, (0, 360), 100)  
         opponentCards = indexesToFilenames (opponentIndexes)
         
         pygame.draw.line(DISPLAYSURF, RED, (0, 350), (DISPLAYWIDTH, 350))

         if statusMessage != "":
            print ( 'Show status: ' + statusMessage )
            height = DISPLAYHEIGHT - 23
            pygame.draw.line(DISPLAYSURF, RED, (0, height), (DISPLAYWIDTH, height)) #status line
            pygame.draw.rect(DISPLAYSURF, BLACK, (0,height+2,DISPLAYWIDTH,25))    
            showLine (statusMessage, 1, height+4) # Show status message
            print ('Done showing Status: ' + statusMessage)
         
         
         pygame.display.update() 
         
         return (sprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites)
         
      targettedOpponentCard = None
      quit = False  
      myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)
      buttons = getButtons (state,myTurn,hand)
      (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
      
      while not quit and (myHealth > 0):            
         myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)       
         (eventType,data,addr) = getKeyOrUdp()

         # Check for opponent move 
         if move != None: 
            print ( '  moveType: ' + move['moveType'])
            if move['moveType'] == 'turndone':
               hostTurn = not hostTurn
               hasPlayedLand = False
               myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)
               if not myTurn:
                  print ('ERR: Should be my turn, hostTurn is not correct: ' + str(hostTurn) + ' iAmHost: ' + str(iAmHost))
               state = 0
               buttons = getButtons (state,myTurn,hand)
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            elif move['moveType'] == 'cast':
               filename = move['filename']
               print ( '  filename: ' + move['filename'])
               index = addCard (filename, False, 'opponent', False)
               opponentIndexes.append (index)
               # print ( 'opponentIndexes: ' + str(opponentIndexes))
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            elif move['moveType'] == 'tap':
               index = opponentIndexes[int(move['index'])]
               allCards[index]['tapped'] = True
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            elif move['moveType'] == 'block':
               blocker = move['blocker']
               attacker = move['attacker']
               blockerIndex = opponentIndexes[blocker]
               attackerIndex = inplayIndexes[attacker]
               blockerFilename = allCards[blockerIndex]['filename']
               attackerFilename = allCards[attackerIndex]['filename']
               print ( blockerFilename + ' is blocking: ' + attackerFilename ) 
            elif move['moveType'] == 'attack':
               opponentIndex = int(move['index'])
               print ( 'Tapping opponent card [' + str(opponentIndex) + ']')                  
               ind = opponentIndexes[opponentIndex]
               allCards[ind]['tapped'] = True
               attackFilename = allCards[ind]['filename']
               attackPower = allCards[ind]['power']
               attackToughness = allCards[ind]['toughness']
               showStatus ( ' You are getting attacked by: ' + attackFilename )
               blocked = False
               count = 0
               for index in inplayIndexes:
                  tapped = allCards[index]['tapped']
                  filename = allCards[index]['filename']                     
                  if not tapped and (filename.find ( '/creatures/' ) > -1):                         
                     power = allCards[index]['power']
                     toughness = allCards[index]['toughness']
                     caption = 'You are getting attacked by a ' + str(attackPower) + '/' + str(attackToughness) + ' ' + filename
                     pygame.display.set_caption(caption)              
                     action = getSingleCardAction ( filename, 'You are being attacked by a ' + \
                                                    str(attackPower) + '/' + str(attackToughness), ['ok','block'])  
                     if action != '':
                        print ( 'Perform action: [' + action + '] on card: ' + filename)                                
                        if action == 'block': 
                           blocked = True 
                           udpBroadcast ( 'exec:move={\'moveType\':\'block\',' + \
                                          '\'blocker\':\'' + str(count) + '\',' + \
                                          '\'attacker\':\'' + str(opponentIndex) + '\'}' )                               
                           print ( 'Creature is blocked ' )
                           break
                        else:
                           pass
                           #print ( 'Pop card: ' + str(card) + ' len(handIndexes: ' + str(len(handIndexes)) )
                           #handIndexes.pop(card)
                           #TODO: Add to discard pile 
                           #hand.remove (selectedCard)                       
                  count = count + 1
                  
               if blocked:
                  # TODO check for trample
                  print ( 'Assign damage ' + str(attackPower) + ' to creature: ' + filename )
                  if attackPower >= toughness: 
                     print ( filename + ' has died in battle' )
                     inplay.pop (count)
                  if power >= attackToughness:
                     print ( 'You killed ' + attackFilename )
                     opponentIndexes.pop (opponentIndex)
                     
               else:                  
                  myHealth = myHealth - allCards[ind]['power']                  
                  showStatus ( ' New health: ' + str(myHealth))
                  if myHealth <= 0: 
                     showStatus ( 'You have lost yo' )
                  
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            elif move['moveType'] == 'untap':
               print ( 'Untap all opponent cards yo' )
               for index in opponentIndexes: 
                  allCards[index]['tapped'] = False
               buttons = getButtons (state,myTurn,hand)
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
               print ( 'Done untapping all opponent cards' )
            elif move['moveType'] == 'quit':
               showStatus( 'You have won, opponent has quit' )
               time.sleep (3)
               quit = True 
            move = None
            
         if eventType == pygame.MOUSEBUTTONUP:
            (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            print ( 'number of handSprites: ' + str(len(handSprites)) + ', num in play: ' + str(len(inplaySprites)) )
            print ( 'number in hand: ' + str(len(hand)) ) 
            
         # Handle the cards in the hand   
         card = getSpriteClick (eventType, data, handSprites)         
         if card != -1:
            selectedCard = hand[card]
            # Show card and get action
            actions = ['ok']
            if myTurn: 
               actions.append ( 'discard')
               if selectedCard.find ( '/lands/' ) == -1: # This is not a land 
                  if c.sufficientManaToCast ( manaPool, selectedCard ): 
                     actions.append ( 'cast' )
               else:
                  if not hasPlayedLand: 
                     actions.append ( 'cast' )
            action = getSingleCardAction ( selectedCard, 'Select an action', actions)  
            if action != '':
               index = handIndexes[card]            
               print ( 'Perform action: [' + action + '] on card: ' + selectedCard )     
               if action == 'discard': 
                  print ( 'Pop card: ' + str(card) + ' len(handIndexes: ' + str(len(handIndexes)) )
                  handIndexes.pop(card)
                  #TODO: Add to discard pile 
                  hand.remove (selectedCard)                   
                     
               elif action == 'cast':                  
                  crd = handIndexes.pop(card)
                  hand.pop (card) 
                  # hand.remove (selectedCard)
                  inplayIndexes.append (crd) 
                  if selectedCard.find ( '/lands/' ) > -1: # This is a land 
                     hasPlayedLand = True
                  elif selectedCard.find ( '/creatures/' ) > -1: # This is a creature  
                     allCards[index]['summoned'] = True
                  udpBroadcast ( 'exec:move={\'moveType\':\'cast\',' + \
                                 '\'filename\':\'' + selectedCard + '\'}') 
                  executeAffect (index, 'inplay')                              
                                 
            buttons = getButtons (state,myTurn,hand)                                    
            (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)

         # Handle the opponent cards ( you can target them )             
         card = getSpriteClick (eventType, data, opponentSprites)         
         if card != -1: # show the card in play
            # Show card and get action 
            index = opponentIndexes[card]
            print ( 'card: ' + str(card) + ' index: ' + str(index) + \
                    ' opponentIndexes: ' + str(opponentIndexes) ) 
            selectedCard = allCards[index]['filename']
            print ( 'selectedCard: ' + selectedCard ) 
            #tapped = allCards[index]['tapped']
            #justSummoned = allCards[index]['summoned']
            actions = ['ok','target']
               
            action = getSingleCardAction (selectedCard,'Select an action',actions)
            if action != '':
               print ( 'Perform action: [' + action + '] on opponent card: ' + selectedCard )
               
               if action == 'target':
                  targettedOpponentCard = card
                  print ( 'You have targeted this card for a spell or effect: ' + selectedCard + \
                          '[' + str(targettedOpponentCard) + ']' )
               
               buttons = getButtons (state,myTurn,hand)                  
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
                          
         # Handle the cards in play             
         card = getSpriteClick (eventType, data, inplaySprites )         
         if card != -1: # show the card in play
            # Show card and get action 
            index = inplayIndexes[card]
            print ( 'card: ' + str(card) + ' index: ' + str(index) + ' inplayIndexes: ' + str(inplayIndexes) ) 
            selectedCard = allCards[index]['filename']
            print ( 'selectedCard: ' + selectedCard ) 
            tapped = allCards[index]['tapped']
            justSummoned = allCards[index]['summoned']
            actions = ['ok']
            if myTurn: 
               if not tapped and not justSummoned:
                  actions.append ( 'tap' )
               print ( 'Get summoned property from allcards[' + str(index) + ']' )               
               if not tapped and not justSummoned: 
                  if selectedCard.find ('/creatures/') > -1: 
                     actions.append ( 'attack' )
               
            action = getSingleCardAction (selectedCard,'Select an action',actions)
            if action != '':
               print ( 'Perform action: [' + action + '] on card: ' + selectedCard )
               if action == 'tap':
                  print ( 'Tapping card inplay [' + str(card) + ']' )
                  allCards[index]['tapped'] = True
                  ind = selectedCard.find ( '/lands/' )
                  if ind > -1:
                     landType = selectedCard[ind+7:]
                     ind = landType.index ( '.' )
                     landType = landType[0:ind]
                     manaPool.append (landType)
                     print ( 'manaPool is now: ' + str(manaPool ))
                  udpBroadcast ( 'exec:move={\'moveType\':\'tap\',' + \
                                 '\'index\':\'' + str(card) + '\'}')
                     
               elif action == 'attack': 
                  showStatus ( 'Attacking with ' + selectedCard)
                  print ( 'Tapping my card with allCards[' + str(index) + ']' )
                  allCards[index]['tapped'] = True
                  udpBroadcast ( 'exec:move={\'moveType\':\'attack\',' + \
                                 '\'index\':\'' + str(card) + '\'}')
            buttons = getButtons (state,myTurn,hand)                     
            (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)

         # Handle button press
         sprite = getSpriteClick (eventType, data, buttonSprites ) 
         if sprite > -1:
            action = buttons[sprite]
            print ( 'Got a button action of: [' + action + ']' )
            if action == 'quit':
               showStatus ( 'You have elected to quit'  )      
               udpBroadcast ( 'exec:move={\'moveType\':\'quit\'}') 
               
               quit = True
            elif action == 'turndone':
               if len(hand) > 7: 
                  showStatus ( 'You must discard a card (maximum hand size == 7)' )
               else:
                  print ( 'Other players turn' )
                  udpBroadcast ( 'exec:move={\'moveType\':\'turndone\'}') 
                  hostTurn = not hostTurn
                  buttons = ['quit']
                  showStatus ( 'Waiting on other player to finish their turn' )

                  buttons = getButtons (state,False,hand)
                  (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)                      
                  targettedOpponentCard = None
                  
            elif action == 'draw':  
               print ( 'Draw a card yo' )
               handIndexes = drawCard(handIndexes)                                      
               state = 2
               buttons = getButtons (state,myTurn,handIndexes)
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
            elif action == 'untap':
               state = 1
               print ( 'Untap all cards yo' )
               for index in inplayIndexes: 
                  allCards[index]['tapped'] = False
                  manaPool = []    
               for card in allCards: 
                  card['summoned'] = False
               udpBroadcast ( 'exec:move={\'moveType\':\'untap\'}')
                  
               buttons = getButtons (state,myTurn,hand)
               (buttonSprites,opponentCards,opponentSprites,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)

   hostTurn = True # Host gets to move first
   myTurn = True
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'MTG\']')
      joining = ''
      playerJoined = False
   else:
      udpBroadcast ( 'exec:joining=\'MTG\'')
      joining = 'MTG' # Opponent should be waiting
      myTurn = False
  
   (allCards,creatureIndexes) = c.allCards() # Database of all cards, their filenames, locations, and status    
   card = selectMainCard(creatureIndexes) # Select one card from a deck of cards 
   filename = allCards[card]['filename']
   print ( 'Filename selected as basis of deck: ' + filename )
   cost = c.actualCost(filename) 
   deckBasis = filename    
   print ( 'Cost of deck basis: ' + str(cost))
   showStatus ( "Build deck based on card: " + filename + " cost: " + str(cost))

   deckFilenames = c.buildDeck (filename)   
   deck = [] 
   allCards = []
   count = 0
   for card_ in deckFilenames: 
      addCard (card_,True,'library',False)      
      deck.append ( count ) # Build a list of indexes 
      count = count + 1
 
   creature = deckBasis   
   print ( 'Got a creature filename: ' + creature )
   showCreatedDeck(deck,creature) # Show the list of cards 
   
   hand = []
   inPlay = []
   # Deal 7 cards 
   for i in range(7):
      hand = drawCard(hand)    

   pygame.display.set_caption('Waiting for player to join MTG')
   print ( 'Waiting for player to join...' )   

   transmitTimeout = 0   
   while joining != 'MTG':
      (eventType,data,addr) = getKeyOrUdp() # This should set games   
      if time.time() > transmitTimeout: 
         udpBroadcast ( 'exec:games=[\'MTG\']')
         transmitTimeout = time.time() + 2
   print ( 'joining: ' + joining )
      
   pygame.display.set_caption('Player joined...Ready')
      
   drawBoard(hand, inPlay) # Also give options for play
        
MTG=inspect.getsource(mtgPage)