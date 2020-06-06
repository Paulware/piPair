import cardDatabase
import gameDeck
import pygame
import inputOutput
import time
import utilityScreens

from pygame.locals import *

class mtgScreens: 
   DISPLAYHEIGHT = 1000
   DISPLAYWIDTH = 800
   
   WHITE = (255, 255, 255)
   BLACK = (0,     0,   0)   
   GREEN = (0,   255,   0)
   RED   = (255,   0,   0)
   
   TEXTBGCOLOR2 = GREEN
   TEXTCOLOR = WHITE
   statusMessage = ''
   lastStatus = ''
   DISPLAYSURF = None
   state = 0
   hasPlayedLand = False
   buttonSprites = None
   myHealth = 20
   
   def __init__(self,myInput,host,DISPLAYSURF): 
      # Instance variables 
      self.manaPool = [] 
      self.targettedOpponentCard = ''
      self.state = 0   
      self.myInput = myInput
      self.host = host
      self.myTurn = host
      self.DISPLAYSURF = DISPLAYSURF
      self.utilScreens = utilityScreens.utilityScreens(DISPLAYSURF)
      self.dbDeck = cardDatabase.cardDatabase()
      
      self.hostTurn = True # Host moves first
      print ( 'hostTurn initialized to : ' + str(self.hostTurn) ) 
      
   def setCaption (self,caption):
      caption = 'Health: ' + str(self.myHealth) + ' ' + caption 
      pygame.display.set_caption(caption)  

   def simpleName (self,filename): 
      name = filename 
      ind = filename.rfind ('/')
      if ind > -1:
         name = filename[ind+1:]
         ind = name.find ( '.jpg')
         if ind > -1:
            name = name[0:ind]
      return name
      
   def showCh (self,ch,x,y):
     FONT = pygame.font.Font('freesansbold.ttf', 16)
     surface = FONT.render(str(ch), True, self.TEXTCOLOR, self.TEXTBGCOLOR2)
     rect = surface.get_rect()
     rect.topleft = (x,y)
     self.DISPLAYSURF.blit(surface, rect)
     pygame.display.update()

   def chOffset (self,ch): 
      offsets = { '.':4, ':':4, ',':4, '-':4, ' ':4, '(':4, ')':4, '[':5, ']':5, '\'':4, '/':4, '=':9, \
                  'A':11, 'I':4, 'W':14, 'O':12, 'M':13, \
                  'a':9, 'b':9, 'c':9, 'e':9, 'f':6, 'i':4, 'j':4, 'k':9, 'l':4, 'm':14, 'r':6, 's':9, 't':5, 'x':9, 'v':9, 'w':12, 'y':9, 'z':8, \
                  '0':9, '1':9, '2':9, '3':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9 \
                }
      offset = 10
      if ch in offsets.keys(): 
         offset = offsets[ch]
      return offset       
      
   def showLine ( self, line, x,y ):
     height = self.DISPLAYHEIGHT - 23
     pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0,height+2,self.DISPLAYWIDTH,height+2+25))    
     pygame.display.update()
     for ch in line:
        self.showCh (ch, x, y)
        x = x + self.chOffset (ch)
         
   def placeImagesOnSurface (self,images,locations):    
      # Sprites contain rectangular information
      sprites = []
      try:
         i = 0
         for image in images: 
             sprites.append (self.DISPLAYSURF.blit (image, locations[i]) )
             i = i + 1
         pygame.display.update()        
      except Exception as ex:
         print ( 'main.showImages, could not place sprite on surface because: ' + str(ex))
      return sprites

   def loadImages (self,filenames):    
      images = [] 
      try:
         for filename in filenames:
            images.append ( pygame.image.load (filename) )     
      except Exception as ex:
         if str(ex).find ('Couldn\'t open') > -1: 
            print ( '\n***ERR\nDoes this file exist?: ' + filename + '\n')
         else:
            print ( '\n***ERR\nCould not load: ' + filename + ' because: ' + str(ex) + '\n')      
      return images
      
   def rotate (self, image, angle): 
       # calculate the axis aligned bounding box of the rotated image
       w, h       = image.get_size()
       originPos  = (w//2,h//2)
       box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
       box_rotate = [p.rotate(angle) for p in box]
       min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
       max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

       # calculate the translation of the pivot 
       pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
       pivot_rotate = pivot.rotate(angle)
       pivot_move   = pivot_rotate - pivot
       
       # get a rotated image
       rotated_image = pygame.transform.rotate(image, angle)
       
       return rotated_image
             
   def transformImages (self,images,width,height,tappedList):    
      try: 
         newImages = []
         count = 0
         for image in images:
            img = pygame.transform.scale(image, (width, height))
            if tappedList != None: 
               tapped = tappedList[count]
               if tapped: 
                  img = self.rotate (img, 90) 
            newImages.append (img) 
            count = count + 1
      except Exception as ex:
         assert False, 'Error in transformImages : ' + str(ex) 
      return newImages            
      
   def showImages (self,filenames,locations):
      images = self.loadImages (filenames)

      # Sprites contain rectangular information
      sprites = self.placeImagesOnSurface (images,locations)
      return sprites
      
   def showButtons (self,filenames,locations):
      images = self.loadImages (filenames)

      # Sprites contain rectangular information
      self.buttonSprites = self.placeImagesOnSurface (images,locations)
 
   # This procedure returns a list of images and the sprite boundaries 
   # tappedList should be None if NA
   def showCards (self,filenameList,tappedList,startLocation,width):      
      x = startLocation [0]
      y = startLocation [1]
      height = int (width * 1.4)      
      images = self.loadImages (filenameList)       
      images = self.transformImages (images,width,height,tappedList)

      # Place all images on the surface and get list of rectangles (sprites)
      sprites = []
      try:
         i = 0
         for image in images: 
             sprites.append (self.DISPLAYSURF.blit (image,(x,y)))
             width,height = image.get_size()
             
             x = x + width
             if x >= self.DISPLAYWIDTH:
                x = startLocation[0]
                y = y + height
             i = i + 1
         pygame.display.update()        
      except Exception as ex:
         assert False, 'Show cards could not place sprite (card) on surface because: ' + str(ex)
        
      assert isinstance (sprites, list), 'showCards is returning a non-list type: ' + str(sprites)
      return sprites            
          
   def actionsToIcons (self,actions): 
      filenames = []
      locations = []
      x = 50 
      y = 10
      for action in actions:
         filenames.append ( 'images/' + action + '.jpg' )
         locations.append ( (x,y) ) 
         x = x + 110
      return (filenames,locations)
      
   def getSpriteClick (self, addr, pos, sprites):    
      found = -1
      # print ( 'getSpriteClick got an addr: ' + addr )      
      if addr == 'mouse': 
         if sprites != []: 
               
            #if sprites != []:             
            #   print ( 'getSpriteClick (' + str(pos) + ',' + str(sprites[0]) + ')' ) 
            #else:
            #   print ( 'sprites == []' ) 
            assert sprites != None, 'getSprite Click, sprites = None' 
            assert not (type(sprites) is tuple), str(sprites) + '\nERR getSpriteClick (sprites), sprites is a tuple, expected a list' 
            assert isinstance(sprites, list), 'ERR getSpriteClick has been sent a non-list:' + str(sprites) 
            assert type(pos) is tuple, 'ERR getSpriteClick pos should be in (x,y) form instead got: ' + str(type(pos))  
               
            try:
               if sprites != None:
                  if self.eventType == pygame.MOUSEBUTTONDOWN: 
                     count = 0
                     for sprite in sprites: 
                        if sprite.collidepoint(pos):
                           found = count
                           break
                        count = count + 1
            except Exception as ex:
               print ( 'Could not getSpriteClick because: ' + str(ex) + 'sprite Err, sprites: ' + str(sprites)) 
               assert False, 'getSpriteClick failure'
      return found 
      
   # Get action from a single card 
   def getSingleCardAction (self,card,caption,actions):
      print ( 'getSingleCardAction (' + card + ',' + caption + ',' + str(actions) + ')' )   
      self.setCaption(caption)   
      self.DISPLAYSURF.fill((self.WHITE))
      
      image  = pygame.image.load (card).convert_alpha()
      width  = image.get_width()
      if width > 400: 
         width = 400
      height = int (width * 1.4)
      image = pygame.transform.scale(image, (width, height))                            
      self.DISPLAYSURF.blit(image, (10, 50))   
      pygame.display.update()        
      
      (filenames,locations) = self.actionsToIcons (actions)     
      sprites = self.showImages (filenames, locations )
      list = [card]
      action = ''
      quit = False
      while not quit and (action == ''):
         self.eventType,data,addr = self.myInput.getKeyOrUdp() 
         sprite = self.getSpriteClick (addr, data, sprites ) 
         if sprite != -1: 
            action = actions[sprite]
      
      print ( '[' + action + ']=getSingleCardAction(' + card + ',' + caption + ',' + str(actions) + ')' )       
      return action     
      
   def selectMainCard(self):
      print ( 'select a main card' )   
      startLocation = (10,10)     
      width = 50
      
      self.DISPLAYSURF.fill((self.WHITE))             
      sprites = self.showCards(self.dbDeck.cardList(),None,startLocation,width)
      quit = False
      print ( 'selectMainCard, display the images ' )
            
      while True:  
         self.eventType,data,addr = self.myInput.getKeyOrUdp()
         card = self.getSpriteClick (addr, data, sprites ) 
         if card != -1:
            print ( 'card: ' + str (card) ) 
            filename = self.dbDeck.cardList()[card]
            actions = ['ok','select']            
            action = self.getSingleCardAction ( filename, 'View card', actions)  
            if action == 'select':                
               break
            else:
               self.DISPLAYSURF.fill((self.WHITE))            
               sprites = self.showCards(self.dbDeck.cardList(),None,startLocation,width) # Draw deck again after viewing card              
      print ( 'card selected as basis of deck: ' + str(card))         
      return filename 

   # This indexList
   def showCreatedDeck(self,myDeck):
      self.myDeck = myDeck
      print ( 'showCreatedDeck' )
      self.DISPLAYSURF.fill((self.WHITE))       
      filenameList = self.myDeck.cardList()
      assert filenameList != [], 'showCreatedDeck filenameList = []' 
      cards = self.showCards (filenameList, None,(0,90), 35 )
      sprites = self.showImages (['images/ok.jpg'], [(400,50)] ) 
      
      while True:  
         self.eventType,data,addr = self.myInput.getKeyOrUdp()
      
         if self.eventType == pygame.MOUSEBUTTONUP:
            self.DISPLAYSURF.fill((self.WHITE))       
            cards = self.showCards (filenameList, None, (0,90), 35 )
            sprites = self.showImages (['images/ok.jpg'], [(400,50)] ) 
          
         assert isinstance(cards,list), 'Cards is not a list why? in showCreated deck'
         card = self.getSpriteClick (addr, data, cards) 
         if card != -1: # show the card
            actions = ['ok'] 
            print ( 'Got a card: ' + str(card) + ' len(myDeck) : ' + str(len(self.myDeck.gameDeck)) )            
            info = self.myDeck.gameDeck[card]            
            filename = info['filename']            
            action = self.getSingleCardAction ( filename, 'View card', actions)          

         # Check for a click on the icons
         assert isinstance(sprites,list), 'sprites is not a list why? in showCreated deck'
         sprite = self.getSpriteClick (addr, data, sprites ) 
         if sprite != -1: # Quit is the only other option           
            if sprite == 0:            
               print ( 'Got ok click' )
               break
      print ( "Done in showCreatedDeck" )
      
   def getButtons (self): 
      hand = self.myDeck.extractLocation ('inhand')   
      if self.myTurn:
         caption = 'Click on card to perform action'
      else:
         caption = 'Waiting for opponent to move'
      self.setCaption (caption)
      
      if self.myTurn:
         if self.state == 0: 
            self.buttons = ['untap', 'quit']
         elif self.state == 1:
            self.buttons = ['draw', 'quit']
         elif self.state == 2:
            if len(hand) > 7:
               self.setCaption ( 'You need to discard a card' )
               self.buttons = ['targetPlayer','quit']
            else:
               self.buttons =  ['targetPlayer','turnDone','quit']
         else: 
            assert False, 'State not handled in getButtons: ' + str(self.state)
      else:
         self.buttons = ['quit']
   
   # Build Lists of all cards in play and in hand
   def createCardLists(self):
      self.handIndexes = self.myDeck.extractLocation ('inhand')
      filenameList = self.myDeck.toFilenames (self.handIndexes) 
      assert len(filenameList) <= 8, 'showBoard too many cards in hand: ' + str(len(filenameList)) 
      self.handSprites = self.showCards (filenameList, None, (0,70), 100 )
      
      self.inplayIndexes = self.myDeck.extractLocation ('inplay')
      filenameList = self.myDeck.toFilenames(self.inplayIndexes)
      self.inplaySprites = self.showCards (filenameList, self.myDeck.tappedList(), (0, 210), 100)  
      
      self.opponentIndexes = self.opponentDeck.extractLocation ('inplay')
      filenameList = self.opponentDeck.toFilenames(self.opponentIndexes)
      self.opponentSprites = self.showCards (filenameList, self.opponentDeck.tappedList(), (0, 360), 100)           
      
   def captionOk (self,caption):
      print ( 'captionOk (' + caption + ')' ) 
      sprites = self.utilScreens.basicScreen (caption, ['ok']) 
      print ( 'sprites: ' + str(sprites) ) 

      while True:
         self.eventType,data,addr = self.myInput.getKeyOrUdp()
         option = self.getSpriteClick (addr, data, sprites )      

         if option != -1:
            break # Ok button was pressed       
      print ( 'done in captionOk' )
      
   def showBoard (self):
      self.getButtons ()    
      self.DISPLAYSURF.fill((self.WHITE))
      (filenames,locations) = self.actionsToIcons (self.buttons) 
      self.showButtons (filenames, locations)      
      self.createCardLists()
      
      pygame.draw.line(self.DISPLAYSURF, self.RED, (0, 350), (self.DISPLAYWIDTH, 350))

      if self.statusMessage != "":
         print ( 'Show status: ' + self.statusMessage )
         height = self.DISPLAYHEIGHT - 23
         pygame.draw.line(self.DISPLAYSURF, self.RED, (0, height), (self.DISPLAYWIDTH, height)) #status line
         pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0,height+2,self.DISPLAYWIDTH,25))    
         self.showLine (self.statusMessage, 1, height+4) # Show status message
         print ('Done showing Status: ' + self.statusMessage)
            
      pygame.display.update() 
            
   # Handle mouse clicks on my cards in play       
   def handleMyCardsInPlay (self,addr,data):   
      if addr == 'mouse': 
         # print ( 'handleMyCardsInPlay (' + str(data) + '), inplaySprites:' + str(self.inplaySprites)  )
         try: 
            card = self.getSpriteClick (addr, data, self.inplaySprites )         
            if card != -1: # show the card in play
               # Show card and get action 
               self.inplayIndexes = self.myDeck.extractLocation ('inplay') # Necessary?
               print ( 'inplayIndexes: ' + str(self.inplayIndexes), ' card: ' + str(card) ) 
               
               index = self.inplayIndexes[card]
               print ( 'card: ' + str(card) + ' index: ' + str(index) + ' inplayIndexes: ' + str(self.inplayIndexes) ) 
               selectedCard = self.myDeck.gameDeck[index]['filename']
               print ( 'selectedCard: ' + selectedCard ) 
               tapped = self.myDeck.gameDeck[index]['tapped']
               justSummoned = self.myDeck.gameDeck[index]['summoned']
               haste = self.myDeck.gameDeck[index]['haste']
               actions = ['ok']
               if self.myTurn: 
                  canAttack = not tapped and (not justSummoned or haste)
                  if canAttack:
                     actions.append ( 'tap' )
                  print ( 'Get summoned property from myDeck.gameDeck[' + str(index) + ']' )               
                  if not tapped and not justSummoned: 
                     if selectedCard.find ('/creatures/') > -1: 
                        actions.append ( 'attack' )
                  
               action = self.getSingleCardAction (selectedCard,'Select an action',actions)
               if action != '':
                  print ( 'Perform action: [' + action + '] on card: ' + selectedCard )
                  if action == 'tap':
                     print ( 'myDeck.gameDeck[' + str(index) + '][tapped] = True' )
                     self.myDeck.gameDeck[index]['tapped'] = True
                     ind = selectedCard.find ( '/lands/' )
                     if ind > -1:
                        landType = selectedCard[ind+7:]
                        ind = landType.index ( '.' )
                        landType = landType[0:ind]
                        self.manaPool.append (landType)
                        print ( 'manaPool is now: ' + str(self.manaPool ))
                     self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'tap\',' + \
                                                 '\'index\':' + str(index) + '}')
                        
                  elif action == 'attack': 
                     self.showStatus ( 'Attacking with ' + selectedCard)
                     print ( 'Tapping my card with myDeck.gameDeck[' + str(index) + ']' )
                     self.myDeck.gameDeck[index]['tapped'] = True
                     self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'attack\',' + \
                                                 '\'index\':\'' + str(index) + '\'}')
               self.showBoard()      
         except Exception as ex:
            assert False, 'Handle my cards in play err: ' + str(ex) 
    
   # Handle an opponent move 
   def handleOpponentMove (self):
      try:    
         move = self.myInput.popMove() 
         # Check for opponent move, handle opponent move 
         # print ( 'handle opponent udp movement' )         
         if move != None:
            moveType = move['moveType']
            print ( '  moveType: ' + moveType)
            if moveType == 'turnDone':
               self.hostTurn = not self.hostTurn
               print ( 'hostTurn is now: ' + str(self.hostTurn) ) 
               self.hasPlayedLand = False
               self.myTurn = (self.hostTurn and self.host) or (not self.hostTurn and not self.host)
               if not self.myTurn:
                  print ('ERR: Should be my turn, hostTurn is not correct: ' + str(self.hostTurn) + ' self.host: ' + \
                         str(self.host))
               self.state = 0
            elif moveType == 'cast':
               index = move['index']
               print ( 'Opponent cast index: ' + str(index))
               self.opponentDeck.gameDeck[index]['location'] = 'inplay'
            elif moveType == 'tap':
               index = move['index']
               self.opponentDeck.gameDeck[index]['tapped'] = True
            elif moveType == 'discard':
               index = move['index']
               self.opponentDeck.gameDeck[index]['location'] = 'discard'
               print ( 'location of index: ' + str(index) + ' set to discard' )
            elif moveType == 'killed':
               index = move['index']
               indexes = self.myDeck.extractLocation ('inplay')
               print ( str(index) + ' was killed, indexes before kill: ' + str(indexes) ) 
               
               self.myDeck.gameDeck[index]['location'] = 'discard'
               indexes = self.myDeck.extractLocation ('inplay')
               print ( str(index) + ' was killed, indexes after kill: ' + str(indexes) ) 
            elif moveType == 'block':
               blockerIndex = move['blocker']
               attackerIndex = move['attacker']
               blockerFilename = self.opponentDeck.gameDeck[blockerIndex]['filename']
               attackerFilename = self.myDeck.gameDeck[attackerIndex]['filename']
               power = self.opponentDeck.gameDeck[blockerIndex]['power']
               toughness = self.myDeck.gameDeck[attackerIndex]['toughness']
               if power >= toughness:                  
                  self.captionOk ( self.simpleName(attackerFilename) + ' has been killed by: ' + \
                                   self.simpleName(blockerFilename) ) 
                  self.myDeck.gameDeck[attackerIndex]['location'] = 'discard'
                  
               power = self.myDeck.gameDeck[attackerIndex]['power']
               toughness = self.opponentDeck.gameDeck[blockerIndex]['toughness']
               if power >= toughness:                  
                  self.captionOk ( self.simpleName ( blockerFilename) + ' has been killed by: ' + \
                                   self.simpleName (attackerFilename)) 
                  self.opponentDeck.gameDeck[blockerIndex]['location'] = 'discard'
                                                 
            elif moveType == 'attack':
               opponentIndex = int(move['index'])
               attackPower = self.opponentDeck.gameDeck[opponentIndex]['power']
               attackToughness = self.opponentDeck.gameDeck[opponentIndex]['toughness']
               caption = 'You are getting attacked by a ' + str(attackPower) + '/' + str(attackToughness)
               self.setCaption(caption)              
               print ( 'Tapping opponent card [' + str(opponentIndex) + ']')                  
               self.opponentDeck.gameDeck[opponentIndex]['tapped'] = True
               attackFilename = self.opponentDeck.gameDeck[opponentIndex]['filename']
               attacker = self.simpleName (attackFilename)
               self.showStatus ( ' You are getting attacked by: ' + attackFilename )
               blocked = False
               count = 0
               # Assign a blocker
               for index in self.inplayIndexes:
                  tapped = self.myDeck.gameDeck[index]['tapped']
                  filename = self.myDeck.gameDeck[index]['filename']
                  blocking = self.myDeck.gameDeck[index]['blocking']
                  if not tapped and (filename.find ( '/creatures/' ) > -1) and not blocking:
                     print ( 'filename creature in play?: ' + filename )
                     power = self.myDeck.gameDeck[index]['power']
                     toughness = self.myDeck.gameDeck[index]['toughness']
                     action = self.getSingleCardAction ( filename, 'You are being attacked by a ' + \
                                                         str(attackPower) + '/' + str(attackToughness), ['ok','block'])  
                     if action != '':
                        print ( 'Perform action: [' + action + '] on card: ' + filename)                                
                        if action == 'block': 
                           blocker = self.simpleName (filename)
                           blocked = True 
                           self.myDeck.gameDeck[index]['blocking'] = True
                           self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'block\',' + \
                                                       '\'blocker\':' + str(index) + ',' + \
                                                       '\'attacker\':' + str(opponentIndex) + '}' )                               
                           print ( 'Creature is blocked ' )
                           break
                     
                  count = count + 1
                  
               if blocked:
                  # TODO check for trample
                  print ( 'Assign damage ' + str(attackPower) + ' to ' + blocker)
                  if attackPower >= toughness: 
                     self.captionOk ( blocker + ' was killed by: ' + attacker  )
                     self.myDeck.gameDeck[index]['location']='discard'
                      
                  if power >= attackToughness:
                     self.captionOk ( blocker + ' killed ' + attacker )
                     self.opponentDeck.gameDeck[opponentIndex]['location']='discard'
                     
               else: # Assign damage               
                  attackingPower = self.opponentDeck.gameDeck[opponentIndex]['power']
                  self.myHealth = self.myHealth - attackingPower                  
                  self.captionOk ( 'You were attacked by ' + attacker + ' with power: ' + \
                                   str(attackingPower) + ' new health: ' + str(self.myHealth))
                  if self.myHealth <= 0: 
                     pass # self.showStatus ( 'You have lost yo' )
                  
            elif move['moveType'] == 'untap':
               print ( 'Untap all opponent cards yo' )
               for index in self.opponentIndexes: 
                  self.opponentDeck.gameDeck[index]['tapped'] = False
               print ( 'Done untapping all opponent cards' )               
            elif move['moveType'] == 'quit':
               self.showStatus( 'You have won, opponent has quit' )
               time.sleep (3)
               quit = True 
            else:
               assert False, 'handleOpponentMove, move not handled: ' + str(move) 
            self.showBoard()
                               
      except Exception as ex:
         assert False, 'handleOpponentMove : ' + str(ex) 
    
   # Handle mouse clicks on the cards in the my hand      
   def handleMyCardsInHand (self,addr, data):
      if addr == 'mouse': 
         try: 
            card = self.getSpriteClick (addr, data, self.handSprites)         
            if card != -1:
               self.handIndexes = self.myDeck.extractLocation ('inhand') # Necessary?
               index = self.handIndexes[card]
               info = self.myDeck.gameDeck[index]
               selectedCard = info['filename']
               # Show card and get action
               actions = ['ok']
               if self.myTurn: 
                  actions.append ( 'discard')
                  if selectedCard.find ( '/lands/' ) == -1: # This is not a land 
                     if self.myDeck.db.sufficientManaToCast ( self.manaPool, selectedCard ): 
                        actions.append ( 'cast' )
                  else:
                     if not self.hasPlayedLand: 
                        actions.append ( 'cast' )
               action = self.getSingleCardAction ( selectedCard, 'Select an action', actions)  
               if action != '':
                  index = self.handIndexes[card]            
                  print ( 'Perform action: [' + action + '] on card: ' + selectedCard )     
                  if action == 'discard': 
                     self.myDeck.gameDeck[index]['location'] = 'discard'
                        
                  elif action == 'cast':                  
                     print ( 'casting: ' + selectedCard )
                     
                     self.myDeck.gameDeck[index]['location']='inplay'
                     if selectedCard.find ( '/lands/' ) > -1: # This is a land 
                        self.hasPlayedLand = True
                        print ( 'Casting a land' + selectedCard) 
                     elif selectedCard.find ( '/creatures/' ) > -1: # This is a creature  
                        self.myDeck.gameDeck[index]['summoned'] = True
                        print ( 'Casting a creature: ' + selectedCard )
                     else:
                        assert False, 'handleMyCardsInHand, casting an unknown type of card: ' + selectedCard
                     self.myInput.udpBroadcast ( 'exec:self.move={\'index\':' + str(index) + ',\'moveType\':\'cast\'}') 
                     # executeAffect (index, 'inplay')                              
                                    
               self.showBoard()   
               
         except Exception as ex:
            assert False, 'ERR in handleMyCardsInHand : ' + str(ex) 

   # Handle mouse click on opponent cards in play 
   def handleOpponentCard (self,addr,pos):  
      if addr == 'mouse': 
         try: 
            # Handle the opponent cards ( you can target them )     
            card = self.getSpriteClick (addr, pos, self.opponentSprites)         
            if card != -1: # show the card in play
               # Show card and get action 
               index = self.opponentIndexes[card]
               print ( 'card: ' + str(card) + ' index: ' + str(index) + \
                       ' opponentIndexes: ' + str(self.opponentIndexes) ) 
               selectedCard = self.opponentDeck.gameDeck[index]['filename']
               print ( 'selectedCard: ' + selectedCard ) 
               actions = ['ok','target']
                  
               action = self.getSingleCardAction (selectedCard,'Select an action',actions)
               if action != '':
                  print ( 'Perform action: [' + action + '] on opponent card: ' + selectedCard )
                  
                  if action == 'target':
                     self.targettedOpponentCard = card
                     print ( 'You have targeted this card for a spell or effect: ' + selectedCard + \
                             '[' + str(self.targettedOpponentCard) + ']' )
                             
                  self.showBoard()
            
         except Exception as ex: 
            assert False, "Error in handleOpponentCard: " + str(ex) + " opponentSprites: " + str(self.opponentSprites)       
         
   # Handle mouse click on the buttons       
   def handleButtonPush(self, addr, mousePosition): 
      if addr == 'mouse': 
         try: 
            # Handle button press
            sprite = self.getSpriteClick (addr,mousePosition, self.buttonSprites) 
            if sprite > -1:
               action = self.buttons[sprite]
               print ( 'Got a button action of: [' + action + ']' )
               if action == 'quit':
                  if self.utilScreens.confirmScreen ('Would you like to quit the game?', self.myInput):                
                     self.showStatus ( 'You have elected to quit'  )      
                     self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'quit\'}') 
                     
                     self.quit = True
               elif action == 'turnDone':
                  self.handIndexes = self.myDeck.extractLocation ('inhand') # necessary?
               
                  if len(self.handIndexes) > 7: 
                     self.showStatus ( 'You must discard a card (maximum hand size == 7)' )
                  else:
                     print ( 'Other players turn' )
                     self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'turnDone\'}') 
                     self.hostTurn = not self.hostTurn
                     print ( 'hostTurn is now set to : ' + str(self.hostTurn)) 
                     self.showStatus ( 'Waiting on other player to finish their turn' )
                     targettedOpponentCard = None
                     self.state = 0
                     self.myTurn = False                      
                     
               elif action == 'targetPlayer': 
                  print ( 'Player is now targetted' )
                  affectTarget = 'player'               
                 
               elif action == 'draw':  
                  print ( 'Draw a card yo' )
                  self.myDeck.drawCard()
                  self.handIndexes = self.myDeck.extractLocation ('inhand')                             
                  self.state = 2
                  
               elif action == 'untap':
                  self.state = 1
                  self.inplayIndexes = self.myDeck.extractLocation ('inplay') # Necessary?
                  for index in self.inplayIndexes: 
                     self.myDeck.gameDeck[index]['tapped'] = False
                     self.manaPool = []    
                  for card in self.myDeck.gameDeck: 
                     self.myDeck.gameDeck[card]['summoned'] = False
                  self.myInput.udpBroadcast ( 'exec:self.move={\'moveType\':\'untap\'}')
               else:
                  assert False, 'handleButtonPush, Action not handled: ' + action             
               self.showBoard()
         except Exception as ex:
            assert False, 'Error in handleButtonPush: ' + str(ex) 
         

   def drawStatus (self,message):    
      if message != self.lastStatus: 
         print (message)
      # print ( 'Show status: ' + message )
      height = self.DISPLAYHEIGHT - 23
      pygame.draw.line(self.DISPLAYSURF, RED, (0, height), (self.DISPLAYWIDTH, height)) #status line
      self.showLine (message, 1, height+4) # Show status message     
      pygame.display.update()     
      self.lastStatus = message
      
   def showLastStatus (self):
      # global lastStatus 
      self.drawStatus (lastStatus)
       
   def showStatus (self,status):
      self.statusMessage = status 
      print ( 'showStatus(' + self.statusMessage + ')' )      
      
   # Draw the entire playing surface with my cards and opponents cards visible   
   def drawBoard(self,myDeck,opponentDeck): 
      self.myDeck = myDeck
      self.opponentDeck = opponentDeck
      print ('drawBoard')   
      myHealth = 20
      self.manaPool = [] 
      self.state = 0 
      self.hasPlayedLand = False
      power = 20
      
      targettedOpponentCard = None
      self.quit = False  
      
      self.showBoard()
      target = ''
      while not self.quit and (self.myHealth > 0):
         self.eventType,data,addr = self.myInput.getKeyOrUdp()     
         #print ( '[addr,data]: [' + addr + ',' + str(data) + ']' )
         self.handleButtonPush(addr,data)
         self.handleMyCardsInHand(addr,data)          
         self.handleMyCardsInPlay(addr,data)
         self.handleOpponentCard(addr,data)
         
         if addr != 'mouse': 
            self.handleOpponentMove()  
           
         if self.eventType == pygame.MOUSEBUTTONUP:
            self.showBoard()
      
