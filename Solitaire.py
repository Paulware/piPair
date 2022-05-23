import inspect
import pygame
import time
import Communications
from Deck import Deck
from Utilities import Utilities
from OptionBox import OptionBox
from SubDeck import SubDeck
 
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
# Show the Uno Pages
class Solitaire (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization Uno' )
       self.iAmHost     = True        
       self.deck = Deck ('images/standardCardSprites.jpg', 13, 5, 55)   
       self.deck.canDeal (52, False)
       self.deck.canDeal (53, False)
       self.deck.canDeal (54, False)
       self.deck.coverIndex = 54
       
       hand1 = SubDeck (self.deck,7,80,120)
       hand1.hideAll () 
       hand1.x = 100
       hand2 = SubDeck (self.deck,6,80,120)
       hand2.hideAll () 
       hand2.x = 200 
       self.hands = [hand1,hand2] 
    
    def gameOver (self): 
       over = False
       return over   
    
    def dropSelection (self,x,y): 
       found = None
       # Find which hand has the selected card 
       selectedHand = None 
       count = 0 
       for hand in self.hands:
          if hand.selected != -1: 
             selectedHand = hand 
             print ( 'The hand that has the selected card is hand: ' + str(count)) 
             break
          count = count + 1   
          
       if selectedHand == None: 
          print ( 'Could not find a hand that has the selected card' )
       else:          
          # Find which hand is getting dropped on 
          found = None
          count = 0 
          for hand in self.hands:
             if hand != selectedHand: 
                index = hand.findSprite (x,y)
                if index != -1:              
                   hand.data[hand.selected].drag = False 
                   print ( 'The hand that is getting dropped on is hand: ' + str(count) + ' index: ' + str(index))  
                   hand.selected = -1
                   found = hand
                   break
                else:
                   print ( 'Could not find a sprite at [' + str(x) + ',' + str(y) + ']' ) 
                count = count + 1
                
          if found == None: 
             print ( 'Could not find a hand that was getting dropped on')
          else:
             print ( 'Found a hand getting dropped on' )       
       return found
                                   
    def runMain (self): 
       window = pygame.display.get_surface()
       quit = False 
       
       drawTime = time.time() + 0.1
       dragging = None
       while not quit:
          x = 100 
          if time.time() > drawTime: 
             window.fill ((0,0,0))
             if dragging == None: 
                for hand in self.hands: 
                   hand.showSprites (hand.x,100,displaySurface,0.0,0.25) # Show and set their x/y locations
             else:
                for hand in self.hands: 
                   hand.showSprites (hand.x,100,displaySurface,0.0,0.25) # Show and set their x/y locations
                print ( 'Dragging should be an image' )
                (x,y) = pygame.mouse.get_pos()
                
                displaySurface.blit (dragging, (x,y))             
                pygame.display.update()                
             drawTime = time.time() + 0.10
             
          (typeInput,data,addr) = utilities.read(blocking=False)
          if utilities.isMouseClick (typeInput): 
             if dragging != None: 
                dragging = None
                (x,y) = pygame.mouse.get_pos()

                h = self.dropSelection(x,y) 
                if h != None:
                   print ( 'Got a hand dropped on ') 
                else:
                   print ( 'Could not find anything dropped on')
                exit(1)                      
             else:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                print ( 'dragging == None')
                for hand in self.hands: 
                   index = hand.findSprite (x,y)                          
                   if index != -1:        
                      optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Untap', 'Cancel','Hide', 'Show', 'Drag', 'Drop'], x, y)
                      selection = optionBox.getSelection()
                      print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
                      if selection == 'Cancel': 
                         quit = True 
                      elif selection == 'Discard':
                         hand.data[index].deleted = True 
                         # hand.discard (index)
                      elif selection == 'Tap':
                         hand.tap(index, True)                
                      elif selection == 'Untap':
                         hand.tap(index, False)
                      elif selection == 'Use':
                         # hand.discard (index)
                         hand.data[index].deleted = True 
                         hand.drawCard()
                      elif selection == 'Hide':
                         hand.hide(index)
                      elif selection == 'Show':
                         hand.unhide(index)                
                      elif selection == 'Drag':
                         hand.drag (index, True) 
                         dragging = hand.data[index].image 
                         print ( 'need to redraw and remove options dragging is an image')
                      elif selection == 'Drop':
                         hand.drag (index, False) 
   
    def main (self):
       self.DISPLAYSURF.fill((BLACK))
       pygame.display.set_caption('Play Uno')        
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,500)] ) 
       pygame.display.update()       
       
       deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 52)   
   
       if self.iAmHost: 
          self.utilities.showStatus ( "Waiting for player to join")
          pygame.display.update()
          self.comm.waitFor ( 'join uno')
          hand = SubDeck (deck,7)
          hand.showSprites(100,600,80,120,self.DISPLAYSURF) 
          opponent = SubDeck (deck,7)
          opponent.changeImage ( 'images/unoFlip.jpg')          
          opponent.showSprites(100,100,80,120,self.DISPLAYSURF)
          inputStack = SubDeck (deck, 52 - 14)
          inputStack.changeImage ( 'images/unoFlip.jpg')
          inputStack.showStack (100,300,80,120,self.DISPLAYSURF)
       else: # Host goes first...
          self.utilities.showStatus ( "Waiting for host to deal")
          pygame.display.update()
          self.comm.waitForPeek ( 'deal uno')
       
       quit = False  
       joinTimeout = 0    
       print ( 'Start while loop' )
       myMove = True 
       while not quit and not self.gameOver(): 
          (event,data,addr) = self.utilities.getKeyOrUdp()
          if self.utilities.isMouseClick (event):           
             pos = data
             x = int(pos[0] / 100) - 2
             y = int(pos[1] / 100) - 1
             if (x >=0) and (y >=0) and (x <=2) and (y <= 2):
                if not myMove: 
                   self.utilities.showStatus ( 'Not your move' )
                else:   
                   if (self.taken[x][y] =='x') or (self.taken[x][y]=='o'): 
                      self.utilities.showStatus ( "Square already taken")
                   else:
                      print ('pos: [' + str(x) + ',' + str(y) + ']' ) 
                      if self.drawingX: 
                         self.drawX (x,y)
                      else:
                         self.drawO (x,y)
                         
                      self.drawingX = not self.drawingX
                      myMove = False
                      self.comm.send ( 'move tictactoe ' + str(x) + ' ' + str(y))
                                
          # Use data above to determine sprite click?          
          sprite = self.utilities.getSpriteClick (event, sprites ) 
          if sprite != -1: # Quit is the only other option           
             print ("Selected command: " + str(sprite))
             quit = True    
                  
          elif event == 'mqtt':
             if data.find ( 'move tictactoe') > -1: # Opponent has moved 
                move = data.split ( ' ' )
                print ( 'move : ' + str(move) ) 
                x = int (move[2])
                y = int (move[3])
                print ( 'x,y: ' + str(x) + ',' + str(y) ) 
                if self.drawingX: 
                   self.drawX (x,y)
                else:
                   self.drawO (x,y)
                self.drawingX = not self.drawingX                
             myMove = True               
       print ( 'Go back to the main page...' )
    
if __name__ == '__main__': 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   solitaire = Solitaire (displaySurface,utilities,None)

   solitaire.runMain() 
