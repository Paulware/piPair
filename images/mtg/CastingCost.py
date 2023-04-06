class CastingCost: 

   def __init__ (self):
      self.dict = {'swamp': 'b', 'island': 'l'}
      
   def count (self,name,target): 
      total = 0 
      value = self.dict[name]
      for i in range(len(value)): 
         ch = value[i:i+1]
         if ch == target: 
            total = total + 1
         else:
            print ( '[' + ch + '] != ' + target) 
      return total 
      
   def numBlacks (self,name):
      return self.count (name,'b')
      
if __name__ == '__main__':
   casting = CastingCost()
   print ( 'Number of blacks in a swamp: ' + str(casting.numBlacks ( 'swamp' ) ) ) 
  