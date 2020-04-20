import pygame
import subprocess
import os
import socket
import select
import math
import time
import glob
import random

# Include game files
import chat
import castingCost
import checkers
import tictactoe
import chess
import mtg
import diplomacy
import panzerleader
exec (chat.CHAT)
exec (checkers.CHECKERS) 
exec (tictactoe.TICTACTOE)
exec (chess.CHESS)
exec (mtg.MTG)
exec (diplomacy.DIPLOMACY)
exec (panzerleader.PANZERLEADER)

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 255,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255,   0,   0)
DARKRED    = (139,  26,  26)
DARKGREY   = (128, 128, 128)
BLUE       = (0,     0, 255)
YELLOW     = (255, 255,   0)
DARKGREEN  = (0,   100,   0)
DARKBLUE   = (75,    0, 130)
LIGHTBLUE  = (64,  244, 208)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

tcpSocket = None
tcpConnection = None
client = None

games = [] 
gameList = ['Chat', 'Tic Tac Toe', 'Checkers', 'Chess', 'MTG', 'Diplomacy', 'PanzerLeader']
iAmHost = False
joining = ''
DISPLAYWIDTH=800
DISPLAYHEIGHT=600
UDPPORT = 3333
configFilename = 'mainConfig.txt'
rightClick = False
move = None
udpCounter = 0

# Sleep so that the desktop display can initialize itself
#time.sleep(15) 

myIpAddress = socket.gethostbyname(socket.gethostname())
statusMessage = ""
lastStatusMessage = ''
lastUdpCount = -1

# Read configuration data
try: 
   f = open ( configFilename, 'r')
   line = f.readline().strip().lower()
   f.close()
   print ("Read line: " + line)
   if line == 'host': 
      print ( 'You are host' )
      iAmHost = True
      games = gameList    
      
   elif line == 'client':
      games = []
      print ( 'You are client')
      iAmHost = False
except Exception as ex:
   print ( "Exception: " + str(ex) )
   iAmHost = None
print ("iAmHost: " + str(iAmHost) + " games:" + str(games)) 

