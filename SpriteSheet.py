#import random
#import copy
import os
import pygame

# Create a class to read in a spriteSheet and chop it into images
# attributes:
#    data is a list, each element has an image, and an index attribute at this level
#       subsequent levels will add attributes to each data element such as x,y,width,height,name
class SpriteSheet:    
   def loadSpriteImages (self): 
      x = 0 
      y = 0 
      h = 0
      data = [] 
      for i in range (self.numImages):
         obj = type ('Object', (object,), {})
         rect = pygame.Rect(( x,y,self.spriteWidth,self.spriteHeight))
         image = pygame.Surface(rect.size).convert()
         image.blit(self.image, (0, 0), rect)
         obj.image = image
         obj.index = i
         data.append (obj)
         # Find the next x/y for the next sprite 
         h = h + 1
         if h == self.numColumns:
            x = 0
            y = y + self.spriteHeight
            h = 0
         else:
            x = x + self.spriteWidth
      print ( 'loaded ' + str(len(data)) + ' images' )
      return data

   def __init__(self, filename, numColumns, numRows, numImages):
    
      self.numImages = numImages
      if os.path.exists (filename): 
         print ( 'This file exists ' + filename )         
      else:
         print ( filename + ' does not exist' )         
      self.filename = filename 
      self.numColumns = numColumns
      self.numRows = numRows
      self.image = pygame.image.load (filename).convert()
      (width,height) = self.image.get_size()
      self.spriteWidth  = int(width/numColumns)
      self.spriteHeight = int(height/numRows) 
      print ( 'sprite [width,height]: [' + str(self.spriteWidth) + ',' + str(self.spriteHeight) + ']' )       
      self.data = self.loadSpriteImages ()        
   
def showCard (sheet, index, displaySurface): 
  image = sheet.data[index].image
  print ( 'Showing index: ' + str(sheet.data[index].index) ) 
  width  = sheet.spriteWidth
  height = sheet.spriteHeight
  position = (10,50)
  displaySurface.blit(image, position)   
  pygame.display.update()     
                  
if __name__ == '__main__':
   import Utilities
   import pygame
   pygame.init()
   DISPLAYSURF = pygame.display.set_mode((1200, 800))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities.Utilities (DISPLAYSURF, BIGFONT)      
   spriteSheet = SpriteSheet ('images/unoSpriteSheet.jpg', 10, 6, 52) 
   showCard (spriteSheet,7,DISPLAYSURF)
   
   (typeInput,data,addr) = utilities.read()
   print ( 'Got (' + str(typeInput) + ',' + str(data) + ',' + str(addr) + ')' )
