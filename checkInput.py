import pygame
import subprocess
import os
import socket
import select
import math
import time
import sys
import platform

print ( "platform: " + platform.platform() )
if platform.platform().find ( 'Linux' ) > -1: 
   import termios
   import tty
   import curses
print ("Done imports" )
   
def getCh():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  ch = ''
  try:
     tty.setraw(sys.stdin.fileno())
     ch = sys.stdin.read(1)
  finally:
     termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
  return ord(ch)

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
  timeEvent = time.time() + 0.01
  while data == '':
    ev = pygame.event.get()
    for event in ev:  
       print ( "Got event: " + str(event) ) 
       if event.type == pygame.KEYDOWN:
          print( "Got a keydown with value: " + str(event.key) )
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
             if (addr == '192.168.4.1') and (myIpAddress == '127.0.1.1'): 
                print ( 'Ignore udp message: [' + data + '] from me' )
                data = ''
             elif (addr == myIpAddress):
                print ( "Ignoring udp message [" + data + "] from me" )
                data = ''
             else:  
                print ( 'addr: ' + addr + ' myIpAddress: ' + myIpAddress)
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
    
    if (data == ''):       
       if platform.platform().find ( 'Linux' ) > -1:
          ch = screen.getch()
          print ("ch: " + str(ch) )
          data = str(ch)
          print ( "Got data: [" + str(ord(data[0])) + str(ord(data[1]))  + "]" )
    
    
    if (data == '') and (time.time() > timeEvent): 
       typeInput = 'time'
       data = ' '
       addr = 'clock'  
       
  # print ( 'returning typeInput: ' + str(typeInput))   
  data = str(ord(data)) 
  return (typeInput,data,addr)
  
tcpConnection = None
tcpSocket = None
# Setup the UDP client socket
UDPPORT = 3333
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP    
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", UDPPORT)) 
client.setblocking(0) # turn off blocking  

try:
   print ( "find Linux again" )
   if platform.platform().find ( 'Linux' ) > -1: 
      screen = curses.initscr()
      screen.keypad(True)

   print ( "Start while loop" )   
   pygame.init()  
   while True: 
      (eventType,data,addr) = getKeyOrUdp()
      
except Exception as ex:
   print ( "Exception: " + str(ex)) 
   
finally:
   print ( "Done yo" )
   if platform.platform().find ( 'Linux' ) > -1: 
      curses.nocbreak()
      screen.keypad(0)
      curses.echo()
      curses.endwin()   
