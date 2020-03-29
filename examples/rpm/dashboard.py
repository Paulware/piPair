# Authors: Michael Greer, Matthew Shepherd

# IMPORTANT FOR CIRCLE DEFINITION:
# We defined our unit circle as a mirror image of the standard unit circle.
# Circle starts at left and goes clockwise
# Code reflects this

###############################################################################################################

# -*- coding: utf-8 -*-

# Import statements

import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math				# sin, cos, etc
import struct			# For converting byte to float

import os

# Is this a test or not
test = True

# Initialize serial
if (not test): 
	ser = serial.Serial('/dev/ttyUSB0',9600)

# Draws pointer on dials
def draw_indicator(angle,length,center_x,center_y):

	x_len = math.cos(math.radians(angle))*float(length) # Finds the x and y compoents of the length
	y_len = math.sin(math.radians(angle))*float(length) 

	x_pos = center_x - x_len # Finds the x and y 
	y_pos = center_y - y_len
	
	inner_x_pos = int(center_x-(.6*x_len))										# x coordinate of inside point
	inner_y_pos = int(center_y-(.6*y_len))

	pygame.draw.line(screen,red,(inner_x_pos,inner_y_pos),(x_pos,y_pos),10)

# Draws tick marks along the outside of circles
def draw_tick_marks(startAngle,stopAngle,numMarks,center_x,center_y,radius):

	angle_diff = stopAngle-startAngle												# Value of the difference between the start and stop angles
	spacing = float(angle_diff)/float(numMarks-1)									# Angle spacing between each mark

	for mark in range(numMarks): 													# Loops through each tick mark
		current_angle=startAngle+(spacing*float(mark))								# Current angle for this tick mark
		y_len = math.sin(math.radians(current_angle))*radius						# y component of length
		x_len = math.cos(math.radians(current_angle))*radius						# x component of length

		x_pos = int(center_x - x_len)												# x coordinate of outside point
		y_pos = int(center_y - y_len)												# y coordinate of outside point

		inner_x_pos = int(center_x-(.9*x_len))										# x coordinate of inside point
		inner_y_pos = int(center_y-(.9*y_len))										# y coordinate of inside point

		num_x_pos = int(center_x-(.8*x_len))
		num_y_pos = int(center_y-(.8*y_len))

		#print x_pos, y_pos, inner_x_pos, inner_y_pos								# debug

		pygame.draw.line(screen,white,(x_pos,y_pos),(inner_x_pos,inner_y_pos),6)	# draws tick mark

		num = font.render(str(mark),1,white)

		(num_width,num_height) = font.size(str(num))

		screen.blit(num,(num_x_pos-5,num_y_pos-(num_height/2)))


# Draws redline on outside of circle
def draw_redline_arc(startAngle,stopAngle,center_x,center_y,radius):

	rect = (center_x-radius,center_y-radius,2*radius,2*radius)		# Defines the rectangle to draw arc in

	start_radians = math.radians((-stopAngle)+180)					# Converts between our "unit circle" and standard unic circle
	stop_radians = math.radians((-startAngle)+180)

	pygame.draw.arc(screen,red,rect,start_radians,stop_radians,10)	# Draws Arc

# Logo Sprite BUG: Refuses to load an image as a sprite
# logo = pygame.sprite.Sprite()
# logo.image = pygame.Surface((100,100))
# logo.image.fill((255,255,255))
# logo.image.set_colorkey((0,0,0))
# logo.rect = (100,100,100,100)

# Draws all parts of display that are not data-dependent
def draw_screen():

#	Draw dial
	pygame.draw.circle(screen, lgrey, (160, 240), 210, 0)
	pygame.draw.circle(screen, black, (160, 240), 200, 0)
	draw_redline_arc(305,315,160,240,200)
	pygame.draw.rect(screen, lgrey, (0,100,20,280))
	pygame.draw.ellipse(screen, black, (8, 100, 20, 280), 0)
	pygame.draw.ellipse(screen, black, (8, 100, 20, 280), 0)
	draw_tick_marks(45,315,14,160,240,200)
# 	pygame.draw.rect(screen, green, (80,240,160,80))  RPM Font Box
#	screen.blit(logo.image,logo.rect)
	
#	Draw rectangles
	pygame.draw.rect(screen, lgrey, (440,10,320,210))
	pygame.draw.rect(screen, green, (450,20,300,190))
	pygame.draw.rect(screen, lgrey, (440,260,320,210))
	pygame.draw.rect(screen, green, (450,270,300,190))
	
#	Draw logo
# 	screen.blit(logo.image,logo.rect)
	

