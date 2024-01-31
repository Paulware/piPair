import inspect
import pygame
import time
from Communications import Communications

from Deck      import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from SubDecks  import SubDecks
from TextBox   import TextBox
from UnoCards  import UnoCards
from Globals   import *
 
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)

import os
from Communications      import Communications
class UnoCommunications (Communications):
   # data is a list of objects that have an image and index attribute
   def __init__ (self, hostOrPlayer, utilities): 
      if hostOrPlayer == 'host':
         broker = 'localhost'
         myName = 'host'
         target = 'player'
      else: # Windows computer 
         broker = 'localhost'
         myName = 'player'
         target = 'host'
         #broker = '192.168.4.1'
         #myName = 'laptop'
         #target = 'pi7'
         #broker = 'testServer' # pi not required to be in loop 
      topic = 'messages'
      
      print ( '[broker,myName,target]: [' + broker + ',' + myName + ',' + target + ']')
      super().__init__(topic,broker,myName)
      self.callback = self.callbackProcedure
      if self.connectBroker():
         self.setTarget (target)
      else:
         raise Exception ( 'Could not connect to broker: ' + broker )
      self.utilities = utilities
      
   def callbackProcedure (self, msg ):
      data = msg.split ( ' ' )
      print ( '\n***callbackProcedure got message: [' + str(data) + ']')  
     
   def handleMessage (self, deck ): 
      myMove = False 
      if self.gotPeek ('move'): 
         message = self.pop() # consume the message
         if message.find ( 'uno move skip' ) > -1: 
            myMove = True # opponent skipping their turn
            pygame.display.set_caption('It is your move')
            self.utilities.showStatus ('Move again')
            
         # Handle the card that has played by the opponent 
         elif message.find ( 'hand discard') > -1: 
            data = message.split ( ' ' )
            index = int ( data [2] )   
            print ( 'Got an index of: ' + str(index) )                 
            sheetIndex = deck.data[index].sheetIndex             
            cardName = deck.cardName (sheetIndex)                
            self.utilities.showStatus ('Opponent discarded ' + cardName )
            
            deck.placeOnTop ( 'discard', index )
            deck.redeal ( 'opponent', 100, 50, 60, 0) 
            if cardName == 'Joker+4':
               for i in range(4): 
                  print ( 'Opponent forced a draw ' + str(i+1) + ' of 4')
                  deck.topToDeck ('draw', 'hand')                      
               self.send ( 'uno move skip' ) 
               self.utilities.showStatus ('Skipping my turn')
               deck.redeal ( 'hand', 100, 400, 60, 0)               
            elif cardName.find ( '+2' ) > -1:
               # draw 2 cards                 
               print ( 'Opponent forced a draw 1 of 2...')
               deck.topToDeck ('draw', 'hand')                      
               deck.redeal ( 'hand', 100, 400, 60, 0)
               print ( 'Opponent forced a draw 2 of 2...')
               deck.topToDeck ('draw', 'hand')                      
               deck.redeal ( 'hand', 100, 400, 60, 0)
               self.send ( 'uno move skip' ) 
               self.utilities.showStatus ('Skipping my turn')
            elif cardName.find ( 'reverse') > -1: 
               self.send ( 'uno move skip' )                
               self.utilities.showStatus ('Skipping my turn')
            elif cardName.find ( 'replay') > -1: 
               self.send ( 'uno move skip' )
               self.utilities.showStatus ('Skipping my turn')
            else:
               myMove = True   

         # The opponent is telling us to draw a hand                                     
         elif message.find ( 'draw hand') > -1:
            print ( 'split data [' + message + ']' )
            data = message.split ( ' ' )
            print ( 'data after split: ' + str(data ) ) 
            index = int ( data [2] )  
            print ( 'draw hand[' + str(index) + ']')                 
            sheetIndex = deck.data[index].sheetIndex                
            print ( 'drawing sheetIndex: ' + str(sheetIndex) ) 
            self.utilities.showStatus ('Opponent drew ' + deck.cardName (sheetIndex) )                
            print ( '*****Before move, opponent deck ****' )
            deck.showInfo ('opponent')            
            deck.moveTo ( 'opponent', index )
            print ( '*****After move, opponent deck *****' )
            deck.showInfo ( 'opponent')
            myMove = True              
            deck.redeal ( 'opponent', 100, 50, 60, 0)
            
         else:
            self.utilities.showStatus ( "Opponent moved[" + message + ", Your Turn")
            myMove = True          
            
      return myMove 
        
   def waitPeek ( self, msg ):
      print ( 'Waiting for msg: [' + msg + ']' )
      while True: 
         if self.gotPeek ( msg ):
            break
            
      print ( '\n***waitPeek, got ' + msg + '!!!!')
      
   # Handle a 'subdeck uno' message    
   def waitData (self, peekString,deck):
      self.waitPeek (peekString)
      globalDictionary['utilities'].showStatus ( "Waiting..." + peekString )
      message = self.peek()
      data = message.split (' ')
      print ( 'data: ' + str(data) ) 
      name     = data[2]                 
      cardsStr = data[3:]

      print ( 'handleSubdeck [name,cardsStr]: [' + name + ',' + str(cardsStr) + ']' )
      if self.gotPeek ('subdeck uno'):   
         message = self.peek () 
         print ( 'handleSubdeck, got message: [' + message + ']') 
         for c in cardsStr: 
            deck.placeOnTop (name, int(c))        
      else: 
         raise Exception ( 'Could not gotPeek subdeck uno' )      
                    
      self.pop() 

