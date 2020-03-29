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
import os.path
import pickle

# import obd
from math import radians, cos, sin, asin, sqrt, atan2, degrees, trunc

version = "v1.04a "
 
latitude = 0
longitude = 0 
mph = 0
lastMphTime = time.time()
gpsTime = ""
gpsDate = ""
gpsPort = ""
gpsBaud = 4800

WINDOWWIDTH  = 480 
WINDOWHEIGHT = 320 

printX = 10
printY = 10

print ('sshBackdoor.py ver 1.03')
print ('Purpose: Listen for ssh commands to execute')

port = 3000
count = 0
quit = False
rpm = "0"
displayLines = []

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
zeroTime = time.time()
lastMsg = ""
sentMsg = ""

print ("Wait 10 seconds...")
time.sleep(10)
pygame.init()
BIGFONT = pygame.font.Font('freesansbold.ttf', 24)
LITTLEFONT = pygame.font.Font('freesansbold.ttf', 16)
DISPLAYSURF = pygame.display.set_mode ((0, 0), pygame.FULLSCREEN) 

usbInsertedFlag = False
internetConnection = False
deviceConnected = False
obdConnected = False
gpsConnected = False
usbFlags = {"a":False, "b":False, "c":False }
iaMap = None
moMap = None
usbPath = "/Raven/rxMaps/"
#urbandaleMap = pygame.image.load ("urbandale.jpg").convert()
#currentSpot = pygame.image.load ("x.png").convert()

currentLocation = (0,0)
lastLocation = (0,0)
latLong = (0,0)
currentMap = ""
mapOffsets = {"ia":(0,0), "mo":(0,0), "urbandale":(0,0)}
obdConnection = None
ports = {} 
lastRpm = ""
lastOil = ""
lastVoltage = ""
lastDtc = "" 
os.putenv('SDL_VIDEODRIVER', 'dummy')   #fbcon
#os.putenv('SDL_FBDEV'      , '/dev/fb1')

def fileExists ( path ): 
   return os.path.isfile (path)

def setPath(path):
   dbfile = open ( 'piData', 'wb')
   db = {}
   db['path'] = path
   pickle.dump (db,dbfile)
   dbfile.close 

def getPath(): 
   global usbPath
   try:
      dbfile = open ('piData', 'rb')
      db = pickle.load (dbfile)
      if (db['path'] != None): 
         usbPath = db['path']
      dbfile.close()
   except Exception as inst:
      print ("Could not get path because:" + str(inst)) 

def addLog ( msg ):
   global gpsTime
   print (msg)
   f = open ( "wod.log", "a") 
   f.write ( gpsTime + " " + msg + "\n" )
   f.close()

def closePort (port):
   if port != None:
      try:
         port.close()
      except:
         pass
         
def showRpm(response):
   global rpm
   global lastRpm
   response = str(response)
   ind = response.find(".")
   if ind > -1:
      response = response [0:ind]      
   msg = "rpm: " + str(response)
   if lastRpm == "": 
      addLog (msg)
      lastRpm = response
   elif (int(response) > int(lastRpm) + 100) or \
      (int(response) < int(lastRpm) - 100):       
      addLog(msg)
      lastRpm = response    
   rpm = str(response)

def showOil (response):
   global lastOil
   msg = "oil: " + str(response)
   if lastOil != msg: 
      addLog (msg)
   
   lastOil = msg 
   
def showVoltage (response):
   global lastVoltage
   msg = "voltage: " + str(response)
   if lastVoltage != msg: 
      addLog ( msg )
   lastVoltage = msg
   
def showDtc (response):
   global lastDtc
   msg = "Dtc: " + str(response)
   if msg != lastDtc: 
      addLog (msg) 
   lastDtc = msg
   
def showSpeed(response):
   response = str(response)
   ind = response.find ( " " )
   if ind > -1:
      response = response [0:ind]
   #print("spd:" + str(response) + " kph yo")   
 