# maps a variable from one space to another
def linear_transform(input,rangeOneStart,rangeOneEnd,rangeTwoStart,rangeTwoEnd):

	return int((input-rangeOneStart)*(float(rangeTwoEnd-rangeTwoStart)/float(rangeOneEnd-rangeOneStart))+rangeTwoStart)


# All code taken from Thomas Kelly's implementation of readData() in serial_thread.py
def readData():
	global ser
	global rpm, engineLoad, throttle, temp, oxygen, speed, gear, volts
	ser.flush()
	if (ser.inWaiting() > 0):
		data = ser.read()
		if (data == bytes(b'!')):
			data = ser.read()

			# Packet Headers:
			# 0x30 : RPMs
			# 0x31 : Engine Load
			# 0x32 : throttle
			# 0x33 : Coolant Temp (F)
			# 0x34 : O2 level
			# 0x35 : Vehicle Speed (The shitty one from the ECU anyway)
			# 0x36 : Gear (Again, shitty ECU version)
			# 0x37 : Battery Voltage

			if (data == bytes(b'0')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				#print(payload)
				rpm = payload

			elif (data == bytes(b'1')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				engineLoad = payload

			elif (data == bytes(b'2')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				throttle = payload

			elif (data == bytes(b'3')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				temp = payload

			elif (data == bytes(b'4')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				oxygen = payload

			elif (data == bytes(b'5')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				speed = payload

			elif (data == bytes(b'6')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = int(list(ser.read())[0])
				#print(payload)
				gear = payload

			elif (data == bytes(b'7')):
				timestamp = struct.unpack('>I',ser.read(4))[0]
				payload = struct.unpack('>f',ser.read(4))[0]
				volts = payload

			else:
				print("ERROR: Corrupted Data")
		else:
			pass
	else:
		pass

# Smooths rpm readout
def smooth_rpm():
	global rpm, display_rpm

	display_rpm += (rpm-display_rpm)/2


############# Color Definitions
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
lgrey=	(150,150,150)
green = (0,120,0)
white = (255,255,255)

def rpmColor(n):
	inpt = linear_transform(n,0,13000,0,255)
	if (inpt < 100):
		return (		250,					250,					250)
	elif (inpt < 150):
		return (		250-3*(inpt-100),		250-(inpt-100),		250-5*(inpt-100))
	elif (inpt < 200):
		return (		100+2*(inpt-150),		200-(inpt-150),			0)
	elif (inpt < 250):
		return (		200+(inpt-200),		150-3*(inpt-200),		0)
	else:
		return (		250,					0,						0)
	
###############################

pygame.init()

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

#pygame.display.toggle_fullscreen() # Sets display mode to full screen

# Display Logo

#img = pygame.image.load("WURacing-Logo-Big.png")# 
# 
#img = pygame.transform.scale(img, (600,480))

screen.fill(green)

# screen.blit(img, (100,0))

pygame.display.flip()

time.sleep(5)

font = pygame.font.Font("fonts/monaco.ttf", 24)

screen.fill(grey)

pygame.draw.circle(screen, black, (160, 240), 200, 0)

display_font = pygame.font.Font("fonts/monaco.ttf", 120)

rpm_font = pygame.font.Font("fonts/monaco.ttf", 40)

draw_tick_marks(45,315,14,160,240,200)

# Overarching state variables
rpm = 0.0
display_rpm = 0.0
engineLoad = 0.0
throttle = 0.0
temp = 0.0
oxygen = 0.0
speed = 0.0
gear = 0
volts = 0.0





# Test code
if (test):
	while 1:
		for i in range(0,13000,50):
			inpt = linear_transform(i,0,13000,45,315)
			
			draw_screen()

			draw_indicator(inpt,190,160,240)

			angle = display_font.render(str(inpt)+u'\N{DEGREE SIGN}',1,white)
			txtrpm = rpm_font.render(str(i),1,rpmColor(i))

			screen.blit(angle,(470,40))
			screen.blit(txtrpm,(100,260))

			pygame.display.update()

# Gets serial values and animates the dashboard
if (not test):
	
	while (True):

		# Animate using new data
		draw_screen()

		smooth_rpm()
		
		draw_indicator(linear_transform(display_rpm,0,13000,45,315),190,160,240)

		text = display_font.render(str(temp) + u'\N{DEGREE SIGN}',1,white)

		txtrpm = rpm_font.render(str(int(rpm)),1,rpmColor(rpm))

		screen.blit(text,(470,40))
		screen.blit(txtrpm,(100,100))

		pygame.display.update()

		readData()

		#print ("end of while loop")












