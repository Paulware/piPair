import pygame, time
from pygame.locals import *

class SF30: 
   X=3
   Y=4
   A=1
   B=0
   R=7
   L=6
   L2=8
   R2=9
   SEL=6
   START=7
   HOME=2
   LEFT = 100 
   RIGHT = 101
   UP = 102
   DOWN = 103
   L_UP = 104
   L_DOWN = 105
   L_LEFT = 106
   L_RIGHT = 107
   R_UP = 108
   R_DOWN = 109
   R_LEFT = 110
   R_RIGHT = 111 
   CLEAR = 112
   UP_PRESSED = 113
   DOWN_PRESSED = 114
   LEFT_PRESSED = 115
   RIGHT_PRESSED = 116
   START_PRESSED = 117
   A_PRESSED = 118
   B_PRESSED = 119
   SELECT_PRESSED = 120
   leftJoy = "S"
   rightJoy = "s"
   upDown = "v"
   leftRight = "u"
   fire = ""
   lastFire = ""
   joystick_detected = False
   cleared = True
   joyButtonCleared = True
   quit = False

   def close(self):
      pygame.joystick.quit()
          
   def __init__(self):   
      print ("in SF30.init" )
      self.joystick_cnt=0
      self.event = -1

      pygame.init()
      pygame.joystick.init()
      
      lastTime = time.time() 
      while self.joystick_detected==False:
          elapsedTime = time.time() - lastTime
          if elapsedTime > 0.5: 
             lastTime = time.time() 
             print ( 'waiting for a joystick in init' )
             pygame.joystick.quit()
             pygame.joystick.init()
             try:
                 self.joystick = pygame.joystick.Joystick(0) # create a joystick instance
                 self.joystick.init() # init instance
                 print("Initialized joystick: {}".format(self.joystick.get_name()))
                 self.joystick_detected = True
                 self.lastReadTime = time.time()
             except pygame.error:
                 print ("Joystick error in joystick init" )
      print ("Done found joystick in init" );
      
   def connected (self):
      return self.joystick_detected; 

   def tank(self):
      #if self.lastFire == "F":
      #   self.fire = ""
      #self.lastFire = self.fire
      return self.leftJoy + self.rightJoy + self.upDown + self.leftRight + self.fire;   

   # Convert pygame events to SF30 events      
   def handleEvent (self,event):   
      events = [self.B, self.A, self.X, self.Y, self.SEL, self.START, self.HOME, self.L, self.L2, self.R, self.R2]
      
      if event.type == pygame.JOYBUTTONDOWN:
         myevent = event.button
         # print ("event.button: " + str(event.button))
         if myevent in events: 
            self.event = myevent;
            if self.event == self.B:
               if self.joyButtonCleared: 
                  self.event = self.B_PRESSED
               self.joyButtonCleared = False
               
            if self.event == self.A:
               if self.joyButtonCleared: 
                  self.event = self.A_PRESSED
                  self.fire = "F"
               self.joyButtonCleared = False
                 
            if self.event == self.SEL:
               if self.joyButtonCleared:
                  self.event = self.SELECT_PRESSED
               self.joyButtonCleared = False
                  
            if self.event == self.START:
               if self.joyButtonCleared:
                  self.event = self.START_PRESSED
               self.joyButtonCleared = False
      elif event.type == pygame.JOYBUTTONUP:
         self.event = self.CLEAR
         self.joyButtonCleared = True
         self.fire = ""
      elif event.type == pygame.JOYAXISMOTION:
         axis = event.axis
         value = event.value
         #print("event detected {}".format(event))           
         #print ("[axis,value]: [" + str(axis) + "," + str(value) + "]" )          
         
         if axis == 1:
            if value > 0.7: 
               self.event = self.L_DOWN
               self.leftJoy = "l"
            elif value < -0.7:
               self.event = self.L_UP
               self.leftJoy = "L"
            else:
               self.leftJoy = "S"
         elif axis == 0:
            if value > 0.7:
               self.event = self.L_RIGHT
            elif value < -0.7:
               self.event = self.L_LEFT            
         elif axis == 3:
            if value > 0.7: 
               self.event = self.R_RIGHT
            elif value < -0.7:
               self.event = self.R_LEFT
         elif axis == 4:                           
            if value > 0.07:
               self.event = self.R_DOWN
               self.rightJoy = "r"
            elif value < -0.07: 
               self.event = self.R_UP
               self.rightJoy = "R"
            else:
               self.rightJoy = "s"                  
      elif event.type == pygame.JOYHATMOTION:
         myevent = event.value;
         if (myevent == (1,0)): 
            self.event = self.RIGHT
            self.leftRight = "T"
            if self.cleared: 
               self.event = self.RIGHT_PRESSED
            self.cleared = False
         elif (myevent == (-1,0)):
            self.event = self.LEFT
            self.leftRight = "t"
            if self.cleared: 
               self.event = self.LEFT_PRESSED
            self.cleared = False
         elif (myevent == (0,1)):
            self.event = self.UP
            self.upDown = "V"
            if self.cleared: 
               self.event = self.UP_PRESSED
            self.cleared = False
         elif (myevent == (0,-1)):
            self.event = self.DOWN
            self.upDown = "V"
            if self.cleared: 
               self.event = self.DOWN_PRESSED
            self.cleared = False
         elif (myevent == (0,0)):
            self.event = self.CLEAR
            self.upDown = "v"
            self.leftRight = "u"
            self.cleared = True
         #else:
         #   print("event yo {}".format(event))
      #else:
      #   print("event detected {}".format(event))                
      
   def read(self):
      self.event = None;
      elapsedTime = time.time() - self.lastReadTime
      if elapsedTime > 0.1: 
         pygame.event.pump()
         for event in pygame.event.get():
            self.handleEvent (event)
         self.lastReadTime = time.time()
      return self.event                        
   
if __name__ == '__main__':

    sf30 = SF30()
    while not sf30.joystick_detected:
       time.sleep (1.0)
       print ("Waiting for joystick " )
       
    lastEvent = -1
    
    while True:
       event = sf30.read()       
       if event != None: 
          print ("Got the event: " + str (event) )       
          if event == sf30.START_PRESSED:
             break
