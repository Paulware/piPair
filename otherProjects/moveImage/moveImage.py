import buttonClass
import imageClass
import pygame
import time
from pygame.locals import *

pygame.init()

image = imageClass.ImageClass()
image.draw ('townscape.jpg',200,100)
image.show()
buttons = buttonClass.ButtonsClass()
speed = 5
FPS = 60 
fpsClock = pygame.time.Clock()

while True:    
    image.clear()       
    if buttons.checkKey ("A"): 
       soundObj = pygame.mixer.Sound('artillery.wav')
       soundObj.play()
    if buttons.checkKey ("B"): 
       soundObj = pygame.mixer.Sound('carHorn.wav')
       soundObj.play()       
    if buttons.checkKey ("Start"):
       break
    if buttons.checkKey ("Right"):
       image.moveX (speed)
    if buttons.checkKey  ("Left"): 
       image.moveX (-speed)
    if buttons.checkKey ("Up"):
       image.moveY (-speed)
    if buttons.checkKey  ("Down"): 
       image.moveY (speed)
    image.show()   
    pygame.display.update()
    fpsClock.tick(FPS)    
pygame.quit()
