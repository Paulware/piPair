#import random
#import copy
import os
import pygame

# Create a class to read in a spriteSheet and chop it into images
# attributes:
#    data is a list, each element has an image, and an index attribute at this level
#       subsequent levels will add attributes to each data element such as x,y,width,height,name
class SpriteSheet:  
   # numImages is the total number of images
   # coverIndex is the zero-based index that points to the back cover 
   def __init__(self, filename, numColumns, numRows, numImages, coverIndex):    
      print ( 'SpriteSheet, filename: ' + filename )
      print ( 'SpriteSheet, numColumns: ' + str(numColumns)) 
      print ( 'SpriteSheet, numRows: ' + str(numRows) )
      print ( 'SpriteSheet numImages: ' + str(numImages ) )
      print ( 'SpriteSheet coverIndex: ' + str(coverIndex) ) 
      self.numImages = numImages
      self.coverIndex = coverIndex 
      print ( 'coverIndex is: ' + str(coverIndex)) 
      if os.path.exists (filename): 
         print ( 'This file exists ' + filename )         
      else:
         print ( filename + ' does not exist' )         
      self.filename = filename 
      self.numColumns = numColumns
      self.numRows = numRows
      if os.path.exists (filename):
         self.image = pygame.image.load (filename).convert()
         (width,height) = self.image.get_size()
         self.spriteWidth  = int(width/numColumns)
         self.spriteHeight = int(height/numRows)
         print ( 'sprite [width,height]: [' + str(self.spriteWidth) + ',' + str(self.spriteHeight) + ']' )       
         self.data = self.loadSpriteImages ()
      else:
         print( 'This filename does not exist: ' + filename)
         exit(1)  
         
   # Get the image of a specific index such as cover image 
   def getIndexImage (self,index): 
      image = None 
      x = 0 
      y = 0 
      h = 0      
      for i in range (self.numColumns * self.numRows):
         if i == index: 
            obj = type ('Object', (object,), {})
            rect = pygame.Rect(( x,y,self.spriteWidth,self.spriteHeight))
            image = pygame.Surface(rect.size).convert()
         # Find the next x/y for the next sprite 
         h = h + 1
         if h == self.numColumns:
            x = 0
            y = y + self.spriteHeight
            h = 0
         else:
            x = x + self.spriteWidth
      if image is None:
         print ( 'Could not find the image for index: ' + str(index) + ' in the spritesheet?' )
         exit(1)
         
      return image        
         
   def length(self):
      return len(self.data)

   def loadSpriteImages (self): 
      x = 0 
      y = 0 
      h = 0
      data = [] 
      maxImages = self.numColumns * self.numRows
      print ( 'maxImages: ' + str(maxImages) + ' coverIndex: ' + str(self.coverIndex)) 
      for i in range (maxImages):
         obj = type ('Object', (object,), {})
         rect = pygame.Rect(( x,y,self.spriteWidth,self.spriteHeight))
         image = pygame.Surface(rect.size).convert()
         image.blit(self.image, (0, 0), rect)
         obj.image       = image
         obj.sheetIndex  = i
         obj.canDealCard = True
         obj.tapped      = False
         obj.hide        = False
         # obj.drag        = False 
         obj.deleted     = False
         obj.location    = ''
         if i < self.numImages:
            data.append (obj)
         if i == self.coverIndex:
            print ( 'Setting self.coverImage' )
            self.coverImage = image 
            
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
   
   
def showCard (sheet, index, displaySurface): 
  image = sheet.data[index].image
  print ( 'Showing index: ' + str(sheet.data[index].sheetIndex) ) 
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
   spriteSheet = SpriteSheet ('images/unoSpriteSheet.jpg', 10, 6, 53, 52) 
   showCard (spriteSheet,7,DISPLAYSURF)
   
   (typeInput,data,addr) = utilities.read()
   print ( 'Got (' + str(typeInput) + ',' + str(data) + ',' + str(addr) + ')' )
