import serial
import time
import threading
import os

global quit
quit = False
def bindRfcomm0():
   while not quit: 
      try:
         print ("Binding rfcomm0" )
         # This will block yo
         ready = True 
         os.system ('rfcomm connect /dev/rfcomm0 30:15:01:07:09:37 1' )
         print ( "Done binding rfcomm0" )
         ready = False 
      except Exception as ex:
         print ( "bindRfcomm0 Got this exception: " + str(ex) + " try again" ) 
         time.sleep (3) 
         break

x = threading.Thread (target=bindRfcomm0)
x.start()
print ( "Wait for bind to complete" )
readyTimeout = time.time() + 5 

while True:
   try:
      port = serial.Serial("/dev/rfcomm0", baudrate=9600)
      print ("Successfully connected serial port" )
      break
   except Exception as ex: 
      print ("Unable to open serial port" )
      time.sleep (1)

try:
   while True:
      print ( "Sending")
      port.write ( str.encode("Hello yes") )
      rcv = port.readline()
      if rcv:
         print (rcv)
         if rcv.strip() == 'quit':
            quit = True
            break
      time.sleep (3)
except Exception as ex:
   print ( "main exception: " + str(ex) ) 
finally: 
   quit = True
   port.close()
