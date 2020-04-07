import inspect
#TODO: Each while loop has its own def 
def mtgPage():
   global joining 
   global move 
   global iAmHost
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
      if (ind == 49) or (ind == 50): 
         print ( 'Adding card: ' + filePath + ',' + str(owned) + ',' + location + ',' + str(tapped) ) 
      card = {'index':ind, 'iOwnIt':owned, 'filename':filePath, 'location':location, 'tapped':tapped}
      allCards.append (card) 
   def modCard (index,owned,loc,isTapped): 
      filename = allCards[index]['filename']
      allCards[index] = {'filename':filename, 'iOwnIt':owned, 'location':loc, 'tapped':isTapped} 
   def modTapped (index,tapped): 
      allCards[index]['tapped'] = tapped
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
      
   def drawCard(hand):
      libraryList = [] 
      for card in allCards:
         location = card['location']
         if location == 'library':
            libraryList.append ( card['index'] )
      
      index = int( random.random() * len(libraryList))
      allCards[index]['location'] = 'inhand'
      hand.append (index)
      return hand
      
   ''' 
   pieces = []   
   
   pieces = [  #   id,  image,            image,                                          x   y    angle, health 
                ['white',extractImage ('images/mtgCards.png', 0, 0, 164, 212, 60, 80) ,     (100,100), 45,   100],\
                ['black',extractImage ('images/mtgCards.png', 168, 428, 340, 605, 60, 80),  (400,400), 135,  100] \
            ]
   
   walls = []
   
                pygame.Rect(150,100,30,200), \
                pygame.Rect(250,300,250,30), \
           ] 
   
   # manaCosts = {
   
   # os.chdir('images/mtg/creatures')
   creaturFilenames = glob.glob('images/mtg/creatures/*.*')
   creatureFilenames = []
   for filename in creaturFilenames:
      filename = filename.replace ( '\\', '/') 
      creatureFilenames.append (filename)
      
   # print ('creatureFilename: ' + str(creatureFilenames)) 
   count = 0
   
   #Note do not run this code as it will overwrite the mana cost
   f = open ( 'castingCost.py', 'w' )
   f.write ( 'class castingCost: \n' )
   f.write ( '   cost = { \\\n' ) 
   for filename in filenames: 
      count = count + 1
      f.write ( '      \'' + filename + '\':\'whiteblackgreenbluered\', \\\n' )
   f.write ( '   }\n' ) 
   f.write ( '   def __init__(self):\n' ) 
   f.write ( '      pass\n' ) 
   f.close()
   '''
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
         '''      
         if joining != 'MTG':
            if time.time() > joinTimeout: 
               joinTimeout = time.time() + 1
               udpBroadcast ( 'exec:games=[\'MTG\']') 
         '''                                  
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
      manaPool = [] 
      hand = indexesToFilenames (handIndexes)
      print ( 'drawBoard hand: ' + str(hand))
      inplay = indexesToFilenames (inplayIndexes)
      print ( 'drawBoard inplay: ' + str(inplay))
      def showBoard (actions): 
         pygame.display.set_caption('Click on card to perform action (hand,inplay):')
         DISPLAYSURF.fill((WHITE))
         (filenames,locations) = actionsToIcons (actions) 
         (images,sprites) = showImages (filenames, locations )
         print ( 'drawBoard.showBoard, draw cards in hand' )         
         (images,handSprites) = showCards (handIndexes, (0,90), 100 )
         print ( 'drawBoard.showBoard, draw cards in play' )
         (images,inplaySprites) = showCards (inplayIndexes, (0, 250), 100)  
         print ( 'Done in drawBoard.showBoard' )
         return (sprites,handSprites,inplaySprites)
         
      quit = False   
      (buttonSprites,handSprites,inplaySprites) = showBoard(['done','quit','draw','nextturn', 'untap'])
      while not quit:  
         (eventType,data,addr) = getKeyOrUdp()

         if eventType == pygame.MOUSEBUTTONUP:
            (buttonSprites,handSprites,inplaySprites) = showBoard(['done','quit','draw','nextturn', 'untap'])
            
         card = getSpriteClick (eventType, data, handSprites)         
         if card != -1: # show the card in hand
            selectedCard = hand[card]
            # Show card and get action
            actions = ['discard', 'ok']
            if selectedCard.find ( '/lands/' ) == -1: # This is not a land 
               if c.sufficientManaToCast ( manaPool, selectedCard ): 
                  actions.append ( 'cast' )             
            else:
               if not hasPlayedLand: 
                  actions.append ( 'cast' )
            action = getSingleCardAction ( selectedCard, 'Select an action', actions)  
            if action != '':
               index = inhandIndexes[card]            
               print ( 'Perform action: (only action should be play/discard)  [' + action + '] on card: ' + selectedCard )     
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
                  hand.remove (selectedCard)
                  inplayIndexes.append (crd) 
                  if selectedCard.find ( '/lands/' ) > -1: # This is a land 
                     hasPlayedLand = False #True
                  elif selectedCard.find ( '/creatures/' ) > -1: # This is a creature  
                     modSummoned (index,True) 
                  
            showBoard(['quit'])
               
         card = getSpriteClick (eventType, data, inplaySprites )         
         if card != -1: # show the card in play
            # Show card and get action 
            index = inplayIndexes[card]
            print ( 'card: ' + str(card) + ' index: ' + str(index) + ' inplayIndexes: ' + str(inplayIndexes) ) 
            selectedCard = allCards[index]['filename']
            print ( 'selectedCard: ' + selectedCard ) 
            tapped = allCards[index]['tapped']
            actions = ['ok']
            if not tapped:             
               actions.append ( 'tap' ) 
            if not allCards[index]['summoned']: 
               actions.append ( 'attack' )             
               
            action = getSingleCardAction (selectedCard,'Select an action',actions)  
            if action != '':
               print ( 'Perform action: [' + action + '] on card: ' + selectedCard )
               if action == 'tap': 
                  print ( 'Tapping card yo' )
                  modTapped (index, True )
                  ind = selectedCard.find ( '/lands/' )
                  if ind > -1: 
                     landType = selectedCard[ind+7:]
                     ind = landType.index ( '.' )
                     landType = landType[0:ind]
                     manaPool.append (landType) 
                     print ( 'manaPool is now: ' + str(manaPool ) ) 
                  # showAllCards()
               
            showBoard(['quit'])

         sprite = getSpriteClick (eventType, data, buttonSprites ) 
         # 'done', 'quit', 'draw', 'nextturn'
         if sprite == 1:
            showStatus ( 'You have elected to quit'  )      
            quit = True
         elif sprite == 0: #done 
            if len(hand) > 7: 
               showStatus ( 'You must discard a card (maximum hand size == 7)' )
            else:
               quit = True
         elif sprite == 2: #draw  
            print ( 'Draw a card yo' )
         elif sprite == 3: #next turn 
            print ( 'Take another turn yo' )
         elif sprite == 4: # untap
            print ( 'Untap all cards yo' )
            
      return (handIndexes,inplayIndexes,hasPlayedLand)      
               
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'MTG\']')
      joining = ''
      playerJoined = False
      myTurn = True
   else:
      udpBroadcast ( 'exec:joining=\'MTG\'')
      joining = 'MTG' # Opponent should be waiting
      move = None
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
   for i in range(8):
      hand = drawCard(hand)
   
   hasPlayedLand = False    
   (hand,inPlay,hasPlayedLand) = drawBoard(hand, inPlay, hasPlayedLand) # Also give options for play
        
MTG=inspect.getsource(mtgPage)