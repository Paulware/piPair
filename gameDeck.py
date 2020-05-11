import random
import copy
import cardDatabase

# Make one of these for you and one for your opponent
class gameDeck: 
   
   def __init__(self, indexes):
      self.gameDeck = {} #instance variable
      self.db = cardDatabase.cardDatabase () 
      count = 0
      for index in indexes:
         info = self.oneRecord(index)
         info['index'] = count
         self.gameDeck[count] = info
         count = count + 1
            
   def oneRecord (self,index): 
      filename = self.db.indexToFilename(index)
      info = self.db.data[filename]
      # Add in fields that change during the game such as summoned or tapped
      data = { 'filename':filename,'power':info['power'], 'toughness':info['toughness'], \
               'toCast':info['toCast'], 'tapped':False, 'location':'library', 'affects':'', \
               'haste':info['haste'], 'summoned':False, 'blocking':False}

      return data                  

   # list of filenames only    
   def cardList(self): 
      list = []
      if len(self.gameDeck) == 0:
         print ("Err, cardDeck.cardList, gameDeck is []" )
      else:
         for card in self.gameDeck:
            info = self.gameDeck[card]
            filename = info['filename']
            list.append (filename)
      return list
      
   def showGameDeck (self): 
      message = '\n'
      count = 0
      for card in self.gameDeck:
         info = self.gameDeck[card]
         message = message + str(count) + ':' + str(info) + '\n'
         count = count + 1
      return message
             
   def toFilenames (self,infoList):
      filenames = []
      try: 
         for card in infoList: # card is a number 
            info = self.gameDeck[card]
            filename = info['filename']
            filenames.append (filename)         
      except Exception as ex: 
         assert False, 'gameDeck.toFilenames had trouble: ' + str(ex) + \
                       ' infoList: ' + str(infoList) + ' gameDeck: ' + showGameDeck()            
      return filenames
         
   # Return a subset of the gameDeck 
   def extractLocation (self, location):   
      indexes = [] 
      count = 0
      for card in self.gameDeck: # card is a number 
         info = self.gameDeck[card]
         if info['location'] == location: 
            index = info['index']
            indexes.append (index) # list of indexes 
            count = count + 1
      #print ( 'extractLocation len(indexes): ' + str(len(indexes)) + ', len(data): ' + str(len(data)) ) 
      return indexes
      
   def toDbIndexes (self): 
      indexList = [] 
      for card in self.gameDeck: 
         info = self.gameDeck[card]
         filename = info['filename']
         index = self.db.filenameToIndex (filename)
         indexList.append (index)
      return indexList
              
   def getRandomItem (self,list):
      item = None
      #print ( 'getRandomItem from list of length: ' + str(len(list))) 
      assert len(list) > 0, 'Cannot get random item, list is empty' 
      #print ( 'getRandomItem, list has (' + str(len(list)) + ' elements' )
      num = int ( random.random() * len(list))
      item = list[num]
      assert item != None, 'getRandomItem returning None'
      # print ( 'Got randomitem: ' + str(item) )
      return item

   # ['location'] = 'inhand'         
   def drawCard (self): 
      info = None
      assert len(self.gameDeck) > 0, "drawCard list is empty" 
      indexes = self.extractLocation ('library')
      print ( 'There are ' + str(len(indexes)) + ' cards in the library ' )
      assert len(indexes) > 0, 'Why is library list empty? Big list:' + str(list) 
      card = self.getRandomItem (indexes)
      self.gameDeck[card]['location'] = 'inhand'
      info = self.gameDeck[card]
      print ( 'drawCard placed this card in hand: ' + str (info) )
      return info
    
   def tappedList(self): 
      indexes = self.extractLocation ( 'inplay' )
      tapped = []
      for index in indexes: 
         tapped.append (self.gameDeck[index]['tapped'])
      return tapped 
    
   def dealtHand (self,hand):  
      print ( 'Opponent was dealt this hand: ' + str(hand))    
      for index in hand: 
         self.gameDeck[index]['location'] = 'inhand'

   def dealHand (self):
      print ( 'dealHand ')
      infoList = []
      assert len(self.gameDeck) > 0, 'Cannot deal a hand from an empty list'
      indexes = []
      for i in range(7):
         info = self.drawCard ()
         index = info['index']
         indexes.append (index)
         self.gameDeck[index]['location'] = 'inhand'
         
      loopbackIndexes = self.extractLocation ('inhand') 
      print ( 'There are now: ' + str(len(loopbackIndexes)) + ' cards in hand yo' )
      print ( str (loopbackIndexes) ) 
      return indexes
                  
if __name__ == '__main__':
    try:
       deck = gameDeck([0,5,6,10,11,12,13,15])
       # print ( 'cardList: ' + str(deck.cardList() )  )
       deck.db.buildDeck('images/mtg/creatures/hulk.png') # Set the gameDeck
       print ( 'buildDeck: ' + str (deck.gameDeck) ) 
       print 
       deck.dealHand ()
       indexes = deck.extractLocation ( 'inhand' )
       print ( 'I was dealt this hand: ' + str (indexes ) )
       filenames = deck.cardList()
       print ( 'Filenames: ' + str(filenames) ) 
    except Exception as ex:
       print ( "Got exception: " + str(ex)) 
    finally:
       print ( 'finally ' )