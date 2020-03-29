import buttonClass
import imageClass
import eventClass
import pygame
import time
from pygame.locals import *

pygame.init()
events = eventClass.EventClass()
image = imageClass.ImageClass()
playerImage = imageClass.ImageClass()
playerImage.draw ( 'playerleft1.png',400-172/2,300-172/2)
image.draw ('townscape.jpg', 0,0)
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
       
    if events.mouseClicked:
       print ("Got a click")
    playerImage.rotate (events.angle)    
    events.update(pygame)
    image.show() 
    playerImage.show()    
    pygame.display.update()
    fpsClock.tick(FPS)    
pygame.quit()
