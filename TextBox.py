import pygame

class TextBox():

    def __init__(self, text, x=40, y=40, w=None, h=None): 
        self.window = pygame.display.get_surface()   
        self.color = (150, 150, 150)
        self.highlight_color = (100, 200, 255)
        self.font = pygame.font.SysFont(None, 30)
        self.text = text
        self.x = x
        self.y = y
        self.pad = 3
        width,height = self.font.size(self.text)
        if w is None:            
           self.width = width
        else:
           self.width = w
           
        if h is None:
           self.height = height
        else:
           self.height = h
        self.width = self.width + self.pad
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def clearLast (self): 
        surf = pygame.display.get_surface()
        print ( 'Clearing with black: ' + str(self.rect))
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 0)
        pygame.display.flip()
        pygame.event.pump()         
 
    def clearLine (self): 
        width,height = self.font.size(self.text)
        width = pygame.display.get_surface().get_width() - self.x
        rect = pygame.Rect (self.x, self.y-3, width, height+6)
        pygame.draw.rect (pygame.display.get_surface(), (0,0,0), rect );
        pygame.display.flip()
        pygame.event.pump()        
        
    def length(self):
        return len (self.text)

    def draw(self, pos=None):
        surf = pygame.display.get_surface()
        msg = self.font.render(self.text, 1, (0, 0, 0))
        width,height = self.font.size(self.text)
        print ( 'size(self.text), [width,height]: [' + str(width) + ',' + str(height) + ']' )
        
        if pos is not None:            
           self.x = pos[0]
           self.y = pos[1]
           self.height = pos[2]
           self.rect = pygame.Rect (self.x, self.y, width + self.pad, self.height)
                 
        pygame.draw.rect(surf, self.highlight_color, self.rect)
        surf.blit(msg, self.rect) # msg.get_rect(center = self.rect.center))
        nextPosition = (self.x,self.y+self.height,self.height)
        return nextPosition


if __name__ == '__main__':
   pygame.init()
   window = pygame.display.set_mode((640, 480))
   line1 = TextBox('Hello is anybody there?')
   pos = line1.draw()
   line2 = TextBox('Goodbye')
   pos = line2.draw(pos)

   pygame.display.flip()
   run = True
   while run:
      event_list = pygame.event.get()   
      for event in event_list:
         if event.type == pygame.MOUSEBUTTONUP:
            run = False
       
   pygame.quit()