def canConnectGps (port, baudRate):
   connected = False
   try: 
      serialPort = serial.Serial(port, baudrate = baudRate, timeout = 0.01)
      startTime = time.time() 
      while (time.time() - startTime < 2): 
         try:
            line = serialPort.readline()  
            if line != "": 
               if (line.find ( "$GPGGA") > -1 ) or (line.find ("$GPGSA") > -1) or (line.find ("$GPRMC") > -1): 
                  if not gpsConnected: 
                     print "Gps (expensive) is connected with baudrate: " + str(baudRate)
                     connected = True 
                     break
                  
         except Exception as inst:
            print ("getDeviceType got exception: " + str(inst)) 
            line = ""
            break 
   except Exception as inst:
      pass 
   closePort (serialPort)
   return connected
   
def getDeviceType (port): 
   global gpsConnected
   global obdConnected
   global gpsPort
   global gpsBaud
   
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
      if canConnectGps (port, 4800): 
         deviceType = "gps$"
         gpsPort = port 
         gpsBaud = 4800
      elif canConnectGps (port, 9600):
         deviceType = "gps$"
         gpsPort = port 
         gpsBaud = 9600
         
   #if deviceType == "":             
   #   deviceType = "obd"         
   #   deviceType = ""
   
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
   
# ttyUSB is used by one of the gps devices and 
# by the obd connection      
# ttyACM is used by the other (cheaper) gps device
def findConnectedDevices():
   global ports 
   global obdConnected
   global gpsConnected
   global obdConnection
   
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
               
      if portsContains ("obd"):
         if not obdConnected:  
            obdConnected = True
            print ("Connecting Async")
            try:
               obdConnection = obd.Async()
               obdConnection.watch (obd.commands.RPM, callback=showRpm)
               obdConnection.watch (obd.commands.SPEED, callback=showSpeed)
               obdConnection.watch (obd.commands.OIL_TEMP, callback=showOil)
               #obdConnection.watch (obd.commands.ELM_VOLTAGE, callback=showVoltage)
               obdConnection.watch (obd.commands.GET_DTC, callback=showDtc)
               obdConnection.start()           
            except Exception as inst:
               print ("Trouble with obd, disconnect and reconnect " + str(inst))
               
      elif obdConnected:
         obdConnected = False      
         try: 
            print ("Disconnecting obd")
            obdConnection.stop()
            obdConnection = None
         except:
            pass
         
      gpsConnected = portsContains ("gps")
      
   except Exception as inst:
      print ("findConnectedDevices got exception: " + str(inst)) 
    
   if len(ports) != numDevices:       
      print ("Found " + str(len(ports)) + " devices" )
      print (str(ports))
   return ports
 
# obd and cheaper gps is on ttyUSB ports 
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
   files = []
   print ("Look for files in : " + path) 
   try: 
      files = os.listdir (path)     
      print ("getfilenames Found files: !" + str(files) + "!")
   except Exception as ex:
      print ("ERR:   Could not find this path: " + path );
      print ("It is possible you need mkdir /vrrx")
   return files
   
'''
def scrollY():
   global DISPLAYSURF

   offsetY = 28
   width,height = DISPLAYSURF.get_size()
   copySurf = DISPLAYSURF.copy()
   DISPLAYSURF.blit(copySurf, (0,offsetY))
   #DISPLAYSURF.blit(copySurf, (0,0), (0,height-offsetY,width,offsetY))
'''   

def sendLines (lines):   
   global DISPLAYSURF
   global BIGFONT
   
   DISPLAYSURF.fill((BLACK)) # Clear the screen   
   x = 0
   y = 10
   count = 0
   for line in lines:
      if count == 0: 
         sendLine (line,y,LITTLEFONT )
         y = y + 22
      elif y < 320:
         sendLine (line,y,BIGFONT)
         y = y + 28
      count = count + 1
   pygame.display.update()
      
