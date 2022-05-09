import pygame
#import time
import subprocess
import os
import socket
import select
from TicTacToe import TicTacToe
from Uno import Uno
import platform

'''
   Pages
'''   
class Pages():
   def __init__ (self,displaySurface,utilities,windowsOs): 
       self.displaySurface = displaySurface
       self.utilities = utilities
       self.windowsOs = windowsOs 
       
   # SSID host     
   def hostPage (self,showOnly=False):
       pygame.display.set_caption('Change your host SSID')        
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))    
       (surface, rect) = self.utilities.createLabel ('Enter the name of your host ssid', 50, 20)   
       self.displaySurface.blit(surface, rect)
       (surface, rect) = self.utilities.createLabel ('SSID:', 250, 55)  
       self.displaySurface.blit(surface, rect)
       pygame.display.update()
       (typeInput,ssid,addr) = self.utilities.getInput(300,55)
       pygame.display.set_caption('Hosting SSID: ' + ssid)
       print ( 'ssid: [' + ssid + ']')
       print ( 'modify /etc/dhcpcd.conf' )
       print ( 'Modify /etc/dnsmasq.conf' ) 
       print ( 'Modify /etc/hostapd/hostapd.conf' )
       print ( 'Done in hostPage' )
       
   # Show the list the SSIDS and join an ssid when it is selected
   # Note: reboot may be necessary    
   def joinPage(self,showOnly=False):       
       pygame.display.set_caption('Join an SSID')    
       BLACK = (0,0,0)       
       self.displaySurface.fill((BLACK))
       sprites = self.utilities.showImages (['quit.jpg', 'join.jpg'], [(400,400), (200,200)] )       
       (ssidSurf, ssidRect) = self.utilities.createLabel ('Press Join to show SSIDs', 50, 20)    
       self.displaySurface.blit(ssidSurf, ssidRect)
       pygame.display.update()

       quit = False
       
       ssids = self.utilities.scanForSsids()      
       labels = self.utilities.showSsids(ssids)
       
       sprites = self.utilities.showImages (['quit.jpg'], [(400,400)] )       
       
       quit = False
       while not quit and not showOnly:   
          ev = pygame.event.get()
          for event in ev:   
            # Check if an ssid is clicked on       
            sprite = self.utilities.getSpriteClick (event, labels ) 
            if sprite != -1:           
               print ("Selected label: " + str(sprite))
               quit = True
               # All passwords are the same (ABCD1234)
               #updateWpaSupplicant (ssids[sprite], 'ABCD1234')            
               #os.system ( 'reboot') # reboot the pi4
               #joinSSID (ssids[sprite])
               #mainPage (True)
               return
               
            sprite = self.utilities.getSpriteClick (event, sprites ) 
            if sprite != -1:           
               print ("Selected command: " + str(sprite))
               self.mainPage (True)
               quit = True

   def getKeyOrUdp(self):
     shiftKeys = { '\\':'|', ']':'}', '[':'{', '/':'?', '.':'>', ',':'<', '-':'_', '=':'+', \
                   '`':'~',  '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^', '7':'&', '8':'*', '9':'(', '0':')' }
     key = None
     upperCase = False
     typeInput = ''
     data = ''
     addr = ''
     while data == '':
       ev = pygame.event.get()
       for event in ev:  
          if event.type == pygame.KEYDOWN:
             if (event.key == 303) or (event.key == 304): #shift
                upperCase = True
             else:
                print ( 'Got event.key: ' + str(event.key)) 
                if event.key in range(0x110000): 
                   key = chr(event.key)
                   if upperCase: 
                      if key in shiftKeys.keys():
                         key = shiftKeys[key]
                      else:                     
                         key = key.upper()
                    
                   typeInput = 'key'
                   data=key
                else:
                   print ( 'Do not know what to do with event.key: ' + str(event.key)) 
       if self.comm.isReady():
          print ( 'in getKeyOrUdp, comm is ready' ) 
          data = self.comm.read()
          typeInput = 'mqtt'
          
     return (typeInput,data,addr)
       
       
   def getInput (self, x,y):
     line = ''
     quit = False
     while not quit:
        (typeInput,data,addr) = self.getKeyOrUdp()
        if typeInput == 'key': 
           if data == chr(13):
              quit = True
           else:
              if data == chr(8):
                 print ( "backspace detected")
                 if len(line) > 0:
                    lastCh = line[len(line)-1]
                    x = x - self.utilities.chOffset (lastCh) #Todo need to get lastCh from 
                    self.utilities.showCh (' ', x, y)
                    self.utilities.showCh (' ', x+4, y)
                    self.utilities.showCh (' ', x+8, y)
                    line = line[:len(line)-1] 
              else:
                 line = line + data
                 ch = data
                 self.utilities.showCh (ch, x, y)           
                 x = x + self.utilities.chOffset(ch)
        elif typeInput == 'mqtt':
           line = data
           quit = True
           print ( 'got some mqtt data: ' + data)
        print ( 'Nothing returned' )
           
     print ( "getInput: (typeInput,line,addr): (" + typeInput + ',' + line + ',' + addr + ')')
     return (typeInput,line,addr)         
               
   # Show the chat page
   def chatPage(self,showOnly=False):
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))
       self.utilities.showLabel ('Enter exit to quit', 50, 20)     
       self.utilities.showLabel ('Chat:', 250, 55)
       
       pygame.display.set_caption('Chatting with ' + self.comm.target)        
       pygame.display.update()  

       quit = False
       y = 55

       while not quit and not showOnly:   
          (typeInput,message,addr) = self.getInput (300,y)
          if message.lower() == 'exit': 
             quit = True
             # utilities.udpBroadcast (client, 'Player left chat', 3333) # key input          
          elif typeInput == 'key': 
             self.comm.send (message)
             y = y + 20  
             
             '''   
             elif typeInput == 'udp':
                addr = str(addr[0])       
                print ('Got udp ' + chat + ' from: ' + addr )
                if addr == socket.gethostbyname(socket.gethostname()): 
                   print ('Ignore this message because it is from myself')
                else:
                   showLine (addr + ':' + chat, 300, y)               
                   y = y + 20             
             '''
          
          elif typeInput == 'mqtt':
             print ( 'Chatpage got mqtt input: ' + message + ' from: ' + addr)
             self.utilities.showLine (addr + ':' + message, 300, y)
             y = y + 20
 
   # Show the list the games and play a game when it is selected
   def joinGamePage(self,showOnly=False):       
       pygame.display.set_caption('Select a game')       
       BLACK = (0,0,0)       
       self.displaySurface.fill((BLACK))
       games = ['Tic Tac Toe', 'Uno']       
       labels = self.utilities.showSsids(games)    
       sprites = self.utilities.showImages (['quit.jpg'], [(400,400)] )       
       self.utilities.showLabel ('Select a game to host (you move first)', 50, 20)    
       pygame.display.update()
       
       quit = False
       while not quit and not showOnly: 
          ev = pygame.event.get()
          for event in ev:
            # Check if an ssid is clicked on
            sprite = self.utilities.getSpriteClick (event, labels )
      
            if sprite != -1:
               print ("Selected game: " + str(sprite))
               if sprite == 0: 
                  self.comm.send ( 'join tictactoe')
                  ticTacToe = TicTacToe(self.displaySurface,self.utilities,self.comm)
                  ticTacToe.iAmHost = False
                  ticTacToe.main()                   
                  quit = True                   
               elif sprite == 1:
                  self.comm.send ( 'join uno')
                  uno = Uno(self.displaySurface,self.utilities,self.comm)
                  uno.iAmHost = False
                  uno.main()                   
                  quit = True                   
          '''
          if self.comm.isReady():
             print ( 'in joinGame, comm is ready' ) 
             data = self.comm.read()
             print ( 'Got a message: ' + data )
             if data.find ( 'join tictactoe' ) > -1: 
                games.append ( 'Tic Tac Toe')
                labels = self.utilities.showSsids(games)    
                sprites = self.utilities.showImages (['quit.jpg'], [(400,400)] )       
                self.utilities.showLabel ('Select a game or Quit', 50, 20)    
                pygame.display.update()
          ev = pygame.event.get()
          for event in ev:   
            # Check if a game is clicked on
            sprite = self.utilities.getSpriteClick (event, labels ) 
            if sprite != -1:          
               print ("Selected game: " + str(sprite)) 
               if sprite == 0: 
                  self.chatPage()
               elif sprite == 1:
                  self.comm.send ( 'joining tictactoe' )
                  ticTacToe = TicTacToe(self.displaySurface,self.utilities,self.comm)
                  ticTacToe.main()                  
                  # tictactoePage(self.displaySurface, self.utilities, self.comm)
               elif sprite == 2:
                  self.checkersPage()
               elif sprite == 3:
                  self.chessPage()
               elif sprite == 4:
                  self.panzerLeaderPage()
               quit = True
          '''
       self.mainPage (True)
               
 
   # Show the list the games and play a game when it is selected
   def hostGamePage(self,showOnly=False):       
       pygame.display.set_caption('Select a game')       
       BLACK = (0,0,0)       
       self.displaySurface.fill((BLACK))
       games = ['Chat', 'Tic Tac Toe', 'Uno', 'Checkers', 'Chess', 'Panzer Leader']       
       labels = self.utilities.showSsids(games)    
       # sprites = self.utilities.showImages (['quit.jpg'], [(400,400)] )       
       self.utilities.showLabel ('Select a game or Quit', 50, 20)    
       pygame.display.update()
       
       quit = False
       while not quit and not showOnly:   
          ev = pygame.event.get()
          for event in ev:   
            # Check if an ssid is clicked on       
            sprite = self.utilities.getSpriteClick (event, labels ) 
            if sprite != -1:          
               print ("Selected game: " + str(sprite)) 
               if sprite == 0: 
                  self.chatPage()
               elif sprite == 1:
                  ticTacToe = TicTacToe(self.displaySurface,self.utilities,self.comm)
                  ticTacToe.main()                                    
               elif sprite == 2:
                  uno = Uno (self.displaySurface,self.utilities,self.comm)
                  uno.main()
               elif sprite == 3:
                  self.checkersPage()
               elif sprite == 4:
                  self.chessPage()
               elif sprite == 5:
                  self.panzerLeaderPage()
               quit = True
               
               
            #sprite = self.utilities.getSpriteClick (event, sprites ) 
            #if sprite != -1: # Quit is the only other option           
            #   print ("Selected command: " + str(sprite))
            #   quit = True  
       print ( 'Done in gamePage, reshow mainPage' )
       self.mainPage (True)
       
   # Show the list of players and allow selection
   def connectPage(self,showOnly=False):       
       pygame.display.set_caption('Select a player to connect to')       
       BLACK = (0,0,0)       
       self.displaySurface.fill((BLACK))
       players = ['pi7', 'laptop']       
       labels = self.utilities.showSsids(players)    
       sprites = self.utilities.showImages (['quit.jpg'], [(400,400)] )       
       self.utilities.showLabel ('Select a player or Quit', 50, 20)    
       pygame.display.update()
       
       quit = False
       while not quit and not showOnly:
          ev = pygame.event.get()
          for event in ev:
            # Check if an ssid is clicked on
            sprite = self.utilities.getSpriteClick (event, labels )
            if sprite != -1:
               print ("Selected player: " + str(sprite))
               if sprite == 0: 
                  print ( 'pi7 selected')
                  self.comm.target = 'pi7'
                  quit = True 
               elif sprite == 1:
                  print ( 'laptop selected')
                  self.comm.target = 'laptop'
                  quit = True 
            # Check if an ssid is clicked on       
            #sprite = self.utilities.getSpriteClick (event, sprites ) 
            #if sprite == 0:
            #   print ( 'Quit selected')
            #   quit = True               
   
       print ( 'Returning to mainpage' )  
       self.mainPage (True)       
       
   def mainPage(self,showOnly = False):   
       if self.comm.target != '': 
          pygame.display.set_caption('Host Join or Play, connected to: ' + self.comm.target)        
       else:
          pygame.display.set_caption('Host Join or Play')        
       
       locations = [ (400,400), (100,100), (300,100), (500,200), (300,200), (300,300)] 
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))    
       sprites = self.utilities.showImages ( ['quit.jpg', 'host.jpg', 'join.jpg', \
                    'connect.jpg', 'joinGame.jpg', 'hostGame.jpg'], locations)
                    
       pygame.display.update()
       self.comm.target = 'pi7' if (platform.system() == 'Windows') else 'laptop'

       quit = False
       try: 
          while not quit and not showOnly:   
             ev = pygame.event.get()
             for event in ev:       
               sprite = self.utilities.getSpriteClick (event, sprites )
               if sprite != -1:
                  if sprite == 0: 
                     print ( 'Quitting on sprite 0' )
                     self.comm.disconnect()
                     quit = True
                     break
                  elif sprite == 1: 
                     self.hostPage()
                  elif sprite == 2:
                     self.joinPage() # Join SSID?
                  elif sprite == 3: # Connect
                     self.connectPage()
                  elif sprite == 4: # Join Game
                     self.joinGamePage()
                  elif sprite == 5: # Host Game
                     self.hostGamePage()
       except Exception as ex:
          print ( 'Trouble in mainPage: ' + str(ex)) 
       #finally:
       #   self.comm.disconnect() 
       print ( 'Done in mainPage are all threads terminated?')