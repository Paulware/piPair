import pygame
from PIL import Image
import os

class ViewImage: 
   def __init__ (self, filename):
      font = pygame.font.SysFont(None, 30)
      surface = pygame.display.get_surface()   
      surfaceRect = surface.get_rect()
      print ( 'Surface info: ' + str(surface.get_rect()) ) 
      image = pygame.image.load(filename).convert()
      width = image.get_width()
      if width > surfaceRect[2]:
         width = surfaceRect[2]
         
      height = image.get_height()
      if (height +50)> surfaceRect[3]:
         height = surfaceRect[3] - 50
         
      image = pygame.transform.scale(image, (width,height))
             
      surface.blit (image, (0,0)) 
      
      # Draw Ok message 
      x = 40
      y = height + 20
      
      buttons = ['Ok']
      buttonRects = [] 
      for buttonText in buttons: 
         buttonSurf     = font.render (buttonText, True, (0,255,0)) # Color is final argument 
         width          = buttonSurf.get_width()
         height         = buttonSurf.get_height()
         buttonTextRect = pygame.Rect ( x, y, width, height) 
         buttonRects.append (buttonTextRect)
         borderRect     = pygame.Rect ( x-5, y-5, width+10, height+10 )  
         surface.blit ( buttonSurf, buttonTextRect)
         pygame.draw.rect ( surface, (255,0,0), borderRect, width=1 )      
         pygame.display.flip()
         x = x + width + 20 # Next button 
            
      # Wait for user to click or press a key 
      selection = ''      
      while selection == '':
         pygame.time.Clock().tick(60)
         for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
               pos = pygame.mouse.get_pos()  
               print ( 'Got pos: ' + str(pos))                
               for rect in buttonRects: 
                  if rect.collidepoint(pos): 
                     index = buttonRects.index (rect)
                     selection = buttons[index]
      print ( 'Got selection: ' + selection )
      surface.fill ((0,0,0))

if __name__ == '__main__':     
   # os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
   pygame.init()
   window = pygame.display.set_mode((800, 600))
   print ( 'window.topleft: ' + str(window.get_rect()) )
   pygame.display.update()
   view = ViewImage ('images/mtg/creatures/alGore.jpg')   
   pygame.quit()