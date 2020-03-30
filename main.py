import pygame
import subprocess
import os
import socket
import select


WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255,   0,   0)
DARKRED    = (139,  26,  26)
DARKGREY   = (128, 128, 128)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

tcpSocket = None
tcpConnection = None
client = None

games = [] 
iAmHost = False
joining = ''
DISPLAYWIDTH=800
DISPLAYHEIGHT=600
UDPPORT = 3333

myIpAddress = socket.gethostbyname(socket.gethostname())

# Read configuration data
try: 
   f = open ( 'config.txt', 'r')
   line = f.readline().strip().lower()
   f.close()
   print ("Read line: " + line)
   if line == 'host': 
      print ( 'You are host' )
      iAmHost = True
      games = ['Chat', 'Tic Tac Toe', 'Checkers', 'Chess', 'Panzer Leader']     
      
   elif line == 'client':
      games = ['Chat']
      print ( 'You are client')
      iAmHost = False
except Exception as ex:
   print ( "Exception: " + str(ex) )
   iAmHost = None
print ("iAmHost: " + str(iAmHost) + " games:" + str(games)) 

'''
   Utilities
'''
def showStatus (status):
    height = DISPLAYHEIGHT - 23
    pygame.draw.line(DISPLAYSURF, RED, (0, height), (DISPLAYWIDTH, height)) #status line
    pygame.draw.rect(DISPLAYSURF, BLACK, (0,height+2,DISPLAYWIDTH,25))    
    # pygame.display.flip()
    showLine (status, 1, height+4)
    print (status)

