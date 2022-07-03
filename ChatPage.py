import inspect
import pygame
from TextBox import TextBox

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
                
    def main (self):
       BLACK = (0,0,0)
       self.displaySurface.fill((BLACK))
       
       line = TextBox('Enter exit to quit')
       pos = line.draw()
       line = TextBox('Chat:')
       pos = line.draw(pos)        
      
       pygame.display.set_caption('Chatting with ' + self.comm.target)        
       pygame.display.update()  

       quit = False
       lastMsg = ''
       while not quit:   
          (event,data,addr) = self.utilities.getKeyOrMqtt()
          print ( '[event,data,addr]: [' + str(event) +',' + str(data) + ',' + str(addr) + ']') 
          if event == pygame.MOUSEBUTTONUP: 
             break
          elif event == 'mqtt':
             print ( 'Write out ' + data + ' to: ' + str(pos) ) 
             line = TextBox(data)
             pos = line.draw (pos)
             pygame.display.flip()
             if data == 'exit': 
                break
             line = None         
             
          if self.utilities.msg != lastMsg:
             if not line is None:
                line.clearLast()
                line = TextBox (self.utilities.msg)
                line.draw (pos)
             lastMsg = self.utilities.msg
             pygame.display.flip()
             
          if self.utilities.message != '':
             if self.utilities.message == 'exit':
                break
             else:
                print ( '[message]: [' + self.utilities.message + ']' )
                line = TextBox (self.utilities.message)
                pos = line.draw(pos)
                pygame.display.flip()
                self.comm.send(self.utilities.message )
                self.utilities.message = ''           
             
       print ( 'Go back to the main page...' )
if __name__ == '__main__':
   from Utilities import Utilities
   import platform
   from Communications import Communications
   pygame.init()
     
   DISPLAYSURF = pygame.display.set_mode((1200, 800))
   FONT = pygame.font.Font('freesansbold.ttf', 16)
   BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
   pygame.display.set_caption('Flippy')
   utilities = Utilities (DISPLAYSURF, BIGFONT)
   name = 'laptop' if (platform.system() == 'Windows') else 'pi7'
   target = 'pi7' if (platform.system() == 'Windows') else 'laptop'
   comm = Communications ('messages', 'localhost', name ) 
   comm.connectBroker()
   comm.setTarget (target)
   utilities.comm = comm
         
   line = TextBox('Enter exit to quit')
   pos = line.draw()
   line = TextBox('Chat:')
   pos = line.draw(pos) 
   
   pygame.display.flip()
   run = True
   lastMsg = ''
   line = None
   while run:
      (event,data,addr) = utilities.getKeyOrMqtt()
      print ( '[event,data,addr]: [' + str(event) +',' + str(data) + ',' + str(addr) + ']') 
      if event == pygame.MOUSEBUTTONUP: 
         break
      elif event == 'mqtt':
         print ( 'Write out ' + data + ' to: ' + str(pos) ) 
         line = TextBox(data)
         pos = line.draw (pos)
         pygame.display.flip()
         if data == 'exit': 
            break
         line = None         
         
      if utilities.msg != lastMsg:
         if not line is None:
            line.clearLast()
            line = TextBox (utilities.msg)
            line.draw (pos)
         lastMsg = utilities.msg
         pygame.display.flip()
         
      if utilities.message != '':
         if utilities.message == 'exit':
            break
         else:
            print ( '[message]: [' + utilities.message + ']' )
            line = TextBox (utilities.message)
            pos = line.draw(pos)
            pygame.display.flip()
            comm.send(utilities.message )
            utilities.message = ''

    
   comm.disconnect()    
   pygame.quit()
