import inspect
def mtgPage():
   global myIO
   global DISPLAYSURF
   global iAmHost
   
   print ( 'Am i the host?: ' + str(iAmHost) ) 
   screens = mtgScreens.mtgScreens (myIO, iAmHost, DISPLAYSURF) 
   import gameDeck
   import cardDatabase
   
   db = cardDatabase.cardDatabase()
   
   mainCard = screens.selectMainCard ()
   print ( 'Build deck yo' )
   indexList = db.buildDeck (mainCard) 
   
   myDeck = gameDeck.gameDeck(indexList)
   
   myIO.udpBroadcast ( 'exec:self.opponentDeck=' + str(indexList) + '')   
   screens.showCreatedDeck (myDeck)   
   myIO.waitFor ('Waiting for opponent to send deck','self.opponentDeck != []')
   print ('Opponent deck:'+ str(myIO.opponentDeck)) 
   
   opponentDeck = gameDeck.gameDeck(myIO.opponentDeck )    
   print ( 'Created opponentdeck: ' + str(opponentDeck.cardList()) ) 
   indexes = myDeck.dealHand()
   myIO.udpBroadcast ( 'exec:self.dealtHand=' + str(indexes) )  
   # Todo: Move opponentDeck indexes to 'inhand' based on myIO.dealtHand
   myIO.waitFor ('Wait for opponent to deal their hand', 'self.dealtHand != []' )              
   opponentDeck.dealtHand (myIO.dealtHand) 
   screens.drawBoard(myDeck,opponentDeck) # Show the game board     
   
MTG=inspect.getsource(mtgPage)   