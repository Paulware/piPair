import inspect

def mtgPage():
   global myIO
   global DISPLAYSURF
   global iAmHost
   
   host = iAmHost
 
   screens = mtgScreens.mtgScreens (myIO, True,DISPLAYSURF) 
   import cardDeck  
   myDeck = cardDeck.cardDeck(True)
   mainCard = screens.selectMainCard (myDeck)
   myDeck.buildDeck (mainCard)
   indexList = myDeck.toDbIndexes ()  
   
   myIO.udpBroadcast ( 'exec:self.opponentDeck=' + str(indexList) + '')   
   screens.showCreatedDeck (myDeck)   
   myIO.waitFor ('Waiting for opponent to send deck','self.opponentDeck != []')
   #Todo: Create opponentDeck from myIO.opponentDeck
   opponentDeck = None
   
   indexes = myDeck.dealHand()
   myIO.udpBroadcast ( 'exec:self.dealtHand=' + str(indexes) )  
   # Todo: Move opponentDeck indexes to 'inhand' based on myIO.dealtHand
   myIO.waitFor ('Wait for opponent to deal hand', 'self.dealtHand != []' )
   
   if opponentDeck != None: 
      screens.drawBoard(host,myDeck,opponentDeck) # Also give options for play      
   
MTG=inspect.getsource(mtgPage)   