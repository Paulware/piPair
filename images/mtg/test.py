import pygame_widgets
import pygame
from pygame_widgets.toggle import Toggle



pygame.init()
win = pygame.display.set_mode ((1000,600))
toggle = Toggle (win,100,100,100,40)


run = True
lastValue = False 
while run:
   events = pygame.event.get()
   for event in events:
      if event.type == pygame.QUIT:
         pygame.quit()
         run = False 
         quit()
         
      
         
   win.fill ((255,255,255))
   pygame_widgets.update(events)
   pygame.display.update()
   
   if toggle.value and not lastValue: 
      print ( 'Transition true' )
   lastValue = toggle.value
   