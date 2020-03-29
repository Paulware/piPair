# -*- coding: utf-8 -*-

# Authors: Michael Greer, Matthew Shepherd

# IMPORTANT FOR CIRCLE DEFINITION:
# We defined our unit circle as a mirror image of the standard unit circle.
# Circle starts at left and goes clockwise
# Code reflects this

###############################################################################################################

#####	Import statements	#####

import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math				# sin, cos, etc
import struct			# For converting byte to float
import datetime			# For delta timing
import os				# For testing?
from subprocess import call 	#Used for calling external functions

from serial_ports import serial_ports

#####	Initialize Libraries and Variable Declarations	  #####

### Initialize pygame
pygame.init()

### Initialize as Testing Mode or Reading Rode
# True => Testing
# False => Reading
test = False

### Initialize serial
ser = None
if (not test): 
	while ser is None:
		ports = serial_ports()
		if ports != []:
			ser = serial.Serial(ports[0], 9600)
		else:
			time.sleep(1)

### [Overarching State Variable] Declarations
rpm = 0.0
display_rpm = 0.0
engineLoad = 0.0
throttle = 0.0
temp = 0.0
oxygen = 0.0
speed = 0.0
gear = 0
volts = 0.0 	# This is actually a running average of the voltage across 20 elements

buf_length = 50
volt_buf = [13] * buf_length
buf_count = 0
buf_sum = sum(volt_buf)

shutoff = False

### Font Declarations
temp_font = pygame.font.Font("fonts/monaco.ttf", 70)
rpm_font = pygame.font.Font("fonts/Roboto-BlackItalic.ttf", 100)
warning_font = pygame.font.Font("fonts/Roboto-BlackItalic.ttf", 120)

### Important Constats
shift_rpm = 11000
high_temp = 210

too_low = 1		# We use this to throw out any obviously wrong data and keep it from skewing the average
low_battery = 11.5

redline_rpm = 12000


##### Function Definitions #####

### Maps a variable from one space to another
def linear_transform(input,rangeOneStart,rangeOneEnd,rangeTwoStart,rangeTwoEnd):
	return int((input-rangeOneStart)*(float(rangeTwoEnd-rangeTwoStart)/float(rangeOneEnd-rangeOneStart))+rangeTwoStart)

### Draws the RPM bar at the top of the screen
def draw_rpm_bar(i):
	inpt = linear_transform(i,0,13000,0,800)
	pygame.draw.rect(screen, rpmColor(i), (0,0,inpt,98))


### Draws all parts of display that are not data-dependent
def draw_screen():
	screen.fill(black)
	#pygame.draw.rect(screen, black, (0,100,800,700))
	
	#Bar line
	pygame.draw.line(screen, lgrey, (0,100),(800,100), 5)

### Smooths rpm readout
def smooth_rpm():
	global rpm, display_rpm
	
	display_rpm += (rpm-display_rpm)/2

### Draws the warning message for flashing warnings on the dashboard
def draw_warning_message(message, primary, secondary):
	pygame.draw.rect(screen, primary, (25,125,750,325))
	pygame.draw.rect(screen, secondary, (50,150,700,275))

	warning = warning_font.render(message,1,white)
	screen.blit(warning, (400-(warning.get_rect().width/2),175))

### Reads data from bus
# All code taken from Thomas Kelly's implementation of readData() in serial_thread.py
def readData():
	global ser
	global rpm, engineLoad, throttle, temp, oxygen, speed, gear, volts, too_low
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
				payload = struct.unpack('>f',ser.read(4))[0]
				rpm = payload

			elif (data == bytes(b'1')):
				payload = struct.unpack('>f',ser.read(4))[0]
				engineLoad = payload

			elif (data == bytes(b'2')):
				payload = struct.unpack('>f',ser.read(4))[0]
				throttle = payload

			elif (data == bytes(b'3')):
				payload = struct.unpack('>f',ser.read(4))[0]
				temp = payload

			elif (data == bytes(b'4')):
				payload = struct.unpack('>f',ser.read(4))[0]
				oxygen = payload

			elif (data == bytes(b'5')):
				payload = struct.unpack('>f',ser.read(4))[0]
				speed = payload

			elif (data == bytes(b'6')):
				payload = ord(struct.unpack('c',ser.read())[0])
				gear = payload

			elif (data == bytes(b'7')):
				payload = struct.unpack('>f',ser.read(4))[0]
				if (payload > too_low):
					voltageUpdate(payload)

			else:
				print("ERROR: Corrupted Data")
		else:
			pass
	else:
		pass

# Used to turn off the RPi when the battery voltage gets critically low
def lowBatteryShutoff():
	global shutoff
	shutoff = True
	call(["shutdown"])	# Executes the shutdown function

def voltageUpdate(vInput):

	global buf_count
	global buf_sum
	global volt_buf

	buf_count %= buf_length

	buf_sum -= volt_buf[buf_count]

	volt_buf[buf_count] = vInput

	buf_sum += volt_buf[buf_count]

	volts = buf_sum/float(buf_length)

	buf_count += 1

### According to carter, this is acting up. Needs work.
	#if (volts < low_battery):
		#lowBatteryShutoff()

