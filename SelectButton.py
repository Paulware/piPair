import pygame

class SelectButton: 
   def __init__ (self, borderText =''):
      self.borderText = borderText
      
   def go (self, x, y, message, buttons):
      font = pygame.font.SysFont(None, 30)
      
      text_surf = font.render(message, True, (255, 0, 0))
      width = text_surf.get_width()
      height = text_surf.get_height()
      #Get rectangle for the total window 
      rectangle = pygame.Rect(x+20, y+20, width+20, height+20)   
      
      borderRectangle = pygame.Rect (x,y,width+30,height+30)
      if self.borderText != '': 
         borderText = font.render(self.borderText, True, (255, 0, 0))                  
         borderTextRectangle = pygame.Rect (x+10,y-10,borderText.get_width(),borderText.get_height())
                     
      window = pygame.display.get_surface()
      clock = pygame.time.Clock()
      window.fill((100,100,100), borderRectangle)
      # Draw the border 
      pygame.draw.rect ( window, (255,0,0), borderRectangle, width=1 )
      
      if self.borderText != '': # Draw the border text
         window.fill((50,50,50),borderTextRectangle)
         window.blit(borderText, borderTextRectangle)
      # Draw the message 
      window.blit(text_surf, rectangle)
      
      # Draw Ok message 
      x = 10
      y = y+90
      buttonRects = [] 
      for buttonText in buttons: 
         buttonSurf     = font.render (buttonText, True, (0,255,0)) # Color is final argument 
         width          = buttonSurf.get_width()
         height         = buttonSurf.get_height()
         buttonTextRect = pygame.Rect ( x, y, width, height) 
         buttonRects.append (buttonTextRect)
         borderRect     = pygame.Rect ( x-5, y-5, width+10, height+10 )  
         window.blit ( buttonSurf, buttonTextRect)
         pygame.draw.rect ( window, (255,0,0), borderRect, width=1 )      
         pygame.display.flip()
         x = x + width + 20 # Next button 
      
      # Wait for user to click or press a key 
      run = True 
      selection = ''      
      while selection == '':
         clock.tick(60)
         for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
               pos = pygame.mouse.get_pos()        
               for rect in buttonRects: 
                  if rect.collidepoint(pos): 
                     index = buttonRects.index (rect)
                     selection = buttons[index]
      return selection 

if __name__ == '__main__':     
   pygame.init()
   window = pygame.display.set_mode((500, 200))
   buttons = ['ok', 'cancel', 'red', 'blue']
   select = SelectButton ('   Warning   ').go(100,50,'This application is done', buttons)
   print ( 'Got a selection: ' + select )
   pygame.quit()
   exit()