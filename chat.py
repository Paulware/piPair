import inspect

# Show the chat page
def chatPage(showOnly=False):
    global tcpSocket 
    global tcpConnection 
    
    DISPLAYSURF.fill((BLACK))
    showLabel ('Chat:', 250, 55)
    (images,spites) = showImages (['images/quit.jpg'], [(400,400)] )
    
    pygame.display.set_caption('Chatting: ')        
    pygame.display.update()  

    quit = False
    y = 55
    if iAmHost:
       udpBroadcast ( 'exec:games=[\'chat\']')
     
    line = ''     
    while not quit and not showOnly:   
       (eventType,data,addr) = getKeyOrUdp() # This should set games   
       if eventType == 'key':
          if data == chr(13): 
             udpBroadcast (line)
             print ( 'line: [' + line + ']' )
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
          
       sprite = getSpriteClick (eventType, data, spites ) 
       if sprite != -1: # Quit is the only other option           
          print ("Selected command: " + str(sprite))
          mainPage (True)
          quit = True
           
CHAT=inspect.getsource(chatPage)