# Show the Uno Pages
class Uno (): 
    def __init__ (self, DISPLAYSURF, utilities, comm, host ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization Uno' )
       self.iAmHost     = host
       
    def exit1 (self):
       self.comm.disconnect()
       exit()       

    def gameOver (self): 
       over = False
       return over
       
    def main (self):             
       discardPile = None
       print ( 'Uno.main' )
       self.DISPLAYSURF.fill((BLACK))
       displaySurface = self.DISPLAYSURF # refactor out?
       if self.iAmHost: 
          pygame.display.set_caption('Play Uno I am host')        
       else:
          pygame.display.set_caption('Play Uno I am player')        
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,600)] )
       pygame.display.update()

       deck = UnoCards (10, 6, 52, 60,100,displaySurface,(100,100),1.0,0.0,coverIndex=52)
       if self.iAmHost:          
          deck.deal   ( 'hand', 7, 60, 120, 100, 400,)
          deck.redeal ( 'hand', 100, 400, 60, 0)
          deck.deal   ( 'opponent', 7, 60, 120, 100, 50)
          deck.redeal ( 'opponent', 100, 50, 60, 0)
          deck.deal   ( 'discard', 1, 60, 120, 100, 200)
          deck.redeal ( 'discard', 100, 200, 0, 0)
          deck.deal   ( 'draw', 37, 60, 120, 300, 200) 
          deck.redeal ( 'draw', 300, 200, 0, 0)          
              
          pygame.display.update()
          self.utilities.showStatus ( "Waiting for join uno")
          self.comm.waitPeek ('join uno' )
          self.utilities.showStatus ( "Give Cards")
          #self.utilities.showStatus ( '\n***Sending cards to opponent' )
          self.comm.send ( 'subdeck uno opponent ' + deck.cardsToStr ('hand') )
          self.comm.send ( 'subdeck uno draw '     + deck.cardsToStr ('draw') )                 
          self.comm.send ( 'subdeck uno discard '  + deck.cardsToStr ('discard') )
          self.comm.send ( 'subdeck uno hand '     + deck.cardsToStr ('opponent') )          
       else: # Host goes first...
          self.comm.send ( 'join uno' )
          self.utilities.showStatus ( "Waiting for host to deal")

          # Get the opponent deck from the host
          self.comm.waitData ( 'subdeck uno opponent',deck)
          deck.redeal ( 'opponent', 100, 50, 60, 0)         
          self.comm.waitData ( 'subdeck uno draw',deck )
          deck.redeal ( 'draw', 300, 200, 0, 0)
          self.comm.waitData ( 'subdeck uno discard',deck )
          deck.redeal ( 'discard', 100, 200, 0, 0)
          
          self.comm.waitData ( 'subdeck uno hand',deck)
          deck.redeal ( 'hand', 100, 400, 60, 0)

          message = self.comm.pop () # Why? 
          
             
       self.comm.pop() # Consume peek why? 
 
       myMove = self.iAmHost # Host goes first 

       dragging   = None
       dragDeck   = None
       sourceDeck = None
       offset     = None
       quit = False
       lastMove = not myMove 
       window = pygame.display.get_surface()    
       while not self.utilities.quit and not self.gameOver() and not quit:
          if myMove != lastMove: 
             lastMove = myMove
             if myMove: 
                pygame.display.set_caption('It is your move')
             else:
                pygame.display.set_caption('Waiting on opponent to move')
          
          window.fill ((0,0,0))  
          TextBox('Opponent', x=100, y=  5).draw()
          TextBox('Discard',  x=100, y=175).draw()
          TextBox('Draw',     x=310, y=175).draw()
          TextBox('Hand',     x=100, y=375).draw()        

          # Draw the decks 
          deck.draw('hand')
          deck.drawTop('discard')
          deck.drawTop('draw')
          deck.draw ('opponent')
          
          sprites = self.utilities.showImages (['quit.jpg'], [(400,600)] )       
          self.utilities.showLastStatus()
          self.utilities.flip() 
          
          if deck.length ('draw') == 1: 
             self.utilities.showStatus ( 'Need to shuffle the discardPile back into the draw pile' )
             break
          
          if (deck.length('opponent') == 0) or (deck.length ('hand') == 0): 
             if deck.length ('opponent') == 0: 
                self.utilities.showStatus ( 'You have lost :(')
             else:
                self.utilities.showStatus ( 'You have won! :)' )
             myMove = False 
          
          if not myMove: 
             myMove = self.comm.handleMessage (deck)
                             
          # pygame.display.update()
          events = self.utilities.readOne()
          for event in events:
             (typeInput,data,addr) = event                                
             
             if typeInput == 'drag': 
                sprite = deck.findCard (data)
                                               
                # Use data above to determine sprite click?               
                name = self.utilities.findSpriteName (data, sprites, ['quit'] )
                if name == 'quit': 
                   quit = True 
                   
                if myMove:
                   print ( '\n\n***DRAG***\n\n' )
                   index = deck.findCard (data) # Returns index in list 
                   if index != -1: 
                      name = deck.cardName ( deck.data[index].sheetIndex)
                      startPos = (deck.data[index].x,deck.data[index].y)                      

                      deckName = deck.data[index].location
                      if deckName == 'opponent': 
                         self.utilities.showStatus ( 'ERR you cannot move an opponents card' )
                      elif deckName == 'discard': 
                         self.utilities.showStatus ( 'ERR this is where you drop cards' )
                         # Return card to starting position 
                         hand.data[dragging].x = startPos[0]
                         hand.data[dragging].y = startPos[1]
                         startPos = None                          
                      elif deckName == 'draw':
                         deck.data[index].hide = False
                         deck.moveTo ( 'hand',index )
                         myMove = False
                         self.utilities.showStatus ( 'Waiting for opponent to move' )
                         self.comm.send ( 'uno move ' + str(index) + ' draw hand' )
                         deck.redeal ( 'hand', 100, 400, 60, 0)                         
                      elif deckName == 'hand':
                         sourceDeck = 'hand'
                         mousePos = data
                         dragging = index                    
                else: 
                   self.utilities.showStatus ('Err, not your move' )                      
 
             elif typeInput == 'move':
                if not dragging is None: 
                   if offset is None: 
                      pos = deck.pos (dragging)
                      offset = ( pos[0] - data[0], pos[1] - data[1])
                      print ( 'Starting pos: ' + str(pos) + ' mouse: ' + str(data) + ' offset: ' + str(offset))
                   newPos = ( data[0] + offset[0], data[1] + offset[1] );
                   deck.move (dragging,newPos)
                mousePos = data
                
             elif typeInput == 'drop':
                if not dragging is None: 
                   print ( 'dragging: ' + str(dragging) )
                   index = deck.findCard(data, dragging)
                   deckName = ''
                   if index != -1: 
                      deckName = deck.data[index].location
                   if (deckName != 'discard'):                     
                      self.utilities.showStatus ( 'Drop on discard pile not: ' + deckName )
                      deck.data[dragging].x = startPos[0]
                      deck.data[dragging].y = startPos[1]
                      startPos = None                       
                   else:                    
                      sheetIndex = deck.data[dragging].sheetIndex
                      if deck.canDrop (sheetIndex, deck.data[index].sheetIndex): # canDrop (topIndex,bottomIndex) 
                         self.comm.send ( 'uno move ' + str(dragging) + ' hand discard' )                                      
                         self.utilities.showStatus ( 'Waiting for opponents move' )

                         deck.moveTo ('discard', dragging )
                         deck.redeal ( 'hand', 100, 400, 60, 0)
                         
                         #print ( 'discardPile now has ' + str(discardPile.length()) + ' cards' )
                         myMove = False 
                         startPos = None
                         cardName = deck.cardName (deck.data[dragging].sheetIndex )
                         print ( 'Dragging and dropping: ' + cardName )
                         count = 0 
                         if cardName.find ( '+2' ) > -1: 
                            count = 2
                         elif cardName.find ( '+4' ) > -1: 
                            count = 4
                         if count > 0: 
                            for i in range(count): 
                               deck.topToDeck ('draw', 'opponent') 
                            deck.redeal ( 'opponent', 100, 50, 60, 0)         
                      else:
                         self.utilities.showStatus ( 'Illegal move' )
                         print ( 'Oops you cannot drop this card here' )
                         # Return card to origin position 
                         print ( '[dragging,x,y]:[' + str(dragging) + ',' + str(startPos[0]) + ',' + \
                                 str(startPos[1]) + ']' )
                         deck.data[dragging].x = startPos[0]
                         deck.data[dragging].y = startPos[1]
                         startPos = None               
                   dragging = None
                   offset = None
             else:
                self.utilities.showStatus ( 'Unknown event: [' + str(event) + ']' )
 
          if self.utilities.quit:
             print ( 'self.utilities.quit' )
          elif self.gameOver(): 
             print ( 'self.gameOver' )
          elif quit: 
             print ( 'quit == True' )          
       print ( 'Go back to the main page...' ) 
    
if __name__ == '__main__':
   try: 
      import sys
      numParameters = len(sys.argv)
      print ( 'number of parameters: ' + str(numParameters) ) 
      
      pygame.init()
      displaySurface = pygame.display.set_mode((900, 800))
      BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
      

      options        = ['host', 'player']
      comboBox       = OptionBox(options)
      result         = comboBox.run ()      
      utilities      = Utilities (displaySurface, BIGFONT)   
      globalDictionary['utilities'] = utilities
 
      comm           = UnoCommunications (result, utilities)           
      utilities.comm = comm                       
      uno = Uno(displaySurface,utilities,comm,result == 'host')
      uno.main()       
         
   finally: 
      comm.disconnect()