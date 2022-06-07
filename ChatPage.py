import inspect
import pygame

WHITE      = (255, 255, 255)

class ChatPage (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.displaySurface = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization of Chat' )
       self.iAmHost     = True        
       
    def main (self):
       # Show screen 
       print ( 'Show screen' )
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))
       self.utilities.showLabel ('Enter exit to quit', 50, 20)     
       self.utilities.showLabel ('Chat:', 250, 55)
       
       pygame.display.set_caption('Chatting with ' + self.comm.target)        
       pygame.display.update()  
     
       
       quit = False  
       joinTimeout = 0    
       print ( 'Start ChatPage while loop' )
       myMove = True 
       while not quit: 
          (typeInput,message,addr) = self.utilities.getKeyOrUdp()  

          if message.lower() == 'exit': 
             quit = True
             # utilities.udpBroadcast (client, 'Player left chat', 3333) # key input          
          elif typeInput == 'key': 
             self.comm.send (message)
             y = y + 20  
             
             '''   
             elif typeInput == 'udp':
                addr = str(addr[0])       
                print ('Got udp ' + chat + ' from: ' + addr )
                if addr == socket.gethostbyname(socket.gethostname()): 
                   print ('Ignore this message because it is from myself')
                else:
                   showLine (addr + ':' + chat, 300, y)               
                   y = y + 20             
             '''
          
          elif typeInput == 'mqtt':
             print ( 'Chatpage got mqtt input: ' + message + ' from: ' + addr)
             self.utilities.showLine (addr + ':' + message, 300, y)
              
       print ( 'Go back to the main page...' )
 
'''
# Show the chat page
def chatPage(showOnly=False):
    global myIO
    
    DISPLAYSURF.fill((BLACK))
    showLabel ('Chat:', 250, 55)
    (images,sprites) = showImages (['images/quit.jpg'], [(400,400)] )
    
    pygame.display.set_caption('Chatting: ')
    pygame.display.update()

    quit = False
    y = 55
    #if iAmHost:
    #   myIO.udpBroadcast ( 'exec:games=[\'chat\']')
     
    line = ''     
    while not quit and not showOnly:   
       (eventType,data,addr) = myIO.getKeyOrUdp() # This should set games   
       if eventType == 'key':
          if data == chr(13): 
             myIO.udpBroadcast (line)
             # print ( 'line: [' + line + ']' )
             showLine ( 'Me:' + line, 300, y) 
             line = ''
             y = y + 20
          elif data == chr(8): 
             if len(line) > 0: 
                if len(line) == 1:
                   line = ''
                else:
                   line = line [0:len(line)-1]
                print ( 'line: [' + line + ']' )
                pygame.draw.rect(DISPLAYSURF, BLACK, (0,y,DISPLAYWIDTH,27)) 
                pygame.display.update()                
                
                showLine ( 'Me:' + line, 300, y) 
          else: 
             line = line + data
             print ( 'line: [' + line + ']' )
             showLine ( 'Me:' + line, 300, y) 
             
       elif eventType == 'udp':       
          print ('Got udp ' + data + ' from: ' + addr )
          if addr == myIpAddress: 
             print ('Ignore this message because it is from myself')
          else:
             if line != '':
                y = y + 20 # Skip my current message
             showLine (data, 300, y)               
             y = y + 20             
          
       sprite = getSpriteClick (eventType, data, sprites ) 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
          
'''          