import socket
import select
import pygame
import time
import datetime
from pygame.locals import *

class inputOutput:      
   UDPTIMEOUT = 0.5 # Maximum time it takes for other unit to respond
   udpTimeout = time.time() + UDPTIMEOUT
   lastMessage = "First, null message"    
   udpCount = 0
   udpMessages = [] 
   acks = [] 
   messageStartTime = time.time() 
   waitingCount = 0   
   myIpAddress = socket.gethostbyname(socket.gethostname())
   UDPPORT = 3333   
   tcpSocket = None
   tcpConnection = None

   
   def __init__(self,utilScreen):
      self.move = None
      self.games = []
      self.opponentDeck = [] 
      self.dealtHand = []   

      # Setup the UDP client socket
      self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP    
      self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

      self.client.bind(("", self.UDPPORT)) 
      self.client.setblocking(0) # turn off blocking 
      self.commLog = open ( file='udp.log', mode='wb', buffering=0 )
             
      self.utilScreen = utilScreen
      
   def __del__(self):
      try:         
         self.commLog.close()
         if self.tcpConnection != None:
            self.tcpConnection.close()     
      except Exception as ex: 
         print ( 'Trouble in inputOutput.__del__ because: ' + str(ex) )       
         
   def waitFor (self, caption, pollEvent):             
      sprites = self.utilScreen.basicScreen ( caption,['quit'] )
      
      pollEvent = 'self.ready=(' + pollEvent + ')'
      print ( 'waitFor pollEvent: [' + pollEvent + ']' )
      self.ready = False
      while not self.ready:
         exec (pollEvent, locals()) 
         # print ( 'Executing: ' + pollEvent ) 
         eventType,data,addr = self.getKeyOrUdp()    
         if eventType == pygame.MOUSEBUTTONDOWN:          
            sprite = self.utilScreen.getSpriteClick (data,sprites) 
            if sprite != -1: 
               break         
                       
   def commLogWrite (self,message): 
      self.commLog.write ( str.encode (message) )    

   def udpBroadcast (self,message):       
      try: 
         message = str(len(self.udpMessages)) + ':' + message
         print ('udpBroadcast: [' + message + ']')
         self.udpMessages.append (message) 
         self.messageStartTime = time.time()
                     
      except Exception as ex:
         print ( "udpBroadcast could not send: [" + message + "] because: " + str(ex))       

   def sendTo (self,message): 
      try: 
         self.commLogWrite ( str(datetime.datetime.now().time()) + ':send:' + message + '\n')
         self.client.sendto(str.encode(message), ('192.168.4.255', self.UDPPORT))
      except Exception as ex: 
         self.commLogWrite ( str(ex) + '\n') 
             
   def getKeyOrUdp(self):
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
     move = None
     
     while data == '':
       if time.time() > self.udpTimeout:  
          if len(self.udpMessages) > len (self.acks): # Some messages have not been acked.
             print ( 'udpTimeout [len(udpMessages),len(acks)]: [' + \
                  str(len(self.udpMessages)) + ',' +  str(len(self.acks)) + \
                  '] elapsedTime: ' + str(time.time() - self.messageStartTime))    
             message = self.udpMessages [len(self.acks)]
             self.sendTo (message )
             self.waitingCount = self.waitingCount + 1
             self.udpTimeout = time.time() + (self.UDPTIMEOUT * self.waitingCount)
             print ( 'Sending: ' + message + ' waitingCount: ' + str(self.waitingCount))
             if self.waitingCount >= 100:
                print ( 'Wondering if other player is actually there still?' )
          else:
             self.waitingCount = 0       
             self.udpTimeout = time.time() + self.UDPTIMEOUT
                   
       rightClick = False
       
       ev = pygame.event.get()
       for event in ev:
          if event.type == VIDEORESIZE:
             DISPLAYSURF = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
          elif event.type == pygame.KEYDOWN:
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
          if self.tcpConnection != None: 
             i,o,e = select.select ([self.tcpConnection], [], [], 0.0001)
          elif self.tcpSocket != None:
             i,o,e = select.select ([self.tcpSocket], [], [], 0.0001)
          else: #udp
             i,o,e = select.select ([self.client], [], [], 0.0001)
             
          for s in i:
             if s == self.client:
                data, addr = self.client.recvfrom (1024)
                data = data.decode();
                addr = str(addr[0])
                if (addr == '192.168.4.1') and (self.myIpAddress == '127.0.1.1'): 
                   data = ''
                elif (addr == self.myIpAddress):
                   data = ''
                else:  
                   print ( '[addr,myIpAddress]: [' + addr + ',' + self.myIpAddress + ']' )
                   ind = data.find ( ':' )
                   if data != '':
                      if data[0:3] == 'ack': # I received an ACK of a previous send
                         ackCount = data[4:] 
                         ackCount = int(ackCount)
                         if ackCount == len(self.acks): 
                            self.acks.append (data)
                         self.commLogWrite ( str(datetime.datetime.now().time()) + ' Got an ' + data + '\n')
                         data = '' # Do not send this forward
                      else:                       
                         udpCount = int(data[0:ind])
                         message = 'ack:' + str(udpCount) 
                         if data != self.lastMessage: 
                            # print ( '[lastMessage,data]: [' + self.lastMessage + ',' + data + ']' )
                            self.commLogWrite ( str(datetime.datetime.now().time()) + ':rcv:' + data + ' from: ' + addr + '\n')
                            
                         print ( 'acking...[' + message + '] lastMessage: [' + self.lastMessage + ']')                         
                         self.sendTo (message) 
                         if data != self.lastMessage:                             
                            self.lastMessage = data
                            data = data[(ind+1):]                   
                            ind = data.find ( 'exec:')
                            if ind > -1: # joining=, self.games=, self.move=, self.opponentDeck
                               command = data[ind+5:]
                               exec (command, locals())
                               print ( 'Executing command: ' + command ) 
                                  
                            typeInput = 'udp'                        
                         else:
                            print ( 'Not executing this message: [' + data + '] because it is identical to the last message' )                      
                   
             elif s == self.tcpConnection: 
                data, addr = self.tcpConnection.recvfrom (1024)
                data = data.decode();
                #print ("Received tcp data:" + data)
                addr = str(addr[0])
                typeInput = 'tcp'
             elif s == self.tcpSocket:
                data, addr = self.tcpSocket.recvfrom (1024)
                data = data.decode();
                #print ("Received tcp data:" + data)
                typeInput = 'tcp'
                addr = str(addr[0])
                
       if (data == '') and (time.time() > timeEvent): 
          addr = socket.gethostbyname(socket.gethostname())
          if (self.myIpAddress != addr ): 
             self.commLogWrite ( str(datetime.datetime.now().time()) + ':change ip address to: ' + addr + '\n') 
             self.myIpAddress = addr       
          typeInput = 'time'
          data = ' '
          addr = 'clock'  
          
     # print ( 'returning typeInput: ' + str(typeInput))   
     return typeInput,data,addr
    
if __name__ == '__main__':
    host = True
    import sys
    if len(sys.argv) > 1:
       param1 = sys.argv[1]
       print ( 'got param1: ' + param1 + ']' )
       if param1 == 'False':
          host = False
    else:    
       print ( 'No param1' )
       
    print ('host: ' + str(host) ) 
       
    try:
       pygame.init()
       DISPLAYWIDTH = 800
       DISPLAYHEIGHT = 600
       DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)       
       import utilityScreens
       utilityScreens = utilityScreens.utilityScreens (DISPLAYSURF)
       myIO = inputOutput(utilityScreens)
       
       if host:
          indexes = [0,1,2,3]          
          myIO.udpBroadcast ( 'exec:self.dealtHand=' + str(indexes) )  
          typeInput, data, addr = myIO.getKeyOrUdp() 
          print ( '[typeInput,data,addr]: [' + str(typeInput) + ',' + str(data) + ',' + addr + ']' )
       else:
          myIO.waitFor ('Wait for opponent to deal their hand', 'self.dealtHand != []' ) 
       
    except Exception as ex:
       print ( "Got exception: " + str(ex)) 
    finally:
       print ( 'finally complete' )