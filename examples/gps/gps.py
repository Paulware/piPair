# sudo systemctl daemon-reload
# sudo systemctl enable backdoor.service

from socket import *
import subprocess
import os
import sys
import pygame
import time
import sys
import select
from pygame.locals import *
from threading import Thread
import datetime
import fcntl
import serial
import pynmea2
import glob
import copy
import buttonClass

from math import radians, cos, sin, asin, sqrt, atan2, degrees
 
latitude = 0
longitude = 0 
mph = 0
lastMphTime = time.time()
gpsTime = ""
gpsDate = ""
gpsPort = ""

print ('gps.py ver 0.01')

port = 3000
count = 0
quit = False

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind (('',port)) # bind to port for listening
fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BLUE       = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255,   0,   0)

TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
WINDOWWIDTH = 800
WINDOWHEIGHT = 480
zeroTime = time.time()
lastMsg = ""
sentMsg = ""

pygame.init()
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
DISPLAYSURF = pygame.display.set_mode ((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)  
usbInsertedFlag = False
internetConnection = False
deviceConnected = False
gpsConnected = False
usbFlags = {"a":False, "b":False, "c":False }
iaMap = None
moMap = None
urbandaleMap = pygame.image.load ("urbandale.jpg").convert()
currentSpot = pygame.image.load ("x.png").convert()

currentLocation = (0,0)
lastLocation = (0,0)
latLong = (0,0)
currentMap = ""
mapOffsets = {"ia":(0,0), "mo":(0,0), "urbandale":(0,0)}
ports = {} 

def closePort (port):
   if port != None:
      try:
         port.close()
      except:
         line = ""
         
def getDeviceType (port): 
   global gpsConnected
   global gpsPort
   
   deviceType = ""
   line = "" 
   serialPort = None
   if port.find ( 'ACM' ) > -1: 
      deviceType = "gps"
      if not gpsConnected:
         print "Gps (normal) is connected"
         gpsConnected = True
         gpsPort = port 
   else: 
      try: 
         serialPort = serial.Serial(port, baudrate = 4800, timeout = 0.01)
         startTime = time.time() 
         while (time.time() - startTime < 2) and (deviceType == ""): 
            try:
               line = serialPort.readline()  
               if line != "": 
                  if (line.find ( "$GPGGA") > -1 ) or (line.find ("$GPGSA") > -1) or (line.find ("$GPRMC") > -1): 
                     deviceType = "gps$"
                     if not gpsConnected: 
                        print "Gps (expensive) is connected"
                        gpsConnected = True
                        gpsPort = port 
                     
            except Exception as inst:
               print ("getDeviceType got exception: " + str(inst)) 
               line = ""
               break
               
         closePort (serialPort) 
         
      except Exception as inst:
         closePort (serialPort)         
   
   return deviceType
   
def portsContains (deviceType): 
   global ports 
   contains = False    
   for port in ports:
      val = ports[port]
      if val.find (deviceType) > -1: 
         contains = True
         break
             
   return contains
   
# ttyUSB is used by one of the gps devices     
# ttyACM is used by the other (cheaper) gps device
def findConnectedDevices():
   global ports 
   global gpsConnected
   
   numDevices = len (ports) 
   newPorts = {} 
   # print ("findConnectedDevices (" + location + ")" ) 
   port = ""
   globs = glob.glob ( '/dev/ttyUSB[0-9]')       
   if len(globs) > 0:         
      for g in globs: 
         newPorts[g] = ''         
   globs = glob.glob ( '/dev/ttyACM[0-9]')       
   if len(globs) > 0:         
      for g in globs: 
          newPorts[g] = ''

   try: # ports can change in the middle of iteration           
      for port in ports:        
         if not port in newPorts: # Remove the port  
            ports.pop (port, None) 
            print ("Removing " + port + " from the list ")
      
      for port in newPorts:       
         if not port in ports: # Only get device type when a port is added.
            ports[port] = getDeviceType (port) 
                       
      gpsConnected = portsContains ("gps")
      
   except Exception as inst:
      print ("findConnectedDevices got exception: " + str(inst)) 
    
   if len(ports) != numDevices:       
      print ("Found " + str(len(ports)) + " devices" )
      print (str(ports))
   return ports
 
# cheaper gps is on ttyUSB ports 
# more expensive gps is on the ttyACM        
def checkForUsbDevice():
   global quit
   
   print ("checkForUsbDevice started")
   while not quit: 
      devices = findConnectedDevices () 
      time.sleep(1)


def haversineFeet(pointA, pointB):
    distance = 0 
    #print ("(lat1/long1): (" + str(pointA[0]) + "," + str(pointA[1]) + ") " + \
    #       "(lat2/long2): (" + str(pointB[0]) + "," + str(pointB[1]) + ")" ) 
    if pointA != (0,0) and pointB != (0,0): 
       if (type(pointA) != tuple) or (type(pointB) != tuple):
           print ("Tuple error " )
           raise TypeError("Only tuples are supported as arguments")

       lat1 = pointA[0]
       lon1 = pointA[1]

       lat2 = pointB[0]
       lon2 = pointB[1]

       # convert decimal degrees to radians 
       lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2]) 

       # haversine formula 
       dlon = lon2 - lon1 
       dlat = lat2 - lat1 
       a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
       if a < 0: 
          print ("Illegal sqrt (" + str(a) + ")" )
       c = 2 * asin(sqrt(a)) 
       # radius of the earth 
       radiusKilometers = 6371
       radiusMiles = 3956
       r = radiusMiles
       distance = c * r * 5280.0
       
    return int(distance) 

