from TextBox import TextBox

class Labels: 
   
   def __init__ (self): 
      self.labels = [] 
      
   def addLabel (self,text,x,y): 
      self.labels.append ( TextBox (text,x,y) )

   def draw (self):
      self.show()   
      
   def show (self):
      for label in self.labels: 
         label.draw()
         

         
      
   