def sendLine(line, y, font):
   global DISPLAYSURF
   global pygame

   print (line)
   msgSurf = font.render(line, True, WHITE, BLUE)
   msgRect = msgSurf.get_rect()
   msgRect.topleft = (20, y)
   DISPLAYSURF.blit(msgSurf, msgRect)
   pygame.display.update()
   
def sendMsg (msg):   
   global BIGFONT
   global LITTLEFONT
   global WINDOWHEIGHT
   global printY
   global displayLines
   lines = msg.split ( '\n' )   
   
   for line in lines:
      if line.strip() != '': 
         if len(displayLines) == 0: 
            displayLines.insert (0, line)
         else:
            if line.find ( '.' ) > -1: 
               line = getTime() + '   ' + line
               
            displayLines.insert (1, line )
            
   sendLines (displayLines)
    
def getTime(): 
   global gpsConnected
   
   if gpsConnected and (gpsTime != ""): 
      theTime = gpsTime
   else:
      theTime = getLocalTime()     
   return theTime
    
def getLocalTime():
   t = str(datetime.datetime.now().time())
   ind = t.find ( ".")
   if ind > -1:
      t = t[0:ind]
   # print ("Got a localtime: " + t)
   return t
 
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
                break
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

def getMountPoint(id='/dev/sd'):
    p = subprocess.Popen ( ['cat', '/proc/mounts'], stdout=subprocess.PIPE)
    out,err = p.communicate()
    lines = out.split ( '\n' )
    mountPoint = '';
    for line in lines:
        if line.find (id) > -1:
           vals = line.split ( ' ' );
           mountPoint = vals[1]
           
    
    #if mountPoint != '':
    #    print ( 'getMountPoint: ' + mountPoint )
        
    return mountPoint
             
def usbInserted():
    global usbInsertedFlag    
    mp = getMountPoint()    
    usbInsertedFlag = (mp != '')
    if usbInsertedFlag:
       time.sleep (2.0)
    return mp

def osCmd (cmd):
   print ("osCmd(" + cmd + ")" )
   try:
      os.system (cmd)
   except Exception as inst:
      print ("Could not execute: " + cmd + " because: " + str(inst) )

