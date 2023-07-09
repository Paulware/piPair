import pygame
from SubDeck      import SubDeck
from Utilities    import Utilities
from SelectButton import SelectButton 
from ViewImage    import ViewImage 
from StatusBar    import StatusBar
from Labels       import Labels 
from images.mtg.CardInfo import CardInfo 

'''
   MTGCards is based on SubDeck but customized to an MTG deck   
   Wherever SubDeck is used, MTGCards can be used instead.  
'''
class MTGShowCards (SubDeck):  

   # data is a list of objects that have an image and index attribute
   def __init__ (self, deckBasis, filename='', width=100, height=150, startXY=(100,100), \
                 displaySurface=None, xMultiplier=1.0, yMultiplier=0.0, cards=[], empty=False, \
                 name='', utils=None):
      data = []
      numCards = 0
      self.cardInfo = CardInfo()
      self.utilities = utils

      if str(filename).isnumeric():  
         print ( 'ERR MTGCards, filename has been passed as a number: ' + str(filename) ) 
         exit ()
      elif filename != '': 
         print ( 'open [filename]: [' + str(filename) + ']' )
         f = open ( filename, 'r' )
         line = f.readline()
         f.close 
         data = line.split ( ',' )
         numCards = len(data)
         print ( 'Got ' + str(numCards) + ' of cards read' )         
         
      cards = [] 
      for d in data: 
         cards.append ( int(d)) 
         
      print ( 'MTGCards.init' )
      SubDeck.__init__ (self,deckBasis=deckBasis, numCards=numCards, width=width, height=height, \
                        startXY=startXY, displaySurface=displaySurface, xMultiplier=xMultiplier, \
                        yMultiplier=yMultiplier, cards=cards, empty=empty, name=name)
                        
      print ('MTGCards, total number of cards: ' + str(self.numImages) + ' done in __init__') 
    
     
   def printInfo (self,sheetIndex):
      print ( 'Show info for card with index: ' + str(sheetIndex)) 
      print ( 'Info for card[' + str(sheetIndex) + ']: ' + \
              self.cardName(sheetIndex))      
              
   def sheetIndex (self,index): 
      ind = self.data[index].sheetIndex
      
   def show (self): 
      window = pygame.display.get_surface()
      width  = window.get_width()
      height = window.get_height()
      count = 0  
      x= 100 
      y= 20       
      for sprite in self.data:
         count = count + 1
         image = self.getImage (sprite)
         # print ( 'card (' + str(count) + ').[x,y,sheetIndex: [' + str(x) + ',' + str(y) + ',' + str (sprite.sheetIndex) + ']'  ) 
         self.displaySurface.blit (image, (x,y))
         sprite.x = x
         sprite.y = y
         x = x + sprite.width
         if (x + sprite.width) > width:
            x = 100 
            y = y + sprite.height
          
   def selectOption ( self, options): 
      x = 600
      y = 100 
      optionBox = OptionBox (options, x,y, width=300)                  
      return optionBox                    
         
    
if __name__ == '__main__':
   from Deck      import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
   from SubDecks  import SubDecks
   from TextBox   import TextBox
   from MTGSetup  import MTGSetup
   import time   
   
   pygame.init()
   displaySurface = pygame.display.set_mode((1400, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   deck         = Deck ('images/mtgSpriteSheet.png', 10, 30, 291, 290)
   filename     = MTGSetup(utilities).chooseDeckFilename('redDeck.txt')   
   drawPile     = MTGShowCards (deck, filename, startXY=(300,200), displaySurface=displaySurface, xMultiplier=1.0, \
                  yMultiplier=0.0, name='drawPile') 
   drawPile.show()
   window = pygame.display.get_surface()
   bar = StatusBar (x=1000)
   
   quit = False 
   while not quit:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0))   
      drawPile.show() # Show and set their x/y locations

      bar.show (['Quit'] )
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drag':
            bar.update (data) 
            if bar.selection != '':
               if bar.selection == 'Quit': 
                  quit = True
                  bar.consumeSelection()
            
            index = drawPile.findSprite (data)
            if index != -1: 
               card = drawPile.data[index]
               sheetIndex = drawPile.data[index].sheetIndex
               name = drawPile.cardInfo.idToName (sheetIndex)            
               drawPile.data[index].filename = name # Set the filename of the card                
               card = drawPile.data[index]
               
               optionBox = drawPile.selectOption (['View'])                  
               selection = optionBox.getSelection()
               
               print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
               if selection == 'View':                 
                  drawPile.view (sheetIndex, 'images/mtg/' + name)               
         elif typeInput != 'move':
            print ( 'event: ' + typeInput)