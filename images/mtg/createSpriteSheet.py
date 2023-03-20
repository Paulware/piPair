from PIL import Image
import os, math, time
max_frames_row = 10.0

tile_width = 0
tile_height = 0

spritesheet_width = 0
spritesheet_height = 0

directories = ['artifacts', 'creatures', 'enchantments', 'instants', 'lands', 'sorcery']

# Step 1: Determine the number of rows and columns in the spritesheet
filenames = []
for d in directories: 
   files = os.listdir(d + "/")
   files.sort()
   print(files)
   for current_file in files :
      try:
         filename = d + '/' + current_file
         # First image sets the size of all subsequent images in the spritesheet
         if tile_width == 0:
            im = Image.open (filename)
            tile_width  = im.getdata().size[0]
            tile_height = im.getdata().size[1]
         filenames.append(filename)
      except Exception as ex:
         print("Trouble processing image: " + filename + " because: " + str(ex))

if len(filenames) > max_frames_row :
   spritesheet_width = tile_width * max_frames_row
   required_rows = math.ceil(len(filenames)/max_frames_row)
   spritesheet_height = tile_height * required_rows
else:
   spritesheet_width = tile_width*len(filenames)
   spritesheet_height = tile_height
    
spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))


# Step 2: Populate the spritesheet 
for filename in filenames:
    
   index = filenames.index(filename)
   top = tile_height * math.floor(index/max_frames_row)
   left = tile_width * (index % max_frames_row)
   bottom = top + tile_height
   right = left + tile_width
    
   box = (left,top,right,bottom)
   box = [int(i) for i in box]
    
   print ( filename + ', [tile_width,tile_height]: [' + str(tile_width) + ',' + str(tile_height) + ']' )
   frame = Image.open(filename)
    
   current_frame = Image.open(filename)
   current_frame = current_frame.resize ((tile_width,tile_height) )

   # cut_frame = current_frame.crop((0,0,tile_width,tile_height))
       
   try: 
      spritesheet.paste(current_frame, box)
   except Exception as ex: 
      print ( 'Cannot paste image because: ' + str(ex)) 
      break
    
spritesheet.save("spritesheet" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png", "PNG")