def checkForUsbDrive():
   global quit
   global usbInsertedFlag
   global usbFlags
   global usbPath
   
   print ("checkForUsbDrive started")
   msg = ""
   lclUsbInserted = False    
   while not quit:
      time.sleep (0.5)
      mp = usbInserted()
      if mp != '':
         if not lclUsbInserted:
            lclUsbInserted = True
            print ("Detected USB inserted" )
            files = getFilenames ("/vrrx")
            returnCode = 0            
            if len(files) > 0:
               if not os.path.exists (mp + usbPath): 
                  sendMsg("Making " + mp + usbPath )
                  os.makedirs ( mp + usbPath )
               else:
                  sendMsg ( mp + usbPath + ' exists already' )
            
               for file in files:
                  try: 
                     cmd = "cp /vrrx/" + file + " " + mp + usbPath + file
                     returnCode = os.system (cmd)
                     if returnCode != 0: 
                        sendMsg ( "bad path " + usbPath) 
                        break
                     else:
                        print ("Successfully executed: " + cmd)
                        # os.system ("ls")
                        time.sleep (0.5)
                  except Exception as inst:
                     print ("Could not " + cmd + " because: " + str(inst) )
                     sendMsg ( "bad path " + usbPath) 
                     returnCode = 1
                     break
               if returnCode == 0:
                  if len(files) != 0:
                     print ("rm /vrrx/*")
                     os.system ("rm /vrrx/*")
                     time.sleep (2)
                     for file in files:
                        # only show .dbf files 
                        if (file.lower().find ( '.shp') == -1) and (file.lower().find ('.shx') == -1): 
                           if msg == "": 
                              msg = "USB inserted\n"
                           msg = msg + "  " + usbPath + file + "\n"
                     msg = msg + "Please remove USB\n"
            else:          
               msg = "No files received from AS400\n"
               msg = msg + "Please remove USB\n"
            sendMsg (msg)
      else:
         lclUsbInserted = False

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
            sendMsg ("Please wait while loading missouri map")
            print ("Load Missouri map" )
            moMap = pygame.image.load("mo.jpg").convert()

         DISPLAYSURF.blit (moMap, (-xOffset + addX,-yOffset + addY)) 
      else: # Iowa 
         # (0,0) = Souix Falls South Dakota   
         xOffset = ((long + 96.731667) * 1109) - 400  # increase xOffset to move map to left 
         yOffset = ((43.536389 - lat) * 1430) - (WINDOWHEIGHT/2) + 120 # increase yOffset to move map up
         currentMap = "ia"
         addX = mapOffsets[currentMap][0]
         addY = mapOffsets[currentMap][1]
         if iaMap == None:
            sendMsg ("Loading iowa map")
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
      
      
def checkForCommand():
   global quit
   global usbPath
   global displayLines
   
   while not quit:
      try:
         data = sock.recv (1024)
         print ("Got command: [" + data  + "]")
      except:
         data = ""

      if data != "":
         if data == "quit":
            quit = True
         else:
            parameters = data.split ( ' ' )
            cmd = parameters [0]
            if cmd == "print":
               msg = ' '.join(parameters[1:])
               sendMsg (msg)
            if cmd == "path":
               usbPath = ' '.join(parameters[1:])
               sendMsg ( "path:" + usbPath)
               setPath (usbPath)
            elif cmd == "clear":
               clearScreen()
            else:
               print ("Ignored command: " + cmd )


def extractDateTime (msg): 
   global gpsTime 
   global gpsDate 
	
   #print ("extractDateTime: " + str(msg ))
   
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
   print ("gpsTime: " + gpsTime + " gpsDate: " + gpsDate + " " + str(msg))
   
def parseGPS(line):
    global longitude
    global latitude
    global latLong
    
    goodParse = False
    if line.find ( 'PRMC') > 0: 
        if (latitude != 0) or (longitude != 0): 
           try:
              msg = pynmea2.parse(line)
              extractDateTime (msg)
           except Exception as e:
              print ("Got exception: " + str(e))
    elif line.find('GGA') > 0:
        msg = pynmea2.parse(line)
        if (msg.latitude != 0) and (msg.longitude != 0): 
           print ("lat/long parse yields: [" + str(msg.latitude) + "," + str(msg.longitude) + "]" ) 
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
   global gpsBaud
   
   connected = False
   startTime = time.time()
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
            print ("Opening port " + gpsPort + " to gps device, baudrate: " + str(gpsBaud) )
            serialPort = serial.Serial(gpsPort, baudrate = gpsBaud, timeout = 0.01)
         try:
            line = serialPort.readline()    
            if parseGPS(line):
               currentLocation = (latitude, longitude)
               elapsedTime = time.time() - startTime
               if elapsedTime > 5: 
                  startTime = time.time()
                  feet = haversineFeet ( currentLocation, lastLocation )
                  speed = int (feet / 5280.0 * 3600.00 / elapsedTime)
                  if speed < 3: # ignore mph less than 3 
                     mph = 0                  
                  elif speed < 100:  
                     mph = speed
                     
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
   
   lastMph = ""
   while not quit: 
      if (latitude != 0) and (longitude != 0) and (gpsDate != "") and \
         (gpsTime != "") and ((str(mph) != "0") or (lastMph == "")) : 
         lastMph = str(mph)   
         f = open ("gps.csv", "a+")
         f.write ( str(latitude) + "," + str(longitude) + "," + \
                   str(mph) + "," + str(rpm) + "," + gpsDate + "," + \
                   gpsTime + "\n")
         f.close()         
         for i in range(30): 
            time.sleep (1)
            if quit:
               break
      
      