def getKeyOrUdp():
  global client 
  global joining 
  shiftKeys = { '\\':'|', ']':'}', '[':'{', '/':'?', '.':'>', ',':'<', '-':'_', '=':'+', ';':':',  \
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
             key = chr(event.key)
             if upperCase: 
                if key in shiftKeys.keys():
                   key = shiftKeys[key]
                else:                     
                   key = key.upper()
             
             typeInput = 'key'
             data=key
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
       elif event.type == pygame.MOUSEMOTION:
          data = pygame.mouse.get_pos()
          typeInput = pygame.MOUSEMOTION
          addr = 'mouse'
       else:
          print ( 'Got a event: ' + str(event.type)) 
             
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
             if addr == myIpAddress:
                print ( "Ignoring udp message [" + data + "] from me" )
                data = ''
             else:  
                showStatus ( "Received udp message [" + data + "]")
                ind = data.find ( 'exec:')
                if ind > -1: # joining=, games=, move= 
                   command = data[ind+5:]
                   showStatus ("Executing command: [" + command + "]")
                   exec (command, globals()) 
                
             typeInput = 'udp'
          elif s == tcpConnection: 
             data, addr = tcpConnection.recvfrom (1024)
             data = data.decode();
             print ("Received tcp data:" + data)
             addr = str(addr[0])
             typeInput = 'tcp'
          elif s == tcpSocket:
             data, addr = tcpSocket.recvfrom (1024)
             data = data.decode();
             print ("Received tcp data:" + data)
             typeInput = 'tcp'
             addr = str(addr[0])
             
   
  # print ( 'returning typeInput: ' + str(typeInput))   
  return (typeInput,data,addr)
  
def showCh (ch,x,y):
  surface = FONT.render(str(ch), True, TEXTCOLOR, TEXTBGCOLOR2)
  rect = surface.get_rect()
  rect.topleft = (x,y)
  DISPLAYSURF.blit(surface, rect)
  pygame.display.update()

def chOffset (ch): 
   offsets = { '.':4, ':':4, ',':4, '-':4, ' ':4, '(':4, ')':4, '[':5, ']':5, '\'':4, '=':9, \
               'I':4, 'W':13, 'O':13, \
               'a':9, 'b':9, 'c':9, 'e':9, 'f':4, 'i':4, 'j':4, 'k':9, 'l':4, 'm':13, 'r':6, 's':9, 't':5, 'x':9, 'v':9, 'w':12, 'y':9, \
               '0':9, '1':9, '2':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9 \
             }
   offset = 10
   if ch in offsets.keys(): 
      offset = offsets[ch]
   return offset 
  
def showLine ( line, x,y ):
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
    
def showImages (filenames,locations):
    images = [] 
    for filename in filenames:
        images.append ( pygame.image.load (filename) )     

    sprites = []
    i = 0
    for image in images: 
        sprites.append (DISPLAYSURF.blit (image, locations[i]) )
        i = i + 1
    pygame.display.update()        
    return (images,sprites)
  
def getSpriteClick (eventType, pos, sprites): 
    found = -1
    if sprites != None:
       if (eventType == pygame.MOUSEBUTTONUP) or (eventType == pygame.MOUSEBUTTONDOWN):
          print (str(pos)) 
     
          # get a list of all sprites that are under the mouse cursor         
          clicked_sprite = [s for s in sprites if s.collidepoint(pos)]
          
          if clicked_sprite != []:
             for i in range (len(sprites)):
                if clicked_sprite[0] == sprites[i]: # just check the first sprite
                   print ( "getSpriteClick: " + str(i)) 
                   found = i
                   break
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
    
def showSsids(ssids):
    DISPLAYSURF.fill((BLACK))
    
    i = 0    
    y = 55 
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

def udpBroadcast (message):
    port = UDPPORT 
    global client
    UDP_IP = '<broadcast>'
    print ("broadcast message:", message)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.sendto(str.encode(message), (UDP_IP, port))    
    showStatus ( "You sent udp message: [" + message + "]")

def readLines (filename, match):
    found = False
    lines = []
    
    try: 
       f = open (filename, 'r') 
       lines = f.readlines()
       f.close
       
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
    
'''
   Pages
'''   
def hostPage (showOnly=False):
    global iAmHost 
    global games
    pygame.display.set_caption('You are now host, click below to change SSID')        
    f = open ( 'config.txt', 'w')
    f.write ( 'host\n' )
    f.close()
    iAmHost = True
    DISPLAYSURF.fill((BLACK)) 
    (images,sprites) = showImages (['quit.jpg'], [(400,400)] )      
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
          games = ['Chat', 'Tic Tac Toe', 'Checkers', 'Chess', 'Panzer Leader']     
          mainPage (True)
          quit = True

# Show the list the SSIDS and join an ssid when it is selected
# Note: reboot may be necessary    
def joinPage(showOnly=False):       
    global iAmHost
    f = open ( 'config.txt', 'w')
    f.write ( 'client\n' )
    f.close()
    pygame.display.set_caption('You are client, click below to join an SSID')        
    f = open ( 'config.txt', 'w')
    f.write ( 'client\n' )
    f.close()
    iAmHost = False
    DISPLAYSURF.fill((BLACK))
    (images,sprites) = showImages (['quit.jpg', 'join.jpg'], [(400,400), (200,200)] )       
    (ssidSurf, ssidRect) = createLabel ('Press Join to show SSIDs', 50, 20)    
    DISPLAYSURF.blit(ssidSurf, ssidRect)
    pygame.display.update()

    quit = False
    
    ssids = scanForSsids()      
    labels = showSsids(ssids)
        
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
 
def checkersPage():
   global joining 
   global move 
   
   SQUAREWIDTH = 50
   BOARDY = 50
   BOARDX = 100 
   RADIUS = int((SQUAREWIDTH/2) - 10)
   OFFSET = 0   
      
   def inBoard (x,y):
      insideBoard = False
      if (x >= BOARDX) and (y >= BOARDY):
         if (x <= (BOARDX+(8*SQUAREWIDTH))) and (y <= (BOARDY+(8*SQUAREWIDTH))): 
            insideBoard = True
      return insideBoard
      
   def legalMove (x1,y1,x2,y2):
      return True
      
   def drawBoard(): 
      DISPLAYSURF.fill((WHITE)) 
      y = BOARDY
      count = 0
      for i in range (8):
         for j in range (8):
            count = count + 1
            x = BOARDX + (j * SQUAREWIDTH)
            if (count % 2) == 1:
               pygame.draw.rect(DISPLAYSURF, BLACK, (x,y,SQUAREWIDTH, SQUAREWIDTH))
            else:                  
               pygame.draw.rect(DISPLAYSURF, RED, (x,y,SQUAREWIDTH, SQUAREWIDTH))
         y = y + SQUAREWIDTH
         count = count + 1 # stagger the colors   
   
      y = BOARDY
      count = 0
      for piece in redPieces:
         x = piece[0]
         y = piece[1]
         print ( 'Place redPiece at [' + str(x) + ',' + str(y) + ']') 
         DISPLAYSURF.blit (redImages[count], (x,y))         
         count = count + 1
         
      count = 0
      for piece in blackPieces:
         x = piece[0]
         y = piece[1]
         print ( 'Place blackPiece at [' + str(x) + ',' + str(y) + ']') 
         DISPLAYSURF.blit (blackImages[count], (x,y))
         count = count + 1

      pygame.display.update()        
            
   # Show screen
   pygame.display.set_caption('Play Tic Tac Toe')        

   (redImages,redPieces) = showImages (['redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png', 'redChecker.png'], \
                           [(BOARDX+OFFSET,BOARDY+OFFSET) , \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET), \
                            (BOARDX+OFFSET,                BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+SQUAREWIDTH), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+SQUAREWIDTH)  \
                           ] ) 
   redLocations = [ \
                    [0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], \
                    [0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], \
                  ]

   (blackImages,blackPieces) = showImages (['blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png', 'blackChecker.png'], \
                           [(BOARDX+OFFSET,BOARDY+OFFSET+(SQUAREWIDTH*6)) , \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+(SQUAREWIDTH*6)), \
                            (BOARDX+OFFSET,                BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*1),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*2),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*3),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*4),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*5),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*6),BOARDY+OFFSET+(SQUAREWIDTH*7)), \
                            (BOARDX+OFFSET+(SQUAREWIDTH*7),BOARDY+OFFSET+(SQUAREWIDTH*7))  \
                           ] ) 
   blackLocations = [ \
                      [0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6], \
                      [0,7], [1,7], [2,7], [3,7], [4,7], [5,7], [6,7], [7,7], \
                    ]
   drawBoard()
   (images,sprites) = showImages (['quit.jpg'], [(400,500)] )      

   showStatus ( "Waiting for player to join")
   pygame.display.update()
   
   if iAmHost:
      # Set opponents list of games
      udpBroadcast ( 'exec:games=[\'Checkers\']')
      joining = ''
      playerJoined = False
      move = (0,0) # Host can move first
      myTurn = True
   else:
      udpBroadcast ( 'exec:joining=\'Checkers\'')
      joining = 'Checkers' # Opponent should be waiting
      move = None
       
   quit = False    
   redSelectedPiece = None
   blackSelectedPiece = None
   while not quit: 
      (eventType,data,addr) = getInput (100,100)
      
      if eventType == pygame.MOUSEBUTTONUP:
         if redSelectedPiece != None: 
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            x = BOARDX + (x * SQUAREWIDTH)
            y = BOARDY + (y * SQUAREWIDTH)
            if legalMove (x,y,x,y): 
               redSelectedPiece[0] = x
               redSelectedPiece[1] = y 
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)])
               move = None
               udpBroadcast ( 'exec:move=(' + str(x) + ',' + str(y) + ')')               
            else:
               showStatus ('Red illegal move' )
            
         if blackSelectedPiece != None: 
            x = int((data[0] - BOARDX) / SQUAREWIDTH)
            y = int((data[1] - BOARDY) / SQUAREWIDTH)
            x = BOARDX + (x * SQUAREWIDTH)
            y = BOARDY + (y * SQUAREWIDTH)
            if legalMove (x,y,x,y): 
               blackSelectedPiece[0] = x
               blackSelectedPiece[1] = y 
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)])
               move = None
               # move = (fromX, fromY, toX, toY)
               udpBroadcast ( 'exec:move=(' + str(x) + ',' + str(y) + ',' + str(x) + ',' + str(y)+ ')')               
            else:
               showStatus ( 'Black illegal move' )
         redSelectedPiece = None
         blackSelectedPiece = None  
         
      elif eventType == pygame.MOUSEBUTTONDOWN:
         if myTurn: 
            if joining == 'Checkers':
               if move == None: 
                  showStatus ( 'Waiting for opponent to move')
               else: 
                  piece = getSpriteClick (eventType, data, redPieces)          
                  if piece != -1:
                     redSelectedPiece = redPieces[piece]
                  piece = getSpriteClick (eventType, data, blackPieces)          
                  if piece != -1:
                     print ("black piece clicked on")
                     blackSelectedPiece = blackPieces[piece]
            else:
               showStatus ( 'Waiting for other player to join')
         else:
            showStatus ( 'Waiting for other player to move' )                                  
         
      elif eventType == pygame.MOUSEMOTION:
         if redSelectedPiece != None:
            print ( 'Move redSelectedPiece to: ' + str(data) )
            if inBoard (data[0], data[1]): 
               redSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               redSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)
            
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)] )                 
             
         elif blackSelectedPiece != None:
            print ( 'Move blackSelectedPiece to: ' + str(data))  
            if inBoard (data[0], data[1]):
               blackSelectedPiece[0] = data[0] - int(SQUAREWIDTH/2)
               blackSelectedPiece[1] = data[1] - int(SQUAREWIDTH/2)
               drawBoard()
               (images,sprites) = showImages (['quit.jpg'], [(400,500)] )                     

      elif eventType == 'udp':         
         if data.find ( 'move=') > -1: # Opponent has moved 
            fromX = move[0]
            fromY = move[1]
            toX = move[2]
            toY = move[3]
            # Lookup piece given the location
            # Move the piece 
            print ( 'got a udp move' )
         print ( 'Got a udp: [' + data + '] from: ' + addr )
          
      sprite = getSpriteClick (eventType, data, sprites ) 
      if sprite != -1: # Quit is the only other option           
         print ("Selected command: " + str(sprite))
         mainPage (True)
         quit = True    
    
