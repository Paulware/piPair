import pygame
import time
DISPLAYWIDTH = 1080
DISPLAYHEIGHT = 800
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
#pygame.display.toggle_fullscreen()      
pygame.display.set_caption('Hello Caption')
print ( "For debugging")
WHITE = (255, 255, 255) # WHITE[0], WHITE[1], WHITE[2]
DISPLAYSURF.fill((WHITE)) #Clear the background
background = pygame.image.load ('images/diplomacy.gif') # Image file
pos = (0,0)
DISPLAYSURF.blit (background,pos )               
pygame.display.update() 
quit = False
while not quit:
    ev = pygame.event.get()
    for event in ev:
       if event.type == pygame.MOUSEBUTTONDOWN:
          quit = True
    