'''
   Utilities
'''
def rotate (image, angle): 
    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    originPos  = (w//2,h//2)
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot
    
    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    
    return rotated_image
    
def blitRotate(image, pos, angle):

    global DISPLAYSURF
    surf = DISPLAYSURF
    
    # calculate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    originPos  = (w//2,h//2)
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    x = int(pos[0] - originPos[0] + min_box[0] - pivot_move[0])
    y = int(pos[1] - originPos[1] - max_box[1] + pivot_move[1])
    # TODO: change x,y to ints 
    # print ( "origin = (" + str(x) + "," + str(y) + ")" )
    
    origin = (x,y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    # pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)  
    
lastStatus = ''    
def drawStatus (message):  
   global lastStatus    
   if message != lastStatus: 
      print (message)
   # print ( 'Show status: ' + message )
   height = DISPLAYHEIGHT - 23
   pygame.draw.line(DISPLAYSURF, RED, (0, height), (DISPLAYWIDTH, height)) #status line
   showLine (message, 1, height+4) # Show status message     
   pygame.display.update()     
   lastStatus = message
   
def showLastStatus ():
   # global lastStatus 
   drawStatus (lastStatus)
    
def showStatus (status):
    global statusMessage
    statusMessage = status 
    print ( 'showStatus(' + statusMessage + ')' )
    
lastPrintMessage = ''    
nextPrintTime = 0
def myPrint (message):    
   global lastPrintMessage
   global nextPrintTime
   if time.time() <= nextPrintTime:
      print ( 'Spam filter, clearing message: [' + message + ']')
      message = ''
      
   if message != '':
      print ( message ) 
      nextPrintTime = time.time() + 1 
   
UDPTIMEOUT = 3 # Maximum time it takes for other unit to respond
udpTimeout = time.time() + UDPTIMEOUT

def getKeyOrUdp():
  global client 
  global joining 
  global move
  global cast
  global rightClick
  global lastUdpCount
  global udpMessages
  global acks
  global udpTimeout
  global UDPTIMEOUT
  
  shiftKeys = { '\\':'|', ']':'}', '[':'{', '/':'?', '.':'>', ',':'<', '-':'_', '=':'+', ';':':',  \
                '`':'~',  '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^', '7':'&', '8':'*', '9':'(', '0':')' }
  key = None
  upperCase = False
  typeInput = ''
  data = ''
  addr = ''
  
  # Note: If timeout is too close to time.time() 
  #       udp could be lost
  timeEvent = time.time() + 1
  while data == '':

    if time.time() > udpTimeout:  
       if len(udpMessages) > len (acks): # Some messages have not been acked.
          print ( 'udpTimeout [len(udpMessages),len(acks)]: [' + \
               str(len(udpMessages)) + ',' +  str(len(acks)) + ']')    
          message = udpMessages [len(acks)]
          print ( 'Sending: ' + message )
          client.sendto(str.encode(message), ('192.168.4.255', UDPPORT))
       udpTimeout = time.time() + UDPTIMEOUT
                
    rightClick = False
    
    ev = pygame.event.get()
    for event in ev:
       if event.type == pygame.KEYDOWN:
          #print( "Got a keydown with value: " + str(event.key) )
          if (event.key == 303) or (event.key == 304): #shift
             upperCase = True
          # chr(273), 'w', chr(274), 's',  chr(275), 'd', chr (276), 'a']             
          elif (event.key == 273):
             data = 'w'
             typeInput = 'key'
          elif (event.key == 274): 
             data = 's'
             typeInput = 'key'
          elif (event.key == 275):
             data = 'd'
             typeInput = 'key'
          elif (event.key == 276):
             data = 'a'
             typeInput = 'key'             
          else:
             key = chr(event.key)
             if upperCase: 
                if key in shiftKeys.keys():
                   key = shiftKeys[key]
                else:                     
                   key = key.upper()
             
             typeInput = 'key'
             data=key
       elif event.type == pygame.KEYUP:
          data = ' '
          typeInput = pygame.KEYUP
          addr = 'key'
       elif event.type == pygame.QUIT:
          data = 'quit'
          typeInput = pygame.QUIT
          addr = 'key'
       elif event.type == pygame.MOUSEBUTTONUP:
          data = pygame.mouse.get_pos()
          typeInput = pygame.MOUSEBUTTONUP
          addr = 'mouse'
       elif event.type == pygame.MOUSEBUTTONDOWN:
          #print ( 'Detected a mouse down yo' )
          data = pygame.mouse.get_pos()
          typeInput = pygame.MOUSEBUTTONDOWN
          addr = 'mouse'
          rightClick = (event.button == 3)
          if rightClick:
             print ("right click detected")
       elif event.type == pygame.MOUSEMOTION:
          data = pygame.mouse.get_pos()
          typeInput = pygame.MOUSEMOTION
          addr = 'mouse'
       #   
       #else:
       #   print ( 'Got a event: ' + str(event.type)) 
             
    if data == '':
       if tcpConnection != None: 
          i,o,e = select.select ([tcpConnection], [], [], 0.0001)
       elif tcpSocket != None:
          i,o,e = select.select ([tcpSocket], [], [], 0.0001)
       else: #udp
          i,o,e = select.select ([client], [], [], 0.0001)
          
       for s in i:
          if s == client:
             data, addr = client.recvfrom (1024)
             data = data.decode();
             addr = str(addr[0])
             if (addr == '192.168.4.1') and (myIpAddress == '127.0.1.1'): 
                myPrint ( 'Ignore udp message: [' + data + '] from me 127.0.01' )
                data = ''
             elif (addr == myIpAddress):
                myPrint ( "[" + myIpAddress + "]: Ignoring udp message [" + data + "] from me" )
                data = ''
             else:  
                ind = data.find ( ':' )
                if data != '':
                   if data[0:3] == 'ack': 
                      print ( 'Got an ack yo: ' + data)
                      ackCount = data[4:] 
                      print ( 'ackcount: [' + ackCount + ']')
                      ackCount = int(ackCount)
                      if ackCount == len(acks): 
                         acks.append (data)
                      else:
                         print ( 'Ignoring this ack: ' + data)
                      print ( 'acks: ' + str(acks) + ' ack: ' + data )
                      data = '' # Do not send this forward
                   else:                       
                      udpCount = int(data[0:ind])
                      message = 'ack:' + str(udpCount) 
                      print ( 'acking...' + message )
                      client.sendto(str.encode(message), ('192.168.4.255', UDPPORT))
                      myPrint ( '[' + myIpAddress + ']:Got a good message from addr: ' + addr + ' data: [' + data + ']')
                      data = data[(ind+1):]                   
                      ind = data.find ( 'exec:')
                      if ind > -1: # joining=, games=, move= 
                         command = data[ind+5:]
                         exec (command, globals())
                      typeInput = 'udp'                         
                
          elif s == tcpConnection: 
             data, addr = tcpConnection.recvfrom (1024)
             data = data.decode();
             #print ("Received tcp data:" + data)
             addr = str(addr[0])
             typeInput = 'tcp'
          elif s == tcpSocket:
             data, addr = tcpSocket.recvfrom (1024)
             data = data.decode();
             #print ("Received tcp data:" + data)
             typeInput = 'tcp'
             addr = str(addr[0])
             
    if (data == '') and (time.time() > timeEvent): 
       typeInput = 'time'
       data = ' '
       addr = 'clock'  
       
  # print ( 'returning typeInput: ' + str(typeInput))   
  return (typeInput,data,addr)
  
def showCh (ch,x,y):
  surface = FONT.render(str(ch), True, TEXTCOLOR, TEXTBGCOLOR2)
  rect = surface.get_rect()
  rect.topleft = (x,y)
  DISPLAYSURF.blit(surface, rect)
  pygame.display.update()

def chOffset (ch): 
   offsets = { '.':4, ':':4, ',':4, '-':4, ' ':4, '(':4, ')':4, '[':5, ']':5, '\'':4, '/':4, '=':9, \
               'A':11, 'I':4, 'W':14, 'O':12, 'M':13, \
               'a':9, 'b':9, 'c':9, 'e':9, 'f':6, 'i':4, 'j':4, 'k':9, 'l':4, 'm':14, 'r':6, 's':9, 't':5, 'x':9, 'v':9, 'w':12, 'y':9, 'z':8, \
               '0':9, '1':9, '2':9, '3':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9 \
             }
   offset = 10
   if ch in offsets.keys(): 
      offset = offsets[ch]
   return offset 
  
def showLine ( line, x,y ):
  height = DISPLAYHEIGHT - 23
  pygame.draw.rect(DISPLAYSURF, BLACK, (0,height+2,DISPLAYWIDTH,height+2+25))    
  pygame.display.update()
  for ch in line:
     showCh (ch, x, y)
     x = x + chOffset (ch)
  
def getInput (x,y):
  global client
  line = ''
  quit = False
  while not quit:
     (typeInput,data,addr) = getKeyOrUdp()
     if typeInput == 'key': 
        if data == chr(13):           
           quit = True
        elif data == chr(273): # Up
           line = data
           quit = True
        elif data == chr(274): # Down
           line = data
           quit = True
        elif data == chr(275): # Right
           line = data
           quit = True
        elif data == chr(276): # Left
           line = data
           quit = True
        else:
           if data == chr(8):
              print ( "backspace detected")
              if len(line) > 0:
                 lastCh = line[len(line)-1]
                 x = x - chOffset (lastCh) #Todo need to get lastCh from 
                 showCh (' ', x, y)
                 showCh (' ', x+4, y)
                 showCh (' ', x+8, y)
                 line = line[:len(line)-1] 
           else:
              line = line + data
              ch = data
              showCh (ch, x, y)           
              x = x + chOffset(ch)
     elif typeInput == pygame.MOUSEBUTTONUP:
        line = data
        quit = True
     elif typeInput == pygame.MOUSEBUTTONDOWN:
        line = data
        quit = True
     elif typeInput == pygame.MOUSEMOTION:
        line = data
        quit = True
     elif typeInput == 'udp':
        line = data
        quit = True
     elif typeInput == 'tcp':
        line = data
        print ( 'got some tcp data yo: ' + data)
        quit = True
        
  if typeInput != pygame.MOUSEMOTION:      
     print ( "getInput: " + str(line))
  return (typeInput,line,addr)  

def updateWpaSupplicant (ssid, password):
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
      
def createLabel (msg, x, y):
    surface = FONT.render(msg, True, TEXTCOLOR, TEXTBGCOLOR2)
    rect = surface.get_rect()
    rect.topleft = (x,y)
    return ((surface,rect))

def showLabel (msg, x, y):
    (surface, rect) = createLabel (msg, x, y)     
    DISPLAYSURF.blit(surface, rect)    
    
def showLabels (labels, locations):
    sprites = []
    i = 0
    for label in labels: 
        x = locations[i][0]
        y = locations[i][1]
        (surface, rect) = createLabel (label, x, y)    
        sprites.append (DISPLAYSURF.blit(surface, rect))
        i = i + 1
    return sprites
    
def actionsToIcons (actions): 
    filenames = []
    locations = []
    x = 50 
    y = 10
    for action in actions:
       filenames.append ( 'images/' + action + '.jpg' )
       locations.append ( (x,y) ) 
       x = x + 110
    return (filenames,locations)
    
    
def showImages (filenames,locations):
    images = [] 
    try:
       for filename in filenames:
          images.append ( pygame.image.load (filename) )     
    except Exception as ex:
       if str(ex).find ('Couldn\'t open') > -1: 
          print ( '\n***ERR\nDoes this file exist?: ' + filename + '\n')
       else:
          print ( '\n***ERR\nCould not load: ' + filename + ' because: ' + str(ex) + '\n')      

    # Sprites contain rectangular information
    sprites = []
    try:
       i = 0
       for image in images: 
           sprites.append (DISPLAYSURF.blit (image, locations[i]) )
           i = i + 1
       pygame.display.update()        
    except Exception as ex:
       print ( 'main.showImages, could not place sprite on surface because: ' + str(ex))
       print ( 'filenames: ' + str(filenames) + ' locations: ' + str(locations) ) 
    return (images,sprites)
  
def getSpriteClick (eventType, pos, sprites): 
    found = -1
    try:
       if sprites != None:
          if eventType == pygame.MOUSEBUTTONDOWN:
             #print ( 'click: ' + str(pos) + ' in sprites: ' + str(sprites) + '?') 
             count = 0
             for sprite in sprites: 
                if sprite.collidepoint(pos):
                   found = count
                   #print ( "Yes! in sprite: " + str(count)) 
                   break
                count = count + 1
    except Exception as ex:
       print ( 'Could not getSpriteClick because: ' + str(ex) + 'sprites: ' + str(sprites)) 
    #if found == -1:
    #   print ( 'No!')
    return found

def scanForSsids ():
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
       ssids = ['RichardsWiFi', 'Logan\'s Wifi', 'NETGEAR14', 'Net751', 'Fake']
       print ("Got exception: " + str(ex)) 
       
    print (str(ssids)) 
    return ssids
    
def showList(ssids):
    print ('showList' + str(ssids) )     
    i = 0    
    y = 75 
    locations = []
    for ssid in ssids:
       x = 150
       locations.append ( (x,y)) 
       y = y + 35
       
    labels = showLabels (ssids, locations)
    (ssidSurf, ssidRect) = createLabel ('Click on SSID to join (password=\'ABCD1234\')', 50, 20)  
 
    pygame.display.update()
    return labels
    
def joinSSID (ssid):
    print ("joinSSID")
    print ( "Join this ssid yo (reboot may be necessary):" + ssid )   

lastMessage = ""    
udpCount = 0
udpMessages = [] 
acks = [] 
         
def udpBroadcast (message):
    global client
    global lastMessage
    global udpMessages
    global UDPPORT
    
    try: 
       if client == None:
          print ("client udp network not set yet" )
       else:
          message = str(len(udpMessages)) + ':' + message
          print ('udpBroadcast: [' + message + ']')
          udpMessages.append (message) 
                   
    except Exception as ex:
       print ( "Could not send: [" + message + "] because: " + str(ex))
       
       
def readLines (filename, match):
    found = False
    lines = []
    
    try: 
       f = open (filename, 'r') 
       lines = f.readlines()
       f.close()
       
       for line in lines:
          if line.find (match) > -1:
             found = True
             break
    except Exception as ex:
       print ( 'Could not readLines because: ' + str(ex)) 
       
    return (lines,found)
    
def modifyDhcpcd():
    filename = '/etc/dhcpcd.conf' 
    print ( 'modify /etc/dhcpcd.conf' )
    (lines,found) = readLines ( filename, 'interface wlan0')
    if found:
       print ( "Not modifying /etc/dhcpcd.conf because interface wlan0 already exists" )
    else: 
       try: 
          f = open ( filename, 'w')
          for line in lines:
             f.write ( line )
          f.write ( 'interface wlan0\n' )
          f.write ( '   static ip_address=192.168.4.1/24\n' )
          f.write ( '   nohook wpa_supplicant\n' )
          f.close()
       except Exception as ex:
          print ( 'Could not update ' + filename + ' because: ' + str(ex))
        
def modifyDnsmasq(): 
    filename = '/etc/dnsmasq.conf' 
    print ( 'Modify /etc/dnsmasq.conf' ) 
    
    (lines,found) = readLines ( filename, 'interface=wlan0')
    if found:
       print ( "Not modifying /etc/dhcpcd.conf because \'interface=wlan0\' already exists")       
       try:
          f = open ( filename, 'w')
          for line in lines:
             f.write ( line )
          f.write ( 'interface=wlan0\n' )
          f.write ( '   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h\n' )
          f.close()
       except Exception as ex:
          print ( 'Could not modify ' + filename + ' because: ' + str (ex) )
    
def modifyHostapd(ssid, password='ABCD1234'):
    filename = '/etc/hostapd/hostapd.conf'
    print ( 'Modify /etc/hostapd/hostapd.conf' )
    try:
       f = open ( filename, 'w')
       f.write ( 'interface=wlan0\n' ) 
       f.write ( 'driver=nl80211\n' )
       f.write ( 'ssid=' + ssid + '\n' ) 
       f.write ( 'hw_mode=g\n' ) 
       f.write ( 'channel=7\n' ) 
       f.write ( 'wmm_enabled=0\n' ) 
       f.write ( 'macaddr_acl=0\n' ) 
       f.write ( 'auth_algs=1\n' ) 
       f.write ( 'ignore_broadcast_ssid=0\n' ) 
       f.write ( 'wpa=2\n' ) 
       f.write ( 'wpa_passphrase=' + password + '\n' ) 
       f.write ( 'wpa_key_mgmt=WPA-PSK\n' ) 
       f.write ( 'wpa_pairwise=TKIP\n' ) 
       f.write ( 'rsn_pairwise=CCMP\n' ) 
       f.close()
    except Exception as ex:
       print ( 'Could not modify ' + filename + ' because: ' + str (ex) )
       
def extractImage (sheetFilename,x1,y1,x2,y2,finalWidth,finalHeight): 
   sheet = pygame.image.load(sheetFilename)  
   width = x2 - x1
   height = y2 - y1      
   image = pygame.Surface((width, height), pygame.SRCALPHA)
   image = image.convert_alpha()
   image.blit(sheet, (0, 0), (x1,y1,x2,y2))                 
   image = pygame.transform.scale(image, (finalWidth, finalHeight)) 
   return image                   
'''
   Pages
'''   
def hostPage (showOnly=False):
    global iAmHost 
    global games
    global gameList
    pygame.display.set_caption('You are now host, click below to change SSID')        
    f = open ( configFilename, 'w')
    f.write ( 'host\n' )
    f.close()
    iAmHost = True
    DISPLAYSURF.fill((BLACK)) 
    (images,sprites) = showImages (['images/ok.jpg'], [(400,400)] )      
    (surface, rect) = createLabel ('Enter the name of your host ssid', 50, 20)   
    DISPLAYSURF.blit(surface, rect)
    (surface, rect) = createLabel ('SSID:', 250, 55)  
    DISPLAYSURF.blit(surface, rect)
    pygame.display.update()
    #(typeInput,ssid,addr) = getInput(300,55)
          
    quit = False
    while not quit: 
       (eventType,data,addr) = getInput (300,55) 

       if eventType == 'key': 
          print ( 'Got an ssid: [' + data + ']' )
          if data != '':
             pygame.display.set_caption('Hosting SSID: ' + data)
             print ( 'ssid: [' + data + ']')
             modifyDhcpcd() 
             modifyDnsmasq()
             modifyHostapd(data)
             quit = True
          
       sprite = getSpriteClick (eventType, data, sprites ) 
       if sprite != -1: # Quit is the only other option           
          games = gameList     
          mainPage (True)
          quit = True

# Show the list the SSIDS and join an ssid when it is selected
# Note: reboot may be necessary    
def joinPage(showOnly=False):       
    global iAmHost
    global games
    games = []
    f = open ( configFilename, 'w')
    f.write ( 'client\n' )
    f.close()
    pygame.display.set_caption('You are client, click below to join an SSID')        
    f = open ( configFilename, 'w')
    f.write ( 'client\n' )
    f.close()
    iAmHost = False
    DISPLAYSURF.fill((BLACK))
    (images,sprites) = showImages (['images/quit.jpg', 'images/join.jpg'], [(400,400), (200,200)] )       
    (ssidSurf, ssidRect) = createLabel ('Press Join to show SSIDs', 50, 20)    
    DISPLAYSURF.blit(ssidSurf, ssidRect)
    pygame.display.update()

    quit = False
    
    ssids = scanForSsids()      
    labels = showList(ssids)
        
    quit = False
    while not quit and not showOnly:   
       (eventType,data,addr) = getInput (100,100)   
       # Check if an ssid is clicked on       
       sprite = getSpriteClick (eventType, data, labels ) 
       if sprite != -1:           
          print ("Selected label: " + str(sprite))
          quit = True
          # All passwords are the same (ABCD1234)
          updateWpaSupplicant (ssids[sprite], 'ABCD1234')            
          os.system ( 'reboot') # reboot the pi4
          joinSSID (ssids[sprite])
          mainPage (True)
          
       sprite = getSpriteClick (eventType, data, sprites ) 
       if sprite != -1:           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
     
        
# Show the list the games and play a game when it is selected
def gamePage(showOnly=False):
    global games   
    global iAmHost

    quit = False
    showTimeout = 0
    count = 0
    while not quit and not showOnly:  
       (eventType,data,addr) = getKeyOrUdp() # This should set games
       
       if time.time() > showTimeout: 
          count = count + 1
          DISPLAYSURF.fill((BLACK))
          labels = showList(games)
          showTimeout = time.time() + 5 
          if iAmHost: 
             showLabel ('Select a game to host', 50, 20)    
          else:
             if games == []: 
                showLabel ('Waiting on host to select game', 50, 20 )
             else:
                showLabel ('Select a game to join', 50, 20)    
          (images,sprites) = showImages (['images/quit.jpg'], [(400,400)] )
          pygame.display.update()
   
       # Check if a game is clicked on       
       sprite = getSpriteClick (eventType, data, labels ) 
       if sprite != -1:          
          print ("Selected game: " + str(sprite)) 
          game = games[sprite].lower()
          game = game.replace ( ' ', '' )
          exec (game + 'Page()' ) # Show the game page 
          quit = True
          mainPage (True)
                 
       sprite = getSpriteClick (eventType, data, sprites ) 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
          
def mainPage(showOnly = False):   
    pygame.display.set_caption('Host Join or Play')        
    locations = [ (400,400), (300,100), (100,100), (500,100)] 
    height = DISPLAYHEIGHT - 50
    DISPLAYSURF.fill((BLACK))    
    showStatus ( "All Operations Check")
    (images,sprites) = showImages ( ['images/quit.jpg', 'images/host.jpg', 'images/join.jpg', 'images/game.jpg'], locations)
    pygame.display.update()

    quit = False
    while not quit and not showOnly:
       (eventType, data, addr) = getInput (100,100)      
       sprite = getSpriteClick (eventType, data, sprites )
       if sprite != -1:
          if sprite == 0: 
             quit = True
             break
          elif sprite == 1: 
             hostPage()
             mainPage(True) 
          elif sprite == 2:
             joinPage()
             mainPage(True)
          elif sprite == 3:
             gamePage()
             mainPage(True)
                                 
print ("pygame.init")
pygame.init()
print ("get the clock")
MAINCLOCK = pygame.time.Clock()

#sf30 = SF30.SF30()
#while not sf30.joystick_detected:
#   time.sleep (1.0)
#   print ("Waiting for joystick " )
#print ("Joystick detected" )

DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
#pygame.display.toggle_fullscreen()      
pygame.display.set_caption('Flippy')

# Setup the UDP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP    
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", UDPPORT)) 
client.setblocking(0) # turn off blocking  

mainPage()
if tcpConnection != None:
   tcpConnection.close()
   
'''  
def getKey():
  key = None
  upperCase = False
  while key == None:
    ev = pygame.event.get()
    for event in ev:  
       if event.type == pygame.KEYDOWN:
          if (event.key == 303) or (event.key == 304): #shift
             upperCase = True
          else:
             key = event.key 
             break
  # print ("Got a key: " + str(key))
  key = chr(key)
  if upperCase:
     key = str(key).upper()
  return key
  
def readLine(x,y):
  line = ''
  ch = ' '
  lastCh = ch
  while ch != chr(13):
     ch = getKey()
     if ch != chr(13):
        if ch == chr(8):
           print ( "Got an 8")
           x = x - chOffset (lastCh) 
           showCh (' ', x, y)
           line[:len(line)-1] 
        else:
           line = line + ch
           showCh (ch, x, y)
           x = x + chOffset(ch)
     print ('ch:' + str(ch))
  print ( "readLine: " + line)
  return line  
'''   