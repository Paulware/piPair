from TextBox import TextBox

class Labels: 
   def addLabel (self,text,x,y): 
      self.labels.append ( TextBox (text,x,y) )
   
   def __init__ (self): 
      self.labels = [] 
      
   def show (self):
      for label in self.labels: 
         label.draw()
         
         

         
      
   