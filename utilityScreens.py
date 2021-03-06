import pygame
import inputOutput 
from pygame.locals import *

class utilityScreens: 
   DISPLAYHEIGHT = 800
   DISPLAYWIDTH = 600
   
   WHITE = (255, 255, 255)
   BLACK = (0,     0,   0)   
   GREEN = (0,   255,   0)
   RED   = (255,   0,   0)
   
   TEXTBGCOLOR2 = GREEN
   TEXTCOLOR = WHITE
   statusMessage = ''
   lastStatus = ''
   DISPLAYSURF = None
   
   WHITE = (255, 255, 255)
   BLACK = (0,     0,   0)   
   GREEN = (0,   255,   0)
   RED   = (255,   0,   0)
   
   def __init__(self,DISPLAYSURF): 
      self.DISPLAYSURF = DISPLAYSURF
      
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
      
   def placeImagesOnSurface (self,images,locations,offset = 0):    
      # Sprites contain rectangular information
      sprites = []
      try:
         i = 0
         for image in images: 
             # locations[i][0] = locations[i][0] + offset
             sprites.append (self.DISPLAYSURF.blit (image, locations[i]) )
             i = i + 1
         pygame.display.update()        
      except Exception as ex:
         print ( 'utilityScreen.placeImagesOnSurface, could not place sprite on surface because: ' + str(ex))
      return sprites      
      
   def showImages (self,filenames,locations,offset =0):
      images = self.loadImages (filenames)

      # Sprites contain rectangular information
      sprites = self.placeImagesOnSurface (images,locations,offset)
      return sprites
      
   def getSpriteClick (self, pos, sprites):    
      found = -1
      assert sprites != None, 'getSprite Click, sprites = None' 
         
      try:
         assert not (type(sprites) is tuple), str(sprites) + '\nERR getSpriteClick (sprites), sprites is a tuple, expected a list' 
         assert isinstance(sprites, list), 'ERR getSpriteClick has been sent a non-list:' + str(sprites) 
         if sprites != None:
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
            
   def actionsToIcons (self,actions): 
      filenames = []
      locations = []
      x = 50 
      y = 10
      for action in actions:
         filenames.append ( 'images/' + action.lower() + '.jpg' )
         locations.append ( (x,y) ) 
         x = x + 110
      return (filenames,locations)
            
   def basicScreen (self,caption,actions,offset=0): 
      pygame.display.set_caption(caption)   
      self.DISPLAYSURF.fill((self.WHITE))      
      (filenames,locations) = self.actionsToIcons (actions)     
      sprites = self.showImages (filenames, locations,offset )   
      pygame.display.update() 
      print ( 'basicScreen returning sprites: ' + str(sprites ) ) 
      return sprites 
      
   def confirmScreen (self,caption,myInput): 
     sprites = self.basicScreen (caption, ['Confirm', 'Cancel'],300)
     confirmed = False

     while True:
        self.eventType,data,addr = myInput.getKeyOrUdp()
        option = self.getSpriteClick (data, sprites )      

        if option != -1:
           confirmed = (option == 0)
           break # Ok button was pressed       
           
         
  