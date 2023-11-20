from images.mtg.Counter       import Counter
class DamageCounter (Counter):
   def __init__ (self):
      x = 10
      y = 100
      title = 'Damage Count'
      print ( 'Create a Damage counter' )   
      self.value = 0
      super().__init__(x,y,title)       
      
   def addDamage (self,damage):
      for i in range(damage):
         self.increment()
      
