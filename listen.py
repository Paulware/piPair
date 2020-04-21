
import socket
import select 

data = ''
UDPPORT = 3333
# Setup the UDP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP    
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", UDPPORT)) 
client.setblocking(0) # turn off blocking  

while data == '':

   i,o,e = select.select ([client], [], [], 0.0001)
     
   for s in i:
      if s == client:
         print ( 'Something from client?' )
         data, addr = client.recvfrom (1024)
         data = data.decode();
         addr = str(addr[0])
         print ( '[data,addr]: [' + data + ',' + addr + ']' )