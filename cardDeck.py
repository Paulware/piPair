import random
import copy
import cardDatabase 

class cardDeck: 

   gameDeck = {}
   
   def __init__(self, host):
      self.db = cardDatabase.cardDatabase () 
      self.host = host  

   def dbList (self):
      return self.db.cardList()   
    
   # list of filenames only    
   def filenameList(self): 
      list = []
      for filename in self.db.data:
         list.append (filename)
      return list   
       
   # list of filenames only    
   def gameFilenameList(self): 
      list = []
      if len(self.gameDeck) == 0: 
         print ("Err, cardDeck.gameFilenameList, gameDeck is []" )
      else: 
         for card in self.gameDeck:
            info = self.gameDeck[card]
            filename = info['filename']
            list.append (filename)
      return list   
             
   # dbList with extra info (such as 'location', 'tapped'      
   def dbCardList (self): 
      list = {}
      count = 0
      for filename in self.db.data:
         info = {} 
         info['filename'] = filename 
         info['tapped'] = False
         info['location'] = 'library'
         info['index'] = count
         list[count] = info
         count = count + 1
      return list  
   
   def extractLocation (self, location):   
      indexes = [] 
      data = {} 
      count = 0
      # print ( 'extractLocation, len(list): ' + str(len(self.list)) + ', location: ' + location )
      for card in self.list: # card is a number 
         info = self.list[card]
         if info['location'] != location: 
            pass # print ( 'extractLocation, (info[location] != location): ([' +  info['location'] + ']!= [' + location + '])')
         else:
            index = info['index']
            indexes.append (index) # list of indexes 
            data[count] = info            
            count = count + 1
     
      #print ( 'extractLocation len(indexes): ' + str(len(indexes)) + ', len(data): ' + str(len(data)) ) 
      return indexes,data
      
   def toFilenames (self,infoList):
      filenames = []
      for card in infoList: # card is a number 
         info = infoList[card]
         filename = info['filename']
         filenames.append (filename)         
      return filenames
         
   # Return a subset of the gameDeck 
   def extractGameLocation (self, location):   
      indexes = [] 
      data = {} 
      count = 0
      for card in self.gameDeck: # card is a number 
         info = self.gameDeck[card]
         if info['location'] != location: 
            pass # print ( 'extractLocation, (info[location] != location): ([' +  info['location'] + ']!= [' + location + '])')
         else:
            index = info['index']
            indexes.append (index) # list of indexes 
            data[count] = info            
            count = count + 1
      #print ( 'extractGameLocation len(indexes): ' + str(len(indexes)) + ', len(data): ' + str(len(data)) ) 
      return indexes,data    
      
   def defaultRecord (self,filename):
      info = {'host':False,'filename':filename,'power':0,'toughness':0, \
              'toCast':0,'tapped':False,'location':'library','affects':''}
      return info      
      
   def oneRecord (self,filename): 
      info = self.db.data [filename]
      data = { 'filename':filename,'power':info['power'], 'toughness':info['toughness'], \
               'toCast':info['toCast'], 'tapped':False, 'location':'library', 'affects':'', \
               'host':False}
      return data      

   def toDbIndexes (self): 
      indexList = [] 
      for card in self.gameDeck: 
         info = self.gameDeck[card]
         filename = info['filename']
         index = self.db.filenameToIndex (filename)
         indexList.append (index)
      return indexList
              
   def buildDeck (self,filename): 
      self.gameDeck = {}
      creatures = self.db.matchingCards (filename)
      colors = self.db.baseCost(filename)
      maxCreatures = 30
      print ( 'len(creatures): ' + str(len(creatures)) )
      count = 0
      while len(self.gameDeck) < maxCreatures: 
         index = count % len(creatures)
         creature = creatures [index]
         aRecord = self.oneRecord (creature)
         aRecord['index'] = count  
         self.gameDeck[count] = aRecord 
         filename = str(aRecord['filename'])
         if str.isnumeric (filename): 
            assert False, 'buildDeck, aRecord bad filename value: ' + filename 
         # For each creature 
         count = count + 1
            
      # Add Lands      
      maxLands = 20 
      while len (self.gameDeck) < (maxCreatures + maxLands):
         for color in colors: 
            land = 'images/mtg/lands/' + color + '.jpg'
            self.gameDeck[count] = self.defaultRecord (land)
            self.gameDeck[count]['index'] = count
            filename = str(self.gameDeck[count]['filename'])
            if str.isnumeric (filename): 
               assert False, 'buildDeck, land, bad filename value: ' + filename             
            
            count = count + 1
            if count == (maxCreatures + maxLands): 
               break
               
      # TODO: Add instants/sorceries/artifacts               
      filename = str(self.gameDeck[0]['filename'])
      if str.isnumeric (filename): 
         assert False, 'buildDeck, gameDeck[0][filename], bad filename value: ' + filename   
         
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
   def dealCard (self): 
      info = None
      assert len(self.gameDeck) > 0, "dealCard list is empty" 
      indexes,infoList = self.extractGameLocation ('library')
      assert len(infoList) > 0, 'Why is library list empty? Big list:' + str(list) 
      info = self.getRandomItem (infoList)
      card = info['index']
      self.gameDeck[card]['location'] = 'inhand'
      # print ( 'dealCard got card: ' + str (info) )
      return info

   def dealHand (self):
      print ( 'dealHand host:' + str(self.host))
      infoList = []
      assert len(self.gameDeck) > 0, 'Cannot deal a hand from an empty list'
      indexes = []
      for i in range(7):
         info = self.dealCard ()
         index = info['index']
         indexes.append (index)
         self.gameDeck[index]['location'] = 'inhand'
      return indexes
                  
   '''           
   def allCards(self): # Used to select card for basis of deck
      cards = []
      indexes = []
      count = 0      
      for key in self.cost:
         power = self.cost[key]['power']
         toughness = self.cost[key]['toughness']
         cards.append ( {'index':count,'iOwnIt':True, 'filename':key, \
                         'location':'library', 'tapped':False, \
                         'summoned':False, 'power':power, \
                         'toughness':toughness} )
         indexes.append (count)
         count = count + 1
      return (cards,indexes)
                 
      
   def getIndex ( self, filename ): 
      count = 0
      found = False 
      for card in self.cost: 
         if card == filename: 
            found = True
            break
         count = count + 1
      print ( 'filename: ' + str(filename) )
      assert found, 'getIndex could not find filename: ' + str(filename) 
      return count
      
   def indexToFilename ( self, index ):
      count = 0
      filename = ''
      for card in self.cost: 
         if count == index:
            filename = card
            break
         count = count + 1
      assert filename != '', 'indexToFilename could not find index: ' + str(index) 
      return filename
   
   def buildDecksMessage (self,allDecks): 
      message = '['
      for card in allDecks: 
         info = allDecks[card]
         index = info['index']
         if message != '[': 
            message = message + ','
         message = message + str(index)
      message = message + ']'
      print ( 'buildDecksMessage created the message: [' + message + ']' )
      return message
      
   def validateAllDecks (self,deck): 
      assert len(deck) > 0, 'Err built an empty deck'      
      
      try: 
         affects = deck[0]['affects']
      except Exception as ex:
         assert False, 'After building decks, allDecks[0][affects] does not exist yo'
         
      filename = str(deck[0]['filename'])
      if str.isnumeric(filename):
         assert False, 'After building decks, allDecks 0 filename is bad: ' + filename
      print ( 'allDecks[0] after buildDecks: ' + str(deck[0]))             
   
      
   def buildDecks (self,hostFilename,opponentFilename):
      allDecks = {}
      # Add host cards
      deck = self.buildDeck (hostFilename)
      count = 0
      for card in deck: 
        info = deck[card]
        filename = info['filename']
        allDecks[count] = {'summoned':False, 'index':info['index'], 'filename':filename, \
                           'affects':'', 'location':'library', 'tapped':False, 'host':True } 
        count = count + 1

      # Add opponent Cards        
      deck = self.buildDeck (opponentFilename)
      for card in deck:
        info = deck[card]
        filename = info['filename']
        allDecks[count] = {'summoned':False, 'index':info['index'], 'filename':filename, \
                           'location':'library', 'tapped':False, 'host':False, 'affects':'' } 
        count = count + 1
      
      self.validateAllDecks (allDecks) 
      return allDecks
      
   def getRandomItem (self,list):
      item = None
      assert len(list) > 0, 'Cannot get random item, list is empty' 
      print ( 'getRandomItem, list has (' + str(len(list)) + ' elements' )
      num = int ( random.random() * len(list))
      item = list[num]
      print (str(list[0])) 
      print ( 'Got randomitem: ' + str(item) )
      assert item != None, 'getRandomItem returning None'
      return item

   def extractLocation (self, list, host, location):
      indexes = [] 
      data = {} 
      count = 0
      print ( 'extractLocation, len(list): ' + str(len(list)) + ', location: ' + location )
      for card in list: 
         info = list[card] # card == count.  TODO: confirm
         if info['location'] != location: 
            pass # print ( 'extractLocation, (info[location] != location): ([' +  info['location'] + ']!= [' + location + '])')
         elif info['host'] != host:
            pass # print ( 'info[host] !=' + str(host)) 
         else:
            index = info['index']
            indexes.append (index) # list of indexes 
            data[count] = info            
            count = count + 1
      print ( 'extractLocation len(indexes): ' + str(len(indexes)) + ', len(data): ' + str(len(data)) ) 
      return indexes,data
      
   # allDecks[index]['location'] = 'inhand'      
   def dealCard (self,list,host): 
      info = None
      assert len(list) > 0, "dealCard list is empty" 
      indexes,infoList = self.extractLocation (list, host, 'library')
      assert len(infoList) > 0, 'Why is library list empty? Big list:' + str(list) 
      info = self.getRandomItem (infoList)
      card = info['index']
      list[card]['location'] = 'inhand'
      print ( 'dealCard got card: ' + str (info) )
      return info
      
'''      
if __name__ == '__main__':
    try:
       deck = cardDeck(False)
       print ( 'rawList: ' + str(deck.dbList() ) )
       # print ( 'cardList: ' + str(deck.cardList() )  )
       deck.buildDeck('images/mtg/creatures/hulk.png') # Set the gameDeck
       print ( 'buildDeck: ' + str (deck.gameDeck) ) 
       print 
       deck.dealHand ()
       indexes, hand = deck.extractGameLocation ( 'inhand' )
       print ( 'I was dealt this hand: ' + str (hand ) )
       filenames = deck.gameFilenameList()
       print ( 'Filenames: ' + str(filenames) ) 
    except Exception as ex:
       print ( "Got exception: " + str(ex)) 
    finally:
       print ( 'finally ' )