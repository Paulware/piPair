import pygame 
class CheckBox: 
   def __init__ (self, text, x=100, y=100, width=30, height=30): 
      self.surface = pygame.display.get_surface()
      self.font = pygame.font.SysFont(None, 30)
      self.text = text   
      self.rect = pygame.Rect ( x-5, y-5, width+10, height+10 ) 
      self.width = width
      self.y = y
      self.x = x
      self.height = height
      self.checked = False 
      self.transitioned = False 
      self.draw() 
      
   # Check if the checkbox has been clicked    
   def update(self,pos): 
      print ( 'update check position: ' + str (pos) + ' compare to rect: ' + str(self.rect) ) 
      if self.rect.collidepoint (pos): 
         print ( 'Got collision...' )
         if not self.checked: 
            print ( 'Got transitioned' )
            self.transitioned = True 
            
         self.checked = not self.checked
             
   def draw (self):
      color = (255,0,0) # red 
      pygame.draw.rect (self.surface, color, self.rect, width=1)       
      msg = self.font.render(self.text, 1, (0, 255, 0))
      msgWidth,msgHeight = self.font.size(self.text)
      msgRect = pygame.Rect ( self.x+self.width+10, self.y, msgWidth, msgHeight ) 
      self.surface.blit(msg, msgRect) 
      if self.checked: 
         x1 = self.rect[0]
         y1 = self.rect[1]
         x2 = self.rect[0] + self.width + 10
         y2 = self.rect[1] + self.height + 10
         
         # Upper left to lower right 
         pygame.draw.line(self.surface, color, (x1,y1), (x2,y2) )

         swapY = y1
         y1 = y2
         y2 = swapY
         
         # Lower left to upper right 
         pygame.draw.line(self.surface, color, (x1,y1), (x2,y2) )
         
   def toChecked(self): 
      transitioned = self.transitioned
      self.transitioned = False 
      return transitioned
      
if __name__ == '__main__': 
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((800, 600))
   utilities = Utilities (window, BIGFONT)    
   check = CheckBox ( 'Hello' )
   
   while True:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      check.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            check.update (data) 
      

      if check.toChecked(): 
         print ( 'It was just checked' )      
   pygame.quit()