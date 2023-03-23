from Button import Button

class Buttons: 
   def add (self,text,x,y): 
      self.buttons.append ( Button (text,x,y) )
   
   def __init__ (self): 
      self.buttons = [] 
      
   def draw (self):
      for button in self.buttons: 
         button.draw()
         
   def update(self,pos):
      for button in self.buttons:
         button.update(pos)
         
   def isPressed (self):
      text = ''
      for button in self.buttons:
         text = button.isPressed()
         if text != '': 
            break
      return text
         
if __name__ == '__main__': 
   import pygame         
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((800, 600))
   utilities = Utilities (window, BIGFONT)    
   
   buttons = Buttons()
   buttons.add ('Hello', 100, 100)
   buttons.add ('Quit', 200,200)

   text = ''   
   while text != 'Quit':
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      buttons.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            buttons.update (data) 
      
      text = buttons.isPressed()
      if text != '': 
         print ( text + ' was just pressed' )      
   pygame.quit()         
         

         
      
   