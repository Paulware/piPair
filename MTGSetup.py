import pygame
from CheckBox import CheckBox

# Select the colors for the deck you wish to play with  
class MTGSetup: 
   def __init__ (self): 
      self.boxes = [] 
      self.boxes.append (CheckBox ('Red',   100, 100))
      self.boxes.append (CheckBox ('Blue',  100, 150))
      self.boxes.append (CheckBox ('Black', 100, 200))
      self.boxes.append (CheckBox ('White', 100, 250))
      self.boxes.append (CheckBox ('Green', 100, 300))
      
   def draw (self):
      for box in self.boxes: 
         box.draw()
         
   def update(self,pos):
      for box in self.boxes:
         box.update(pos)
      
if __name__ == '__main__': 
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((800, 600))
   utilities = Utilities (window, BIGFONT)    
   setup = MTGSetup()
   
   while True:
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      setup.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            setup.update (data) 
      
      #if check.toChecked(): 
      #   print ( 'It was just checked' )      
   pygame.quit()