# Show the Tic-Tac-Toe Pages
def tictactoePage ():
    global joining 
    global move
    taken = [[False, False, False],[False, False, False], [False, False, False]]
    
    drawingX = True
    def drawX (x,y):
       taken [x][y]=True       
       x = (x * 100) + 200
       y = (y * 100) + 100 
       print ( 'Draw X at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.line(DISPLAYSURF, RED, (x, y), (x+100, y+100))
       pygame.draw.line(DISPLAYSURF, RED, (x+100, y), (x, y+100))
       pygame.display.update()
    def drawO (x,y):
       taken [x][y]=True
       x = (x * 100) + 250
       y = (y * 100) + 150 
       print ( 'Draw O at [' + str(x) + ',' + str(y) + ']' )
       pygame.draw.circle(DISPLAYSURF, RED, (x, y), 50, 1)       
       pygame.display.update()
           
    # Show screen 
    DISPLAYSURF.fill((BLACK))
    pygame.display.set_caption('Play Tic Tac Toe')        
    pygame.draw.line(DISPLAYSURF, RED, (300, 100), (300, 400))
    pygame.draw.line(DISPLAYSURF, RED, (400, 100), (400, 400))
    pygame.draw.line(DISPLAYSURF, RED, (200, 200), (500, 200))
    pygame.draw.line(DISPLAYSURF, RED, (200, 300), (500, 300))
    pygame.display.flip()
    (images,sprites) = showImages (['quit.jpg'], [(400,500)] )      
    showStatus ( "Waiting for player to join")
    pygame.display.update()
    
    if iAmHost: 
       # Set opponents list of games
       udpBroadcast ( 'exec:games=[\'Tic Tac Toe\']')
       joining = ''
       playerJoined = False
       move = (0,0)
       myTurn = True
    else:
       udpBroadcast ( 'exec:joining=\'Tic Tac Toe\'')    
       joining = 'Tic Tac Toe' # Opponent should be waiting
       move = None
    
    quit = False    
    while not quit: 
       (eventType,data,addr) = getInput (100,100)
       if eventType == pygame.MOUSEBUTTONUP:
          pos = data
          x = int(pos[0] / 100) - 2
          y = int(pos[1] / 100) - 1
          if (x >=0) and (y >=0) and (x <=2) and (y <= 2):
             if taken[x][y]: 
                showStatus ( "Square already taken")
             else:
                print ('pos: [' + str(x) + ',' + str(y) + ']' ) 
                if joining == 'Tic Tac Toe':
                   if move == None:
                      showStatus ( 'Waiting on opponent\'s move' )             
                   else:
                      print ( 'process: [' + str(x) + ',' + str(y) + ']' )
                      if drawingX: 
                         drawX (x,y)
                      else:
                         drawO (x,y)
                      drawingX = not drawingX
                      move = None
                      udpBroadcast ( 'exec:move=(' + str(x) + ',' + str(y) + ')')
                else:
                   print ( 'Waiting for player, joining: [' + joining + ']' )
                   showStatus ( 'Ignoring click, waiting for player to join')
                   # udpBroadcast ( 'exec:joining=\'Tic Tac Toe\'')             
       elif eventType == 'udp':
          if data.find ( 'move=') > -1: # Opponent has moved 
             if drawingX: 
                drawX (move[0], move[1])
             else:
                drawO (move[0], move[1])
             drawingX = not drawingX
             
          print ( 'Got a udp: [' + data + '] from: ' + addr )
           
 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
     
# Show the chat page
def chatPage(showOnly=False):
    global tcpSocket 
    global tcpConnection 
    
    DISPLAYSURF.fill((BLACK))
    showLabel ('Chat:', 250, 55)
    (images,sprites) = showImages (['quit.jpg'], [(400,400)] )
    
    pygame.display.set_caption('Chatting: ')        
    pygame.display.update()  

    quit = False
    y = 55
    if iAmHost:
       udpBroadcast ("hosting chat")
       
    while not quit and not showOnly:   
       (typeInput,chat,addr) = getInput (300,y)
       if (typeInput == 'key') and (chat.lower() == 'exit'): 
          quit = True
          udpBroadcast ('Player left chat') # key input
       elif typeInput == 'key': 
          if chat.lower() == 'bind': # server
             myAddress = socket.gethostbyname(socket.gethostname()) 
             tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             serverAddress = (myAddress,6666)
             tcpSocket.bind (serverAddress)
             tcpSocket.listen(1)   
             print ("tcp server binding at: port 6666.  Blocking on the accept, other should issue command: connect " + myAddress)
             udpBroadcast ("tcp server waiting... connect " + myAddress) # key input              
             tcpConnection, addr = tcpSocket.accept()
             print ("tcp socket accepted and connected with: " + str(addr) + " tcpConnection initialized")
             tcpConnection.sendall (b'We are all good and ready')
             print ("tcp message sent")
          elif chat.lower().find ('connect') > -1: #client
             if tcpSocket == None: 
                info = chat.split ( ' ' )
                addr = info[1]
                print ( 'TODO; get addr from chat? Server will be 192.164.4.1 if using pis' )
                print ( 'Now connect to: ' + addr + ' using tcp yo' )
                tcpSocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
                tcpSocket.connect ( (addr, 6666)) 
                print ( 'We may now be connected possibly with address:' + addr + 'sending message now')
                tcpSocket.sendall (b'Client ready yo')
             else:
                print ( 'Cannot connect to ' + addr + ' my tcpSocket is already used yo' )        
          elif tcpConnection != None:             
             tcpConnection.sendall (str.encode(chat))          
          elif tcpSocket != None:
             tcpSocket.sendall (str.encode(chat))
          else:             
             udpBroadcast (chat) # key input 
          y = y + 20  
       elif typeInput == 'udp':       
          print ('Got udp ' + chat + ' from: ' + addr )
          if addr == myIpAddress: 
             print ('Ignore this message because it is from myself')
          else:
             showLine (addr + '(udp):' + chat, 300, y)               
             y = y + 20             
       elif typeInput == 'tcp':
          print ( 'Got tcp input: ' + chat + ' from: ' + addr)
          showLine (addr + ':' + chat, 300, y)
          y = y + 20
          
       sprite = getSpriteClick (typeInput, chat, sprites ) 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
            
# Show the list the games and play a game when it is selected
def gamePage(showOnly=False):
    global games   
    global iAmHost

    print ("games: " + str(games))    
    if iAmHost: 
       pygame.display.set_caption('Select a game to host')
    else:
       pygame.display.set_caption('Select the game to join')    
    DISPLAYSURF.fill((BLACK))
    labels = showSsids(games)    
    (images,sprites) = showImages (['quit.jpg'], [(400,400)] )
    if iAmHost: 
       showLabel ('Select a game to host', 50, 20)    
    else:
       showLabel ('Select a game to join', 50, 20)    
    pygame.display.update()
    
    quit = False
    while not quit and not showOnly:  
       (eventType, data, addr) = getInput (100,100)    
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
    (images,sprites) = showImages ( ['quit.jpg', 'host.jpg', 'join.jpg', 'game.jpg'], locations)
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