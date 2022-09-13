import pygame
#import time
import subprocess
import os
import socket
import select
from Utilities import Utilities
from Pages import Pages
from Communications import Communications
import platform

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

print ("pygame.init")
pygame.init()
print ("get the clock")
MAINCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1200, 800))
FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
#pygame.display.toggle_fullscreen()      
pygame.display.set_caption('Flippy')
utilities = Utilities (DISPLAYSURF, BIGFONT)
pages = Pages(DISPLAYSURF, utilities, platform.system()=='Windows') 
name = 'laptop' if (platform.system() == 'Windows') else 'pi7'
comm = Communications ('messages', 'localhost', name ) # '192.168.4.1', name )
comm.connectBroker()
print ( 'Back from connectBroker' )
utilities.comm = comm
pages.comm = comm
pages.mainPage()