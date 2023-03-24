import pygame

class Prompt: 
   def __init__ (self):
      self.width = 300
      self.height = 50
      
   def setWidthHeight (self,w,h):
      self.width = w
      self.height = h       
      
   def go (self, x, y, borderPrompt=''):
      font = pygame.font.SysFont(None, 30)
      borderRectangle = pygame.Rect (x,y,self.width,self.height)
      if borderPrompt != '': 
         borderText = font.render(borderPrompt, True, (255, 0, 0))                  
         borderTextRectangle = pygame.Rect (x+10,y-10,borderText.get_width(),borderText.get_height())
         
      rectangle = pygame.Rect(x+20, y+20, self.width-20, self.height-20)   
      window = pygame.display.get_surface()
      clock = pygame.time.Clock()
      
      text = ""
      
      run = True
      
      while run:
         clock.tick(60)
         
         window.fill(0)
         pygame.draw.rect ( window, (255,0,0), borderRectangle, width=1 )
         if borderPrompt != '':
            window.fill(0,borderTextRectangle)
            window.blit(borderText, borderTextRectangle)
         text_surf = font.render(text, True, (255, 0, 0))
         window.blit(text_surf, rectangle) # text_surf.get_rect(center = window.get_rect().center))
         pygame.display.flip()
         
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
               input_active = True
               text = ""
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                  print ( 'Got a return' )
                  return text 
               elif event.key == pygame.K_BACKSPACE:
                  text =  text[:-1]
               elif event.key == pygame.K_ESCAPE:
                  return ''
               else:
                  text += event.unicode

            
      return text      

if __name__ == '__main__':     
   pygame.init()
   window = pygame.display.set_mode((500, 200))
   response = Prompt ().go(100,50,'Please enter your text')
   print ( 'Got response: [' + response + ']')
   
   pygame.quit()
   exit()