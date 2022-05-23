import pygame
import subprocess
import os
import socket
import select

'''
   Utilities
'''
class Utilities ():
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
       
   def fileExists (self, filename): 
      exists = os.path.exists ( filename )   
      return exists
      
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
       
   def getSpriteClick (self, event, sprites): 
       self.clicks = {}       
       found = -1
       if self.isMouseClick (event): 
          print ( 'got a mouse up [' + str(event) + ']')
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

   def showStatus (self,status):
       self.statusMessage = status 
       if self.statusMessage != "":
          print ( 'Show status: ' + self.statusMessage )
          height = self.DISPLAYHEIGHT - 23
          pygame.draw.line(self.displaySurface, self.RED, (0, height), (self.DISPLAYWIDTH, height)) #status line
          pygame.draw.rect(self.displaySurface, self.BLACK, (0,height+2,self.DISPLAYWIDTH,25))    
          self.showLine (self.statusMessage, 1, height+4) # Show status message
          print ( 'pygame.update')
          pygame.display.update()
          print ('Done showing Status: ' + self.statusMessage)
       
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
      
   def getKeyOrUdp(self, blocking=True):
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
                key = chr(event.key)
                if upperCase: 
                   if key in shiftKeys.keys():
                      key = shiftKeys[key]
                   else:                     
                      key = key.upper()
                
                typeInput = pygame.KEYDOWN
                data=key
          elif self.isMouseClick (event): 
             typeInput = event
             data = pygame.mouse.get_pos()
          else: 
             pass 
             # print ( 'No handled: ' + str(event.type)) 
 
       if not blocking: 
          break        
     return (typeInput,data,addr)

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
     
     
   def showLabels (self, labels, locations):
       sprites = []
       i = 0
       for label in labels: 
           x = locations[i][0]
           y = locations[i][1]
           (surface, rect) = self.createLabel (label, x, y)    
           sprites.append (self.displaySurface.blit(surface, rect))
           i = i + 1
       return sprites  
     
   def createLabel (self, msg, x, y):
       WHITE = (255,255,255)  
       GREEN = (0,155,0)
       surface = self.font.render(msg, True, WHITE, GREEN)
       rect = surface.get_rect()
       rect.topleft = (x,y)
       return ((surface,rect))
       
   def showCh (self, ch,x,y):
     WHITE = (255,255,255) 
     GREEN = (0,155,0)
     surface = self.font.render(str(ch), True, WHITE, GREEN)
     rect = surface.get_rect()
     rect.topleft = (x,y)
     self.displaySurface.blit(surface, rect)
     pygame.display.update()
    
   def showLine ( self,line, x,y ):
     height = self.DISPLAYHEIGHT - 23
     BLACK = (0,0,0)
     pygame.draw.rect(self.displaySurface, BLACK, (0,height+2,self.DISPLAYWIDTH,height+2+25))    
     pygame.display.update()
     for ch in line:
        self.showCh (ch, x, y)
        x = x + self.chOffset (ch)
        
   def read (self, blocking=True): 
     (typeInput,data,addr) = self.getKeyOrUdp(blocking)
     return (typeInput,data,addr)
     
   # event.type == 1025 for button down 
   # event.type == 1026 for button up   
   # event.button == 1 for left button 
   # event.button == 3 for right button 
   def readOne (self):
      events = []       
      ev = pygame.event.get()
      data = '' 
      for event in ev:       
         typeInput = ''
         try: 
            if event.type == 1024: # Mouse Motion                
               typeInput = 'move'
               data = event.pos
               if self.lastType != 1024: 
                  print ('[lastType,event.type]: [' + str(self.lastType) + ',' + str(event.type) + ']' + str(event)) 
                  self.lastType = 1024
            else:
               if hasattr(event, 'button'): 
                  if event.button == 1: 
                     print ( 'drag' )
                     if event.type == 1025: # button down 
                        typeInput = 'drag'
                        data = event.pos 
                        if self.lastType != 1025: 
                           print ('drag: ' + str(event)) 
                           self.lastType = 1025
                     elif event.type == 1026: # button up 
                        print ( 'drop event' )
                        typeInput = 'drop'              
                        data = event.pos                                    
                        if self.lastType != 1026: 
                           print ('drop: ' + str(event)) 
                           self.lastType = 1026
                  elif event.button == 3: 
                     if event.type == 1025: # button down 
                        typeInput = 'select'
                        data = event.pos 
                        if self.lastType != 1025: 
                           print ('select ' + str(event)) 
                           self.lastType = 1025
                     elif event.type == 1026: # button up 
                        print ( 'Ignore right button up' )
         except Exception as ex:
            print ( 'readOne has exception : ' + str(ex)) 
         if typeInput != '': 
            events.append ( (typeInput, data, 'mouse' ) )
      #if len(events) > 0: 
      #   print ( 'events: ' + str(events) ) 
      return events
        
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
        elif typeInput == 'udp':
           line = data
           quit = True
        elif typeInput == 'tcp':
           line = data
           print ( 'got some tcp data yo: ' + data)
           quit = True
           
     print ( "getInput: " + line)
     return (typeInput,line,addr)  

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
       
   def showLabel (self, msg, x, y):
       (surface, rect) = self.createLabel (msg, x, y)     
       self.displaySurface.blit(surface, rect)    
       
if __name__ == "__main__":
   print ("pygame.init")
   pygame.init()
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   DISPLAYSURF = pygame.display.set_mode((1200, 800))
   utilities = Utilities(DISPLAYSURF, BIGFONT)
   from Communications import Communications
   
   comm = Communications ('messages', '192.168.4.1', 'laptop')
   comm.connect()
   utilities.comm = comm

   sprites = utilities.showImages (['quit.jpg'], [(400,500)] )      
   pygame.display.update() 
   
   quit = False
   while not quit:
      (event,data,addr) = utilities.getKeyOrUdp()
      print ( 'Got an input of: ' + str(event)) 
      
      # Use data above to determine sprite click?          
      sprite = utilities.getSpriteClick (event, sprites ) 
      if sprite != -1: # Quit is the only other option           
         print ("Selected command: " + str(sprite))
         quit = True       
   
   comm.disconnect()