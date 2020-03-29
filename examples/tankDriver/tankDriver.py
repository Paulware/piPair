from socket import *
import re
import os
import time
import sys
import buttonClass
import imageClass
import eventClass
import pygame
import glob
import serial
from pygame.locals import *
from threading import Thread
quit = False
btConnected = False

def getLocalAddress ():
  line = os.popen("/sbin/ifconfig wlan0").read().strip()  
  p = re.findall ( r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', line )
  if p: 
     ipAddress = p[0]  
  
  return ipAddress 
  
def getBroadcastAddress ():
  address = getLocalAddress()
  index = address.rfind ('.')
  addr = address[0:index] + '.255'
  # print ("BroadcastAddress: " + str(addr))
  return addr  

def sendMsg (message): 
   try: 
      port = 3333
      sock = socket(AF_INET, SOCK_DGRAM)
      sock.bind (('',0)) # bind to any old port 
      sock.setsockopt (SOL_SOCKET, SO_BROADCAST, 1)
      destination = getBroadcastAddress() # '192.168.0.255'  
      sock.sendto(message, (destination, port)) # broadcast to all devices listening on port 3333
      print 'Sent ' + message + ' to ' + destination + ':' + str(port) + '\n'         
   except Exception as inst:
      print str(inst)
      
pygame.init()
events = eventClass.EventClass()
image = imageClass.ImageClass()
buttons = buttonClass.ButtonsClass(0)
speed = 5
FPS = 60 
fpsClock = pygame.time.Clock()
image.draw ('stop.jpg', 300, 150)
lastCommand = ""
command = ""
globTimeout = time.time() + 3
serialPort = None
buttonTimeout = time.time()
while True: 
    try:    
       if time.time() > globTimeout: 
          globTimeout = time.time() + 3
          globs = glob.glob ( '/dev/ttyUSB0')
          if len(globs) > 0:
             if not btConnected:
                print ("Blue Tooth now connected" )
                baudRate = 9600
                serialPort = serial.Serial(globs[0], baudrate = baudRate, timeout = 0.01)
             btConnected = True
          else:
             if btConnected:
                print ("Blue Tooth now disconnected" )
                serialPort.close()
             btConnected = False
             
       image.clear()       
          
       if time.time() > buttonTimeout: 
          buttonTimeout = time.time() + 0.2
          if buttons.checkKey ("Start"):
             break                   
          if buttons.checkKey ("Select"):
             #msg = 'server ' + getLocalAddress() 
             #sendMsg (msg)
             if btConnected:
                print ( 'Sending ! to device' )
                serialPort.write ( '!' );
             time.sleep (2)                                
          if buttons.checkKey ("Right"):
             command = "right"
             image.draw ('rightArrow.jpg', 300,150)
             if btConnected:
                serialPort.write ( 'd' );
          elif buttons.checkKey  ("Left"): 
             image.draw ('leftArrow.jpg', 300, 150)
             command = "left"
             if btConnected:
                serialPort.write ( 'a' );
          elif buttons.checkKey ("Up"):
             image.draw ('upArrow.jpg', 300, 150)
             command = "forward"
             if btConnected:
                serialPort.write ( 'w' );
          elif buttons.checkKey  ("Down"): 
             image.draw ('downArrow.jpg', 300, 150)
             command = "reverse"
             if btConnected:
                serialPort.write ( 's' );
          elif buttons.checkKey ("X"): 
             command = "X"
             image.draw ('upArrow.jpg', 300, 150)          
          elif buttons.checkKey ("Y"):
             command = "Y"
             image.draw ('downArrow.jpg', 300, 150)
          elif buttons.checkKey ("TL"):
             command = "TL"
             if btConnected:
                serialPort.write ( 'l' );
          elif buttons.checkKey ("TR"):
             command = "TR"
             if btConnected:
                serialPort.write ( 'r' );
          elif buttons.checkKey ("Press"):
             command = ""
             sendMsg ("fire")
             if btConnected:
                serialPort.write ( 'f' );
             time.sleep (0.5)          
          elif buttons.checkKey ("A"): 
             #soundObj = pygame.mixer.Sound('artillery.wav')
             #soundObj.play()
             command = ""
             sendMsg ("A")
             time.sleep (0.5)
          elif buttons.checkKey ("B"): 
             #soundObj = pygame.mixer.Sound('carHorn.wav')
             #soundObj.play()       
             command = ""
             sendMsg ("B")
             time.sleep (0.5)
          else:
             command = ""
             if (lastCommand != "A") and (lastCommand != "B") and \
                (lastCommand != "fire"): 
                if btConnected:
                   image.draw ('stopBt.jpg', 300,150) 
                   serialPort.write ( 'S' );
                else:
                   image.draw ('stop.jpg', 300,150) 
                command = "stop"
          
          if (command != lastCommand) and (command != ""):
             sendMsg (command)          
             lastCommand = command 
          
       image.show() 
       pygame.display.update()
       fpsClock.tick(FPS)    
    except Exception as inst:
       print (str(inst) )
       quit = True
       break
       
pygame.quit()
quit = True
serialPort.close()