def getFilenames (path):
   print ("Look for files in : " + path) 
   files = os.listdir (path)     
   print ("getfilenames Found files: !" + str(files) + "!")
   return files

def sendLine(line, y):
   global BIGFONT
   global DISPLAYSURF
   global pygame

   msgSurf = BIGFONT.render(line, True, WHITE, BLUE)
   msgRect = msgSurf.get_rect()
   msgRect.topleft = (20, y)
   DISPLAYSURF.blit(msgSurf, msgRect)
   
def showMsg (msg):   
   # print (msg)
   lines = msg.split ( '\n' )   
   y = 10
   for line in lines:
      if line != "": 
         sendLine ( line, y )
         y = y + 35

def getLocalTime():
   t = str(datetime.datetime.now().time())
   ind = t.find ( ".")
   if ind > -1:
      t = t[0:ind]
   # print ("Got a localtime: " + t)
   return t

def sendMsg (msg):
   global latitude
   global longitude
   global mph
   global gpsTime
   global sentMsg
   global gpsConnected
   
   if gpsConnected: 
      theTime = gpsTime
   else:
      theTime = getLocalTime()
      
   if sentMsg != msg:
      sentMsg = msg
      print msg 
      
   if msg != "":    
      msg = gpsDate + " " + theTime + "\n" + msg 
      if latitude != 0:
         lat = int(latitude * 100.0)
         long = int(longitude * 100.0)
         msg = "[" + str(lat/100.0) + "," + str(long/100.0) + "] " + str(mph) + " mph " + msg 
      else:
         msg = "[NoLat/Long] " + msg       

      showMsg (msg)
   
def refreshMouse ():
   global quit
   global mapOffsets
   global currentMap

   mousePressed = False   
   while not quit:
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONDOWN:
             downPosition = pygame.mouse.get_pos()
             mousePressed = True
         elif event.type == pygame.MOUSEBUTTONUP:
             mousePressed = False 
             
         if mousePressed:
             upPosition = pygame.mouse.get_pos()
             xOffset = upPosition[0] - downPosition [0]
             yOffset = upPosition[1] - downPosition [1]
             try:
                mapOffsets[currentMap] = (mapOffsets[currentMap][0] + xOffset, \
                                          mapOffsets[currentMap][1] + yOffset )
             except Exception as inst:
                print ("Trouble with mouse: ?" + str(inst))
             # print ("mapOffsets: " + str(mapOffsets) ) 
             downPosition = upPosition

      time.sleep (0.1)
      
def getUsbFlags (usbFlags): 
    p = subprocess.Popen (['fdisk', '-l'], stdout=subprocess.PIPE)
    out,err = p.communicate()
    for flag in usbFlags:
       usbFlags [flag] = False
    try:
       lines = out.split ("\n")
       for line in lines:
          for flag in usbFlags:
             if line.find ("/dev/sd" + flag) > -1:
                usbFlags[flag] = True
    except:
       pass

    # print (str(usbFlags))

def usbInserted():
    global usbFlags
    global usbInsertedFlag 
    
    newFlags = {"a":False, "b":False, "c":False}
    getUsbFlags (newFlags)
        
    for flag in usbFlags:
       if newFlags[flag] != usbFlags[flag]:
          print ( "Got a new value for flag: " + flag )
          if newFlags[flag]: 
             usbInsertedFlag = True
          else:
             usbInsertedFlag = False
             
    usbFlags = newFlags  
    return usbInsertedFlag

