try: 
   import paho.mqtt.client as mqtt
except Exception as ex:
   print ( 'pip install paho-mqtt' )
   exit(1)
   
import threading 
import time
import sys

class Communications: 
   def acknowledge ( self, destination):   
      self.publish (destination, 'ACK', self.count)  # self.count is probably not correct here.  Don't care?   

   def connectBroker (self): 
      ok = True 
      if not self.debug: 
         try:
            print ( 'Connect to: ' + self.broker )
            self.client.connect(self.broker, 1883, 30)
         except Exception as ex:
            print ( 'Could not connect to ' + self.broker + '  because: ' + str(ex))
            print ( 'Make sure that the mosquito broker is running...' )
            ok = False 
            exit(1)
      
         self.thread = threading.Thread(target=self.client.loop_forever, args=())
         self.thread.start()
         self.target = ''
         self.waitConnected()
      return ok 

   def disconnect (self): 
      print ( 'Disconnecting.' )         
      try: 
         self.publish (self.target, 'disconnect yo', self.count)
         self.client.disconnect();
      except Exception as ex:
         print ( 'Could not disconnect because: ' + str(ex)) 
      print ( 'Done in disconnect' )

   def empty (self): 
      return (self.head == self.tail)

   def __init__ (self,topic,broker,name):
      ok = True 
      self.name = name
      print ( 'My name is : ' + self.name )
      self.count = 0
      self.ack = False
      self.client = mqtt.Client()
      self.topic = topic
      self.broker = broker
      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message
      self.connected = False
      
      # set the will (last testament) message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients      
      message = '{\"id\":0, \"from\":\"' + self.name + '\",\"to\":\"*\", \"message\":\"Off\"}'
      self.client.will_set(topic, message.encode())
      self.message = '' 
      self.target = ''
      self.buffer = ['','','','','','','','','','']
      self.head = 0
      self.tail = 0
      
      self.debug = False 
      self.quit = False

   def isReady (self): 
      return self.message != ''   
      
   def peek (self):
      message = ''
      print ( ' in peek, self.tail: ' + str(self.tail) )
      if self.empty(): 
         print ( 'Nothing to return in peek' );
      else:
         message = self.buffer[self.tail]
         print ( 'in peek, return [' + message + ']' )
         
      return message
  
   def pop (self):
      value = self.peek()        
      self.tail = self.tail if self.empty() else (self.tail + 1) % 10
      print ( 'Returning from pop ' )
      return value
      
   def publish (self,destination,message,id):
      message = '{\'id\':' + str(id) + ',\'from\':\'' + self.name + '\',\'to\':\'' + destination + \
                '\',\'message\':\'' + message + '\'}'  
      print ( 'Publish [topic,payload]: [' + self.topic + ',' + message + ']' )
      self.client.publish(self.topic, payload=message, qos=0, retain=False)
      
   def on_connect(self,client, userdata, flags, rc):
      print(f"Connected with result code {rc}, subscribe to " + self.topic)
      # subscribe, which need to put into on_connect
      # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
      self.client.subscribe(self.topic)
      self.connected = True 
  
   # the callback function, it will be triggered when receiving messages
   def on_message(self, client, userdata, msg):
       message = msg.payload.decode()
       try: 
          info = eval (message) 
       except Exception as ex:
          print ( 'Could not eval: [' + message + '] because ' + str(ex)) 
          exit(1)
       print ( 'message: ' + message + ' info: ' + str(info)) 
       fromName = info['from']
       toName   = info['to']
       msg      = info['message']
       
       if (toName != self.name) and (toName != '*') :
          print ( 'This message (' + msg + ') is for: ' + toName + ' not me (' + self.name + ')') 
       else:
          if msg == 'ACK': 
             self.ack = True 
             self.count = self.count + 1 
          else:
             print ( 'RCVD ' + msg + ' from ' + fromName ) 
             self.message = msg
             # print ( 'This is for me, and not an ACK so ack it' )
             self.acknowledge ( fromName)
             print ( 'Append ' + msg + ' to the message buffer ' ) 
             self.push (msg)
       
   def push (self,value): 
      print ( 'self.buffer[' + str(self.head) + '] = ' + value )
      self.buffer[self.head] = value
      self.head = (self.head + 1) % 10
      print ( 'self.head = ' + str(self.head) ) 
  
   def read (self): 
      value = self.message 
      self.message = ''
      return value
      
   def setTarget (self,target): 
      self.target = target
      print ( 'Target is now set to: ' + target )
      
   def send ( self, message):
      if self.target == '': 
         raise Exception('Communication.target not set, use setTarget')
      else:
         print ( 'comm.send [' + message + ']' )
         while True: 
            self.publish (self.target, message, self.count)         
            if self.waitAck (): 
               self.count = self.count + 1 
               break
            else:
               print ( 'Re publish message: ' + message)
      
   def stop(self):
      self.quit = True
      self.client.loop_stop()
      self.disconnect()
      print ( '***Done in Communications.stop***' )
          
   def waitAck (self): 
      if self.debug:
         ack = True
      else:
         ack = False       
         # Wait for ack...
         # print ( 'Block...Waiting for an ACK...' )
         endTime = time.time() + 10
         while not ack:
            if self.ack:
               ack = True 
               break
            else:
               if time.time() > endTime: 
                  break         
               time.sleep (1)
         if ack:         
            print ( 'ACK Received' )
         else:
            print ( '***ERR No ack received ***' ) 
      return ack
      
   def waitConnected (self):
      print ( '***Communications...Wait to get connected' )
      while not self.connected and not self.quit: 
         time.sleep (0.1) 
      print ( '***Communications done in waitConnected' )
  
   def waitFor ( self, message):
      print ( 'Waiting for: [' + message + ']' )   
      while not self.quit: 
         if not self.empty(): 
            msg = self.pop()
            if msg.find (message) > -1: 
               print ( 'comm.waitFor found: ' + message + ' in ' + msg)
               break
      print ( 'Received: [' + message + ']' ) 
      
   def gotPeek (self,message): 
      peeked = False
      if not self.empty(): 
         msg = self.peek()
         if msg.find (message) > -1: 
            print ( 'comm.waitFor found: ' + message + ' in ' + msg)
            peeked = True 
         else:
            print ( 'Got message: [' + msg + '] looking for: [' + message + ']')
      return peeked 
      
   def waitForPeek ( self, message):    
      while True: 
         if gotPeek (message):
            break         
               
