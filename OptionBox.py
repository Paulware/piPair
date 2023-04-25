import pygame

class OptionBox():

    def __init__(self, options, x=40, y=40, width=160, height=40, selected = 0): 
        self.window = pygame.display.get_surface()   
        self.color = (150, 150, 150)
        self.highlight_color = (100, 200, 255)
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 30)
        self.option_list = options
        self.selected = selected
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        for i, text in enumerate(self.option_list):
           rect = self.rect.copy()
           rect.y += (i+1) * self.rect.height
           pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
           msg = self.font.render(text, 1, (0, 0, 0))
           surf.blit(msg, msg.get_rect(center = rect.center))
        outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
        pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        
        self.active_option = -1
        for i in range(len(self.option_list)):
           rect = self.rect.copy()
           rect.y += (i+1) * self.rect.height
           if rect.collidepoint(mpos):
              self.active_option = i
              break

        for event in event_list:
           if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
              self.selected = self.active_option
              return self.active_option
        return -1
    
    def getSelection (self):
       result = -1
       selection = ''
       run = True
       print ( 'getSelection....')
       while run:    
          pygame.time.Clock().tick(60)
          event_list = pygame.event.get()
          for event in event_list:
             if event.type == pygame.QUIT:
                run = False

          selected_option = self.update(event_list)       
          if selected_option >= 0:
             print(selected_option)
             result = selected_option
             break

          self.draw(self.window)
          pygame.display.flip()
       if result != -1: 
          selection = self.option_list[result]
       print ( 'Got selection: [' + selection + ']') 
       return selection

if __name__ == '__main__':
   pygame.init()
   window = pygame.display.set_mode((640, 480))

   options = ['option 1', '2nd Option', 'another Option', 'cancel']
   comboBox = OptionBox(options)

   run = True
   while run:
      result = comboBox.getSelection()
      if result == 'cancel':
         break
       
   pygame.quit()
   exit()