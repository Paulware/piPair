from socket import *
import re
import os
import time
import sys

whichAdapter = 'wlan0'

def getLocalAddress ():
  global whichAdapter
  ipAddress = '192.168.0.X'
  line = os.popen("/sbin/ifconfig " + whichAdapter).read().strip()  
  p = re.findall ( r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', line )
  if p: 
     ipAddress = p[0]   
     
  return ipAddress 
  
def getBroadcastAddress ():
  address = getLocalAddress()
  index = address.rfind ('.')
  addr = address[0:index] + '.255'
  return addr  

try: 
   global whichAdapter
   if (len(sys.argv) > 1):
      whichAdapter = sys.argv[1]
      print "check adapter: " + whichAdapter

   port = 3333
   sock = socket(AF_INET, SOCK_DGRAM)
   sock.bind (('',0)) # bind to any old port 
   sock.setsockopt (SOL_SOCKET, SO_BROADCAST, 1)
   msg = 'server ' + getLocalAddress() 
   print 'Local Address: ' + getLocalAddress()
   destination = getBroadcastAddress() # '192.168.0.255'  
   sock.sendto(msg, (destination, port)) # broadcast to all devices listening on port 3333
   print 'Sent ' + msg + ' to ' + destination + ':' + str(port) + '\n'

except Exception as inst:
   print str(inst)