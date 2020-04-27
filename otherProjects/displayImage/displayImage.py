import pygame
from pygame.locals import *
pygame.init()
display = pygame.display.set_mode( ( 128,128 ), pygame.FULLSCREEN )
img=pygame.image.load("sky.bmp").convert()
display.blit (img,(0,0))
pygame.display.flip()


