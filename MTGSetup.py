import pygame 
from CheckBox import CheckBox
from InputBox import InputBox
from Button   import Button

# Select the colors for the deck you wish to play with  
class MTGSetup: 
   def __init__ (self): 
      self.items = [] 
      self.items.append (CheckBox ('Red',   100, 100))
      self.items.append (CheckBox ('Blue',  100, 150))
      self.items.append (CheckBox ('Black', 100, 200))
      self.items.append (CheckBox ('White', 100, 250))
      self.items.append (CheckBox ('Green', 100, 300))
      
      self.items.append (InputBox ( 'Enter Card1: ', 100, 400, 'psilocybin' ) ) 
      self.items.append (InputBox ( 'Enter Card2: ', 100, 430, 'DMT' ) )       
      self.items.append (InputBox ( 'Enter Card3: ', 100, 460 ) ) 
      self.items.append (InputBox ( 'Enter Card4: ', 100, 490 ) )       
      
      self.items.append (InputBox ( 'Number of Lands: '    , 400, 400, '20' ) )
      self.items.append (InputBox ( 'Number of Creatures: ', 400, 430, '20' ) )
      self.items.append (InputBox ( 'Number of artifacts: ', 400, 460, '5' ) )
      self.items.append (InputBox ( 'Number of sorceries: ', 400, 490, '5' ) )
      self.items.append (InputBox ( 'Number of instants: ' , 400, 520, '5' ) )
      
      self.quitButton   = Button ( 'Done', 100, 550 )       
      self.createButton = Button ( 'Create Deck', 200, 550 )
      
      self.items.append (self.quitButton)  
      self.items.append (self.createButton)
      
   def draw (self):
      for item in self.items: 
         item.draw()
         
   def update(self,pos):
      for item in self.items:
         item.update(pos)
         
   def getValue (self,text,intValue=False):
      value = ''
      for item in self.items:
         if hasattr ( item, 'getValue' ): 
            value = item.getValue(text)
            if value != '': 
               break
               
      if intValue:
         try:       
            value = int(value)
         except Exception as ex:
            value = 0
            
      return value
      
   def createDeck (self): 
      print ('Create the deck')
      artifacts = setup.getValue ('artifacts', True)
      if artifacts != '': 
         print ('Artifacts: ' + str(artifacts))
         
      lands = setup.getValue ( 'Lands', True )
      for I in range(lands):
         print ( 'Find a land in the deck that matches the colors' ) 
         break         
      
if __name__ == '__main__': 
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((800, 600))
   utilities = Utilities (window, BIGFONT)    
   setup = MTGSetup()

   text = ''      
   while text == '':
      pygame.time.Clock().tick(60)   
      window.fill ((0,0,0)) 
      setup.draw()
      pygame.display.update() 
      
      events = utilities.readOne()
      for event in events:
         (typeInput,data,addr) = event
         if typeInput == 'drop': 
            setup.update (data) 
      
      text = setup.quitButton.isPressed()      
      if setup.createButton.isPressed(): 
         setup.createDeck()
                        
   pygame.quit()