def osCmd (cmd):
   print ("osCmd(" + cmd + ")" )
   try:
      os.system (cmd)
   except Exception as inst:
      print ("Could not execute: " + cmd + " because: " + str(inst) )
    
def mountUsb():
   p = subprocess.Popen (['fdisk', '-l'], stdout=subprocess.PIPE)
   out,err = p.communicate()
   if (str(out) != ""): 
      lines = out.split ("\n")
      for line in lines:
         if line.find ( "/dev/sd") > -1: 
            if line.find ( "Disk") == -1: 
               device = line.split ( " ")[0]
               print ("Use Device: " + device)
               osCmd ("mkdir /share/usbdrv") 
               osCmd ("umount /share/usbdrv")
               osCmd ("mount -t vfat " + device + " /share/usbdrv")

def showMap ():
   global iaMap
   global moMap
   global urbandale
   global currentSpot
   global DISPLAYSURF
   global latitude
   global longitude
   global currentMap
   global mapOffsets
   
   lat = latitude
   long = longitude
   addX = 0
   addY = 0
   
   if (lat != 0) and (long != 0): 
      if (lat < 41.688465) and (long > -93.911602) and \
         (lat > 41.498580) and (long < -93.486857): 
         #urbandale      
         longDiff = 93.911602 - 93.486857 
         longPx =  2794 - 320 # x pixel difference between Carlisle C and point
         latDiff = 41.688465 - 41.498580
         latPx = 2135 - 659 # y pixel difference between Carlisle C and point    
         xOffset = 320 + ((long + 93.911602) * longPx / longDiff) - (WINDOWWIDTH/2)  
         yOffset = 659 + ((41.688465 - lat) * latPx / latDiff) - (WINDOWHEIGHT/2)
         
         currentMap = "urbandale"
         addX = mapOffsets[currentMap][0]
         addY = mapOffsets[currentMap][1]
         DISPLAYSURF.blit (urbandaleMap, (-xOffset + addX,-yOffset + addY)) 
      elif lat < 40.378611: # South of Ridgeway Mo
         # (0,0) near Watson, Missouri
         longDiff = 95.623889 - 89.995278 # Watson - Alexandria
         longPx = 5004 - 146 # Alexandria - Watson 
         latDiff = 40.47889 - 36.637778 # Watson - Branson
         latPx = 4423 - 126 # Branson - Watson       
         xOffset = ((long + 95.623889) * longPx / longDiff) - (WINDOWWIDTH/2) + 125
         yOffset = ((40.478889 - lat) * latPx / latDiff) - (WINDOWHEIGHT/2) + 163
         currentMap = "mo"
         addX = mapOffsets[currentMap][0]
         addY = mapOffsets[currentMap][1]
         if moMap == None:
            addMessage ("Please wait while loading missouri map")
            print ("Load Missouri map" )
            moMap = pygame.image.load("mo.jpg").convert()

         DISPLAYSURF.blit (moMap, (-xOffset + addX,-yOffset + addY)) 
      else: # Iowa 
         # (0,0) = Souix Falls South Dakota   
         xOffset = ((long + 96.731667) * 1109) -565
         yOffset = ((43.536389 - lat) * 1430) - (WINDOWHEIGHT/2) + 135
         currentMap = "ia"
         addX = mapOffsets[currentMap][0]
         addY = mapOffsets[currentMap][1]
         if iaMap == None:
            addMessage ("Please wait while loading iowa map")
            print ("Load Iowa map" )
            iaMap = pygame.image.load("ia.jpg").convert()
         
         DISPLAYSURF.blit (iaMap, (-xOffset + addX,-yOffset + addY)) 
         
      if (lat !=0) and (long != 0): 
         DISPLAYSURF.blit (currentSpot, (WINDOWWIDTH/2-13 + addX, WINDOWHEIGHT/2 -43 + addY))

      pygame.display.update()      

