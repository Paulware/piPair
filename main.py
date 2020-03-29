import pygame
#import time
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

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

tcpSocket = None
tcpConnection = None
client = None

'''
   Utilities
'''
def getKeyOrUdp(client):
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
             key = chr(event.key)
             if upperCase: 
                if key in shiftKeys.keys():
                   key = shiftKeys[key]
                else:                     
                   key = key.upper()
             
             typeInput = 'key'
             data=key
             
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
             print ("Received broadcast:" + data)
             typeInput = 'udp'
             addr = str(addr[0])
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
             
       
  return (typeInput,data,addr)
  
def showCh (ch,x,y):
  surface = FONT.render(str(ch), True, TEXTCOLOR, TEXTBGCOLOR2)
  rect = surface.get_rect()
  rect.topleft = (x,y)
  DISPLAYSURF.blit(surface, rect)
  pygame.display.update()

def chOffset (ch): 
   offsets = { '.':4, ':':4, ',':5, '-':4, ' ':4, \
               'I':4, 'W':13, \
               'a':9, 'b':9, 'c':9, 'e':9, 'i':4, 'l': 4, 'm':13, 'r':6, 's':9, 't':5, 'x':9, 'v':9, 'w':12, 'y':9, \
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
     (typeInput,data,addr) = getKeyOrUdp(client)
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
     elif typeInput == 'udp':
        line = data
        quit = True
     elif typeInput == 'tcp':
        line = data
        print ( 'got some tcp data yo: ' + data)
        quit = True
        
  print ( "getInput: " + line)
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
    return sprites
  
def getSpriteClick (event, sprites): 
    found = -1
    if event.type == pygame.MOUSEBUTTONUP:
       pos = pygame.mouse.get_pos()
       # print (str(pos)) 
  
       # get a list of all sprites that are under the mouse cursor         
       clicked_sprite = [s for s in sprites if s.collidepoint(pos)]
       
       if clicked_sprite != []:
          for i in range (len(sprites)):
             if clicked_sprite[0] == sprites[i]: # just check the first sprite
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

def udpBroadcast (client, message, port):
 UDP_IP = '<broadcast>'
 print ("broadcast message:", message)
 # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
 client.sendto(str.encode(message), (UDP_IP, port))    
 
'''
   Pages
'''   
def mainPage(showOnly = False):   
    pygame.display.set_caption('Host Join or Play')        
    locations = [ (400,400), (300,100), (100,100), (500,100)] 
    
    DISPLAYSURF.fill((BLACK))    
    sprites = showImages ( ['quit.jpg', 'host.jpg', 'join.jpg', 'game.jpg'], locations)
    pygame.display.update()

    quit = False
    while not quit and not showOnly:   
       ev = pygame.event.get()
       for event in ev:       
         sprite = getSpriteClick (event, sprites )
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
               
def hostPage (showOnly=False):
    pygame.display.set_caption('Change your host SSID')        
    DISPLAYSURF.fill((BLACK))    
    (surface, rect) = createLabel ('Enter the name of your host ssid', 50, 20)   
    DISPLAYSURF.blit(surface, rect)
    (surface, rect) = createLabel ('SSID:', 250, 55)  
    DISPLAYSURF.blit(surface, rect)
    pygame.display.update()
    (typeInput,ssid,addr) = getinput(300,55)
    pygame.display.set_caption('Hosting SSID: ' + ssid)
    print ( 'ssid: [' + ssid + ']')
    print ( 'modify /etc/dhcpcd.conf' )
    print ( 'Modify /etc/dnsmasq.conf' ) 
    print ( 'Modify /etc/hostapd/hostapd.conf' )

# Show the list the SSIDS and join an ssid when it is selected
# Note: reboot may be necessary    
def joinPage(showOnly=False):       
    pygame.display.set_caption('Join an SSID')        
    DISPLAYSURF.fill((BLACK))
    sprites = showImages (['quit.jpg', 'join.jpg'], [(400,400), (200,200)] )       
    (ssidSurf, ssidRect) = createLabel ('Press Join to show SSIDs', 50, 20)    
    DISPLAYSURF.blit(ssidSurf, ssidRect)
    pygame.display.update()

    quit = False
    
    ssids = scanForSsids()      
    labels = showSsids(ssids)
    
    sprites = showImages (['quit.jpg'], [(400,400)] )       
    
    quit = False
    while not quit and not showOnly:   
       ev = pygame.event.get()
       for event in ev:   
         # Check if an ssid is clicked on       
         sprite = getSpriteClick (event, labels ) 
         if sprite != -1:           
            print ("Selected label: " + str(sprite))
            quit = True
            # All passwords are the same (ABCD1234)
            updateWpaSupplicant (ssids[sprite], 'ABCD1234')            
            os.system ( 'reboot') # reboot the pi4
            joinSSID (ssids[sprite])
            mainPage (True)
            
         sprite = getSpriteClick (event, sprites ) 
         if sprite != -1:           
            print ("Selected command: " + str(sprite))
            mainPage (True)
            quit = True
            
# Show the list the games and play a game when it is selected
def gamePage(showOnly=False):       
    pygame.display.set_caption('Select a game')        
    DISPLAYSURF.fill((BLACK))
    games = ['Chat', 'Tic Tac Toe', 'Checkers', 'Chess', 'Panzer Leader']       
    labels = showSsids(games)    
    sprites = showImages (['quit.jpg'], [(400,400)] )       
    showLabel ('Select a game or Quit', 50, 20)    
    pygame.display.update()
    
    quit = False
    while not quit and not showOnly:   
       ev = pygame.event.get()
       for event in ev:   
         # Check if an ssid is clicked on       
         sprite = getSpriteClick (event, labels ) 
         if sprite != -1:          
            print ("Selected game: " + str(sprite)) 
            if sprite == 0: 
               chatPage()
            elif sprite == 1:
               ticTacToePage()
            elif sprite == 2:
               checkersPage()
            elif sprite == 3:
               chessPage()
            elif sprite == 4:
               panzerLeaderPage()
            quit = True
            mainPage (True)
            
            
         sprite = getSpriteClick (event, sprites ) 
         if sprite != -1: # Quit is the only other option           
            print ("Selected command: " + str(sprite))
            mainPage (True)
            quit = True
            
# Show the chat page
def chatPage(showOnly=False):
    global tcpSocket 
    global tcpConnection 
    global client
    
    DISPLAYSURF.fill((BLACK))
    # sprites = showImages (['quit.jpg'], [(400,400)] )       
    showLabel ('Enter exit to quit', 50, 20)     
    showLabel ('Chat:', 250, 55)
    
    pygame.display.set_caption('Chatting: ')        
    pygame.display.update()  

    quit = False
    y = 55
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP    
    # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client.bind(("", 3333)) 
    client.setblocking(0) # turn off blocking  
    print ("My ip address:" + socket.gethostbyname(socket.gethostname()))    
    while not quit and not showOnly:   
       (typeInput,chat,addr) = getInput (300,y)
       if chat.lower() == 'exit': 
          quit = True
          udpBroadcast (client, 'Player left chat', 3333) # key input
       elif typeInput == 'key': 
          if chat.lower() == 'bind': # server
             myAddress = socket.gethostbyname(socket.gethostname()) 
             tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             serverAddress = (myAddress,6666)
             tcpSocket.bind (serverAddress)
             tcpSocket.listen(1)   
             print ("tcp server binding at: port 6666.  Blocking on the accept, other should issue command: connect " + myAddress)
             udpBroadcast (client, "tcp server waiting... connect " + myAddress, 3333) # key input              
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
             udpBroadcast (client, chat, 3333) # key input 
          y = y + 20  
       elif typeInput == 'udp':
          addr = str(addr[0])       
          print ('Got udp ' + chat + ' from: ' + addr )
          if addr == socket.gethostbyname(socket.gethostname()): 
             print ('Ignore this message because it is from myself')
          else:
             showLine (addr + ':' + chat, 300, y)               
             y = y + 20             
       elif typeInput == 'tcp':
          print ( 'Got tcp input: ' + chat + ' from: ' + addr)
          showLine (addr + ':' + chat, 300, y)
          y = y + 20
          
            
print ("pygame.init")
pygame.init()
print ("get the clock")
MAINCLOCK = pygame.time.Clock()

#sf30 = SF30.SF30()
#while not sf30.joystick_detected:
#   time.sleep (1.0)
#   print ("Waiting for joystick " )
#print ("Joystick detected" )

DISPLAYSURF = pygame.display.set_mode((800, 600))
FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
#pygame.display.toggle_fullscreen()      
pygame.display.set_caption('Flippy')
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