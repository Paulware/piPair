try: 
   import paho.mqtt.client as mqtt
except Exception as ex:
   print ( 'pip install paho-mqtt' )
   exit(1)
   
import threading 
import time
import sys

class Communications: 
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
      
   def waitFor ( self, message):
      print ( 'Waiting for: [' + message + ']' )   
      while True: 
         if not self.empty(): 
            msg = self.pop()
            if msg.find (message) > -1: 
               print ( 'comm.waitFor found: ' + message + ' in ' + msg)
               break
      print ( 'Received: [' + message + ']' ) 
      
   def waitForPeek ( self, message):    
      while True: 
         if not self.empty(): 
            msg = self.peek()
            if msg.find (message) > -1: 
               print ( 'comm.waitFor found: ' + message + ' in ' + msg)
               break
            else:
               print ( 'Got message: [' + msg + '] looking for: [' + message + ']')
                                    
   def empty (self): 
      return (self.head == self.tail)

   def push (self,value): 
      print ( 'self.buffer[' + str(self.head) + '] = ' + value )
      self.buffer[self.head] = value
      self.head = (self.head + 1) % 10
      print ( 'self.head = ' + str(self.head) ) 
  
   def peek (self):
      print ( ' in peek, self.tail: ' + str(self.tail) )
      return '' if self.empty() else self.buffer [self.tail]
  
   def pop (self):
      value = self.peek()        
      self.tail = self.tail if self.empty() else (self.tail + 1) % 10
      print ( 'Returning from pop ' )
      return value
      
   def isReady (self): 
      return self.message != ''   
      
   def read (self): 
      value = self.message 
      self.message = ''
      return value
      
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

   def setTarget (self,target): 
      self.target = target
      print ( 'Target is now set to: ' + target )
      
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
            print ( 'ERR No ack received' ) 
            exit()         
      return ack
   
   def publish (self,destination,message,id):
      message = '{\'id\':' + str(id) + ',\'from\':\'' + self.name + '\',\'to\':\'' + destination + \
                '\',\'message\':\'' + message + '\'}'  
      print ( 'Publish [topic,payload]: [' + self.topic + ',' + message + ']' )
      self.client.publish(self.topic, payload=message, qos=0, retain=False)
      
         
   def send ( self, message):
      print ( 'comm.send [' + message + ']' )
      while True: 
         self.publish (self.target, message, self.count)         
         if self.waitAck (): 
            self.count = self.count + 1 
            break
         else:
            print ( 'Re publish message: ' + message)

      
   def stop(self):
      self.client.stop()
    
   def on_connect(self,client, userdata, flags, rc):
      print(f"Connected with result code {rc}, subscribe to " + self.topic)
      # subscribe, which need to put into on_connect
      # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
      self.client.subscribe(self.topic)
      self.connected = True 
       
   def waitConnected (self):
      while not self.connected: 
         time.sleep (0.1) 

   def acknowledge ( self, destination):   
      self.publish (destination, 'ACK', self.count)  # self.count is probably not correct here.  Don't care?   

   def disconnect (self): 
      print ( 'Disconnecting.' )         
      try: 
         self.publish (self.target, 'disconnect yo', self.count)
         self.client.disconnect();
      except Exception as ex:
         print ( 'Could not disconnect because: ' + str(ex)) 
      print ( 'Done in disconnect' )

  
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
             # print ( 'Found an ack...for me, check count' )
             #if info['id'] == self.count: 
             #   # print ( 'Received an expected ack [' + str(self.count) + ']')
             self.ack = True 
             self.count = self.count + 1 
             #else:
             #   print ( 'Unexpected count: ' + str(info['id']) + ' still waiting....' )
          else:
             print ( 'RCVD ' + msg + ' from ' + fromName ) 
             self.message = msg
             # print ( 'This is for me, and not an ACK so ack it' )
             self.acknowledge ( fromName)
             print ( 'Append ' + msg + ' to the message buffer ' ) 
             self.push (msg)

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

      
   if len(sys.argv) != 4:
      print ( 'Note mosquitto should be installed and running' )
      print ( 'Usage: python3 Communications.py broker myName targetName' )
      print ( 'python3 Communications.py localhost pi7 laptop' )
   else:
      print ( 'To test, install mosquitto and then run mosquitto from the C:\Program Files\Mosquitto' )
      try: 
         topic = 'messages'
         broker = sys.argv[1]
         myName = sys.argv[2]
         target = sys.argv[3]          

         print ( 'I am ' + myName + ' talking to: ' + target ) 
         comm = Communications (topic,broker,myName);
         if comm.connectBroker(): 
            comm.setTarget (target)            

            while True:  
               (event,data,addr) = utilities.getKeyOrMqtt()
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