def checkForKeyboard():
   global quit
   global latLong
   
   while not quit:
      i,o,e = select.select ([sys.stdin],[],[],0.0001)
      for s in i:
         if s == sys.stdin:
            input = sys.stdin.readline()
            if input.strip() == "w": #Washington, Iowa for multiplier
               latLong = (41.3, -91.689167)
            elif input.strip() == "m": # Muscatine, Iowa
               latLong = (41.423889, -91.056111)
            elif input.strip() == "s": #St Charles, Iowa
               latLong = (41.287778,-93.808056)
            elif input.strip() == "c": # Cameron, Missouri 
               latLong = (39.743056,-94.240556)
            elif input.strip() == "h": # Hamburg, Iowa for offset
               latLong = (40.605833, -95.655)          
            elif input.strip() == "k": # Keokuk, Iowa for offset and multiplier
               latLong = (40.397222,-91.385)  
            elif input.strip() == "i": # Winterset, Iowa 
               latLong = (41.335833, -94.013889)            
            elif input != "":
               print ( "Got input: [" + input + "]" )
               quit = True
               break
            
def internet (host="8.8.8.8", port=53, timeout=3):
   connection = False
   try: 
      # setdefaulttimeout (timeout)
      socket(AF_INET, SOCK_STREAM).connect((host,port))
      connection = True
   except: 
      pass
      
   return connection 
   
def checkForInternet():
   global quit
   global internetConnection 

   while not quit:
      if internet(): 
         internetConnection = True
      else:
         internetConnection = False
      time.sleep (0.5)
      
def addMessage (msg):
   global lastMsg
   global DISPLAYSURF
   global BLACK

   lastMsg = msg   
      
def checkForCommand():
   global quit
   while not quit:
      try:
         data = sock.recv (1024)
         print ("Got command: [" + data  + "]")
      except:
         data = ""

      if data != "":
         if data == "quit":
            break
         else:
            parameters = data.split ( ' ' )
            cmd = parameters [0]
            if cmd == "print":
               msg = ' '.join(parameters[1:])
               addMessage (msg)

            elif cmd == "mountusb":
               mountUsb()
            else:
               print ("Could not handle command: " + cmd )

   quit = True

def extractDateTime (msg): 
   global gpsTime 
   global gpsDate 
   
   timestamp = str(msg.timestamp)    
   # clean the timestamp    
   ind = timestamp.find ( " " )
   if ind > -1:
      timestamp = (timestamp[ind+1:]).strip()            
   ind = timestamp.find ( "." )
   if ind > -1:
      timestamp = timestamp[0:ind].strip()
      
   datestamp = str(msg.datestamp)
   stamp = datestamp + " " + timestamp 

   if stamp.find ( "None" ) > -1: 
      theTime = datetime.datetime.strptime (stamp, "None %H:%M:%S")   
   else:       
      theTime = datetime.datetime.strptime (stamp, "%Y-%m-%d %H:%M:%S")
      gpsDate = ""
      if theTime.month < 10: 
         gpsDate = gpsDate + "0"
      gpsDate = gpsDate + str(theTime.month) + "/"
      if theTime.day < 10:
         gpsDate = gpsDate + "0"
      gpsDate = gpsDate + str(theTime.day) + "/" + str(theTime.year)
      
   theTime = theTime - datetime.timedelta(hours=5)

   gpsTime = ""
   if theTime.hour < 10:               
      gpsTime = gpsTime + "0"
   gpsTime = gpsTime + str(theTime.hour) + ":"
   if theTime.minute < 10:
      gpsTime = gpsTime + "0" 
   gpsTime = gpsTime + str(theTime.minute) + ":"
   if theTime.second < 10:
      gpsTime = gpsTime + "0"
   gpsTime = gpsTime + str(theTime.second)   
   
def parseGPS(line):
    global longitude
    global latitude
    global latLong
    
    goodParse = False
    if line.find ( 'PRMC') > 0: 
        msg = pynmea2.parse(line)
        extractDateTime (msg)
    elif line.find('GGA') > 0:
        msg = pynmea2.parse(line)
        try: 
           if latLong == (0,0): 
              if (msg.longitude != longitude):           
                 longitude = msg.longitude
                 latitude = msg.latitude 
           else: #debug 
              latitude = latLong [0]
              longitude = latLong [1]
           goodParse = (longitude != 0) and (latitude != 0)
        except Exception as inst:
           print ("could not parseGPS (" + line + ") because: " + str(inst)) 
    return goodParse
       
