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
   def addCard (filePath,owned,location,tapped): 
      ind = len(allCards)
      card = {'index':ind, 'iOwnIt':owned, 'filename':filePath, \
              'location':location, 'tapped':tapped, \
              'summoned':False}
      allCards.append (card) 
   def modCard (index,owned,loc,isTapped): 
      allCards[index]['iOwnIt'] = owned
      allCards[index]['location'] = loc
      allCards[index]['tapped'] = isTapped
   def modSummoned (index,summoned): 
      allCards[index]['summoned'] = summoned
   def showAllCards():
      for card in allCards:
         filename = card['filename']
         iOwnIt = card['iOwnIt']
         location = card['location']
         tapped = card['tapped']
         index = card['index']
         msg = 'card{index:'
         if index<10: 
            msg = msg + ' '
         msg = msg + str(index) + ',iOwnIt:' + str(iOwnIt) 
         if iOwnIt:
            msg = msg + ' tapped:' 
         msg = msg + str(tapped) 
         if tapped:
            msg = msg = ' ' 
         msg = msg + ',location:'
         if location == 'inhand':
            msg = msg + ' ' 
         
         msg = msg + location + ',filename:' + filename + '}'
         msg = msg + ', cost=' + str(c.totalManaCost ( filename )) 
         print (msg)
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
      print ( 'showCards (indexList: ' + str(indexList) + \
              ' startLocation: ' + str(startLocation) + ',width: ' + str(width) + ')' )
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
            
   def actionsToIcons (actions): 
      filenames = []
      locations = []
      x = 50 
      y = 10
      for action in actions:
         filenames.append ( 'images/' + action + '.jpg' )
         locations.append ( (x,y) ) 
         x = x + 110
      return (filenames,locations)
      
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
   def drawBoard(handIndexes, inplayIndexes, hasPlayedLand): 
      global move
      global iAmHost
      global hostTurn
      
      manaPool = [] 
      opponentIndexes = []
      
      def showBoard (actions): 
         pygame.display.set_caption('Click on card to perform action (hand,inplay):')
         DISPLAYSURF.fill((WHITE))
         (filenames,locations) = actionsToIcons (actions) 
         (images,sprites) = showImages (filenames, locations )
         print ( 'drawBoard.showBoard, draw cards in hand' )         
         (images,handSprites) = showCards (handIndexes, (0,70), 100 )
         hand = indexesToFilenames (handIndexes)
         print ( 'drawBoard hand: ' + str(hand))
         print ( 'drawBoard.showBoard, draw cards in play' )
         (images,inplaySprites) = showCards (inplayIndexes, (0, 210), 100)  
         inplay = indexesToFilenames (inplayIndexes)
         print ( 'drawBoard inplay: ' + str(inplay))
         print ( 'drawBoard.showBoard, draw opponent cards' )
         (images,opponentSprites) = showCards (opponentIndexes, (0, 360), 100)  
         opponentCards = indexesToFilenames (opponentIndexes)
         print ( 'drawBoard opponentCards: ' + str(opponentCards))
         print ( 'Done in drawBoard.showBoard' )
         pygame.draw.line(DISPLAYSURF, RED, (0, 350), (DISPLAYWIDTH, 350))
         pygame.display.update() 
         
         
         return (sprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites)
         
      quit = False  
      myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)  
      if myTurn:
         buttons = ['done','quit','draw','untap','turndone']
      else:   
         buttons = ['quit']
         showStatus ( 'Waiting on other player to finish their turn' )
      (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
         
      while not quit:            
         myTurn = (hostTurn and iAmHost) or (not hostTurn and not iAmHost)       
         (eventType,data,addr) = getKeyOrUdp()
         
         if move != None:
            print ( "Got a move yo" )
            print ( '  moveType: ' + move['moveType'] )
            print ( '  filename: ' + move['filename'] )
            if move['moveType'] == 'turndone':
               buttons = ['done','quit','draw','untap','turndone']
               (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
               hostTurn = not hostTurn
               
            move = None
            
         if eventType == pygame.MOUSEBUTTONUP:
            (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
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
                  if len(hand) <= 7: 
                     showStatus ( "Your turn is over due to discard" )
                     quit = True 
               elif action == 'cast':                  
                  crd = handIndexes.pop(card)
                  hand.pop (card) 
                  # hand.remove (selectedCard)
                  inplayIndexes.append (crd) 
                  if selectedCard.find ( '/lands/' ) > -1: # This is a land 
                     hasPlayedLand = True
                  elif selectedCard.find ( '/creatures/' ) > -1: # This is a creature  
                     modSummoned (index,True) 
                  udpBroadcast ( 'exec:move={\'moveType\':\'cast\', \
                                 \'filename\':\'' + selectedCard + '\'}') 

            (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(['quit'])

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
                  print ( 'Tapping card ' + str(index) )
                  allCards[index]['tapped'] = True                  
                  ind = selectedCard.find ( '/lands/' )
                  if ind > -1: 
                     landType = selectedCard[ind+7:]
                     ind = landType.index ( '.' )
                     landType = landType[0:ind]
                     manaPool.append (landType) 
                     print ( 'manaPool is now: ' + str(manaPool ) ) 
                  # showAllCards()               
               elif action == 'attack': 
                  allCards[index]['tapped'] = True
                  
            (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(['quit'])

         sprite = getSpriteClick (eventType, data, buttonSprites ) 
         if sprite > -1:
            action = buttons[sprite]
            print ( 'Got a button action of: [' + action + ']' )
            if action == 'quit':
               showStatus ( 'You have elected to quit'  )      
               quit = True
            elif action == 'turndone':
               if len(hand) > 7: 
                  showStatus ( 'You must discard a card (maximum hand size == 7)' )
               else:
                  print ( 'Other players turn' )
                  hostTurn = not hostTurn
                  buttons = ['quit']
                  showStatus ( 'Waiting on other player to finish their turn' )
                  (buttonSprites,opponentCards,opponentIndexes,hand,handSprites,inplay,inplaySprites) = showBoard(buttons)
                      
                  udpBroadcast ( 'exec:move={\'moveType\':\'turndone\'}') 

               '''
               #TODO: when other player finished their turn                
               hasPlayedLand = False              
               for index in inplayIndexes: 
                  allCards[index]['summoned'] = False 
                  print ( 'next turn, allCards[' + str(index) + '][summoned] == False' )          
               '''                  
            elif action == 'draw':  
               print ( 'Draw a card yo' )
               handIndexes = drawCard(handIndexes)                                      
            elif action == 'untap':
               print ( 'Untap all cards yo' )
               for index in inplayIndexes: 
                  allCards[index]['tapped'] = False
                  manaPool = []    

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
   
   pygame.display.set_caption('Getting artifact,lands,instants and sorceries that share mana with:' + creature)
   hand = []
   inPlay = []
   # Deal 7 cards 
   for i in range(7):
      hand = drawCard(hand)
      
   if myTurn: 
      hand = drawCard(hand)
   
   hasPlayedLand = False    
   drawBoard(hand, inPlay, hasPlayedLand) # Also give options for play
        
MTG=inspect.getsource(mtgPage)