from TextBox import TextBox

class Counter: 
   def __init__ (self, x, y): 
      self.count = 0
      self.label = TextBox (str(self.count), x, y)
      self.x = x 
      self.y = y

   def draw (self):
      self.label.draw()   
      
   def move (self,x,y):
      print ( 'Move Counter from  to: [' + str(x) + ',' + str(y) + ']' )
      self.x = x
      self.y = y
      self.label.move (x,y)     
      
   def increment (self):
      self.count = self.count + 1      
      self.label = TextBox (str(self.count), self.x, self.y)
      print ( 'counter incremented to: ' + str(self.count))
      self.draw()
      