if __name__ == '__main__':
    try:
       pygame.init()
       DISPLAYWIDTH = 800
       DISPLAYHEIGHT = 600
       DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
       import utilityScreens
       utilScreen = utilityScreens.utilityScreens (DISPLAYSURF)       
       myInput = inputOutput.inputOutput(utilScreen)     
       screens = mtgScreens (myInput, True,DISPLAYSURF) 
       
       dbDeck = cardDatabase.cardDatabase() 
       
       mainCard = screens.selectMainCard ()
       indexList = dbDeck.buildDeck (mainCard)
       import gameDeck       
       myDeck = gameDeck.gameDeck(indexList)
       screens.showCreatedDeck (myDeck)
       
       print ( 'create opponentdeck' )       
       mainCard = screens.selectMainCard ()
       indexList = dbDeck.buildDeck (mainCard)
       opponentDeck = gameDeck.gameDeck(indexList)
       # screens.showCreatedDeck (opponentDeck)
      
       print ( 'deal' )
       myDeck.dealHand()
       opponentDeck.dealtHand ( [30,5,9,46,40,22,49] ) 
       opponentIndexes = opponentDeck.extractLocation ('inhand')
       print ( 'List of opponent cards in hand: ' + str(opponentIndexes) ) 
       
       screens.drawBoard (myDeck,opponentDeck)
    except Exception as ex:
       print ( "Got exception: " + str(ex)) 
    finally:
       print ( 'finally ' )