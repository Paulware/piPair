import pygame
import subprocess
import os
import socket
import select
from TextBox import TextBox

'''
   Utilities
'''
class Utilities ():
   def chOffset (self, ch): 
      offsets = { '.':4, ':':4, ',':5, '-':4, ' ':4, \
                  'I':4, 'W':13, \
                  'a':9, 'b':9, 'c':9, 'e':9, 'i':4, 'l': 4, 'm':13, 'r':6, 's':9, 't':5, 'x':9, 'v':9, 'w':12, 'y':9, \
                  '0':9, '1':9, '2':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9 \
                }
      offset = 20
      #if ch in offsets.keys(): 
      #   offset = offsets[ch]
      return offset 
    
   def createLabel (self, msg, x, y):
       WHITE = (255,255,255)  
       GREEN = (0,155,0)
       surface = self.font.render(msg, True, WHITE, GREEN)
       rect = surface.get_rect()
       rect.topleft = (x,y)
       return ((surface,rect))

   def fileExists (self, filename): 
      exists = os.path.exists ( filename )   
      return exists      
      
   def findSpriteClick (self, pos, sprites ): 
      print ( 'findSpriteClick' )
      found = -1
     
      clicked_sprite = [s for s in sprites if s.collidepoint(pos)]
      if len(clicked_sprite) == 0: 
         print ( 'len(clicked_sprite) == 0' ) 
      else: 
         for i in range (len(sprites)): 
            print ( 'i: ' + str(i) + ' len(sprites): ' + str(len(sprites)) )
            if clicked_sprite[0] == sprites [i]: 
               found = i
               break
               
      return found      
      
   def flip(self):
      pygame.display.flip()
      pygame.event.pump()
                     
   def getInput (self, x,y):
     line = ''
     quit = False
     while not quit:
        (typeInput,data,addr) = self.getKeyOrMqtt()
        if typeInput == 'key': 
           if data == chr(13):
              quit = True
           else:
              if data == chr(8):
                 print ( "backspace detected")
                 if len(line) > 0:
                    lastCh = line[len(line)-1]
                    x = x - self.chOffset (lastCh) #Todo need to get lastCh from 
                    self.showCh (' ', x, y)
                    self.showCh (' ', x+4, y)
                    self.showCh (' ', x+8, y)
                    line = line[:len(line)-1] 
              else:
                 line = line + data
                 ch = data
                 self.showCh (ch, x, y)           
                 x = x + self.chOffset(ch)
        elif typeInput == 'mqtt':
           print ( 'get_input, handle mqtt' )
           exit(1)
           line = data
           quit = True
        elif typeInput == 'tcp':
           line = data
           print ( 'got some tcp data yo: ' + data)
           quit = True
           
     print ( "getInput: " + line)
     return (typeInput,line,addr)        
      
   def getKeyOrMqtt(self, blocking=True):
     shiftKeys = { '\\':'|', ']':'}', '[':'{', '/':'?', '.':'>', ',':'<', '-':'_', '=':'+', \
                   '`':'~',  '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^', '7':'&', '8':'*', '9':'(', '0':')' }
     key = None
     upperCase = False
     typeInput = ''
     data = ''
     addr = ''
     while data == '':
       if self.comm != None: 
          if not self.comm.empty(): 
             print ( 'Communications is not empty' ) 
             data = self.comm.pop()
             typeInput = 'mqtt'
             print ( 'Utilities, comm.pop: ' + data) 
     
       ev = pygame.event.get()
       for event in ev:  
          # print ( 'event.type: ' + str(event.type))
          if event.type == pygame.KEYDOWN:
             if (event.key == 303) or (event.key == 304): #shift
                upperCase = True
             else:
                try: 
                   key = chr(event.key)
                   if upperCase: 
                      if key in shiftKeys.keys():
                         key = shiftKeys[key]
                      else:                     
                         key = key.upper()
                   print ( 'event.key: ' + str(event.key)) 
                   if (event.key == 13): 
                      self.message = self.msg
                      self.msg = ''
                   elif (event.key == 8): #Backspace
                      if len(self.msg) > 0: 
                         self.msg = self.msg [0:len(self.msg)-1]
                         print ( 'New self.msg: [' + self.msg + ']' )
                   else:
                      self.msg = self.msg + key 
                   typeInput = pygame.KEYDOWN
                   data=key
                except Exception as ex: 
                   print ( 'getKeyOrMqtt, ignore this: ' + str(ex) ) 
          elif self.isMouseClick (event): 
             typeInput = pygame.MOUSEBUTTONUP
             data = pygame.mouse.get_pos()
          else: 
             pass 
             # print ( 'No handled: ' + str(event.type)) 
 
       if not blocking: 
          break  
     print ( 'getKeyOrMqtt[typeInput,data,addr]: [' + str(typeInput) + ',' + str(data) + ',' + str(addr) + ']' )           
     return (typeInput,data,addr)
      
   def getSpriteClick (self, event, sprites): 
       # print ( 'getSpriteClick event: ' + str(event)  )
       self.clicks = {}       
       found = -1
       if (event == pygame.MOUSEBUTTONUP) or self.isMouseClick (event): 
          print ( 'Utilities.getSpriteClick got a mouse up [' + str(event) + ']')
          pos = pygame.mouse.get_pos()
          print (str(pos)) 
     
          # get a list of all sprites that are under the mouse cursor         
          clicked_sprite = [s for s in sprites if s.collidepoint(pos)]
          
          if clicked_sprite != []:
             for i in range (len(sprites)):
                if clicked_sprite[0] == sprites[i]: # just check the first sprite
                   found = i
                   break
          if found == -1: 
             print ( 'Could not find a sprite' )
          else:
             print ( 'Found sprite: ' + str(found)) 
       return found
      
   def __init__ (self,displaySurf, font):
       self.displaySurface = displaySurf
       self.font = font
       self.DISPLAYWIDTH=800
       self.DISPLAYHEIGHT=600       
       self.statusMessage = ''
       self.BLACK      = (  0,   0,   0)
       self.GREEN      = (  0, 155,   0)
       self.BRIGHTBLUE = (  0,  50, 255)
       self.BROWN      = (174,  94,   0)
       self.RED        = (255,   0,   0) 
       self.comm       = None    
       self.lastType   = 0   
       self.message    = ''  
       self.msg        = '' 
       self.quit       = False
       self.debugIt    = False
       self.debugIt1   = True       
       
   def isMouseClick (self,event): 
       isClick = False 
       ev = str(event)
       if ev.find ('MouseButtonUp') > -1: 
           if ((ev.find ( '\'button\': 1') > -1) or \
               (ev.find ( '\'button\': 3') > -1)): 
               print ( 'event: ' + ev ) 
               print ( 'Got a click' )
               isClick = True 
       return isClick
       
   def read (self, blocking=True): 
     (typeInput,data,addr) = self.getKeyOrMqtt(blocking)
     return (typeInput,data,addr)
     
   # event.type == 1025 for button down 
   # event.type == 1026 for button up   
   # event.button == 1 for left button 
   # event.button == 3 for right button 
   # event.type == 769 for keyup 
   def readOne (self):
      debugIt = True
      events = []       
      ev = pygame.event.get()
      data = '' 
      for event in ev:       
         typeInput = ''
         try: 
            if event.type == pygame.QUIT:
               typeInput = 'quit'
            elif event.type == 1024: # Mouse Motion                
               typeInput = 'move'
               data = event.pos
               if self.lastType != 1024: 
                  if debugIt: 
                     print ('[lastType,event.type]: [' + str(self.lastType) + ',' + str(event.type) + ']' + str(event)) 
                  self.lastType = 1024
            else:
               if hasattr(event, 'button'): 
                  if event.button == 1: 
                     if self.debugIt1:
                        print ( 'drag' )
                     if event.type == 1025: # button down 
                        typeInput = 'drag'
                        data = event.pos 
                        if self.lastType != 1025: 
                           if self.debugIt1:
                              print ('drag: ' + str(event)) 
                           self.lastType = 1025
                     elif event.type == 1026: # button up 
                        if self.debugIt1:
                           print ( 'drop event' )
                        typeInput = 'drop'              
                        data = event.pos                                    
                        if self.lastType != 1026: 
                           if self.debugIt1:
                              print ('drop: ' + str(event)) 
                           self.lastType = 1026
                  elif event.button == 3: 
                     if event.type == 1025: # button down 
                        typeInput = 'select'
                        data = event.pos 
                        if self.lastType != 1025: 
                           if self.debugIt1:
                              print ('select ' + str(event)) 
                           self.lastType = 1025
                     elif event.type == 1026: # button up 
                        typeInput = 'right'
                        data = event.pos
               elif event.type == 769: # keyup 
                  typeInput = 'keypress'
                  data = event.unicode
                  if debugIt:
                     print ( 'event: ' + str(event) ) 
                  if event.key == 27: 
                     typeInput = 'escape'
               elif debugIt: 
                  print ( 'Not handled event: ' + str(event))
                                     
         except Exception as ex:
            print ( 'readOne has exception : ' + str(ex)) 
         if typeInput != '': 
            events.append ( (typeInput, data, 'mouse' ) )
      if (len(events) > 0) and self.debugIt: 
         print ( 'events: ' + str(events) ) 
      return events
       
   def scanForSsids (self):
       ssids = []
       print ( "Show wlan ssids" )               
       try:
          os.system ( 'iw dev wlan0 scan | grep SSID > it.log')
          f = open ( 'it.log', 'r')
          lines = f.readlines()
          f.close()
          for line in lines:
             data = line.split ( 'SSID:' )
             ssid = data[1].strip()
             if ssid != '':
                if ssid.find ( '\\x00') == -1: 
                   ssids.append(ssid)
          
       except Exception as ex: # This might be a windows machine
          ssids = ['7Inch']
          print ("Got exception: " + str(ex)) 
          
       print (str(ssids)) 
       return ssids  
        
   def showCh (self, ch,x,y):
     WHITE = (255,255,255) 
     GREEN = (0,155,0)
     surface = self.font.render(str(ch), True, WHITE, GREEN)
     rect = surface.get_rect()
     rect.topleft = (x,y)
     self.displaySurface.blit(surface, rect)
     pygame.display.update()
         
   def showLabels (self, labels, locations):
       print ( 'Utilities.showLabels, len(labels): ' + str(len(labels)) ) 
       sprites = []
       i = 0
       for label in labels: 
           x = locations[i][0]
           y = locations[i][1]
           (surface, rect) = self.createLabel (label, x, y)    
           sprites.append (self.displaySurface.blit(surface, rect))
           i = i + 1
       return sprites  
     
   def showImages (self,filenames,locations):
       images = [] 
       for filename in filenames:
           filename = 'images/' + filename 
           if self.fileExists ( filename): 
              images.append ( pygame.image.load (filename) )   
           else:
              print ( 'This file is missing: ' + filename )           

       sprites = []
       i = 0
       for image in images: 
           sprites.append (self.displaySurface.blit (image, locations[i]) )
           i = i + 1
       return sprites
       
   def showLabel (self, msg, x, y):
       (surface, rect) = self.createLabel (msg, x, y)     
       self.displaySurface.blit(surface, rect)    
              
   def showLastStatus (self):
       if self.statusMessage != "":
          width, height = pygame.display.get_surface().get_size()
          # pygame.draw.line(self.displaySurface, self.RED, (0, height-40), (self.DISPLAYWIDTH, height-40)) #status line
          line1 = TextBox ( '                                                           ')
          line1.draw ( (0,height-35,30) ) 
          line1 = TextBox ( self.statusMessage )
          line1.draw ( (0,height-35,30) )
          
   def showLine ( self,line, x,y ):
     height = self.DISPLAYHEIGHT - 23
     BLACK = (0,0,0)
     pygame.draw.rect(self.displaySurface, BLACK, (0,height+2,self.DISPLAYWIDTH,height+2+25))    
     pygame.display.update()
     for ch in line:
        self.showCh (ch, x, y)
        x = x + self.chOffset (ch)       
                    
   def showSsids(self,ssids):
       BLACK      = (0,   0,   0)
       self.displaySurface.fill((BLACK))
       
       i = 0    
       y = 55 
       locations = []
       for ssid in ssids:
          x = 150
          locations.append ( (x,y)) 
          y = y + 35
          
       labels = self.showLabels (ssids, locations)
       (ssidSurf, ssidRect) = self.createLabel ('Click on SSID to join (password=\'ABCD1234\')', 50, 20)  
    
       pygame.display.update()
       return labels
       
   def showStatus (self,status):
       self.statusMessage = status 
       if self.statusMessage != "":
          print ( 'Show status: ' + self.statusMessage )
          width, height = pygame.display.get_surface().get_size()
          pygame.draw.line(self.displaySurface, self.RED, (0, height-40), (self.DISPLAYWIDTH, height-40)) #status line
          #pygame.draw.rect(self.displaySurface, self.BLACK, (0,height+2,self.DISPLAYWIDTH,25))    
          #self.showLine (self.statusMessage, 1, height+4) # Show status message
          line1 = TextBox ( '                                                           ')
          line1.draw ( (0,height-35,30) ) 
          line1 = TextBox ( status )
          line1.draw ( (0,height-35,30) )
          print ( 'pygame.update')
          pygame.display.update()
          print ('Done showing Status: ' + self.statusMessage)
          
       
   def stop (self):
       self.quit = True  
       print ( '*** Done in Utilities.stop ***' )
       # pygame.display.quit()
       # exit(1)       
                       
   def updateWpaSupplicant (self, ssid, password):
      print ('updateWpaSupplicant...tbd' )
      return 
      try: 
         f = open ( '/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
         lines = f.readlines()
         f.close()
         found = False
         for line in lines:
            if line.find ( 'network=') > -1: 
               found = True
               break
               
         if found:
            f = open ( '/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
            for line in lines:
                if line.lower().find ( 'ssid=') > -1: 
                   f.write ( '     ssid=\"' + ssid + '\"\n')
                elif line.lower().find ( 'psk=') > -1:
                   f.write ( '     psk=\"' + password + '\"\n')
                else:
                   f.write (line)
            f.close()
         else:
            f = open ( '/etc/wpa_supplicant/wpa_supplicant.conf', 'a')
            f.write ( 'network={\n')
            f.write ( '     ssid=\"' + ssid + '\"\n')
            f.write ( '     psk=\"' + password + '\"\n')
            f.write ( '}\n' )
            f.close()      
      except Exception as ex:
         print ("Could not modify wpa_supplicate because: " + str(ex) )
         
   def waitForClick(self): 
      found = False 
      print ( 'Wait for click' )
      while not found:
         ev = pygame.event.get()
         for event in ev:  
            # print ( 'Got event: ' + str(event)) 
            if self.isMouseClick (event): 
               found = True 
      print ( 'Done waiting for click' )    
      
       
if __name__ == "__main__":
   print ("pygame.init")
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   DISPLAYSURF = pygame.display.set_mode((1200, 800))
   utilities = Utilities(DISPLAYSURF, BIGFONT)
   from Communications import Communications
   
   
   
   comm = Communications ('messages', 'localhost', 'laptop')
   if comm.connectBroker():
      comm.setTarget ( 'pi7' )
      utilities.comm = comm

      sprites = utilities.showImages (['quit.jpg'], [(400,500)] )      
      pygame.display.update   () 
      
      quit = False
      while not quit:
         (event,data,addr) = utilities.getKeyOrMqtt()
         if utilities.message != '': 
            print ( '[message]: [' + utilities.message + ']' )
            utilities.message = ''
         
         # Use data above to determine sprite click?          
         sprite = utilities.getSpriteClick (event, sprites ) 
         if sprite != -1: # Quit is the only other option           
            print ("Selected command: " + str(sprite))
            quit = True       
   
   comm.disconnect()