import pygame

class Button: 
   def __init__ (self, text, x, y):
      self.surface = pygame.display.get_surface()
      self.text    = text
      self.font    = pygame.font.SysFont(None, 30)
      text_surf    = self.font.render(text, True, (255, 0, 0))
      self.width   = text_surf.get_width() + 3
      self.height  = text_surf.get_height()
      self.x       = x
      self.y       = y
      #Get rectangle for the total window 
      self.rect    = pygame.Rect(self.x, self.y, self.width, self.height)   
      self.pressed = False
      self.draw ()  

   def draw (self): 
      color = (255,0,0) # Red 
      pygame.draw.rect (self.surface, color, self.rect, width = 1)
      textRect = self.rect.move ((1,1))
      msg = self.font.render (self.text, 1, (0, 255, 0)) # Green 
      self.surface.blit (msg, textRect) 
      
   def isPressed(self): 
      text = ''
      if self.pressed: 
         text = self.text
      self.pressed = False 
      return text
   
   # Check if the button has been pressed   
   def update(self,pos): 
      print ( 'update check position: ' + str (pos) + ' compare to rect: ' + str(self.rect) ) 
      if self.rect.collidepoint (pos): 
         print ( 'Got collision...' )
         if not self.pressed: 
            print ( 'Got transitioned' )
            self.pressed = True 
                

if __name__ == '__main__':     
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((800, 600))
   utilities = Utilities (window, BIGFONT)    
   button = Button ( 'Hello', 100, 100 )
   
   while True:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      button.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            button.update (data) 
      
      text = button.isPressed()
      if text != '': 
         print ( text + ' was just pressed' )      
   pygame.quit()