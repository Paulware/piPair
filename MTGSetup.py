import pygame 
from CheckBox import CheckBox
from InputBox import InputBox
from Button   import Button
import pygame_widgets
from pygame_widgets import slider
from TextBox import TextBox
from images.mtg.ManaCost import ManaCost 
from MessageBox import MessageBox
from Globals import *

# Select the colors for the deck you wish to play with  
class MTGSetup: 
   def createSetupPage (self): 
      self.red = CheckBox   ('Red', 100, 100)
      self.items.append     (self.red)
      self.blue = CheckBox  ('Blue',  100, 150)
      self.items.append     (self.blue)
      self.black = CheckBox ('Black', 100, 200)
      self.items.append     (self.black)      
      self.white = CheckBox ('White', 100, 250)
      self.items.append     (self.white)
      self.green = CheckBox ('Green', 100, 300)
      self.items.append     (self.green)
      
      self.card1 = InputBox   ( 'Enter Card1: ', 100, 400 )
      self.items.append       (self.card1)
      self.card2 = InputBox   ( 'Enter Card2: ', 100, 430 )      
      self.items.append       (self.card2)
      self.card3 = InputBox   ( 'Enter Card3: ', 100, 460 )      
      self.items.append       (self.card3) 
      self.deckFilename   =   InputBox ( 'Filename of deck: ', 100, 490 )
      self.items.append       (self.deckFilename) 
      self.deckFilename.value = 'deck.txt'      
      
      self.textbox = TextBox   ( 'Complexity', 740, 375 )
      self.numLands = InputBox ( 'Number of Lands: '    , 400, 400, '20' )
      self.items.append        (self.numLands)
      
      self.numCreatures = InputBox ( 'Number of Creatures: ', 400, 430, '20' )
      self.items.append            (self.numCreatures)
      self.creatureComplexity      = slider.Slider (self.window, 700, 430, 200, 20, min=0, max=99, step=1, handleColour=(0,255,255))
      
      self.numArtifacts = InputBox ( 'Number of artifacts: ', 400, 460, '5' )
      self.items.append            (self.numArtifacts)
      self.artifactComplexity      = slider.Slider (self.window, 700, 460, 200, 20, min=0, max=99, step=1, handleColour=(0,255,255))
      
      self.numSorceries = InputBox ( 'Number of sorceries: ', 400, 490, '5' )
      self.items.append            (self.numSorceries)
      self.sorceryComplexity       = slider.Slider (self.window, 700, 490, 200, 20, min=0, max=99, step=1, handleColour=(0,255,255))
      
      self.numInstants = InputBox ( 'Number of instants: ' , 400, 520, '5' )
      self.items.append           (self.numInstants)
      self.instantComplexity      = slider.Slider (self.window, 700, 520, 200, 20, min=0, max=99, step=1, handleColour=(0,255,255))
      
      self.numEnchantments = InputBox ( 'Number of enchantments: ' , 400, 550, '5' )
      self.items.append               (self.numEnchantments)
      self.enchantmentComplexity      = slider.Slider (self.window, 700, 550, 200, 20, min=0, max=99, step=1, handleColour=(0,255,255))
      
      self.quitButton   = Button  ( 'Done', 100, 580 )       
      self.createButton = Button  ( 'Create Deck', 200, 580 )
      
      self.items.append (self.quitButton)  
      self.items.append (self.createButton)
      
   def __init__ (self):    
      self.manaCost = ManaCost()
      self.items = []       
      self.deck = [] 
      self.window = pygame.display.get_surface()
      
   def draw (self):
      for item in self.items: 
         item.draw()
      self.textbox.draw()
         
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
      mana = self.totalSelectedMana()
      # Minimum complexity = 1, maximum = 6
      complexity = ( self.creatureComplexity.value / 20) + 1 
      creatures = self.manaCost.matchCards ( mana , complexity, self.numCreatures.getNumber(), 'creatures' )

      complexity = ( self.artifactComplexity.value / 20) + 1 
      artifacts = self.manaCost.matchCards ( mana , complexity, self.numArtifacts.getNumber(), 'artifacts' )
      
      complexity = ( self.instantComplexity.value / 20) + 1 
      instants = self.manaCost.matchCards ( mana , complexity, self.numInstants.getNumber(),   'instants' )

      print ( 'Got ' + str(len(instants)) + ' instants matched' )

      complexity = ( self.sorceryComplexity.value / 20) + 1 
      print ( 'sorcery complexity: ' + str(complexity))       
      sorceries = self.manaCost.matchCards ( mana , complexity, self.numSorceries.getNumber(),  'sorcery' )
      
      lands = self.manaCost.matchCards (mana, 5, 20, 'lands' )
      
      complexity = ( self.enchantmentComplexity.value / 20) + 1 
      print ( 'enchantment complexity: ' + str(complexity))       
      enchantments = self.manaCost.matchCards ( mana , complexity, self.numEnchantments.getNumber(),  'enchantments' )
      
      self.deck = creatures + artifacts + instants + sorceries + lands + enchantments
      
      if self.card1.value != '':
         for i in range (4):
            self.deck.append (self.card1.value) 
            
      if self.card2.value != '':
         for i in range (4):
            self.deck.append (self.card2.value)  
            
      if self.card3.value != '':
         for i in range (4):
            self.deck.append (self.card3.value)  

      print ( 'deck created with ' + str(len(self.deck)) + ' cards ' )
      f = open ('images/mtg/' + self.deckFilename.value, 'w' )
      msg = ''
      for card in self.deck: 
         if msg != '':
            msg = msg + ','
         msg = msg + str(card) 
      f.write (msg) 
      f.close()
      print ( self.deckFilename.value + ' written' )
      

   def totalSelectedMana (self): # return man for the user selection (all quantities = 1)
      mana = {} 
      if self.red.checked: 
         mana ['red'] = 1
      if self.green.checked:
         mana ['green'] = 1
      if self.black.checked:
         mana ['black'] = 1
      if self.white.checked:
         mana ['white'] = 1 
      if self.blue.checked:
         mana ['blue'] = 1
      
      print ( 'totalSelectedMana: ' + str(mana) )
      
      return mana
      
   def showDeck (self): 
      print ( str(len(self.deck)) + ' cards in this deck: ' )
      count = 0 
      for card in self.deck: 
         count = count + 1 
         info = self.manaCost.idToInfo (card) 
         print ( str(count) + ':' + str(info)) 
    
   def mainPage (self):
      window = self.window 
      setup.createSetupPage ()
      text = ''      
      typeInput = ''
      while (text == '') and (typeInput != 'quit'):
         pygame.time.Clock().tick(60)   
         window.fill ((0,0,0)) 
         self.draw()
         
         events = globalDictionary['utilities'].readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'drop': 
               self.update (data) 
            elif typeInput == 'quit':
               break         
            
         text = self.quitButton.isPressed()      
         if self.createButton.isPressed(): 
            self.createDeck()
            setup.showDeck()

         pygame_widgets.update (events)
         pygame.display.update()
      # WidgetHandler.removeWidget(self.enchantmentComplexity)
      
   def chooseDeckFilename (self, defaultFilename='deck.txt'): 
      window = self.window 
      # Create the choose deck page 
      self.items = [] 
      self.deckFilename       =   InputBox ( 'Filename of deck: ', 100, 190 )
      self.deckFilename.value = defaultFilename
      self.items.append       (self.deckFilename) 
     
      self.quitButton   = Button  ( 'Done',  100, 290 )             
      self.items.append (self.quitButton)  

      self.selectButton   = Button  ( 'Select',  300, 290 )             
      self.items.append (self.selectButton)  

      text      = ''      
      typeInput = ''
      filename  = ''
      while (text == '') and (typeInput != 'quit'):
         pygame.time.Clock().tick(60)   
         window.fill ((0,0,0)) 
         for item in self.items: 
            item.draw()
         
         events = globalDictionary['utilities'].readOne()
         for event in events:
            (typeInput,data,addr) = event
            if typeInput == 'drop': 
               self.update (data) 
            elif typeInput == 'quit':               
               break         
            
         text = self.quitButton.isPressed()      
         
         if self.selectButton.isPressed() != '':  
            filename = 'images/mtg/' + self.deckFilename.value
            if not globalDictionary['utilities'].fileExists (filename): 
               MessageBox ('   Warning   ').go(100,50,filename + ' does not exist' )
            else:
               break

         pygame.display.update()
         
      return filename
     
if __name__ == '__main__': 
   from Utilities import Utilities    
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   window = pygame.display.set_mode((1000, 600))

   setup = MTGSetup()
   setup.mainPage  ()   

   filename = setup.chooseDeckFilename ()
   if filename == '': 
      print ( 'No file was selected' )
   else:
      print ( 'This file exists and was selected filename: [' + filename + ']')  
   pygame.quit()