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
import re

# import obd
from math import radians, cos, sin, asin, sqrt, atan2, degrees, trunc

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BLUE       = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255,   0,   0)

whichAdapter = 'wlan0'

def getLocalAddress ():
  global whichAdapter
  ipAddress = '192.168.0.X'
  line = os.popen("/sbin/ifconfig " + whichAdapter).read().strip()  
  p = re.findall ( r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', line )
  if p: 
     ipAddress = p[0]   
     
  return ipAddress 

def sendLine(line, y, font):
   global DISPLAYSURF
   global pygame
   print (line)
   msgSurf = font.render(line, True, WHITE, BLUE)
   msgRect = msgSurf.get_rect()
   msgRect.topleft = (20, y)
   DISPLAYSURF.blit(msgSurf, msgRect)
   
   
pygame.init()
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
LITTLEFONT = pygame.font.Font('freesansbold.ttf', 16)
DISPLAYSURF = pygame.display.set_mode ((0, 0), pygame.FULLSCREEN)
pygame.display.update()      
sendLine ( getLocalAddress(), 20, BIGFONT )
pygame.display.update()
time.sleep (10)
pygame.quit()
