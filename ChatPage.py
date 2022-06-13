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
          else:
             print ( 'typeInput: ' + typeInput )
          print ( 'Nothing returned' )
             
       print ( "getInput: (typeInput,line,addr): (" + typeInput + ',' + line + ',' + addr + ')')
       return (typeInput,line,addr)         
                
    def main (self):
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))
       self.utilities.showLabel ('Enter exit to quit2', 50, 20)     
       self.utilities.showLabel ('Chat:', 250, 55)
       
       pygame.display.set_caption('Chatting with ' + self.comm.target)        
       pygame.display.update()  

       quit = False
       y = 55

       while not quit:   
          (typeInput,message,addr) = self.getChatInput (300,y)
          if message.lower() == 'exit': 
             quit = True
             # utilities.udpBroadcast (client, 'Player left chat', 3333) # key input          
          elif typeInput == 'mqtt': 
             self.utilities.showLine (addr + ':' + message, 300, y)               
             print ( 'Received mqtt input: [' + message + ']' )
             y = y + 20  
          else:
             if typeInput != '':
                print ( 'Got a typeInput of [' + typeInput + ']' )  
             else:
                print ( 'Got a nothing typeInput ' )             
       print ( 'Go back to the main page...' )
 
