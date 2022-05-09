import paho.mqtt.client as mqtt
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
      # set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
      
      self.client.will_set(topic, b'{"status": "Off", "name":"' + name.encode() + b'"}')
      self.message = '' 
      self.target = ''
      self.buffer = ['','','','','','','','','','']
      self.head = 0
      self.tail = 0
      
      self.debug = False 
      
   def waitFor ( self, message):    
      while True: 
         if not self.empty(): 
            msg = self.pop()
            if msg.find (message) > -1: 
               print ( 'comm.waitFor found: ' + message + ' in ' + msg)
               break
               
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
      self.buffer[self.head] = value
      self.head = (self.head + 1) % 10
  
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
            self.client.connect(self.broker, 1883, 60)
         except Exception as ex:
            print ( 'Could not connect to ' + self.broker + '  because: ' + str(ex))
            ok = False 
      
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
   
   def publish (self,destination,message):
      message = str(self.count) + ':' + self.name + ':' + destination + ':' + message 
      print ( 'Publish [topic,payload]: [' + self.topic + ',' + message + ']' )
      self.client.publish(self.topic, payload=message, qos=0, retain=False)
         
   def send ( self, message):
      while True: 
         self.publish (self.target, message)
         if self.waitAck (): 
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

   def acknowledge ( self, destination, count ):    
      message = count + ':' + self.name + ':' + destination + ':ACK' 
      print ( 'Send acknowledgment: ' + message )
      self.client.publish(self.topic, payload=message, qos=0, retain=False)          

   def disconnect (self): 
      print ( 'Disconnecting.' )         
      try: 
         self.publish (self.target, 'disconnect yo')
         self.client.disconnect();
      except Exception as ex:
         print ( 'Could not disconnect because: ' + str(ex)) 
      print ( 'Done in disconnect' )
   # the callback function, it will be triggered when receiving messages
   def on_message(self,client, userdata, msg):
       message = msg.payload.decode()
       data = message.split ( ':' )
       ignore = False
       if len(data) > 1:
          if data[1] == self.name:
             ignore = True 
             
       target = ''
       if len(data) > 2: 
          target = data[2]       
   
       if not ignore:    
          # print(f"{msg.topic} {msg.payload}")
          # print ( 'Got data: ' + str(data)) 
          ignore = False
          if target == self.name:
             if message.find ( ':ACK' ) > -1: 
                # print ( 'Found an ack...for me, check count' )
                if data[0] == str(self.count): 
                   # print ( 'Received an expected ack [' + str(self.count) + ']')
                   self.ack = True 
                   self.count = self.count + 1 
                else:
                   print ( 'Unexpected count: ' + data[0] + ' still waiting....' )
             else:
                print ( 'RCVD: [' + data[3] + '] from ' + data[1] + ' I am ' + self.name + ' target: ' + target)
                self.message = data[3]
                # print ( 'This is for me, and not an ACK so ack it' )
                self.acknowledge ( data[1], data[0] )
                print ( 'Append ' + data[3] + ' to the message buffer ' ) 
                self.push (data[3])
          else: 
             print ( 'This message is for: ' + target)

if __name__ == "__main__":
   if len(sys.argv) == 1:
      print ( 'Usage: python3 Communications.py myId' )
   else:
      try: 
         topic = 'messages'
         broker = '192.168.4.1' 
         myName = sys.argv[1]

         comm = Communications (topic,broker,myName);
         if comm.connectBroker(): 
            print ( 'Enter target' )
            target = input()
            comm.setTarget (target) 
            while True:   
               print ( 'Enter message' )
               message = input() 
               comm.send(message )
         else:
            print ( 'Could not initialize Communications')
            
      finally:
         comm.disconnect()      