def clearScreen():
   global DISPLAYSURF
   global printY
   global latitude
   global longitude 
   global gpsConnected
   global gpsTime
   global gpsDate 
   global displayLines 
   
   theTime = getTime()
   
   printY = 10
   DISPLAYSURF.fill((BLACK)) # Clear the screen
   
   # msg = rpm + "rpm " 
   if latitude != 0:
      lat = int(latitude * 100.0)
      long = int(longitude * 100.0)
      header = "[" + str(lat/100.0) + "," + str(long/100.0) + "] " + str(mph) + " mph "
   else:
      header = "[NoLat/Long] " 
      
   if internetConnection:
      header = header + "Internet Detected (Good)"
   else:
      header = header + "No Internet!!!"

   displayLines = []        
   header = header + gpsDate + " " + theTime + "\n"    
   sendMsg ( version + header)
   pygame.display.update()
      
      
def stateMachine():
   global quit
   global latitude
   global longitude
   global usbInsertedFlag
   global internetConnection 
   global deviceConnected
   global DISPLAYSURF
   global BLACK
   global gpsConnected
   global obdConnected
   global connection
   
   state = {'latitude':False, 'usb':False, 'internet':False, \
            'device':False, 'obd': False, 'gps':False, 'mph': 0, \
            'msg': "" }
   lastState = state
   lastTime = time.time()  
   while not quit:  
      state ['latitude']  = (latitude != 0)  
      state ['usb']       = usbInsertedFlag
      state ['internet']  = internetConnection
      state ['device']    = deviceConnected  
      state ['gps']       = gpsConnected
      state ['obd']       = obdConnected      
       
      msg = ""       
      if lastState ['latitude'] != state ['latitude']:    
         if state['latitude']:
            msg = msg + "[Lat/Long] acquired " + str(latitude) + "\n"
         else:
            msg = msg + "[Lat/Long] lost\n" 
         
      if lastState ['usb'] != state ['usb']:    
         if state['usb']:
            msg = msg + "USB detected, copying files...\n"
         else:
            clearScreen()
            msg = msg + "USB removed"
            
      if lastState ['internet'] != state ['internet']: 
         clearScreen()      
         if state['internet']:
            msg = msg + "Internet Detected...Ready!\n"
         else:
            msg = msg + "No Internet Detected...Please wait.\n"
            
      if lastState ['device'] != state ['device']:    
         if state['device']:
            msg = msg + "Device connected\n"
         else:
            msg = msg + "Device removed\n"
       
      if lastState ['obd'] != state ['obd']:    
         if state['obd']:         
            msg = msg + "On board diagnostics connected\n"
         else:
            msg = msg + "On board diagnostics removed\n"
       
      if lastState ['gps'] != state ['gps']:    
         if state['gps']:
            msg = msg + "GPS device connected\n"
         else:
            msg = msg + "GPS device removed\n"
       
      state['mph'] = mph # update mph 
      
      if msg != "":
         print ("stateMachine adding msg: " + msg )
         sendMsg (msg)      
         
      lastState = copy.deepcopy(state) 
      time.sleep (0.5)        
      
if not fileExists ("gps.csv"): 
   f = open ("gps.csv","w")
   f.write ( "Latitude,Longitude,Mph,Rpm,Date,Time\n")
   f.close 

getPath()
   
# gpsTime = extractTime (datetime.datetime.now(), False)
getUsbFlags(usbFlags)

t = Thread(target=checkForUsbDrive)
t.start()

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

t7 = Thread(target=logGps)
t7.start()

t8 = Thread(target=checkForUsbDevice)
t8.start()

clearScreen()
sendMsg ( "Starting...")
pygame.display.update()
   
checkForCommand()
pygame.quit()
sock.close()
try:
   obdConnection.stop()
except:
   pass
print ("Done in sshBackdoor.py")
