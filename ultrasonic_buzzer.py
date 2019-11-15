import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
import pigpio
import math
pi = pigpio.pi(port = 8887)

buzPin=18
TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def siren(pos):
    return 440*math.sin(pos)+440

def pulseIn():
    while True:
        GPIO.output(TRIG, False)
        time.sleep(.000005)
        GPIO.output(TRIG, True) # Sending out a trigger pulse for 10 microseconds
        time.sleep(.00001)
        GPIO.output(TRIG, False)
        pulse_start = time.time()
        pulse_end = time.time()
        now = time.time()
        while GPIO.input(ECHO)==0 and time.time()-now<.1: # This is where it keeps getting stuck
            pulse_start = time.time()
            
        now = time.time()  
        while GPIO.input(ECHO)==1 and time.time()-now<.1:
            pulse_end = time.time()
        return pulse_end-pulse_start

time.sleep(2) # Giving the sensor some time to warm up
for i in range(10000):
    print(pulseIn()*17500)
    print(i)
    time.sleep(.1)