######	Color Definitions	######
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
lgrey=	(150,150,150)
green = (0,120,0)
white = (255,255,255)

#Returns the color of the RPM bar depending on the RPM
def rpmColor(n):
	# HSLA formatting
	if n < 4000:
		inpt = 100
	else:	
		inpt = linear_transform(n,4000,13000,100,0)
	color = pygame.Color(255)
	color.hsla = (inpt,100,50,0)
	return color

#####	MAIN CODE	#####

# Setup Screen
display_size=width, height=800,480 	# Size of the Adafruit screen
screen = pygame.display.set_mode(display_size)
pygame.display.toggle_fullscreen() 	# Sets display mode to full screen
pygame.mouse.set_visible(False)		# Turns off cursor visibility

# More Screen Setup (I dunno what this does? artifact from old code?)
screen.fill(black)

# Display Logo (doesn't work on my laptop for some reason; uncomment to display)
img = pygame.image.load("WURacing-Logo-Big.png")
img = pygame.transform.scale(img, (600,480))
screen.blit(img, (100,0))
pygame.display.update()
time.sleep(5)

###		Testing Mode	 ###
if (test):

# 	Setup for warning delta timing
	warning_state = True
	previousTime = datetime.datetime.now()
	
	while 1:
		for i in range(0,13000,50):
			inpt = linear_transform(i,0,13000,0,800)
			inptTemp = linear_transform(i,0,13000,45,315)
			draw_screen()
			draw_rpm_bar(i)
			
# 			Get Raw Input RPM
			txtrpm = rpm_font.render(str(int(i)),1,white)
			
# 			Readability RPM (I prefer this formatting; replace line above to implement
# 			txtrpm = rpm_font.render((str(int(i / 1000)) + "." + str(int((i % 1000) / 100)) + "k"),1,white)

# 			Draw Raw Input RPM (Always text-centered)
			if (i < 100):
				screen.blit(txtrpm,(355,180))
			elif (i < 1000):
				screen.blit(txtrpm,(320,180))
			elif (i < 10000):
				screen.blit(txtrpm,(285,180))
			else:
				screen.blit(txtrpm,(250,180))
			
# 			Draw Temperature
			txttemp = temp_font.render((str(int(inptTemp)) + "\xb0"),1,white)
			screen.blit(txttemp,(80,315))
			
# 			Delta Timing for warning message
			currentTime = datetime.datetime.now()
			deltaTime = currentTime - previousTime
			
			
###			Warning Message Code
	
# 			Flashing Message State Machine
			if (deltaTime.microseconds > 500000):
				if (warning_state):
					# Draw State
					warning_state = False
					previousTime = datetime.datetime.now()
				else:
 					# Don't Draw State
					warning_state = True
					previousTime = datetime.datetime.now()
			
# 			Draw/Don't Draw depending on state
			if (warning_state):
				draw_warning_message("test",red,grey)
			 
			pygame.display.update()


###		Reading Mode	 ###
# Gets serial values and animates the dashboard
if (not test):
	ser.flush()
	warning_state = True
	previousTime = datetime.datetime.now()

	while (True):

		draw_screen()
		draw_rpm_bar(rpm)

###			Warning Message Code

# 			Delta Timing for warning message
		currentTime = datetime.datetime.now()
		deltaTime = currentTime - previousTime

# 			Flashing Message State Machine
		if (deltaTime.microseconds > 500000):
			if (warning_state):
				# Draw State
				warning_state = False
				previousTime = datetime.datetime.now()
			else:
					# Don't Draw State
				warning_state = True
				previousTime = datetime.datetime.now()

		#			Check for warnings
		redline = rpm > redline_rpm
		shift 	= rpm > shift_rpm
		overheat= temp > high_temp

		if (warning_state and shutoff):
			draw_warning_message("SHUTOFF",red,grey)
		elif (warning_state and redline):
			draw_warning_message("REDLINE",red,grey)
		elif (warning_state and overheat):
			draw_warning_message("OVERHEAT",red,grey)
		elif (warning_state and shift):
			draw_warning_message("SHIFT",green,grey)
		else:
			
	# 			Get Raw Input RPM
			txtrpm = rpm_font.render(str(int(rpm)),1,white)
			
	# 			Readability RPM (I prefer this formatting; replace line above to implement
	# 			txtrpm = rpm_font.render((str(int(i / 1000)) + "." + str(int((i % 1000) / 100)) + "k"),1,white)

	# 			Draw Raw Input RPM (Always text-centered)
			if (rpm < 100):
				screen.blit(txtrpm,(355,180))
			elif (rpm < 1000):
				screen.blit(txtrpm,(320,180))
			elif (rpm < 10000):
				screen.blit(txtrpm,(285,180))
			else:
				screen.blit(txtrpm,(250,180))
			
	# 			Draw Temperature
			txttemp = temp_font.render((str(int(temp)) + "\xb0"),1,white)
			screen.blit(txttemp,(80,315))
			
	# 			Draw/Don't Draw depending on state
		 
		pygame.display.update()

		readData()

#		print ("end of while loop")
