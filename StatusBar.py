import pygame
from PIL import Image
import os

# Create a bar at the bottom with buttons that will cause actions 
class StatusBar: 
   def consumeSelection (self):
      self.selection = ''

   def __init__ (self, x=40):
      self.surface = pygame.display.get_surface()   
      surfaceRect = self.surface.get_rect()      
      print ( 'Surface info: ' + str(self.surface.get_rect()) ) 
      height = self.surface.get_rect()[3]
      self.y = height - 30
      self.x = x       
      self.selection = ''
      
   def show (self, buttons):
      x = self.x
      y = self.y
      font = pygame.font.SysFont(None, 30)
      self.buttons = buttons
      
      self.buttonRects = [] 
      for buttonText in buttons: 
         buttonSurf     = font.render (buttonText, True, (0,255,0)) # Color is final argument 
         width          = buttonSurf.get_width()
         height         = buttonSurf.get_height()
         buttonTextRect = pygame.Rect ( x, y, width, height) 
         self.buttonRects.append (buttonTextRect)
         borderRect     = pygame.Rect ( x-5, y-5, width+10, height+10 )  
         self.surface.blit ( buttonSurf, buttonTextRect)
         pygame.draw.rect ( self.surface, (255,0,0), borderRect, width=1 )      
         x = x + width + 20 # Next button 
      pygame.display.flip()
         
   def update (self, mousePosition): 
      print ( 'Got pos: ' + str(mousePosition))                
      for rect in self.buttonRects: 
         if rect.collidepoint(mousePosition): 
            index = self.buttonRects.index (rect)
            self.selection = self.buttons[index]
            break
      
      if self.selection != '':       
         print ( 'Got selection: ' + self.selection )


if __name__ == '__main__':
   # os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
   pygame.init()
   window = pygame.display.set_mode((800, 600))
   print ( 'window.topleft: ' + str(window.get_rect()) )
   # pygame.display.update()
   bar = StatusBar ()
   bar.show (['ok', 'cancel'] )
   
   while (bar.selection == ''):
      pygame.time.Clock().tick(60)
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()    
            bar.update (pos)   
     
   pygame.quit()