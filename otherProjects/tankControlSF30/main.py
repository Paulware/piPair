import SF30
from threading import Thread

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
import RPi.GPIO as GPIO
import time
from socket import *
import os 

import random, sys, pygame
from pygame.locals import *

os.environ['SDL_AUDIODRIVER'] = 'dsp'
#LCD = LCD_1in44.LCD()
sf30 = SF30.SF30()

def checkKey (pin,msg, LCD):
   if GPIO.input(pin) == 0:
      showText (msg,LCD)
      print msg
      while GPIO.input(pin) == 0:         
         time.sleep (0.01)
 
def showText (msg,LCD):
   image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
   draw = ImageDraw.Draw(image)
   print "***draw text"
   draw.text((33, 22), msg, fill = "BLUE")
   
def sendMsg (message): 
   try: 
      port = 3333
      sock = socket(AF_INET, SOCK_DGRAM)
      sock.bind (('',0)) # bind to any old port 
      sock.setsockopt (SOL_SOCKET, SO_BROADCAST, 1)
      sock.sendto(message, ('192.168.4.255', port)) # broadcast to all devices listening on port 3333
      print 'Sent ' + message          
   except Exception as inst:
      print str(inst)   
      
def main():
   pygame.init()
   MAINCLOCK = pygame.time.Clock()
   DISPLAYSURF = pygame.display.set_mode((480, 320))
   pygame.display.toggle_fullscreen()    
   pygame.display.set_caption('Tanky')
   DISPLAYSURF.fill ((255,255,255))
   #FONT = pygame.font.Font('freesansbold.ttf', 16)
   #BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

   # Set up the background image.
   #boardImage = pygame.image.load('battleBlock.bmp')
   # Use smoothscale() to stretch the board image to fit the entire board:
   #boardImage = pygame.transform.smoothscale(boardImage, (480,320))
   #boardImageRect = boardImage.get_rect()
   #boardImageRect.topleft = (0, 0)
   image = pygame.image.load('flower.bmp')
   # Use smoothscale() to stretch the background image to fit the entire window:
   #BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (480,320))
   #BGIMAGE.blit(boardImage, boardImageRect)
   DISPLAYSURF.blit (image, (0,0))
   pygame.display.update()

   
   while not sf30.joystick_detected:
      time.sleep (1.0)
      print ("Waiting for joystick " )      
   
   print "**********Start**********"
   
   buttonTimeout = time.time()
   
   lastCommand = ""
   white = (255,255,255)
   while True: 
       event = sf30.read()
       msg = sf30.tank()
       
       if event == sf30.START_PRESSED:   
          break
       elif event == sf30.SELECT_PRESSED:
          break
          
       if msg != lastCommand:
          print msg
          lastCommand = msg
          
          image = None
          if msg.find ( 'F' ) > -1:
             image = pygame.image.load('tankFire.jpg')
             print ("Showing image tankFire yo")
          elif msg.find ( 'LR' ) > -1:
             image = pygame.image.load('upArrow.jpg')            
          elif msg.find ( 'lr' ) > -1:
             image = pygame.image.load('downArrow.jpg')
          elif msg.find ( 'L') > -1:
             image = pygame.image.load('rightArrow.jpg')
          elif msg.find ( 'R') > -1:
             image = pygame.image.load('leftArrow.jpg')
          elif msg.find ( 'T' ) > -1:
             image = pygame.image.load('rightArrow.jpg' )
          elif msg.find ( 't' ) > -1:
             image = pygame.image.load('leftArrow.jpg' )
          elif msg.find ( 'V' ) > -1:
             image = pygame.image.load('upArrow.jpg' )
          elif msg.find ( 'Ss' ) > -1: 
             image = pygame.image.load('stop.jpg' )
             
          if image != None:
             DISPLAYSURF.fill (white)
             DISPLAYSURF.blit (image, (0,0))
             pygame.display.update()
                       
          sendMsg (msg)
       
	
if __name__ == '__main__':
   try:
    main()
   except Exception as ex:
     sf30.close()
     print("exception " + str(ex))
#	GPIO.cleanup()