if __name__ == "__main__":
   import time
   try: 
      import pygame
   except Exception as ex: 
      print ( 'pip install pygame' )
      exit(1)
   from Utilities import Utilities
   pygame.init()
   DISPLAYSURF = pygame.display.set_mode((200, 70)) # make a little screen so pygame will work
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   utilities = Utilities(DISPLAYSURF, BIGFONT)  
   userMessage = ''            

   if len(sys.argv) == 1: 
      broker = 'localhost'
      myName = 'pi7'
      target = 'laptop'
   elif len(sys.argv) != 4:
      print ( 'Note mosquitto should be installed and running' )
      print ( 'Usage: python3 Communications.py broker myName targetName' )
      print ( 'python3 Communications.py localhost pi7 laptop' )
      exit(1)
   else:
      broker = sys.argv[1]
      myName = sys.argv[2]
      target = sys.argv[3]          
      
   topic = 'messages'
      
   try: 
      print ( 'I am ' + myName + ' talking to: ' + target ) 
      comm = Communications (topic,broker,myName);
      if comm.connectBroker(): 
         comm.setTarget (target)            
         quit = False 
         print ( 'Ready to accept test commands 1,2,q' )
         while not quit:  
            events = utilities.readOne()
            for ev in events: 
               (event, data, addr ) = ev
               if (event == 'keypress'):
                  if (data == '1'): 
                     print ( 'send dealuno' )
                     comm.send ( 'join uno')                       
                  elif (data == '2'): 
                     print ( 'Output test data for command 2' ) 
                  elif (data == 'q'): 
                     quit = True
                     
               if utilities.message != '': 
                  print ( 'handle message : [' + utilities.message + ']' )               
                  comm.send(utilities.message )
                  if utilities.message == 'quit': 
                     break
                  utilities.message = ''
      else:
         print ( 'Could not initialize Communications')
         
   finally:
      comm.disconnect()      
