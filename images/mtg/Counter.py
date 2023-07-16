from TextBox import TextBox

class Counter: 
   def __init__ (self, x, y): 
      self.count = 0
      self.x = x
      self.y = y
      self.label = TextBox (str(self.count), x, y)

   def draw (self):
      self.label.draw()   
      
   def increment (self):
      self.count = self.count + 1
      self.label.clearLast ()
      
      self.label = TextBox (str(self.count), self.x, self.y)
      print ( 'counter incremented to: ' + str(self.count))
      self.draw()
      