def checkForLatLong():
   global quit
   global latitude
   global longitude
   global currentLocation
   global lastLocation 
   global mph
   global lastMphTime
   global gpsConnected 
   global gpsPort 

   connected = False
   while not quit: 
      if not gpsConnected :
         if connected: 
            print ( "Closing serial port to gps device" )
            closePort (serialPort)
         connected = False
         latitude = 0
         longitude = 0
         time.sleep (0.1)
      else: 
         if not connected:
            connected = True
            print ("Opening port " + gpsPort + " to gps device" )
            serialPort = serial.Serial(gpsPort, baudrate = 4800, timeout = 0.01)
         try:
            line = serialPort.readline()  
               
            if parseGPS(line):
               currentLocation = (latitude, longitude)
               feet = haversineFeet ( currentLocation, lastLocation )
               elapsedSeconds = time.time() - lastMphTime;
               speed = int (feet / 5280.0 * 3600.00 / elapsedSeconds)
               mph = speed 
               lastMphTime = time.time()
               # print ("haversine Feet: " + str(feet) ) 
               lastLocation = currentLocation 
               
         except Exception as inst:
            pass
            # print ("ERR, could not checkForLatLong line: [" + line  + "] because: "  + str(inst))
         
      time.sleep (0.01)  
 
def logGps ():
   global latitude
   global longitude 
   global mph
   global quit
   global gpsTime
   
   while not quit: 
      if (latitude != 0) and (longitude != 0) and (gpsDate != "") and \
         (gpsTime != ""): 
         for i in range(60): 
            time.sleep (1)
            if quit:
               break
         
def updateScreen ():
   global lastMsg
   global quit
   
   while not quit:
      DISPLAYSURF.fill((BLACK))             
      showMap()
      sendMsg (lastMsg)         
      pygame.display.update()
      time.sleep (1.0)
  
def checkForQuit():
   global quit
      
   buttons = buttonClass.ButtonsClass()   
   while not quit:   
      for event in buttons.eventGet(): # event handling loop
         if event.key == K_ESCAPE:
            # Player pressed the "Start" button
            quit = True   
      time.sleep (0.1) 
      
def stateMachine():
   global quit
   global latitude
   global longitude
   global usbInsertedFlag
   global internetConnection 
   global deviceConnected
   global DISPLAYSURF
   global BLACK
   global lastMsg
   global gpsConnected
   global connection
   
   state = {'latitude':False, 'usb':False, 'internet':False, \
            'device':False,'gps':False, 'mph': 0 }
   lastState = state
   lastTime = time.time()  
   while not quit:  

      state ['latitude']  = (latitude != 0)  
      state ['usb']       = usbInsertedFlag
      state ['internet']  = internetConnection
      state ['device']    = deviceConnected  
      state ['gps']       = gpsConnected     
       
      msg = ""       
      if lastState ['latitude'] != state ['latitude']:    
         if state['latitude']:
            msg = msg + "[Lat/Long] acquired\n"
         else:
            msg = msg + "[Lat/Long] lost\n" 
         
      # print ("usb [state,last]: [" + str(state['usb']) + "," + str(lastState['usb']) + "]")         
      if lastState ['usb'] != state ['usb']:    
         if state['usb']:
            msg = msg + "USB detected, please wait as I copy files...\n"
         else:
            msg = msg + "USB removed"
            
      if lastState ['internet'] != state ['internet']:    
         if state['internet']:
            msg = msg + "Internet Detected...Ready!\n"
         else:
            msg = msg + "No Internet Detected...Please wait.\n"
            
      if lastState ['device'] != state ['device']:    
         if state['device']:
            msg = msg + "Device connected\n"
         else:
            msg = msg + "Device removed\n"
       
      if lastState ['gps'] != state ['gps']:    
         if state['gps']:
            msg = msg + "GPS device connected\n"
         else:
            msg = msg + "GPS device removed\n"
       
      state['mph'] = mph # update mph 
      
      if msg != "":
         addMessage (msg)      
         
      lastState = copy.deepcopy(state) 
      time.sleep (0.5)        
      
# gpsTime = extractTime (datetime.datetime.now(), False)
getUsbFlags(usbFlags)

t2 = Thread(target=checkForKeyboard)
t2.start()

t3 = Thread(target=checkForInternet)
t3.start() 

t4 = Thread(target=checkForLatLong)
t4.start()

t5 = Thread(target=stateMachine)
t5.start()

t6 = Thread(target=refreshMouse)
t6.start()

t7 = Thread(target=updateScreen)
t7.start()

t8 = Thread(target=logGps)
t8.start()

t9 = Thread(target=checkForUsbDevice)
t9.start()

t10 = Thread(target=checkForQuit)
t10.start()

addMessage ( "Starting...")
pygame.display.update()
   
checkForCommand()
pygame.quit()
sock.close()

print ("Done in gps.py")
