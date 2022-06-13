import inspect
import pygame

WHITE      = (255, 255, 255)
BLACK      = ( 0,0,0 )

class ChatPage (): 
    def __init__ (self, DISPLAYSURF, utilities, comm ):
       self.comm = comm
       self.DISPLAYSURF = DISPLAYSURF
       self.displaySurface = DISPLAYSURF
       self.utilities   = utilities       
       print ( 'Initialization of Chat' )
       self.iAmHost     = True  
       self.DISPLAYWIDTH  =800
       self.DISPLAYHEIGHT = 600

    def getChatInput (self, x,y):
       line = ''
       quit = False
       while not quit:
          (typeInput,data,addr) = self.utilities.getKeyOrUdp()
          if typeInput == 'key': 
             if data == chr(13):
                quit = True
             else:
                if data == chr(8):
                   print ( "backspace detected")
                   if len(line) > 0:
                      lastCh = line[len(line)-1]
                      x = x - self.utilities.chOffset (lastCh) #Todo need to get lastCh from 
                      self.utilities.showCh (' ', x, y)
                      self.utilities.showCh (' ', x+4, y)
                      self.utilities.showCh (' ', x+8, y)
                      line = line[:len(line)-1] 
                else:
                   line = line + data
                   ch = data
                   self.utilities.showCh (ch, x, y)           
                   x = x + self.utilities.chOffset(ch)
          elif typeInput == 'mqtt':
             line = data
             quit = True
             print ( 'got some mqtt data: ' + data)
          print ( 'Nothing returned' )
             
       print ( "getInput: (typeInput,line,addr): (" + typeInput + ',' + line + ',' + addr + ')')
       return (typeInput,line,addr)         
                 

    def showLine ( self, line, x,y ):
       height = self.DISPLAYHEIGHT - 23
       pygame.draw.rect(self.displaySurface, BLACK, (0,height+2,self.DISPLAYWIDTH,height+2+25))    
       pygame.display.update()
       for ch in line:
          self.showCh (ch, x, y)
          x = x + self.chOffset (ch)
                
    def main (self):
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))
       self.utilities.showLabel ('Enter exit to quit2', 50, 20)     
       self.utilities.showLabel ('Chat:', 250, 55)
       
       pygame.display.set_caption('Chatting with ' + self.comm.target)        
       pygame.display.update()  

       quit = False
       y = 55

       while not quit and not showOnly:   
          (typeInput,message,addr) = self.getChatInput (300,y)
          if message.lower() == 'exit': 
             quit = True
             # utilities.udpBroadcast (client, 'Player left chat', 3333) # key input          
          elif typeInput == 'mqtt': 
             self.showLine (addr + ':' + message, 300, y)               
             print ( 'Received mqtt input: [' + message + ']' )
             y = y + 20  
          else:
             if typeInput != '':
                print ( 'Got a typeInput of [' + typeInput + ']' )  
              
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