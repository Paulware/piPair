import pygame

'''
   SubDeck is like a hand or a discard pile 
   It will use Decks ability to deal and will add the attributes x,y,width,height to each element in the dealt hand.
   There is no descriptive name on each element, that will be added based on id in the particular game class.   
'''
class SubDeck (): 
   # data is a list of objects that have an image and index attribute
   def __init__ (self, deck, numCards,width,height,hide=False):
      self.deck = deck
      dealtCards = self.deck.deal (numCards)
      self.data = dealtCards
      for card in self.data: # Set the width/height of each image 
         card.image = pygame.transform.scale(card.image, (width, height))                                     
         card.angle = 0
         card.hide  = hide 
      self.numImages = len(self.data) 
      print ('Total number of cards: ' + str(self.numImages)) 
   
   def shuffle (self): 
      print ( 'Shuffle the deck' )

   def changeImage (self, filename): 
      image = pygame.image.load (filename).convert()
      for d in self.data:
         d.image = image
         
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

    # Show the sprites at specified start position and update the location of each   
   def showSprites (self, startX, startY, displaySurface, offsetX=0, offsetY=0): 
      x = startX
      y = startY 
      print ('showSprites, self.data: ' + str(self.data)) 
      
      if len(self.data) > 0:
         width = self.data[0].image.get_width()
         height = self.data[0].image.get_height()
      for sprite in self.data:
         if sprite.hide: 
            image = pygame.transform.scale(self.deck.data[len(self.deck.data)-1].image, (width, height))             
         else: 
            image = sprite.image         
         displaySurface.blit (image, (x,y)) 
         # Update location so it can be found later
         sprite.x = x
         sprite.y = y
         
         x = x + sprite.image.get_width ()
         y = y + offsetY
         
      print ( 'showSprites, self.data after adding data ' + str(self.data))
      pygame.display.update()
      
   def showStack (self, x, y, displaySurface): 
      for sprite in self.data:  
         if sprite.hide: 
            sprite.image = self.data[len(self.data)-1].image
         else: 
            sprite.image = pygame.transform.scale(sprite.image, (width, height))                                     
         displaySurface.blit (sprite.image, (x,y)) 
         # Update location so it can be found later
         sprite.x = x
         sprite.y = y
         sprite.width = width
         sprite.height = height 
         
      pygame.display.update()
      
      
   def findSprite (self,x,y):
      index = 0 
      found = -1
      print ( 'findSprite (' + str(x) + ',' + str(y) + ')' ) 
      for sprite in self.data: 
         print ( '[x,y,sprite0,sprite1]: [' + str(x) + ',' + str(y) + ',' + str(sprite.x) + ',' + str(sprite.y) + ']' )
         if ((x > sprite.x) and (x < (sprite.x + sprite.image.get_width())) and \
             (y > sprite.y) and (y < (sprite.y + sprite.image.get_height()))): 
            print ( 'Found sprite at index: ' + str(index))
            found = index 
            break
         index = index + 1
      return found 
      
   def discard (self,index): 
      self.data.pop (index) 

   def tap (self,index):
      print ( 'Rotate the image by 90 degrees' )
      image = self.data[index].image
      if self.data[index].angle == 90: 
         self.data[index].image = self.rotate (image,-90) 
      else: # Current angle == 0
         self.data[index].image = self.rotate (image,90) 
      if self.data[index].angle == 0:       
         self.data[index].angle = 90
      else:
         self.data[index].angle = 0      

   def drawCard (self): 
      cards = self.deck.deal (1)
      self.data.append (cards[0]) 
      
   def hide (self,index):
      self.data[index].hide = True 
      
   def unhide (self,index):
      self.data[index].hide = False 
      
      
             
if __name__ == '__main__':
   from Deck import Deck
   from Utilities import Utilities
   from OptionBox import OptionBox
 
   pygame.init()
   displaySurface = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (displaySurface, BIGFONT)   
   
   deck = Deck ('images/unoSpriteSheet.jpg', 10, 6, 53)   
   
   hand = SubDeck (deck,7,80,120)
   # hand.showSprites(100,100,50,100)   
   window = pygame.display.get_surface()
   
   while True: # len(deck.sprites) > 0:
      hand.showSprites(100,100,displaySurface) # Show and set their x/y locations
      (typeInput,data,addr) = utilities.read()
      if utilities.isMouseClick (typeInput): 
         pos = pygame.mouse.get_pos()
         x = pos[0]
         y = pos[1]
         index = hand.findSprite (x,y)
         if index != -1: 
             optionBox = OptionBox (['Use', 'Discard', 'Tap', 'Cancel', 'Hide', 'Show'], x, y)
             selection = optionBox.getSelection()
             print ( '[index,selection]: [' + str(index) + ',' + selection + ']' ) 
             if selection == 'Cancel': 
                break
             elif selection == 'Discard':
                hand.discard (index) 
             elif selection == 'Tap':
                print ( 'Call hand.tap (' + str(index) + ') ' )
                hand.tap (index)
             elif selection == 'Use':
                hand.discard (index)
                hand.drawCard()
             elif selection == 'Hide':
                hand.hide(index)
             elif selection == 'Show':
                hand.unhide(index)

             window.fill ((0,0,0))