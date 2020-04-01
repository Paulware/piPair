GPIO.setup(03, GPIO.OUT)
#Now setup PWM on pin #3 at 50Hz
pwm=GPIO.PWM(03, 50)
#Then start it with 0 duty cycle so it doesn't set any angles on startup
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)