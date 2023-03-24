import pygame
from Prompt import Prompt

class InputBox():
   def __init__(self, prompt, x=40, y=40 ): 
      self.window          = pygame.display.get_surface()   
      self.color           = (150, 150, 150)
      self.highlight_color = (100, 200, 255)
      self.font            = pygame.font.SysFont(None, 30)
      self.prompt          = prompt         
      self.x               = x
      self.y               = y
      self.value           = ''
      promptWidth,promptHeight = self.font.size(self.prompt)
      self.width = promptWidth
      self.height = promptHeight
      self.promptRect = pygame.Rect(x, y, promptWidth, promptHeight)
      self.valueRect  = pygame.Rect(x+promptWidth, y, 150, promptHeight)

   def draw(self):
      msg = self.font.render(self.prompt, 1, (255, 0, 0))
      self.window.blit(msg, self.promptRect)
      x = self.valueRect [0]
      y = self.valueRect [1]         
      if self.value == '': 
         self.valueRect  = pygame.Rect(x, y, 150, self.height)
      else: 
         msg = self.font.render (self.value, 1, (255,0,0)) 
         valueWidth,valueHeight = self.font.size(self.value)
         self.valueRect = pygame.Rect(x, y, valueWidth, valueHeight)
         self.window.blit(msg, self.valueRect)          
                           
      pygame.draw.rect (self.window, (255,0,0), self.valueRect, width=1)       
        
   def update (self, pos):
      if self.valueRect.collidepoint (pos): 
         print ( 'Call prompt' )
         self.value = Prompt ().go(100,50,'Please enter your value') 
         
if __name__ == '__main__':
   from Utilities import Utilities
   pygame.init()
   window = pygame.display.set_mode((640, 480))
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities (window, BIGFONT)    
   
   inputBox = InputBox ( 'Name:' ) 

   pygame.display.flip()
   run = True
   while run:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      inputBox.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            inputBox.update (data)         
   pygame.quit()
